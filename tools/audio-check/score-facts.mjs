// 楽譜の点検を「感想」でなく「小節番号つきの事実の一覧」にする（docs/sound/ai-composition-workflow.md の提案 8・9、chord-theory-deep.md の提案 9）。
// 戻り値の facts は [{ bar(1から数える), part, kind, detail }]。kind は次のどれか:
//   音域外 / 拍の合計 / 拍頭の不一致 / アヴォイドノート / 同じ4小節の反復 / 動機 / 入り方の重複
// 言語モデル（作者でも校正係でも）は、この一覧だけを読んで直す。数字の目安は一般的な作曲の知見で、わざとなら直さなくてよい。
import { DRUMS, RANGE, midi, midiName, chordPcs, expand, partLength, barChords, melodyParts, estimateKey } from "./score-lib.mjs";
import { describeSong } from "../composer/novelty.mjs";

export const FACT_KINDS = ["音域外", "拍の合計", "拍頭の不一致", "アヴォイドノート", "同じ4小節の反復", "動機", "入り方の重複"];

const barOf = (t, beats) => Math.floor(t / beats + 1e-9) + 1;
const label = (p, i) => `${p.role || p.instrument}（${i + 1}番目・${p.instrument}）`;
const isMelodyPart = (p) => /メロディ|旋律/.test(p.role ?? "") && !/重ね|下で/.test(p.role ?? "");

/** 近い和音の構成音を、旋律の音の上下から2つ選ぶ（直し方の候補）。 */
function nearestChordTones(pitch, chord) {
  const cand = [];
  for (let d = -4; d <= 4; d++) if (chord.pcs.has((((pitch + d) % 12) + 12) % 12)) cand.push({ d, n: pitch + d });
  return cand.sort((a, b) => Math.abs(a.d) - Math.abs(b.d) || a.d - b.d).slice(0, 2).map((c) => midiName(c.n).replace(/-?\d+$/, ""));
}

/**
 * アヴォイドノート: 強拍（小節の1拍目・3拍目）か1拍以上の長さの音が、そのときの和音の構成音の「半音上」にある音階内の音。
 * 和音の音に半音でぶつかって濁って聞こえる。strong は拍頭だけのとき true にして返す（拍頭の不一致との区別用）。
 */
export function isAvoid(pitchPc, chord, scale) {
  if (chord.pcs.has(pitchPc)) return false;
  if (!scale.has(pitchPc)) return false;
  for (const c of chord.pcs) if ((c + 1) % 12 === pitchPc) return true;
  return false;
}

