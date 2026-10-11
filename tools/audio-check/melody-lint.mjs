// 旋律の点検（docs/sound/melody-craft-guide.md §8 の提案 P1〜P6・P11）。
// score-check.mjs から呼ぶ。純粋関数だけで、ファイルは読まない（テストしやすい）。
// 入力は { melodies: [{ role, seq: [{t, dur, pitch, name}] }], beats, bpm, chords: 小節ごとのコード名 }。
// 戻り値は [{ id: "P1", level: "ok" | "warn" | "info", msg }]。警告は目安で、わざとなら直さなくてよい。
import { chordPcs, midiName } from "./score-lib.mjs";

/** 旋律ではなく「刻み・リフ・伴奏」の役割は、P1〜P4 の対象から外す。 */
export const isRiffRole = (role) => /リフ|刻み|ostinato|アルペジオ|伴奏|カッティング/i.test(role ?? "");

const barOf = (t, beats) => Math.floor(t / beats + 1e-9) + 1;
const chunk = (n, size) => Array.from({ length: Math.ceil(n / size) }, (_, i) => [i * size, Math.min(n, (i + 1) * size)]);
const noteName = (n) => n.name ?? midiName(n.pitch);

/** 区切りの長さ（小節）。8小節未満の曲は2小節ごと、それ以外は4小節ごと。 */
export function phraseBars(totalBars) {
  return totalBars < 8 ? 2 : 4;
}

/**
 * P1 頂点（最高音）の点検。区切りごとに最高音の回数と位置を数える。
 * 回数が2以上、または最初に現れる位置が区切りの前25%なら警告。音が4つ未満の区切りは見ない。
 */
export function checkPeaks(seq, beats, totalBars) {
  const size = phraseBars(totalBars) * beats;
  const bad = [];
  let looked = 0;
  for (let s = 0; s < totalBars * beats - 1e-9; s += size) {
    const ph = seq.filter((n) => n.t >= s - 1e-9 && n.t < s + size - 1e-9);
    if (ph.length < 4) continue;
    looked++;
    const top = Math.max(...ph.map((n) => n.pitch));
    const tops = ph.filter((n) => n.pitch === top);
    const pos = (tops[0].t - s) / size;
    const bar = barOf(tops[0].t, beats);
    if (tops.length >= 2) bad.push(`${bar}小節目付近の最高音 ${noteName(tops[0])} が区切りの中で${tops.length}回（1回に）`);
    else if (pos < 0.25) bad.push(`${bar}小節目の最高音 ${noteName(tops[0])} が区切りの前${Math.round(pos * 100)}%にある（後ろ3分の1が目安）`);
  }
  if (!looked) return { id: "P1", level: "ok", msg: "頂点の点検: 見る区切りなし" };
  if (!bad.length) return { id: "P1", level: "ok", msg: "頂点（最高音）は区切りごとに1回で、前すぎない" };
  return { id: "P1", level: "warn", msg: `頂点: ${bad.slice(0, 3).join("／")}${bad.length > 3 ? `（ほか${bad.length - 3}か所）` : ""}` };
}

/** P2 同音の再訪・連打。4小節（短い曲は2小節）の中で同じ高さが4割超、または同じ音が4回以上つづく。 */
export function checkRepeatedPitch(seq, beats, totalBars) {
  const size = phraseBars(totalBars) * beats;
  const bad = [];
  for (let s = 0; s < totalBars * beats - 1e-9; s += size) {
    const ph = seq.filter((n) => n.t >= s - 1e-9 && n.t < s + size - 1e-9);
    if (ph.length < 5) continue;
    const cnt = new Map();
    for (const n of ph) cnt.set(n.pitch, (cnt.get(n.pitch) ?? 0) + 1);
    const [p, c] = [...cnt.entries()].sort((a, b) => b[1] - a[1])[0];
    if (c / ph.length > 0.4) bad.push(`${barOf(s, beats)}小節目からの区間で ${midiName(p)} が${Math.round((c / ph.length) * 100)}%`);
  }
  let run = 1;
  for (let i = 1; i < seq.length; i++) {
    run = seq[i].pitch === seq[i - 1].pitch ? run + 1 : 1;
    if (run === 4) bad.push(`${barOf(seq[i].t, beats)}小節目付近で ${noteName(seq[i])} が4回以上つづく`);
  }
  if (!bad.length) return { id: "P2", level: "ok", msg: "同じ高さの音への偏り・連打なし" };
  return { id: "P2", level: "warn", msg: `同音の再訪・連打: ${bad.slice(0, 3).join("／")}${bad.length > 3 ? `（ほか${bad.length - 3}か所）` : ""}` };
}

