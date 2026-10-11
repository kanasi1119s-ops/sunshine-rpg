// 動機変形の関数（docs/sound/melody-craft-guide.md §8 の提案 P7）。
// 「音名:拍」の文字列（例 "E4:1 G4:0.5 A4:1.5!"）→ 文字列。拍の合計が保たれることを前提に作ってある
// （拡大・縮小と断片化は意図して合計が変わる。断片化は pad: true で休符を足して合計を保てる）。
// 使い方（CLI）: node tools/composer/song.mjs motif <操作> "<動機>" [--n 2] [--tonic C] [--scale major|minor] ...
//   shift   … 音階内で n 度ずらす（--n 2）      semitone … 半音で n ずらす
//   invert  … 軸の音（--axis E4）で逆さに         retro    … 逆行
//   augment … 長さを倍率で伸ばす（--factor 2）    diminish … 縮める（--factor 2 で半分）
//   fragment … 先頭 n 音だけ（--n 3 [--pad]）     thin     … 1つおきに間引く（長さは前の音へ足す）
//   ornament … 長い音の頭に隣の音を足す（--minDur 1）
import { midi, midiName } from "../audio-check/score-lib.mjs";

export const SCALES = {
  major: [0, 2, 4, 5, 7, 9, 11],
  minor: [0, 2, 3, 5, 7, 8, 10],
  harmonicMinor: [0, 2, 3, 5, 7, 8, 11],
  dorian: [0, 2, 3, 5, 7, 9, 10],
  mixolydian: [0, 2, 4, 5, 7, 9, 10],
  pentatonic: [0, 2, 4, 7, 9],
  minorPentatonic: [0, 3, 5, 7, 10],
  miyako: [0, 1, 5, 7, 8],
  ritsu: [0, 2, 5, 7, 9],
};

