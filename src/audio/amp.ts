/**
 * アンプシミュレーター（アンプ風の音づくり）。
 *
 * 外部のソフトやプラグイン、音声ファイル（インパルス応答など）は使わない。
 * ブラウザに入っている Web Audio API の部品（歪み・イコライザー・フィルター）だけで作る。
 * したがって無料で、素材の規約も関係しない（`docs/assets-credits.md` への記録は不要）。
 *
 * 信号の流れ: 音 → 入力ゲイン（ドライブ） → 歪み（ウェーブシェイパー）
 *   → 低音・中音・高音のイコライザー（トーンスタック） → キャビネット（低域カット＋高域カット） → 出力
 *
 * これは「アンプを通したような質感」を、ゲーム内の波形（矩形波・ノコギリ波など）に足すもの。
 * 実在のアンプや機材のモデリングではない。特定の製品の音を写したものでもない（CLAUDE.md 1-1）。
 * プリセット名は、ジャンル（音の性格）で付けている。
 */

/** 歪みカーブの形。 */
export type AmpShape =
  /** なめらかに潰れる（真空管風）。 */
  | "soft"
  /** 角を立てて潰す（ファズ・メタル寄り）。 */
  | "hard"
  /** 上下で潰れ方を変える（偶数次の倍音が増えて、あたたかい）。 */
  | "asym"
  /** 波形を階段状にする（ローファイ・8bit風）。 */
  | "steps";

export type AmpPresetName =
  | "clean"
  | "jazz"
  | "blues"
  | "funk"
  | "crunch"
  | "rock"
  | "hardrock"
  | "punk"
  | "metal"
  | "fuzz"
  | "shoegaze"
  | "lofi"
  | "retro8bit"
  | "radio"
  | "loudmetal"
  | "loudrock"
  | "delicate";

export interface AmpSettings {
  /** 日本語の呼び名。 */
  label: string;
  /** 向いているジャンル・場面の一言。 */
  genre: string;
  /** 入力への増幅（1で素通し。大きいほど強く潰れる）。 */
  drive: number;
  shape: AmpShape;
  /** 歪みの硬さ（大きいほど角が立つ）。`steps` のときは階段の段数。 */
  hardness: number;
  /** 0〜1。`asym` のときの、上下の潰れ方の差。 */
  asymmetry: number;
  /** 低音（約200Hz以下）の増減（dB）。 */
  bassDb: number;
  /** 中音の増減（dB）。 */
  midDb: number;
  /** 中音の中心周波数（Hz）。 */
  midHz: number;
  /** 高音（約3kHz以上）の増減（dB）。 */
  trebleDb: number;
  /** キャビネットの低域カット（Hz）。これより低い音を削る。 */
  highpassHz: number;
  /** キャビネットの高域カット（Hz）。これより高い音を削る（歪みのざらつきを丸める）。 */
  lowpassHz: number;
  /** 出力の大きさ（1で、歪みのないときと同じくらいの大きさ）。 */
  level: number;
}

/**
 * ジャンル別プリセット。曲の1パートに `amp: "rock"` のように指定して使う。
 * 数値は、各ジャンルの一般的な音の性格（クリーンは歪みなしで高域がきれい、メタルは
 * 低域を締めて中域を削り強く歪ませる、など）に沿って決めた。耳で聞いて調整してよい。
 */