/** 小節ごとの「音価の並び」の文字列（拍頭からの位置と長さ）。 */
export function rhythmSignatures(seq, beats, totalBars) {
  const sigs = Array.from({ length: totalBars }, () => []);
  for (const n of seq) {
    const b = barOf(n.t, beats) - 1;
    if (b < 0 || b >= totalBars) continue;
    sigs[b].push(`${+(n.t - b * beats).toFixed(3)}:${+n.dur.toFixed(3)}`);
  }
  return sigs.map((a) => a.join(","));
}

/**
 * P3 リズム型の点検（1音テスト）。同じ小節の型が4小節以上つづく、または8小節の中に型が6種を超えたら警告。
 * 全部の音が拍頭（整数拍）にあるときは参考として表示（シンコペ0%）。
 */
export function checkRhythmTypes(seq, beats, totalBars) {
  const sigs = rhythmSignatures(seq, beats, totalBars);
  const out = [];
  const warns = [];
  let start = 0;
  for (let i = 1; i <= sigs.length; i++) {
    if (i === sigs.length || sigs[i] !== sigs[start]) {
      if (sigs[start] && i - start >= 4) warns.push(`${start + 1}〜${i}小節目が全部同じリズム型`);
      start = i;
    }
  }
  for (const [a, b] of chunk(totalBars, 8)) {
    const kinds = new Set(sigs.slice(a, b).filter(Boolean));
    if (kinds.size > 6) warns.push(`${a + 1}〜${b}小節目にリズム型が${kinds.size}種（6種以内に絞る）`);
  }
  out.push(warns.length ? { id: "P3", level: "warn", msg: `リズム型: ${warns.slice(0, 3).join("／")}` } : { id: "P3", level: "ok", msg: `リズム型は ${new Set(sigs.filter(Boolean)).size} 種で、適度に使い回されている` });
  const off = seq.filter((n) => Math.abs(n.t - Math.round(n.t)) > 1e-6).length;
  if (seq.length >= 8 && off === 0) out.push({ id: "P3", level: "info", msg: "参考: 旋律の音がすべて拍の頭にある（シンコペ0%）。1音で叩くと単調かも" });
  return out;
}

/** ジャンルの推測（バラード・民謡・和風なら息を短めに見る） */
export function breathSeconds(song) {
  const text = `${song.genre ?? ""} ${song.title ?? ""} ${song.description ?? ""}`;
  return /バラード|ballad|民謡|和風|folk|和の|わらべ/i.test(text) ? 4 : 6;
}

/**
 * P4 息（休符・長音）の点検。休符（0.5拍以上の隙間）か2拍以上の音を「息」として、息なしで続いた長さを秒に直す。
 * 6秒（バラード・民謡は4秒）を超えたら警告。
 */
