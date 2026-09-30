// バンド曲ジェネレーター（作曲用の補助。曲のJSONを書き出す）
import fs from 'node:fs';
const PC = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };
const SHARP = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
const FLAT = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B'];
const RANGE = {
  bass: [28, 55], slap: [28, 55], sub808: [24, 48], guitar: [40, 76], crunch: [40, 76], distGuitar: [40, 64],
  leadGuitar: [52, 88], echoGuitar: [52, 88], piano: [21, 108], keys: [36, 84], harpsichord: [36, 84],
  strings: [36, 96], pad: [36, 84], choir: [48, 84], brass: [40, 84], lead: [48, 96], bell: [60, 96],
};
const DRUMS = ['kick', 'snare', 'hihat', 'crash', 'tom'];

function parseChord(sym) {
  const m = /^([A-G])([#b]?)(.*)$/.exec(sym);
  if (!m) throw new Error('chord ' + sym);
  let pc = PC[m[1]] + (m[2] === '#' ? 1 : m[2] === 'b' ? -1 : 0);
  pc = (pc + 12) % 12;
  const q = m[3];
  const minor = /^m(?!aj)/.test(q);
  return { pc, minor, dim: q.startsWith('dim'), sus: q.startsWith('sus'), maj7: q.includes('maj7'), sev: /7/.test(q) };
}
function rootMidi(pc, base) { let m = base; while (m % 12 !== pc) m++; return m; }
function scaleSet(tonic, mode) {
  const t = PC[tonic[0]] + (tonic[1] === '#' ? 1 : tonic[1] === 'b' ? -1 : 0);
  const iv = mode === 'minor' ? [0, 2, 3, 5, 7, 8, 10] : [0, 2, 4, 5, 7, 9, 11];
  return new Set(iv.map((i) => (t + i + 12) % 12));
}
function name(m, flat) { return (flat ? FLAT : SHARP)[m % 12] + (Math.floor(m / 12) - 1); }
function parseNote(s) {
  const m = /^([A-G])([#b]?)(-?\d)$/.exec(s);
  if (!m) return null;
  return PC[m[1]] + (m[2] === '#' ? 1 : m[2] === 'b' ? -1 : 0) + 12 * (Number(m[3]) + 1);
}

export function build(spec) {
  const beats = spec.beats || 4;
  const S = beats * 4;
  const flat = !!spec.flat;
  const scale = scaleSet(spec.tonic, spec.mode);
  // 全小節のコードを並べる
  const bars = [];
  spec.sections.forEach((sec, si) => {
    sec.chords.trim().split(/\s+/).forEach((c, i) => bars.push({ sec, si, i, chord: c, n: sec.chords.trim().split(/\s+/).length }));
  });
  const out = {};
  for (const p of spec.parts) out[p.id] = [];
  const isFillBar = bars.map((b) => {
    const f = b.sec.fill === undefined ? 4 : b.sec.fill;
    if (b.sec.nofill || !b.sec.dr) return false;
    if (b.i === b.n - 1) return true;
    return f > 0 && b.i % f === f - 1;
  });

  const fail = (msg) => { throw new Error(spec.id + ': ' + msg); };

  bars.forEach((b, bi) => {
    const ch = parseChord(b.chord);
    const nx = bars[bi + 1] ? parseChord(bars[bi + 1].chord) : ch;
    for (const p of spec.parts) {
      const loc = `${p.id} bar${bi + 1}(${b.sec.name}#${b.i + 1})`;
      if (DRUMS.includes(p.instrument)) continue;
      let pat = b.sec.p && b.sec.p[p.id];
      if (Array.isArray(pat)) pat = pat[b.i % pat.length];
      if (!pat) pat = `R:${beats}`;
      const toks = pat.trim().split(/\s+/);
      let sum = 0;
      const outToks = [];
      for (const t of toks) {
        const [nm, dstr] = t.split(':');
        const d = Number(dstr);
        if (!(d > 0)) fail(`拍が読めません ${loc} "${t}"`);
        sum += d;
        if (nm === 'R') { outToks.push(`R:${d}`); continue; }
        let midi = parseNote(nm);
        const [lo, hi] = RANGE[p.instrument];
        if (midi === null) {
          const mm = /^([rtfsnaAo])([+-]*)$/.exec(nm);
          if (!mm) fail(`音が読めません ${loc} "${t}"`);
          const base = p.base || 48;
          const R0 = rootMidi(ch.pc, base);
          let v;
          const k = mm[1];
          if (k === 'a' || k === 'A') {
            let R1 = rootMidi(nx.pc, base);
            while (R1 - R0 > 6) R1 -= 12;
            while (R0 - R1 > 6) R1 += 12;
            if (nx.pc === ch.pc) v = R0;
            else if (k === 'a') v = scale.has((R1 - 2 + 120) % 12) ? R1 - 2 : R1 - 1;
            else v = scale.has((R1 + 2) % 12) ? R1 + 2 : R1 + 1;
          } else {
            const third = ch.sus ? 5 : ch.minor || ch.dim ? 3 : 4;
            const fifth = ch.dim ? 6 : 7;
            const sev = ch.maj7 ? 11 : ch.sev || ch.minor ? 10 : 9;
            const iv = { r: 0, o: 12, t: third, f: fifth, s: sev, n: 14 }[k];
            v = R0 + iv;
          }
          for (const c of mm[2]) v += c === '+' ? 12 : -12;
          while (v > hi) v -= 12;
          while (v < lo) v += 12;
          midi = v;
        } else if (midi < lo || midi > hi) {
          fail(`音域外 ${loc} "${t}" (${name(lo, flat)}〜${name(hi, flat)})`);
        }
        outToks.push(`${name(midi, flat)}:${d}`);
      }
      if (Math.abs(sum - beats) > 1e-9) fail(`拍の合計が${sum}（${beats}のはず）${loc} "${pat}"`);
      out[p.id].push(...outToks);
    }
    // ドラム
    const kit = b.sec.dr ? spec.drums[b.sec.dr] : null;
    const fill = isFillBar[bi];
    const prevFill = bi > 0 && isFillBar[bi - 1];
    const hasTom = spec.parts.some((p) => p.instrument === 'tom');
    const steps = {};
    for (const key of ['k', 's', 'h', 'c', 't']) {
      const src = kit && kit[key] ? kit[key] : '.'.repeat(S);
      if (src.length !== S) fail(`ドラム型の長さ ${b.sec.dr}.${key} ${src.length}!=${S}`);
      steps[key] = src.split('').map((ch2) => ch2 === 'x');
    }
    if (kit && prevFill && b.sec.crash !== false && !kit.nocrash) steps.c[0] = true;
    if (kit && b.i === 0 && b.sec.crash) steps.c[0] = true;
    if (kit && fill) {
      const ft = b.sec.ft || 'a';
      let from = S - 4;
      let sn = [], tm = [];
      if (ft === 'a') { from = S - 4; sn = hasTom ? [S - 4, S - 3] : [S - 4, S - 3, S - 2, S - 1]; tm = hasTom ? [S - 2, S - 1] : []; }
      if (ft === 'b') { from = S - 8; sn = hasTom ? [S - 8, S - 6] : [S - 8, S - 6, S - 4, S - 3, S - 2, S - 1]; tm = hasTom ? [S - 4, S - 3, S - 2, S - 1] : []; }
      if (ft === 'c') { from = S - 4; sn = [S - 4, S - 2, S - 1]; tm = []; }
      for (let s = from; s < S; s++) { steps.k[s] = false; steps.h[s] = false; steps.s[s] = false; steps.t[s] = false; steps.c[s] = false; }
      if (ft === 'a' || ft === 'b') steps.k[from] = ft === 'a';
      sn.forEach((s) => (steps.s[s] = true));
      tm.forEach((s) => (steps.t[s] = true));
    }
    const map = { kick: 'k', snare: 's', hihat: 'h', crash: 'c', tom: 't' };
    for (const p of spec.parts) {
      if (!DRUMS.includes(p.instrument)) continue;
      const arr = steps[map[p.instrument]];
      for (let s = 0; s < S; s++) out[p.id].push(arr[s] ? 'x:0.25' : 'R:0.25');
    }
  });
  const totalBars = bars.length;
  const parts = spec.parts.map((p) => {
    // 休みをまとめる
    const merged = [];
    for (const t of out[p.id]) {
      const [n, d] = t.split(':');
      const last = merged[merged.length - 1];
      if (n === 'R' && last && last[0] === 'R') last[1] += Number(d);
      else merged.push([n, Number(d)]);
    }
    // 長い休みは 16 拍ごとに分割しない（そのまま）
    return { instrument: p.instrument, role: p.role, volume: p.volume, pan: p.pan || 0, amp: p.amp || 'auto', notes: merged.map(([n, d]) => `${n}:${d}`).join(' ') };
  });
  const json = {
    title: spec.title, description: spec.description, bpm: spec.bpm, beats, chords: bars.map((b) => b.chord).join(' '),
    barsPerChord: 1, repeats: 1, autoAccompaniment: false, feel: spec.feel || 'rock', tone: spec.tone || 'rock', parts,
  };
  fs.writeFileSync(new URL(`../${spec.id}.json`, import.meta.url), JSON.stringify(json, null, 2) + '\n');
  const sec = ((totalBars * beats) / spec.bpm) * 60;
  console.log(`${spec.id}: ${totalBars}小節 ${sec.toFixed(1)}秒`);
}

// 便利: 同じ型をn小節くり返した配列
export const rep = (s, n) => Array(n).fill(s);