export function collectFacts(song, { plan = null, others = [] } = {}) {
  const facts = [];
  const beats = Number(song.beats) || 4;
  const chords = barChords(song);
  const bars = chords.length;
  const totalBeats = bars * beats;
  const key = estimateKey(chords);
  const scale = key ? new Set((key.minor ? [0, 2, 3, 5, 7, 8, 10, 11] : [0, 2, 4, 5, 7, 9, 11]).map((x) => (key.tonic + x) % 12)) : new Set();
  const add = (bar, part, kind, detail) => facts.push({ bar, part, kind, detail });

  // 1. 音域外（小節・パートごとにまとめる）／拍の合計
  song.parts.forEach((p, i) => {
    const name = label(p, i);
    const len = partLength(p);
    if (len > totalBeats + 1e-6) add(bars + 1, name, "拍の合計", `パートの長さが${len}拍で、曲（${totalBeats}拍）より${(len - totalBeats).toFixed(2).replace(/\.?0+$/, "")}拍長い。後ろが切られます。`);
    else if (len > 0 && len < totalBeats - 1e-6) {
      const rem = len % beats;
      if (Math.abs(rem) > 1e-6 && Math.abs(rem - beats) > 1e-6) add(barOf(len, beats), name, "拍の合計", `パートの長さが${len}拍で、1小節（${beats}拍）の整数倍でない（${rem}拍はみ出し）。くり返すと小節がずれます。`);
      else if (Math.abs((totalBeats / len) - Math.round(totalBeats / len)) > 1e-6) add(barOf(Math.floor(totalBeats / len) * len, beats), name, "拍の合計", `パートの長さ${len}拍が曲（${totalBeats}拍）にちょうど収まらず、最後のくり返しが途中で切れます。`);
    }
    const r = RANGE[p.instrument];
    if (!r || DRUMS.has(p.instrument)) return;
    const lo = midi(r[0]), hi = midi(r[1]);
    const byBar = new Map();
    for (const n of expand(p, totalBeats)) if (n.pitch !== null && (n.pitch < lo || n.pitch > hi)) {
      const b = barOf(n.t, beats);
      if (!byBar.has(b)) byBar.set(b, []);
      byBar.get(b).push(n.name);
    }
    for (const [b, ns] of byBar) add(b, name, "音域外", `${[...new Set(ns)].join("・")} は ${p.instrument} の音域（${r[0]}〜${r[1]}）の外。`);
  });

  // 2. 旋律: 拍頭の不一致／アヴォイドノート
  const mels = melodyParts(song, (p) => expand(p, totalBeats));
  for (const mp of mels) {
    const idx = song.parts.indexOf(song.parts.find((q) => q.notes === mp.notes && q.instrument === mp.instrument));
    const name = label(mp, idx < 0 ? 0 : idx);
    for (const n of mp.seq) {
      const bar = barOf(n.t, beats);
      const c = chordPcs(chords[bar - 1]);
      if (!c) continue;
      const inBar = n.t - (bar - 1) * beats;
      const strong = Math.abs(inBar % 2) < 1e-9 && inBar < beats; // 1拍目・3拍目の頭
      const sustained = n.dur >= 1;
      if (!strong && !sustained) continue;
      const pc = n.pitch % 12;
      if (c.pcs.has(pc)) continue;
      const chordName = chords[bar - 1];
      if (isAvoid(pc, c, scale)) {
        const fix = nearestChordTones(n.pitch, c);
        add(bar, name, "アヴォイドノート", `${inBar + 1}拍目${sustained && !strong ? "から続く長い音" : ""}の ${n.name} は ${chordName} の構成音の半音上でぶつかります。${fix.join(" か ")} に。`);
      } else if (strong) {
        add(bar, name, "拍頭の不一致", `${inBar + 1}拍目の ${n.name} は ${chordName} の構成音ではない（経過音・倚音なら次で解決しているか確認）。`);
      }
    }
  }

  // 3. 同じ4小節の反復（旋律パートだけ。4小節すべて同じ内容の1小節ループは数えない）
  for (const mp of mels) {
    const idx = song.parts.indexOf(song.parts.find((q) => q.notes === mp.notes && q.instrument === mp.instrument));
    const perBar = [];
    for (let b = 0; b < bars; b++) perBar.push(mp.seq.filter((n) => n.t >= b * beats - 1e-9 && n.t < (b + 1) * beats - 1e-9).map((n) => `${(n.t - b * beats).toFixed(2)}${n.name}:${n.dur}`).join(" "));
    const win = new Map();
    for (let b = 0; b + 4 <= bars; b++) {
      const w = perBar.slice(b, b + 4);
      if (w.every((x) => x === "") || new Set(w).size === 1) continue;
      const k = w.join("|");
      if (!win.has(k)) win.set(k, []);
      win.get(k).push(b + 1);
    }
    for (const starts of win.values()) {
      const nonOverlap = [];
      for (const s of starts) if (!nonOverlap.length || s >= nonOverlap[nonOverlap.length - 1] + 4) nonOverlap.push(s);
      if (nonOverlap.length >= 3) add(nonOverlap[0], label(mp, idx < 0 ? 0 : idx), "同じ4小節の反復", `同じ4小節が${nonOverlap.length}回出る（${nonOverlap.map((s) => `${s}〜${s + 3}`).join("・")}小節）。2回目以降は音域・リズム・音数のどれかを変える。`);
    }
  }

  // 4. 動機（plan.motif か description の「動機: C4:1 E4:1 G4:2」）
  const motifText = plan?.motif?.notes ?? /動機[:：]\s*((?:[A-G][#b]?\d:[\d.]+\s*)+)/.exec(song.description ?? "")?.[1];
  if (motifText && mels.length) {
    const motif = [];
    let t0 = 0;
    for (const tok of motifText.trim().split(/\s+/)) { const [n, d] = tok.split(":"); const pm = midi(n); if (pm !== null && Number(d) > 0) { motif.push({ pitch: pm, dur: Number(d) }); t0 += Number(d); } }
    if (motif.length >= 2) {
      const ivs = motif.slice(1).map((m, i) => m.pitch - motif[i].pitch);
      const seq = mels[0].seq;
      const hits = [];
      for (let i = 0; i + motif.length <= seq.length; i++) {
        if (ivs.every((iv, k) => seq[i + k + 1].pitch - seq[i + k].pitch === iv)) {
          const exact = motif.every((m, k) => seq[i + k].pitch === m.pitch && seq[i + k].dur === m.dur);
          hits.push({ bar: barOf(seq[i].t, beats), exact, rhythm: motif.every((m, k) => seq[i + k].dur === m.dur) });
        }
      }
      const name = label(mels[0], 0);
      const secs = Array.isArray(song.sections) ? song.sections : plan?.sections?.map((s) => ({ kind: s.name || s.kind, bars: s.bars })) ?? [];
      if (!hits.length) add(1, name, "動機", `動機（${motifText.trim()}）の音程の並びが旋律に1回も出てこない。`);
      else {
        if (hits.length >= 4 && hits.every((h) => h.exact)) add(hits[0].bar, name, "動機", `動機が${hits.length}回、高さもリズムも同じまま出る（${hits.map((h) => h.bar).join("・")}小節）。変形（高さをずらす・リズムを変える・断片にする）が見えない。`);
        let from = 1;
        for (const s of secs) {
          const to = from + Math.round(Number(s.bars)) - 1;
          if (Number(s.bars) >= 1 && !hits.some((h) => h.bar >= from && h.bar <= to)) add(from, name, "動機", `セクション「${s.kind}」（${from}〜${to}小節）に動機が現れない。`);
          from = to + 1;
        }
      }
    }
  }

  // 5. 入り方の重複（直前の曲と同じ）— novelty.mjs の判定を使う
  if (others.length) {
    noveltyFacts(song, others, plan).forEach((t) => add(1, "全体", "入り方の重複", t));
  }
  facts.sort((a, b) => a.bar - b.bar || FACT_KINDS.indexOf(a.kind) - FACT_KINDS.indexOf(b.kind));
  return { meta: { title: song.title, bars, beats, key: key?.label ?? null }, facts };
}

function noveltyFacts(song, others, plan) {
  const me = describeSong(song, "", plan);
  const o = others[0];
  const d = describeSong(o.song, o.name);
  return me.intro.id && me.intro.id === d.intro.id ? [`入り方が直前の曲「${o.name}」と同じ（${me.intro.id}：${me.intro.label}${me.intro.declared ? "" : "。推測"}）。`] : [];
}

/** 事実の一覧を、表（文字）にする。 */
export function formatFacts(result) {
  const { meta, facts } = result;
  const lines = [`■ ${meta.title}（${meta.bars}小節・${meta.beats}拍子${meta.key ? "・" + meta.key + "と推定" : ""}）事実の一覧: ${facts.length}件`];
  if (!facts.length) lines.push("  （該当なし）");
  else {
    lines.push("  小節 | パート | 種類 | 内容");
    for (const f of facts) lines.push(`  ${String(f.bar).padStart(3)} | ${f.part} | ${f.kind} | ${f.detail}`);
    const count = {};
    for (const f of facts) count[f.kind] = (count[f.kind] ?? 0) + 1;
    lines.push("  集計: " + Object.entries(count).map(([k, v]) => `${k} ${v}`).join("・"));
  }
  return lines.join("\n");
}