export function checkBreath(seq, beats, bpm, totalBars, limitSec = 6) {
  const limit = (limitSec * bpm) / 60; // 拍
  const total = totalBars * beats;
  const spans = [[0, 0]]; // 息の区間 [開始, 終了]
  for (let i = 0; i < seq.length; i++) {
    const n = seq[i];
    if (n.dur >= 2 - 1e-9) spans.push([n.t, n.t + n.dur]);
    const next = seq[i + 1];
    const gapEnd = next ? next.t : total;
    if (gapEnd - (n.t + n.dur) >= 0.5 - 1e-9) spans.push([n.t + n.dur, gapEnd]);
  }
  spans.sort((a, b) => a[0] - b[0]);
  spans.push([total, total]);
  const bad = [];
  for (let i = 1; i < spans.length; i++) {
    const gap = spans[i][0] - spans[i - 1][1];
    if (gap > limit + 1e-9) bad.push(`${barOf(spans[i - 1][1], beats)}〜${Math.min(totalBars, barOf(spans[i][0] - 1e-6, beats))}小節目が息なしで続く（約${((gap * 60) / bpm).toFixed(1)}秒）`);
  }
  if (!bad.length) return { id: "P4", level: "ok", msg: `旋律に息（休符か2拍以上の音）が${limitSec}秒以内ごとにある` };
  return { id: "P4", level: "warn", msg: `息: ${bad.slice(0, 3).join("／")}${bad.length > 3 ? `（ほか${bad.length - 3}か所）` : ""}` };
}

/** 区切り（blockBars 小節）の最後に鳴っている旋律の音 */
function endNote(seq, endBeat) {
  let cur = null;
  for (const n of seq) if (n.t < endBeat - 1e-9) cur = n;
  return cur;
}

/**
 * P5 問いと答えの終わり方。4小節ごとの区切りの最後の音を取り、8小節ブロックの前半の終わりと後半の終わりが
 * 同じ音（音名）になっていないかを見る。全ブロックで同じなら警告（毎回「閉じて」しまっている）。
 */
export function checkAnswerEndings(seq, beats, totalBars) {
  const pairs = [];
  for (let b = 0; b + 8 <= totalBars; b += 8) {
    const q = endNote(seq, (b + 4) * beats), a = endNote(seq, (b + 8) * beats);
    if (q && a) pairs.push({ bar: b + 1, q, a });
  }
  if (!pairs.length) return { id: "P5", level: "info", msg: "問いと答えの終わり: 8小節ブロックがなく点検しない" };
  const same = pairs.filter((p) => p.q.pitch % 12 === p.a.pitch % 12);
  if (same.length === pairs.length) return { id: "P5", level: "warn", msg: `問いの終わりと答えの終わりが同じ音（${pairs.map((p) => `${p.bar}小節目からの8小節: ${noteName(p.q)}`).slice(0, 3).join("／")}）。問いは主音以外で止めて開いておく` };
  return { id: "P5", level: "ok", msg: `問いと答えの終わりの音が違う（${pairs.length - same.length}/${pairs.length}ブロック）` };
}

/**
 * P6 セクション間の音域差。plan.sections（name・kind・bars）を使い、サビの旋律の平均音高が Aメロ以上に +2半音あるか、
 * 最高音がサビにあるかを見る。plan がなければ null。
 */
export function checkSectionRange(seq, beats, plan) {
  const secs = plan?.sections;
  if (!Array.isArray(secs) || !secs.length) return null;
  let bar = 0;
  const rows = secs.map((s) => {
    const r = { name: s.name ?? "", kind: s.kind ?? "", from: bar * beats, to: (bar + (s.bars | 0)) * beats };
    bar += s.bars | 0;
    return r;
  }).map((r) => {
    const ns = seq.filter((n) => n.t >= r.from - 1e-9 && n.t < r.to - 1e-9);
    return { ...r, n: ns.length, mean: ns.length ? ns.reduce((a, n) => a + n.pitch, 0) / ns.length : null, max: ns.length ? Math.max(...ns.map((n) => n.pitch)) : null };
  });
  const isVerse = (r) => r.kind === "verse" || /Aメロ|Bメロ|verse/i.test(r.name);
  const isChorus = (r) => r.kind === "chorus" || /サビ|chorus/i.test(r.name);
  const verse = rows.filter((r) => isVerse(r) && r.n);
  const chorus = rows.filter((r) => isChorus(r) && r.n);
  if (!verse.length || !chorus.length) return { id: "P6", level: "info", msg: "セクション間の音域: 旋律のある Aメロとサビが設計図になく点検しない" };
  const vMean = verse.reduce((a, r) => a + r.mean, 0) / verse.length;
  const cMean = chorus.reduce((a, r) => a + r.mean, 0) / chorus.length;
  const vMax = Math.max(...verse.map((r) => r.max)), cMax = Math.max(...chorus.map((r) => r.max));
  const bad = [];
  if (cMean < vMean + 2) bad.push(`サビの平均音高が Aメロ+${(cMean - vMean).toFixed(1)}半音（+2半音以上が目安）`);
  if (cMax < vMax) bad.push(`最高音（${midiName(vMax)}）が Aメロにあり、サビ（${midiName(cMax)}）より高い`);
  if (!bad.length) return { id: "P6", level: "ok", msg: `サビは Aメロより高い（平均 +${(cMean - vMean).toFixed(1)}半音・最高音 ${midiName(cMax)}）` };
  return { id: "P6", level: "warn", msg: `セクション間の音域: ${bad.join("／")}` };
}

