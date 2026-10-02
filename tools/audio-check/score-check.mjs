// 使い方: node tools/audio-check/score-check.mjs <曲.json> [...]
// AIソング形式のJSON（音符データ）を、WAVにする前に楽理の面から点検する（docs/sound/music-knowledge.md の 17）。
// 数値の目安は一般的な作曲の知見で、良し悪しの最終判断は耳で。警告が出ても、わざとなら直さなくてよい。
import fs from "fs";

const NAMES = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };
const DRUMS = new Set(["kick", "snare", "hihat", "crash", "tom"]);
// 楽器の音域（MIDI番号。作曲ソフトの手引きの音域）
const RANGE = {
  bass: ["E1", "G3"], slap: ["E1", "G3"], sub808: ["C1", "C3"], guitar: ["E2", "E5"], crunch: ["E2", "E5"],
  distGuitar: ["E2", "E4"], leadGuitar: ["E3", "E6"], echoGuitar: ["E3", "E6"], keys: ["C2", "C6"], harpsichord: ["C2", "C6"],
  strings: ["C2", "C7"], pad: ["C2", "C6"], choir: ["C3", "C6"], brass: ["E2", "C6"], lead: ["C3", "C7"], bell: ["C4", "C7"],
  sitar: ["C3", "C6"], koto: ["C3", "C6"], shamisen: ["C3", "C6"], banjo: ["C3", "C6"], harp: ["C2", "C7"], kalimba: ["C4", "C7"],
  panflute: ["C4", "C7"], shakuhachi: ["C4", "C6"], ocarina: ["C4", "C7"], fiddle: ["G3", "E6"], bagpipe: ["A3", "A5"], piano: ["A0", "C8"],
};