export const AMP_PRESETS: Record<AmpPresetName, AmpSettings> = {
  clean: {
    label: "クリーン",
    genre: "ポップス・カントリー・アコースティック寄りの明るい場面",
    drive: 1, shape: "soft", hardness: 1.2, asymmetry: 0,
    bassDb: 0, midDb: 0, midHz: 1200, trebleDb: 3,
    highpassHz: 80, lowpassHz: 9000, level: 1,
  },
  jazz: {
    label: "ジャズ",
    genre: "ジャズ・ラウンジ・ボサノバ・落ち着いた大人の場面",
    drive: 1, shape: "soft", hardness: 1, asymmetry: 0,
    bassDb: 3, midDb: -2, midHz: 800, trebleDb: -6,
    highpassHz: 70, lowpassHz: 4500, level: 1.05,
  },
  blues: {
    label: "ブルース",
    genre: "ブルース・ソウル・R&B・哀愁のある場面",
    drive: 2.5, shape: "asym", hardness: 2, asymmetry: 0.35,
    bassDb: 1, midDb: 4, midHz: 900, trebleDb: -2,
    highpassHz: 90, lowpassHz: 5500, level: 0.95,
  },
  funk: {
    label: "ファンク",
    genre: "ファンク・ディスコ・ソウル・軽快でリズムが主役の場面",
    drive: 1.6, shape: "soft", hardness: 1.5, asymmetry: 0.1,
    bassDb: -3, midDb: 2, midHz: 1800, trebleDb: 5,
    highpassHz: 140, lowpassHz: 7500, level: 1,
  },
  crunch: {
    label: "クランチ",
    genre: "ロック・ポップロック・インディー・元気のよい場面",
    drive: 4, shape: "asym", hardness: 3, asymmetry: 0.25,
    bassDb: 1, midDb: 3, midHz: 1000, trebleDb: 2,
    highpassHz: 100, lowpassHz: 6500, level: 0.9,
  },
  rock: {
    label: "ロック",
    genre: "ロック・ブルースロック・王道の戦闘の場面",
    drive: 8, shape: "soft", hardness: 4, asymmetry: 0.15,
    bassDb: 2, midDb: 4, midHz: 1100, trebleDb: 1,
    highpassHz: 100, lowpassHz: 6000, level: 0.85,
  },
  hardrock: {
    label: "ハードロック",
    genre: "ハードロック・ヘヴィロック・強敵との戦闘の場面",
    drive: 14, shape: "soft", hardness: 6, asymmetry: 0.1,
    bassDb: 3, midDb: 2, midHz: 900, trebleDb: 3,
    highpassHz: 110, lowpassHz: 5500, level: 0.8,
  },
  punk: {
    label: "パンク",
    genre: "パンク・ガレージ・ポップパンク・勢いで押す場面",
    drive: 11, shape: "hard", hardness: 5, asymmetry: 0,
    bassDb: -1, midDb: 3, midHz: 1500, trebleDb: 4,
    highpassHz: 150, lowpassHz: 6500, level: 0.8,
  },
  metal: {
    label: "メタル",
    genre: "メタル・ハードコア・ボス戦・終盤の切迫した場面",
    drive: 30, shape: "hard", hardness: 8, asymmetry: 0,
    bassDb: 4, midDb: -6, midHz: 700, trebleDb: 5,
    highpassHz: 130, lowpassHz: 5000, level: 0.7,
  },
  fuzz: {
    label: "ファズ",
    genre: "サイケ・ストーナー・グランジ・不穏で荒々しい場面",
    drive: 40, shape: "hard", hardness: 10, asymmetry: 0.3,
    bassDb: 5, midDb: -3, midHz: 600, trebleDb: -2,
    highpassHz: 70, lowpassHz: 4000, level: 0.65,
  },
  shoegaze: {
    label: "シューゲイザー",
    genre: "シューゲイザー・オルタナ・夢のように霞む場面",
    drive: 18, shape: "asym", hardness: 5, asymmetry: 0.4,
    bassDb: 2, midDb: 1, midHz: 1400, trebleDb: -5,
    highpassHz: 90, lowpassHz: 3800, level: 0.7,
  },
  lofi: {
    label: "ローファイ",
    genre: "ローファイ・チルホップ・インディー・眠たげな場面",
    drive: 3, shape: "steps", hardness: 24, asymmetry: 0,
    bassDb: 2, midDb: 0, midHz: 1000, trebleDb: -8,
    highpassHz: 120, lowpassHz: 3200, level: 0.95,
  },
  retro8bit: {
    label: "レトロ8bit",
    genre: "8bitゲーム音楽・チップチューン・粗い音の場面",
    drive: 1.5, shape: "steps", hardness: 8, asymmetry: 0,
    bassDb: 0, midDb: 0, midHz: 1500, trebleDb: 2,
    highpassHz: 60, lowpassHz: 9000, level: 0.95,
  },
  radio: {
    label: "ラジオ・電話",
    genre: "ラジオ・電話・遠くから聞こえる声や音の場面",
    drive: 5, shape: "soft", hardness: 3, asymmetry: 0,
    bassDb: -12, midDb: 6, midHz: 1500, trebleDb: -10,
    highpassHz: 400, lowpassHz: 3000, level: 0.9,
  },
  // ── ラウド系・繊細系（2026-10-02 追加）。出力は音割れしないよう、歪みの量のわりに小さめにそろえてある ──
  loudmetal: {
    label: "ラウドメタル",
    genre: "ラウドメタル・モダンメタル・ボス戦・重くて密度の高い場面（低音は締め、中域をえぐり、高音は刺さらせない）",
    drive: 26, shape: "hard", hardness: 6, asymmetry: 0,
    bassDb: 3, midDb: -5, midHz: 650, trebleDb: 2,
    highpassHz: 120, lowpassHz: 4800, level: 0.6,
  },
  loudrock: {
    label: "ラウドロック",
    genre: "ラウドロック・ヘヴィロック・オルタナ・太くて前に出る、歌のある激しい場面（中域が厚く、サビで壁になる）",
    drive: 16, shape: "soft", hardness: 7, asymmetry: 0.12,
    bassDb: 2, midDb: 3, midHz: 1000, trebleDb: 2,
    highpassHz: 105, lowpassHz: 5400, level: 0.7,
  },
  delicate: {
    label: "繊細",
    genre: "繊細なアルペジオ・静かな回想・祈り・弱い音の粒が聞こえる場面（歪ませず、高音はやわらかく、細かな強弱が残る）",
    drive: 1, shape: "soft", hardness: 0.8, asymmetry: 0,
    bassDb: -1, midDb: 1, midHz: 2200, trebleDb: -1,
    highpassHz: 90, lowpassHz: 7000, level: 1,
  },
};

