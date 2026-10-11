/**
 * テンポマップ（途中でテンポが変わる曲）。docs/sound/rhythm-groove-guide.md §10 の提案5・7。
 * - `Score.tempoMap`：拍の位置ごとのテンポ。`ramp`（拍）があれば、その長さで直線的に速まり・遅まり。
 * - 拍→秒の変換を `makeTempoClock` にまとめる。MIDI書き出し（テンポイベント）と再生（flattenScore）で同じ値を使う。
 * - `ritPoints`：終わりの減速（rit.）の曲線。v(x) = (1 + (w^q − 1)·x)^(1/q)（w＝最後の速さ÷最初、q＝2、x＝0〜1）。
 * - `rubatoPoints`：ルバート。ループの長さで1周して元に戻る、ゆるやかなテンポのゆれと、フレーズの終わりの小さな伸び。
 * テンポマップが無い曲は、今までと同じ計算（拍×60÷bpm）のまま。
 */

export interface TempoPoint {
  /** この拍から変わる（0始まりの拍位置）。 */
  beat: number;
  bpm: number;
  /** 拍。指定すると、beat から beat+ramp にかけて直線的に bpm へ近づく（1/8拍ごとの階段で近似）。省略は、beat でいきなり変わる。 */
  ramp?: number;
}

export interface TempoSeg {
  beat: number;
  bpm: number;
}

export const RAMP_STEP = 0.125;
export const MIN_BPM = 20;
export const MAX_BPM = 300;
const clampBpm = (b: number): number => Math.max(MIN_BPM, Math.min(MAX_BPM, b));

/** 点の並びを、階段状の区間（beat から次の区間まで一定の bpm）に展開する。先頭は必ず beat 0。 */
export function expandTempoMap(baseBpm: number, map?: readonly TempoPoint[]): TempoSeg[] {
  const segs: TempoSeg[] = [{ beat: 0, bpm: baseBpm }];
  if (!map || map.length === 0) return segs;
  const put = (beat: number, bpm: number): void => {
    const b = Math.max(0, Math.round(beat * 1e6) / 1e6);
    const v = clampBpm(bpm);
    const last = segs[segs.length - 1];
    if (b <= last.beat + 1e-9) {
      // 同じ位置は後のものが勝つ（先頭の beat 0 も上書きできる）
      last.bpm = v;
      return;
    }
    if (Math.abs(last.bpm - v) < 1e-9) return;
    segs.push({ beat: b, bpm: v });
  };
  const sorted = [...map].filter((p) => Number.isFinite(p.beat) && Number.isFinite(p.bpm) && p.bpm > 0).sort((a, b) => a.beat - b.beat);
  for (const p of sorted) {
    const from = segs[segs.length - 1].bpm;
    const ramp = Number(p.ramp) > 0 ? Number(p.ramp) : 0;
    if (ramp > 0) {
      const n = Math.max(1, Math.ceil(ramp / RAMP_STEP - 1e-9));
      for (let i = 0; i < n; i++) put(p.beat + (i * ramp) / n, from + (p.bpm - from) * ((i + 0.5) / n));
      put(p.beat + ramp, p.bpm);
    } else put(p.beat, p.bpm);
  }
  return segs;
}

export interface TempoClock {
  segs: TempoSeg[];
  /** 拍の位置 → 秒。 */
  beatToSec(beat: number): number;
  /** 秒 → 拍の位置。 */
  secToBeat(sec: number): number;
  /** その拍でのテンポ。 */
  bpmAt(beat: number): number;
  /** テンポマップが無い（今までと同じ計算）。 */
  constant: boolean;
}

/** 拍と秒を変換する時計。マップが無いときは (拍×60)÷bpm で、今までと全く同じ値になる。 */
export function makeTempoClock(baseBpm: number, map?: readonly TempoPoint[]): TempoClock {
  if (!map || map.length === 0) {
    return {
      segs: [{ beat: 0, bpm: baseBpm }],
      beatToSec: (beat) => (beat * 60) / baseBpm,
      secToBeat: (sec) => (sec * baseBpm) / 60,
      bpmAt: () => baseBpm,
      constant: true,
    };
  }
  const segs = expandTempoMap(baseBpm, map);
  // 区間の始まりの秒（累積）
  const secAt: number[] = [0];
  for (let i = 1; i < segs.length; i++) secAt.push(secAt[i - 1] + ((segs[i].beat - segs[i - 1].beat) * 60) / segs[i - 1].bpm);
  const index = (beat: number): number => {
    let lo = 0, hi = segs.length - 1;
    while (lo < hi) {
      const mid = (lo + hi + 1) >> 1;
      if (segs[mid].beat <= beat + 1e-12) lo = mid;
      else hi = mid - 1;
    }
    return lo;
  };
  return {
    segs,
    constant: false,
    beatToSec(beat) {
      const i = index(Math.max(0, beat));
      return secAt[i] + ((Math.max(0, beat) - segs[i].beat) * 60) / segs[i].bpm;
    },
    secToBeat(sec) {
      let lo = 0, hi = segs.length - 1;
      while (lo < hi) {
        const mid = (lo + hi + 1) >> 1;
        if (secAt[mid] <= sec + 1e-12) lo = mid;
        else hi = mid - 1;
      }
      return segs[lo].beat + ((Math.max(0, sec) - secAt[lo]) * segs[lo].bpm) / 60;
    },
    bpmAt: (beat) => segs[index(Math.max(0, beat))].bpm,
  };
}