function midi(name) {
  const m = /^([A-G])([#b]?)(-?\d)$/.exec(name);
  if (!m) return null;
  return 12 * (Number(m[3]) + 1) + NAMES[m[1]] + (m[2] === "#" ? 1 : m[2] === "b" ? -1 : 0);
}
function chordPcs(name) {
  const m = /^([A-G])([#b]?)(.*)$/.exec(name);
  if (!m) return null;
  const root = (NAMES[m[1]] + (m[2] === "#" ? 1 : m[2] === "b" ? -1 : 0) + 12) % 12;
  const q = m[3];
  let iv = [0, 4, 7];
  if (/^(m|min)(?!aj)/.test(q)) iv = [0, 3, 7];
  if (q.startsWith("dim")) iv = [0, 3, 6];
  if (q.startsWith("aug")) iv = [0, 4, 8];
  if (q.includes("sus4")) iv = [0, 5, 7];
  else if (q.includes("sus2")) iv = [0, 2, 7];
  if (/7/.test(q)) iv = [...iv, q.includes("maj7") ? 11 : 10];
  if (q.includes("add9") || /9/.test(q)) iv = [...iv, 2];
  return { root, pcs: new Set(iv.map((x) => (root + x) % 12)) };
}
function parseNotes(str) {
  const out = [];
  let t = 0;
  for (const tok of str.trim().split(/\s+/)) {
    const [n, d] = tok.split(":");
    const dur = Number(d);
    if (!Number.isFinite(dur)) continue;
    out.push({ t, dur, name: n, pitch: midi(n) });
    t += dur;
  }
  return { notes: out, total: t };
}
// 曲の長さにそろえてくり返した、音のならび
function expand(part, totalBeats) {
  const { notes, total } = parseNotes(part.notes);
  if (total <= 0) return [];
  const out = [];
  for (let base = 0; base < totalBeats - 1e-9; base += total) {
    for (const n of notes) if (base + n.t < totalBeats - 1e-9) out.push({ ...n, t: base + n.t });
  }
  return out;
}

function check(file) {
  const song = JSON.parse(fs.readFileSync(file, "utf8"));
  const chords = song.chords.trim().split(/\s+/);
  const bars = chords.length * song.barsPerChord * song.repeats;
  const beats = song.beats;
  const totalBeats = bars * beats;
  const chordAt = (t) => {
    const bar = Math.floor(t / beats);
    const idx = Math.floor((bar % (chords.length * song.barsPerChord)) / song.barsPerChord);
    return chordPcs(chords[idx]);
  };
  const first = chordPcs(chords[0]);
  const minor = first && first.pcs.has((first.root + 3) % 12);
  const scale = new Set((minor ? [0, 2, 3, 5, 7, 8, 10, 11] : [0, 2, 4, 5, 7, 9, 11]).map((x) => (first.root + x) % 12));
  const lines = [];
  const warn = (ok, okMsg, ngMsg) => lines.push((ok ? "○ " : "△ ") + (ok ? okMsg : ngMsg));
  lines.push(`■ ${song.title}（${bars}小節・${beats}拍子・テンポ${song.bpm}・約${Math.round((totalBeats / song.bpm) * 60)}秒、主音${["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"][first.root]}${minor ? "短調" : "長調"}と推定）`);

  const parts = song.parts.map((p) => ({ ...p, seq: DRUMS.has(p.instrument) ? [] : expand(p, totalBeats).filter((n) => n.pitch !== null) }));
  const pitched = parts.filter((p) => p.seq.length);

  // 1. 音域
  for (const p of pitched) {
    const r = RANGE[p.instrument];
    if (!r) continue;
    const lo = midi(r[0]), hi = midi(r[1]);
    const out = p.seq.filter((n) => n.pitch < lo || n.pitch > hi).length;
    if (out) warn(false, "", `音域外 ${p.instrument}（${p.role ?? ""}）: ${out}音（${r[0]}〜${r[1]}）`);
  }
  if (!lines.some((l) => l.includes("音域外"))) warn(true, "全パートが音域内", "");

  // 2〜4. 旋律（役割に「メロディ」「旋律」を含むパート）
  const melodies = pitched.filter((p) => /メロディ|旋律/.test(p.role ?? "") && !/重ね|下で/.test(p.role ?? ""));
  for (const p of melodies) {
    const s = p.seq;
    let step = 0, leaps = 0, bigLeaps = 0, noReturn = 0, ints = 0;
    for (let i = 1; i < s.length; i++) {
      const d = s[i].pitch - s[i - 1].pitch;
      ints++;
      if (Math.abs(d) <= 2) step++;
      else if (Math.abs(d) >= 7) {
        leaps++;
        if (Math.abs(d) > 12) bigLeaps++;
        const nx = s[i + 1] ? s[i + 1].pitch - s[i].pitch : 0;
        if (nx && Math.sign(nx) === Math.sign(d)) noReturn++;
      }
    }
    const stepRate = ints ? step / ints : 0;
    warn(stepRate >= 0.55, `旋律「${p.role}」の順次進行 ${(stepRate * 100) | 0}%`, `旋律「${p.role}」の順次進行が ${(stepRate * 100) | 0}%（目安 6〜7割以上）`);
    if (bigLeaps) warn(false, "", `旋律「${p.role}」にオクターブ超の跳躍が ${bigLeaps}回`);
    if (leaps) warn(noReturn / leaps <= 0.5, `大きな跳躍のあとの戻り OK`, `旋律「${p.role}」: 5度以上の跳躍${leaps}回のうち${noReturn}回が戻らず同じ向き`);
    // 強拍（小節の1拍目と3拍目）のコード外音
    let strong = 0, nonCt = 0;
    for (const n of s) {
      const inBar = n.t % beats;
      if (Math.abs(inBar % 2) > 1e-9 || n.pitch == null) continue; // 1拍目・3拍目の頭だけ
      strong++;
      const c = chordAt(n.t);
      if (c && !c.pcs.has(n.pitch % 12)) nonCt++;
    }
    if (strong) warn(nonCt / strong <= 0.35, `強拍の和音外音 ${((nonCt / strong) * 100) | 0}%`, `旋律「${p.role}」の強拍の和音外音が ${((nonCt / strong) * 100) | 0}%（目安 2〜3割以下）`);
    // 音域の幅
    const ps = s.map((n) => n.pitch);
    const span = Math.max(...ps) - Math.min(...ps);
    warn(span <= 24, `旋律の音域 ${span}半音`, `旋律「${p.role}」の音域が ${span}半音（2オクターブ超）`);
    // 最高音の回数
    const top = Math.max(...ps);
    const topCount = s.filter((n) => n.pitch === top).length;
    lines.push(`  ・最高音 ${top}（MIDI）は ${topCount}回（サビの山は1フレーズに1回が目安）`);
    // モチーフの再利用: 最初の6音の音程列が後半に出るか
    const iv = [];
    for (let i = 1; i < s.length; i++) iv.push(s[i].pitch - s[i - 1].pitch);
    const motif = iv.slice(0, 5).join(",");
    let found = 0;
    for (let i = 5; i + 5 <= iv.length; i++) if (iv.slice(i, i + 5).join(",") === motif) found++;
    warn(found > 0, `「${p.role}」の冒頭の音型が後半に ${found}回出る`, `「${p.role}」の冒頭の音型（${motif}）が後半に出てこない（動機の再利用が目安）`);
    // リズムの多様性
    const durs = new Set(s.map((n) => n.dur));
    warn(durs.size >= 3, `音価の種類 ${durs.size}`, `旋律「${p.role}」の音価が${durs.size}種類だけ（単調かも）`);
  }

  // 5. 平行5度・8度（旋律とベース。拍の頭で比べる）
  const bass = pitched.find((p) => ["bass", "slap", "sub808"].includes(p.instrument));
  if (bass && melodies.length) {
    const at = (seq, t) => {
      let cur = null;
      for (const n of seq) if (n.t <= t + 1e-9 && n.t + n.dur > t + 1e-9) cur = n;
      return cur;
    };
    const mel = melodies[0].seq;
    let par = 0, prev = null;
    for (let t = 0; t < totalBeats; t += 1) {
      const a = at(bass.seq, t), b = at(mel, t);
      if (!a || !b) { prev = null; continue; }
      const iv = (((b.pitch - a.pitch) % 12) + 12) % 12;
      if (prev && (iv === 7 || iv === 0) && prev.iv === iv && (a.pitch !== prev.a || b.pitch !== prev.b) && a.pitch !== prev.a && b.pitch !== prev.b) par++;
      prev = { iv, a: a.pitch, b: b.pitch };
    }
    warn(par <= 4, `ベースと旋律の平行5度・8度 ${par}か所（拍の頭で判定）`, `ベースと旋律の平行5度・8度が ${par}か所（拍の頭で判定。ロック系では許容されることも多い）`);
  }

  // 6. 音階内の音の割合
  let all = 0, inScale = 0;
  for (const p of pitched) for (const n of p.seq) { all++; if (scale.has(n.pitch % 12)) inScale++; }
  warn(all === 0 || inScale / all >= 0.9, `音階内の音 ${((inScale / all) * 100) | 0}%`, `音階外の音が多い（音階内 ${((inScale / all) * 100) | 0}%。借用和音なら問題なし）`);

  // 7. 終わり方
  if (melodies[0]) {
    const last = melodies[0].seq[melodies[0].seq.length - 1];
    warn(last.pitch % 12 === first.root || chordAt(totalBeats - 0.01)?.pcs.has(last.pitch % 12), "旋律の最後の音は主音かその時の和音の音", `旋律の最後の音が主音でも和音の音でもない（${last.name}）`);
  }

  // 8. 曲の起伏: 8小節ごとに鳴っているパート数（ドラム含む）
  const secBeats = 8 * beats;
  const dens = [];
  for (let s0 = 0; s0 < totalBeats; s0 += secBeats) {
    let n = 0;
    for (const p of song.parts) {
      const q = expand(p, totalBeats).filter((x) => x.t >= s0 && x.t < s0 + secBeats && x.name !== "R");
      if (q.length) n++;
    }
    dens.push(n);
  }
  lines.push(`  ・8小節ごとの鳴るパート数: ${dens.join(" → ")}`);
  warn(dens.length < 2 || dens[0] <= Math.max(...dens) * 0.7, "冒頭は最大より小さく始まる", "冒頭から最大に近いパート数（小さく始める起伏が目安）");
  const minIdx = dens.indexOf(Math.min(...dens));
  warn(dens.length < 4 || (minIdx > 0 && minIdx < dens.length - 1) || dens[0] === Math.min(...dens), "途中で一度引く区間がある", "途中で引く区間がない（間奏で一度減らすと最後のサビが映える）");

  // 9. 同時に鳴る音数の詰めすぎ（拍ごとに低域で重なる音）
  console.log(lines.join("\n"));
  return lines.filter((l) => l.startsWith("△")).length;
}

let warnings = 0;
for (const f of process.argv.slice(2)) warnings += check(f);
console.log(`\n警告 ${warnings}件（目安。耳で確かめて決める）`);
