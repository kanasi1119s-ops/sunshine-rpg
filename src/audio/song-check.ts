/**
 * 曲の自動チェック（2026-10-07）。曲を作ったあとに「ここがよくないかも」を、日本語の注意として返す。
 * - checkScore: 楽譜（音の並び）を見る。低音のにごり・同じ音域のぶつかり・単調さ。
 * - analyzeMix: 鳴らした音（WAVの波形）を見る。音割れ・低音の多すぎ・強弱の平らさ・途中の無音。
 * 注意は直すヒントつき。曲が作れなくなるものではない（警告だけ）。
 */
import { measureLufs } from "./loudness";
import { noteNameToMidi } from "./note";
import { REST, type Instrument, type Score } from "./score";

const NO_PITCH = new Set<string>(["kick", "snare", "hihat", "crash", "tom", "cowbell", "sfxDown", "sfxUp", "impact", "swoosh", "pierce", "wind", "rain", "stream", "bird", "crickets"]);
const BASS = new Set<string>(["bass", "slap", "sub808"]);
const LABEL: Partial<Record<Instrument, string>> = { bass: "ベース", slap: "スラップベース", sub808: "808", lead: "リード", piano: "ピアノ", strings: "弦", pad: "パッド", choir: "合唱", brass: "ブラス", guitar: "ギター", keys: "鍵盤" };
const name = (inst: string | undefined, i: number): string => `${LABEL[inst as Instrument] ?? inst ?? "パート"}（${i + 1}番目）`;

interface Span { start: number; end: number; midi: number }

function spans(track: Score["tracks"][number]): Span[] {
  const out: Span[] = [];
  let pos = 0;
  for (const n of track.notes) {
    if (n.note !== REST) {
      let midi = NaN;
      try { midi = noteNameToMidi(n.note); } catch { /* 読めない音名は数えない */ }
      if (Number.isFinite(midi)) out.push({ start: pos, end: pos + n.durationBeats * Math.max(0.2, Math.min(1.5, n.gate ?? 1)), midi });
    }
    pos += n.durationBeats;
  }
  return out;
}

const median = (a: number[]): number => { const s = [...a].sort((x, y) => x - y); return s[Math.floor(s.length / 2)]; };

export function checkScore(score: Score): string[] {
  const warnings: string[] = [];
  const pitched = score.tracks
    .map((t, i) => ({ t, i, sp: NO_PITCH.has(t.instrument ?? "") || t.gmDrum ? [] : spans(t) }))
    .filter((x) => x.sp.length > 0);
  const total = Math.max(0, ...pitched.flatMap((x) => x.sp.map((s) => s.end)));

  // 1. 低音のにごり: C♯3（MIDI 52）より下で、別々のパートが近い高さ（1〜3半音差）を同時に鳴らしている時間の割合
  if (total > 0 && pitched.length > 1) {
    let muddy = 0, steps = 0;
    for (let b = 0; b < total; b += 0.5) {
      steps++;
      const low = pitched.flatMap((x) => x.sp.filter((s) => s.start <= b && b < s.end && s.midi < 52).map((s) => ({ i: x.i, midi: s.midi })));
      if (low.some((a, k) => low.some((c, j) => j > k && a.i !== c.i && Math.abs(a.midi - c.midi) >= 1 && Math.abs(a.midi - c.midi) <= 3))) muddy++;
    }
    if (muddy / steps > 0.08) warnings.push(`低音がにごりそうです: 低い音域（C♯3より下）で、別のパートが近い高さ（1〜3半音差）を同時に鳴らしている時間が ${Math.round((muddy / steps) * 100)}% あります。低い音はベースだけにするか、ほかのパートを1オクターブ上げてください。`);
  }

  // 2. 同じ音域のぶつかり: ベース以外の2パートの中央値が2半音以内で、どちらも音数が多い
  const mid = pitched.filter((x) => !BASS.has(x.t.instrument ?? "") && x.sp.length >= 16);
  for (let a = 0; a < mid.length; a++) {
    for (let b = a + 1; b < mid.length; b++) {
      if (Math.abs(median(mid[a].sp.map((s) => s.midi)) - median(mid[b].sp.map((s) => s.midi))) <= 2) {
        warnings.push(`${name(mid[a].t.instrument, mid[a].i)}と${name(mid[b].t.instrument, mid[b].i)}が、ほぼ同じ音域で重なっています。どちらかを3度〜1オクターブずらすと、音がぶつからず聞き分けやすくなります。`);
      }
    }
  }

  // 3. 単調さ: 同じ音ばかり／音の長さも強さも一定
  let anyVariation = false;
  for (const x of pitched) {
    const notes = x.t.notes.filter((n) => n.note !== REST);
    if (notes.length < 16) continue;
    if (new Set(x.sp.map((s) => s.midi)).size <= 2 && !BASS.has(x.t.instrument ?? "")) warnings.push(`${name(x.t.instrument, x.i)}が、ほぼ同じ音（${new Set(x.sp.map((s) => s.midi)).size}種類）だけを繰り返しています。単調に聞こえるかもしれません。`);
    if (new Set(notes.map((n) => n.velocity ?? 1)).size > 1 || new Set(notes.map((n) => n.gate ?? 1)).size > 1) anyVariation = true;
  }
  if (pitched.length && !anyVariation && score.swing === undefined) warnings.push("どのパートも音の強さ・長さが一定です。メロディに phrase（フレーズの強弱）や、奏法の記号（! , ' _）、曲全体に dynamics: true を足すと、機械的に聞こえにくくなります。");
  return warnings;
}

