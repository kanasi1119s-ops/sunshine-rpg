/**
 * ドラム（ノイズパート）の音色。
 *
 * ファミコン世代の音源が「ノイズ」の1チャンネルで打楽器を鳴らしていた考え方にならい、
 * ホワイトノイズを短く鳴らし、フィルター（通す音域）と長さで楽器を作り分ける。
 * キックとタムだけは、ノイズだけでは低い「ドン」が出にくいため、音程を急に下げる
 * サイン波（ピッチの落ちる短い音）で作り、ノイズを少しだけ重ねてアタックを付ける。
 *
 * ブラウザに入っている Web Audio API の部品だけで作る（外部の音声ファイル・サンプルは使わない）。
 * 実在のドラムマシンや特定の機材の音を写したものではない（CLAUDE.md 1-1）。
 *
 * 楽譜での書き方: パートの `waveform` を `"noise"` にし、音名の代わりに下の記号を書く。
 *   例: notes("K:0.5 H:0.5 S:0.5 H:0.5")
 */

export type DrumKind =
  /** キック（バスドラム）。いちばん低い「ドン」。 */
  | "K"
  /** スネア。「タッ」「パン」。 */
  | "S"
  /** クローズド・ハイハット。短い「チッ」。 */
  | "H"
  /** オープン・ハイハット。長めの「シャー」。 */
  | "O"
  /** クラッシュ・シンバル。長い「ジャーン」。 */
  | "C"
  /** 高いタム。 */
  | "T"
  /** 低いタム。 */
  | "L"
  /** クラップ（手拍子）。 */
  | "P"
  /** リムショット（ふちを打つ「カッ」）。 */
  | "R2";

export interface DrumSettings {
  label: string;
  /** ノイズを通すフィルターの種類。 */
  noiseFilter: "highpass" | "bandpass" | "lowpass";
  /** フィルターの周波数（Hz）。 */
  noiseFilterHz: number;
  /** フィルターの鋭さ。 */
  noiseQ: number;
  /** ノイズの大きさ（0なら鳴らさない）。 */
  noiseGain: number;
  /** ノイズが消えるまでの時間（秒）。 */
  noiseDecaySec: number;
  /** ピッチの落ちる音（キック・タム用）の始まりの周波数（Hz）。0なら鳴らさない。 */
  toneStartHz: number;
  /** ピッチの落ちる音の終わりの周波数（Hz）。 */
  toneEndHz: number;
  /** ピッチの落ちる音の大きさ。 */
  toneGain: number;
  /** ピッチの落ちる音が消えるまでの時間（秒）。 */
  toneDecaySec: number;
  /** クラップ用: 最初に細かく何回打つか（1なら普通に1回）。 */
  bursts: number;
}

/** 記号として使える文字。休符（R）と重ならないよう、リムショットは "R2" とする。 */
export const DRUM_KINDS: DrumKind[] = ["K", "S", "H", "O", "C", "T", "L", "P", "R2"];

export const DRUM_SETTINGS: Record<DrumKind, DrumSettings> = {
  K: {
    label: "キック",
    noiseFilter: "lowpass", noiseFilterHz: 1500, noiseQ: 0.7, noiseGain: 0.25, noiseDecaySec: 0.02,
    toneStartHz: 150, toneEndHz: 45, toneGain: 1, toneDecaySec: 0.28, bursts: 1,
  },
  S: {
    label: "スネア",
    noiseFilter: "highpass", noiseFilterHz: 1200, noiseQ: 0.7, noiseGain: 0.8, noiseDecaySec: 0.16,
    toneStartHz: 240, toneEndHz: 170, toneGain: 0.35, toneDecaySec: 0.08, bursts: 1,
  },
  H: {
    label: "ハイハット（閉）",
    noiseFilter: "highpass", noiseFilterHz: 7000, noiseQ: 0.7, noiseGain: 0.45, noiseDecaySec: 0.045,
    toneStartHz: 0, toneEndHz: 0, toneGain: 0, toneDecaySec: 0, bursts: 1,
  },
  O: {
    label: "ハイハット（開）",
    noiseFilter: "highpass", noiseFilterHz: 6500, noiseQ: 0.7, noiseGain: 0.4, noiseDecaySec: 0.3,
    toneStartHz: 0, toneEndHz: 0, toneGain: 0, toneDecaySec: 0, bursts: 1,
  },
  C: {
    label: "クラッシュ",
    noiseFilter: "highpass", noiseFilterHz: 4500, noiseQ: 0.5, noiseGain: 0.45, noiseDecaySec: 1.1,
    toneStartHz: 0, toneEndHz: 0, toneGain: 0, toneDecaySec: 0, bursts: 1,
  },
  T: {
    label: "タム（高）",
    noiseFilter: "bandpass", noiseFilterHz: 2000, noiseQ: 1, noiseGain: 0.15, noiseDecaySec: 0.04,
    toneStartHz: 260, toneEndHz: 150, toneGain: 0.8, toneDecaySec: 0.22, bursts: 1,
  },
  L: {
    label: "タム（低）",
    noiseFilter: "bandpass", noiseFilterHz: 1500, noiseQ: 1, noiseGain: 0.15, noiseDecaySec: 0.05,
    toneStartHz: 160, toneEndHz: 80, toneGain: 0.85, toneDecaySec: 0.3, bursts: 1,
  },
  P: {
    label: "クラップ",
    noiseFilter: "bandpass", noiseFilterHz: 1300, noiseQ: 1.2, noiseGain: 0.9, noiseDecaySec: 0.14,
    toneStartHz: 0, toneEndHz: 0, toneGain: 0, toneDecaySec: 0, bursts: 3,
  },
  R2: {
    label: "リムショット",
    noiseFilter: "bandpass", noiseFilterHz: 3000, noiseQ: 2, noiseGain: 0.5, noiseDecaySec: 0.03,
    toneStartHz: 1700, toneEndHz: 1500, toneGain: 0.3, toneDecaySec: 0.03, bursts: 1,
  },
};

export function isDrumKind(value: string): value is DrumKind {
  return (DRUM_KINDS as string[]).includes(value);
}

/** クラップの細かい打ち直しの間隔（秒）。 */
export const CLAP_BURST_GAP_SEC = 0.011;

/** ドラム1打が鳴り終わるまでの長さ（秒）。 */
export function drumTailSec(kind: DrumKind): number {
  const s = DRUM_SETTINGS[kind];
  const burstLead = (s.bursts - 1) * CLAP_BURST_GAP_SEC;
  return burstLead + Math.max(s.noiseGain > 0 ? s.noiseDecaySec : 0, s.toneGain > 0 ? s.toneDecaySec : 0);
}

/** ノイズの素（1秒分のホワイトノイズ）。乱数の種を固定して、毎回同じ音にする。 */
export function makeWhiteNoise(length: number, seed = 12345): Float32Array<ArrayBuffer> {
  const data = new Float32Array(new ArrayBuffer(length * 4));
  let x = seed >>> 0 || 1;
  for (let i = 0; i < length; i++) {
    // xorshift32
    x ^= x << 13;
    x >>>= 0;
    x ^= x >>> 17;
    x ^= x << 5;
    x >>>= 0;
    data[i] = (x / 0xffffffff) * 2 - 1;
  }
  return data;
}