/** 曲の長さ（秒）。 */
export function tempoDurationSec(baseBpm: number, map: readonly TempoPoint[] | undefined, totalBeats: number): number {
  return makeTempoClock(baseBpm, map).beatToSec(totalBeats);
}

/** 終わりの減速の速さの曲線 v(x)。x＝0〜1、w＝最後の速さ÷最初の速さ（0.7 なら 30% 遅く）、q＝形（2が既定。大きいほど終わりに急）。 */
export function ritSpeed(x: number, w: number, q = 2): number {
  const xx = Math.max(0, Math.min(1, x));
  return Math.pow(1 + (Math.pow(w, q) - 1) * xx, 1 / q);
}

export interface RitSpec {
  /** 始まりの拍。 */
  beat: number;
  /** 減速（加速）にかける拍の数。 */
  beats: number;
  /** 最後の速さ ÷ 最初の速さ。0.7＝30%遅く、1.2＝20%速く。 */
  to: number;
  /** 曲線の形（既定 2）。 */
  q?: number;
  /** true なら、終わったところで元のテンポに戻る（a tempo。曲の途中の rit 向け）。 */
  aTempo?: boolean;
}

/** rit. をテンポ点の並びにする（半拍ごとの階段）。baseBpm は rit の直前のテンポ。 */
export function ritPoints(spec: RitSpec, baseBpm: number): TempoPoint[] {
  const to = Math.max(0.3, Math.min(3, spec.to));
  const n = Math.max(1, Math.round(spec.beats * 2));
  const out: TempoPoint[] = [];
  for (let i = 0; i < n; i++) out.push({ beat: spec.beat + (i * spec.beats) / n, bpm: baseBpm * ritSpeed((i + 0.5) / n, to, spec.q ?? 2) });
  out.push({ beat: spec.beat + spec.beats, bpm: spec.aTempo ? baseBpm : baseBpm * to });
  return out;
}

export interface RubatoSpec {
  /** 0〜1。0＝なし、1＝テンポが ±3% ほどゆれ、フレーズの終わりで最大 5% 伸びる。 */
  amount: number;
  totalBeats: number;
  beatsPerBar: number;
  /** フレーズの長さ（小節）。既定 4。 */
  phraseBars?: number;
}

/** ゆれの倍率（1が元のテンポ）。曲の頭と末尾で連続するよう、周期は totalBeats をわりきる長さにする。 */
export function rubatoFactor(beat: number, spec: RubatoSpec): number {
  const a = Math.max(0, Math.min(1, spec.amount));
  if (a === 0 || spec.totalBeats <= 0) return 1;
  // ゆるやかなゆれ: 周期はおよそ3小節。曲をちょうど整数回まわす（ループで元に戻る）
  const cycles = Math.max(1, Math.round(spec.totalBeats / (spec.beatsPerBar * 3)));
  const wave = Math.sin((2 * Math.PI * cycles * beat) / spec.totalBeats);
  let f = 1 + 0.03 * a * wave;
  // フレーズの終わりの小さな伸び: 最後の拍で −5%、その前の拍で −2%
  const phrase = spec.beatsPerBar * (spec.phraseBars ?? 4);
  if (phrase > 0 && spec.totalBeats >= phrase) {
    const pos = beat % phrase;
    const left = phrase - pos;
    if (left <= 1) f *= 1 - 0.05 * a;
    else if (left <= 2) f *= 1 - 0.02 * a;
  }
  return f;
}

/** ルバートをかけたテンポ点の並びを返す。explicit（既にある点）の区間の上に、1拍ごとのゆれの倍率を掛ける。 */
export function rubatoPoints(baseBpm: number, explicit: readonly TempoPoint[] | undefined, spec: RubatoSpec): TempoPoint[] {
  if (!(spec.amount > 0) || !(spec.totalBeats > 0)) return explicit ? [...explicit] : [];
  const segs = expandTempoMap(baseBpm, explicit);
  const bpmOf = (beat: number): number => {
    let v = segs[0].bpm;
    for (const s of segs) if (s.beat <= beat + 1e-9) v = s.bpm;
    return v;
  };
  const marks = new Set<number>();
  for (let b = 0; b < spec.totalBeats; b++) marks.add(b);
  for (const s of segs) if (s.beat < spec.totalBeats) marks.add(s.beat);
  const out: TempoPoint[] = [];
  for (const b of [...marks].sort((x, y) => x - y)) {
    // 区間の真ん中でゆれを測る（1拍ぶんの平均）
    const mid = Math.min(spec.totalBeats, b + 0.5);
    out.push({ beat: b, bpm: Math.round(bpmOf(b) * rubatoFactor(mid, spec) * 1000) / 1000 });
  }
  return out;
}

/** ループ曲で、最後のテンポと最初のテンポが違うとき、継ぎ目の警告文を返す（なければ null）。 */
export function loopTempoWarning(baseBpm: number, map: readonly TempoPoint[] | undefined, totalBeats: number): string | null {
  if (!map || map.length === 0) return null;
  const clock = makeTempoClock(baseBpm, map);
  const last = clock.bpmAt(Math.max(0, totalBeats - 1e-6));
  const first = clock.segs[0].bpm;
  if (Math.abs(last - first) / first > 0.03) return `ループの継ぎ目でテンポが飛びます（曲の頭 ${Math.round(first)}、最後 ${Math.round(last)}）。rit のあとに aTempo を付けるか、別の曲に分けてください`;
  return null;
}