/**
 * P11 倚音・掛留の見える化。強拍（1拍目・3拍目）の和音外音のうち、次の音が順次下行（1〜2半音）で
 * 構成音に着地するものを「倚音／掛留（OK）」、そうでないものを要確認として数える。
 */
export function classifyStrongNonChord(seq, beats, chords) {
  const ok = [], bad = [];
  for (let i = 0; i < seq.length; i++) {
    const n = seq[i];
    const inBar = n.t % beats;
    if (Math.abs(inBar % 2) > 1e-9) continue;
    const bar = barOf(n.t, beats) - 1;
    const c = chordPcs(chords[Math.min(chords.length - 1, bar)] ?? "");
    if (!c || c.pcs.has(n.pitch % 12)) continue;
    const nx = seq[i + 1];
    const nxChord = nx ? chordPcs(chords[Math.min(chords.length - 1, barOf(nx.t, beats) - 1)] ?? "") : null;
    const resolved = nx && nxChord && nx.pitch < n.pitch && n.pitch - nx.pitch <= 2 && nxChord.pcs.has(nx.pitch % 12);
    (resolved ? ok : bad).push({ bar: bar + 1, name: noteName(n) });
  }
  return { ok, bad };
}

export function checkAppoggiatura(seq, beats, chords) {
  const { ok, bad } = classifyStrongNonChord(seq, beats, chords);
  if (!ok.length && !bad.length) return { id: "P11", level: "ok", msg: "強拍の和音外音なし" };
  const head = ok.length ? `強拍の和音外音のうち${ok.length}個は倚音／掛留（次の音で下へ解決。OK）` : "";
  if (!bad.length) return { id: "P11", level: "info", msg: head };
  return { id: "P11", level: "warn", msg: `${head ? head + "。" : ""}解決していない強拍の和音外音 ${bad.length}個（${bad.slice(0, 3).map((b) => `${b.bar}小節目${b.name}`).join("・")}）` };
}

/** 旋律の点検をまとめて実行する。 */
export function melodyLint(song, melodies, { chords, plan = null } = {}) {
  const beats = Number(song.beats) || 4;
  const bpm = Number(song.bpm) || 120;
  const totalBars = chords.length;
  const results = [];
  for (const m of melodies) {
    const tag = `旋律「${m.role ?? ""}」`;
    const add = (r) => r && results.push({ ...r, msg: `${tag}: ${r.msg}` });
    if (!isRiffRole(m.role)) {
      add(checkPeaks(m.seq, beats, totalBars));
      add(checkRepeatedPitch(m.seq, beats, totalBars));
      checkRhythmTypes(m.seq, beats, totalBars).forEach(add);
      add(checkBreath(m.seq, beats, bpm, totalBars, breathSeconds(song)));
    }
    add(checkAnswerEndings(m.seq, beats, totalBars));
    add(checkSectionRange(m.seq, beats, plan));
    add(checkAppoggiatura(m.seq, beats, chords));
  }
  return results;
}