const TOKEN = /^(R|r|[A-G][#b]?-?\d)(?::(\d+(?:\.\d+)?)([!,'_~^/\\*]*))?$/;

/** "E4:1 R:0.5" → [{ name, pitch, dur, mark, rest }] */
export function parseMotif(str) {
  const out = [];
  for (const tok of String(str).trim().split(/\s+/).filter(Boolean)) {
    const m = TOKEN.exec(tok);
    if (!m) throw new Error(`読めない音です: ${tok}（"E4:1" や "R:0.5" の形で書く）`);
    const rest = m[1] === "R" || m[1] === "r";
    out.push({ name: m[1], pitch: rest ? null : midi(m[1]), dur: m[2] === undefined ? 1 : Number(m[2]), mark: m[3] ?? "", rest });
  }
  return out;
}

const fmt = (x) => String(+x.toFixed(4));
/** 音の並びを文字列へ */
export function formatMotif(notes) {
  return notes.map((n) => `${n.rest ? "R" : midiName(n.pitch).replace(/^([A-G])#/, "$1#")}:${fmt(n.dur)}${n.mark ?? ""}`).join(" ");
}

export const totalBeats = (str) => parseMotif(str).reduce((s, n) => s + n.dur, 0);

const scaleOf = (scale) => (Array.isArray(scale) ? scale : SCALES[scale] ?? SCALES.major);
const tonicPc = (tonic) => {
  if (typeof tonic === "number") return ((tonic % 12) + 12) % 12;
  const m = /^([A-G])([#b]?)$/.exec(tonic ?? "C");
  if (!m) throw new Error(`主音が読めません: ${tonic}`);
  return (midi(`${m[1]}${m[2]}4`) % 12);
};

/** MIDI 番号 → 音階上の位置（度数の通し番号と、音階からの半音のずれ）。音階外なら直下の音階音からのずれで持つ。 */
function toDegree(pitch, tonic, scale) {
  const rel = pitch - tonic;
  const oct = Math.floor(rel / 12);
  const pc = rel - oct * 12;
  let idx = 0;
  for (let i = 0; i < scale.length; i++) if (scale[i] <= pc) idx = i;
  return { deg: oct * scale.length + idx, off: pc - scale[idx] };
}
function fromDegree(deg, off, tonic, scale) {
  const n = scale.length;
  const oct = Math.floor(deg / n);
  const idx = ((deg % n) + n) % n;
  return tonic + oct * 12 + scale[idx] + off;
}

/** 音階内で steps 度ずらす（音階外の音は直下の音階音からのずれを保つ）。 */
export function shiftDiatonic(str, steps, { tonic = "C", scale = "major" } = {}) {
  const sc = scaleOf(scale), t = tonicPc(tonic);
  return formatMotif(parseMotif(str).map((n) => {
    if (n.rest) return n;
    const d = toDegree(n.pitch, t, sc);
    return { ...n, pitch: fromDegree(d.deg + steps, d.off, t, sc) };
  }));
}

/** 半音で semis ずらす。 */
export function shiftSemitones(str, semis) {
  return formatMotif(parseMotif(str).map((n) => (n.rest ? n : { ...n, pitch: n.pitch + semis })));
}

/**
 * 逆さ（反転）: 軸の音を中心に上下をひっくり返す。scale を渡すと、音階の度数で反転する（音階内に収まる）。
 * 渡さなければ半音で反転。axis は音名（"E4"）。
 */
export function invert(str, axis, { tonic = null, scale = null } = {}) {
  const ax = typeof axis === "number" ? axis : midi(axis);
  if (ax === null || Number.isNaN(ax)) throw new Error(`軸の音が読めません: ${axis}`);
  const notes = parseMotif(str);
  if (scale) {
    const sc = scaleOf(scale), t = tonicPc(tonic ?? "C");
    const a = toDegree(ax, t, sc);
    return formatMotif(notes.map((n) => {
      if (n.rest) return n;
      const d = toDegree(n.pitch, t, sc);
      return { ...n, pitch: fromDegree(2 * a.deg - d.deg, -d.off, t, sc) };
    }));
  }
  return formatMotif(notes.map((n) => (n.rest ? n : { ...n, pitch: 2 * ax - n.pitch })));
}

/** 逆行: 音を後ろから並べる（長さも音と一緒に動く）。 */
export function retrograde(str) {
  return formatMotif(parseMotif(str).reverse());
}

/** 拡大: 長さを factor 倍する（0.5 で縮小）。合計は factor 倍になる。 */
export function augment(str, factor = 2) {
  if (!(factor > 0)) throw new Error("倍率は正の数にしてください");
  return formatMotif(parseMotif(str).map((n) => ({ ...n, dur: n.dur * factor })));
}
/** 縮小: 長さを 1/factor にする。 */
export const diminish = (str, factor = 2) => augment(str, 1 / factor);

/** 断片化: 先頭 n 音だけを残す。pad: true なら残りの拍を休符で埋めて合計を保つ。 */
export function fragment(str, n, { pad = false } = {}) {
  const notes = parseMotif(str);
  const total = notes.reduce((s, x) => s + x.dur, 0);
  const keep = notes.slice(0, Math.max(1, n));
  const used = keep.reduce((s, x) => s + x.dur, 0);
  if (pad && total - used > 1e-9) keep.push({ name: "R", pitch: null, dur: total - used, mark: "", rest: true });
  return formatMotif(keep);
}

/** 間引き: 1つおきに音を落とし、落とした音の長さは直前の音へ足す（合計は保たれる）。 */
export function thin(str) {
  const notes = parseMotif(str);
  const out = [];
  notes.forEach((n, i) => {
    if (i % 2 === 1 && out.length) out[out.length - 1] = { ...out[out.length - 1], dur: out[out.length - 1].dur + n.dur };
    else out.push({ ...n });
  });
  return formatMotif(out);
}

/**
 * 装飾: minDur 拍以上の音の頭に、音階内の下隣の音を 0.25 拍だけ足す（前打音ふうに、長さは元の音から引く。合計は保たれる）。
 * 下隣のかわりに upper: true で上隣。
 */
export function ornament(str, { tonic = "C", scale = "major", minDur = 1, upper = false } = {}) {
  const sc = scaleOf(scale), t = tonicPc(tonic);
  const out = [];
  for (const n of parseMotif(str)) {
    if (n.rest || n.dur < minDur - 1e-9 || n.dur <= 0.25) { out.push(n); continue; }
    const d = toDegree(n.pitch, t, sc);
    out.push({ name: "", pitch: fromDegree(d.deg + (upper ? 1 : -1), 0, t, sc), dur: 0.25, mark: "", rest: false });
    out.push({ ...n, dur: n.dur - 0.25 });
  }
  return formatMotif(out);
}

/** CLI から使う入口。args は ["shift", "E4:1 G4:1", "--n", "2", ...] */
export function runMotifCommand(args) {
  const op = args[0];
  const motif = args[1];
  const opt = (name, d) => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : d; };
  const num = (name, d) => (opt(name, undefined) === undefined ? d : Number(opt(name)));
  const sc = { tonic: opt("--tonic", "C"), scale: opt("--scale", "major") };
  if (!op || motif === undefined) throw new Error("使い方: song.mjs motif <shift|semitone|invert|retro|augment|diminish|fragment|thin|ornament> \"<動機>\" [--n 2] [--tonic C] [--scale major] [--axis E4] [--factor 2] [--pad] [--minDur 1]");
  switch (op) {
    case "shift": return shiftDiatonic(motif, num("--n", 1), sc);
    case "semitone": return shiftSemitones(motif, num("--n", 1));
    case "invert": return invert(motif, opt("--axis", parseMotif(motif).find((n) => !n.rest)?.name), args.includes("--scale") ? sc : {});
    case "retro": return retrograde(motif);
    case "augment": return augment(motif, num("--factor", 2));
    case "diminish": return diminish(motif, num("--factor", 2));
    case "fragment": return fragment(motif, num("--n", 2), { pad: args.includes("--pad") });
    case "thin": return thin(motif);
    case "ornament": return ornament(motif, { ...sc, minDur: num("--minDur", 1), upper: args.includes("--upper") });
    default: throw new Error(`知らない操作です: ${op}`);
  }
}