export const AMP_PRESET_NAMES = Object.keys(AMP_PRESETS) as AmpPresetName[];

/**
 * この音量を基準に、ドライブの強さを決める。
 * （曲のパートの音量は0.05〜0.2くらいのため。小さい音のパートは、大きいパートより歪みが浅くなる）
 */
export const AMP_REFERENCE_VOLUME = 0.2;

/** ウェーブシェイパーに渡すカーブの点の数（奇数。真ん中がちょうど0になる）。 */
export const AMP_CURVE_SAMPLES = 2049;

/**
 * 歪みカーブを作る。入力 x は -1〜1、出力も -1〜1 に収まる。
 * `steps` 以外は、入力が大きいほど出力も大きい（単調に増える）。
 */
export function makeDistortionCurve(
  shape: AmpShape,
  hardness: number,
  asymmetry: number,
  samples: number = AMP_CURVE_SAMPLES,
): Float32Array<ArrayBuffer> {
  const curve = new Float32Array(new ArrayBuffer(samples * 4));
  const k = Math.max(0.01, hardness);
  const a = Math.min(1, Math.max(0, asymmetry));
  const denom = samples - 1;

  for (let i = 0; i < samples; i++) {
    const x = (i * 2) / denom - 1;
    let y: number;
    switch (shape) {
      case "soft": {
        // なめらかに潰れる。tanhで、x=±1のとき出力が±1になるよう正規化する。
        y = Math.tanh(k * x) / Math.tanh(k);
        break;
      }
      case "hard": {
        // 角を立てる。硬いほど、小さな入力でもすぐ天井に張りつく。
        y = Math.max(-1, Math.min(1, k * x));
        break;
      }
      case "asym": {
        // プラス側を潰れにくく、マイナス側を潰れやすくして、上下の非対称を作る。
        const kPos = k * (1 - 0.5 * a);
        const kNeg = k * (1 + 0.5 * a);
        y = x >= 0 ? Math.tanh(kPos * x) / Math.tanh(kPos) : Math.tanh(kNeg * x) / Math.tanh(kNeg);
        break;
      }
      case "steps": {
        // 階段状。hardness を段数（片側）として扱う。
        const levels = Math.max(2, Math.round(hardness));
        y = Math.round(x * levels) / levels;
        break;
      }
    }
    curve[i] = y;
  }
  return curve;
}

/** プリセット名から設定を取り出す。 */
export function getAmpSettings(name: AmpPresetName): AmpSettings {
  return AMP_PRESETS[name];
}