/** 鳴らした音を調べる。channels は書き出し後（音量をそろえたあと）の波形。 */
export function analyzeMix(channels: Float32Array[], sampleRate: number): string[] {
  const warnings: string[] = [];
  const n = channels[0]?.length ?? 0;
  if (!n) return ["音が空です。"];
  // 音割れ: 山が天井（±0.999）に張りついたサンプル
  let clipped = 0, peak = 0;
  for (const c of channels) for (let i = 0; i < n; i++) { const a = Math.abs(c[i]); if (a > peak) peak = a; if (a >= 0.999) clipped++; }
  if (clipped > 0) warnings.push(`音が割れている所があります（天井に当たった音が ${clipped} 回）。パートの volume を下げるか、重なる音を減らしてください。`);
  // 強弱の幅（3秒ごとの聞こえる大きさの、大きい所と小さい所の差）
  const win = Math.round(3 * sampleRate);
  const levels: number[] = [];
  for (let s = 0; s + win <= n; s += win) levels.push(measureLufs(channels.map((c) => c.subarray(s, s + win)), sampleRate));
  const live = levels.filter((l) => Number.isFinite(l) && l > -50).sort((a, b) => a - b);
  if (live.length >= 4) {
    const range = live[Math.floor(live.length * 0.95)] - live[Math.floor(live.length * 0.1)];
    if (range < 2) warnings.push(`曲の中の強弱がほとんどありません（大きい所と小さい所の差が ${range.toFixed(1)}dB）。出だしを小さく始める・サビで厚くする・間奏で引く、など起伏をつけてください。`);
  }
  // 途中の無音（4秒以上）。曲の頭と終わりの余韻は数えない
  const first = levels.findIndex((l) => Number.isFinite(l) && l > -60), last = levels.length - 1 - [...levels].reverse().findIndex((l) => Number.isFinite(l) && l > -60);
  let gap = 0;
  for (let i = Math.max(0, first); i <= last; i++) { gap = !Number.isFinite(levels[i]) || levels[i] < -60 ? gap + 1 : 0; if (gap >= 2) { warnings.push(`曲の途中に ${(gap * 3).toFixed(0)}秒以上の無音があります。意図したものでなければ、パートの入りを確かめてください。`); break; } }
  // 低音の多すぎ: 150Hz より下のエネルギーの割合（左右を足した音に、1極ローパスを2段）
  let lo = 0, all = 0, y1 = 0, y2 = 0;
  const k = 1 - Math.exp((-2 * Math.PI * 150) / sampleRate);
  for (let i = 0; i < n; i++) {
    const m = channels.reduce((s, c) => s + c[i], 0) / channels.length;
    y1 += k * (m - y1); y2 += k * (y1 - y2);
    lo += y2 * y2; all += m * m;
  }
  if (all > 0 && lo / all > 0.7) warnings.push(`低音が多すぎます（150Hz以下がエネルギーの ${Math.round((lo / all) * 100)}%）。ベース・キック・パッドの低い音を減らすと、メロディが聞こえやすくなります。`);
  return warnings;
}
