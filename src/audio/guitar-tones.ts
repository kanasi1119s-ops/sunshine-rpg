/**
 * ギターの音色プリセット（2026-10-15、人間の指示「この音自体も保存して使いまわせるようにして」）。
 * AIソング形式のパートに `"guitarTone": "warm-lead-b"` のように書くと、アンプ・歪み・高音・キャビネット・残響・ディレイを
 * まとめて入れる。パートに同じ項目を書いたときは、パートの値が優先（プリセットは「出発点」）。
 * 2026-10-15: リードギターの自動ビブラート（CC1）と音量のふくらみ（CC11）は midi-export.ts で止めた（「ゴムが伸びたような音」）。
 * 聞き比べで人間が「いい」と言った音だけを足す。耳での確認は人間が行う（作者は音を聴けない）。
 */
import type { AiFx } from "./ai-song";

export interface GuitarTone {
  /** 日本語の呼び名。 */
  label: string;
  /** どんな音か・向く場面・決めた経緯。 */
  description: string;
  amp: string;
  ampDrive?: number;
  ampTone?: number;
  /** 録音のキャビネットIR（作曲ソフトのみ）。"none" で外す。 */
  ampCabIr?: string;
  reverb?: number;
  chorus?: number;
  humanPitch?: number;
  fx?: AiFx[];
  /** true なら、MIDI のこだま（0.75拍・1.5拍後の弾き直し）を止める（ディレイの fx で響かせるので不要。伸ばした音が途中で弾き直されない）。 */
  noRestrike?: boolean;
  /** true なら、曲の autoScoop（長い音を半音下から持ち上げる自動のしゃくり）を、曲に書いていなければ止める。 */
  noScoop?: boolean;
  // ── 2026-10-20 ラウドロックの音作り（DI → ゲート → ブースト → アンプ → 録音のキャビネットIR）──
  ampGate?: number;
  ampGateHz?: number;
  ampTight?: number;
  ampTightHz?: number;
  /** ダブルトラック（左右に別々に弾いた2本）。 */
  double?: boolean | { spread?: number; irR?: string; timing?: number; diR?: "emily" | "fsbs" | "shiny" | "gretsch" | "hofner" };
  /** 弦の雑音を足す（パートの stringNoise と同じ）。 */
  stringNoise?: boolean;
  /** このパートのギターの録音（パートの di と同じ）。 */
  partDi?: "emily" | "fsbs" | "shiny" | "gretsch" | "hofner";
  /** false でパワーコードを自動で重ねない（単音の刻み）。 */
  powerChord?: boolean;
  /** この音色は歪ませる前の録音（DI）で鳴らす前提。曲に diGuitar が無ければ、これを入れる。 */
  di?: "emily" | "fsbs";
}

/** 1音1音を聞き取りやすくする EQ（2026-10-21 人間「B と D は聞き取りにくいかも」）: 低い中域のこもり（300Hz）を削り、芯（1.5kHz）を少し出す。 */
const CLARITY_EQ: AiFx[] = [
  { type: "eq", low: 0, mid: -3.5, midHz: 300, high: 0 },
  { type: "eq", low: 0, mid: 2.5, midHz: 1500, high: 0 },
];
/** ラウドロックの4つの音作りに共通の、DI で鳴らす設定（自動のしゃくり・音程の揺れなし）。 */
const LOUD_BASE = { humanPitch: 0, noScoop: true, di: "emily" as const };

/** 響かせるリードのディレイと残響（『ネオンハートビート』で決めた組み合わせ）。 */
const RINGING_FX: AiFx[] = [
  { type: "delay", beats: 0.75, mix: 0.18, feedback: 0.35 },
  { type: "plate", mix: 0.16 },
];

export const GUITAR_TONES: Record<string, GuitarTone> = {
  // ── 2026-10-21 人間「全部採用」: ラウドロックの4つの音作り（パワーコードの聞き比べ A〜D）。歪ませる前の録音（DI）で鳴らす ──
  "loud-high": {
    label: "ラウドロック A: ハイゲイン（締まった壁）",
    description: "Dark Days のハイゲインアンプ（namDD）を強めに。ゲート 40・低音を締めるブースト・V30 2x12 のIR（左 tight／右 balanced）・左右のダブルトラック。刻み・ブレイクダウン向き。クレジット必要（Dark Days, CC BY 4.0）。",
    amp: "namDD", ampGate: 40, ampTight: 0.6, ampCabIr: "dd-v30-2x12-mix-tight", double: { irR: "dd-v30-2x12-mix-balanced" }, ...LOUD_BASE,
  },
  "loud-mid": {
    label: "ラウドロック B: 中くらいの歪み（左右で別のスピーカー）",
    description: "namDD の入力を絞った中くらいの歪み。ゲートは浅く（20）、左 V30／右 Greenback のIR。1音1音が聞こえるよう 300Hz を削り 1.5kHz を少し出す。メロコア・ギターロック向き。クレジット必要（Dark Days, CC BY 4.0）。" +
      "2026-10-21 パワーコードの聞き比べ B3 で人間「b3がめちゃくちゃいい」（学習式アンプのあとの EQ が効くよう直した版）。",
    amp: "namDD", ampDrive: 0.45, ampGate: 20, ampTight: 0.6, ampTightHz: 140, ampCabIr: "dd-v30-2x12-mix-balanced", double: { irR: "jd-greenback-4x12-01" }, fx: CLARITY_EQ, ...LOUD_BASE,
  },
  "loud-mid-noise": {
    label: "ラウドロック B（B3）＋弦の雑音",
    description: "採用（2026-10-21 人間「全部採用」）。B3 に、跳ぶ前に指が弦をこする音・音を止めるときの弦を押さえる音を足したもの。生の演奏らしさを足したいとき。",
    amp: "namDD", ampDrive: 0.45, ampGate: 20, ampTight: 0.6, ampTightHz: 140, ampCabIr: "dd-v30-2x12-mix-balanced", double: { irR: "jd-greenback-4x12-01" }, fx: CLARITY_EQ, ...LOUD_BASE,
    stringNoise: true,
  },
  "loud-mid-hs": {
    label: "ラウドロック B（B3）・左ハムバッカー／右シングルコイル",
    description: "採用（2026-10-21 人間「全部採用」）。B3 の二重録りの右だけ、シングルコイル（FSBS）の録音にする。左は太く、右は明るく、左右で音の色が分かれる。右の音量は自動でそろえる（DI_LEVEL）。",
    amp: "namDD", ampDrive: 0.45, ampGate: 20, ampTight: 0.6, ampTightHz: 140, ampCabIr: "dd-v30-2x12-mix-balanced", double: { irR: "jd-greenback-4x12-01", diR: "fsbs" }, fx: CLARITY_EQ, ...LOUD_BASE,
  },
  "marshall-mid": {
    label: "マーシャル系の中くらいの歪み（中域が前に出る）",
    description: "マーシャル JVM410H の録音データから学習したアンプ（namJVM、試用中）。B3（loud-mid）と同じ作り（ゲート浅め・低音を締めるブースト・左 V30／右 Greenback・300Hz を削り 1.5kHz を少し出す）。2026-10-21 試聴セットで人間「どっちも入れて」。曲を公開するときはデータの作者のクレジットが必要（docs/assets-credits.md）。",
    amp: "namJVM", ampDrive: 1.0, ampGate: 15, ampTight: 0.5, ampTightHz: 120, ampCabIr: "dd-v30-2x12-mix-balanced", double: { irR: "jd-greenback-4x12-01" }, fx: CLARITY_EQ, ...LOUD_BASE,
  },
  "loud-builtin": {
    label: "ラウドロック C: 内蔵アンプの太い歪み",
    description: "作曲ソフト内蔵の loudrock（中域が厚い太い歪み）に、録音のIR（左 V30／右 Greenback）とダブルトラック。外部のアンプのクレジット不要（IR は Dark Days のため必要）。",
    amp: "loudrock", ampGate: 20, ampCabIr: "dd-v30-2x12-mix-balanced", double: { irR: "jd-greenback-4x12-01" }, ...LOUD_BASE,
  },
  "loud-mid-b": {
    label: "ラウドロック D: 別のハイゲインを絞った中くらいの歪み",
    description: "ハイゲインB（NAM の見本モデル。MIT）の入力を絞った中くらいの歪み。左 V30／右 Greenback。300Hz を削り 1.5kHz を少し出して粒を立てる。",
    // 2026-10-21 人間「D はまだ聴きにくい」: 入力 0.4 では上の倍音がほとんど出ず、1.6〜3.2kHz が B より 18dB 弱くて暗かった → 入力 0.7 にして 250Hz を少し削り 2kHz を少し出す
    amp: "namB", ampDrive: 0.7, ampGate: 20, ampTight: 0.6, ampTightHz: 140, ampCabIr: "dd-v30-2x12-mix-balanced", double: { irR: "jd-greenback-4x12-01" },
    fx: [{ type: "eq", low: 0, mid: -2, midHz: 250, high: 0 }, { type: "eq", low: 0, mid: 2, midHz: 2000, high: 0 }], ...LOUD_BASE,
  },
  // ── 2026-10-21 バンドの音の質感を調べて作った出発点（出典つきの調査: ELLEGARDEN・Meshuggah・Bring Me The Horizon・Linkin Park・Mrs. GREEN APPLE）。
  //    曲・リフはまねず、機材と音の作り方の傾向だけを数値にした。人間の耳での確認はまだ（試作）。──
  "melodic-punk": {
    label: "メロディックパンク（マーシャル系の中くらいの歪み・中域が前）",
    description: "試作。ハムバッカー＋マーシャル系の中〜中の上の歪み（メタルより少ない）、中域を前に、低音を締める。ブーストは低音を削るためだけ。左 V30／右 Greenback の別テイク。パワーコードはルート＋5度＋オクターブ。マーシャルのモデルができたら差し替える。",
    amp: "namDD", ampDrive: 0.4, ampGate: 15, ampTight: 0.5, ampTightHz: 120, ampCabIr: "dd-v30-2x12-mix-balanced", double: { irR: "jd-greenback-4x12-02" },
    fx: [{ type: "eq", low: 0, mid: -2.5, midHz: 300, high: 0 }, { type: "eq", low: 0, mid: 1.5, midHz: 1000, high: -1.5 }], ...LOUD_BASE,
  },
  "djent-8": {
    label: "8弦の低い刻み（ジェント・締まった壁）",
    description: "試作。8弦の半音下げ（F1〜）を単音で刻む前提（パワーコードを重ねない）。DI の段階で 3kHz を +4dB（低く下げた録音のこもりを補う）→ ゲート（検出 500Hz で低い音でも途中で閉じない）→ 200Hz から下をゆるく削るブースト → ハイゲイン → V30 系の 4x12 に Greenback を混ぜたIR。",
    amp: "namDD", ampDrive: 1.4, ampGate: 50, ampGateHz: 500, ampTight: 1, ampTightHz: 200, ampCabIr: "jd-brutal-4x12-01+jd-greenback-4x12-02", double: { irR: "jd-brutal-4x12-06+jd-brutal-4x12-12" },
    powerChord: false, fx: [{ type: "eq", low: 0, mid: 4, midHz: 3000, high: 0, pre: true }], ...LOUD_BASE,
  },
  "modern-metalcore": {
    label: "現代のメタルコア（明るく広い・シンセと混ざる）",
    description: "試作。ゲインは多すぎず、ブーストでアンプを押す（140Hz から下を削る）。V30 の明るいマイクと太いマイクを混ぜたIR。アンプのあとで 300Hz を少し引き、2.5kHz と高域を少し出す（耳に痛い所は出しすぎない）。キックに合わせて少し凹ませる（duck）とシンセと一体になる。",
    amp: "namDD", ampDrive: 0.6, ampGate: 25, ampTight: 0.7, ampTightHz: 140, ampCabIr: "jd-brutal-4x12-01+dd-v30-2x12-cone-1in", double: { irR: "jd-brutal-4x12-05+dd-v30-2x12-cone-1in" },
    fx: [{ type: "eq", low: 0, mid: -2, midHz: 300, high: 1.5 }, { type: "eq", low: 0, mid: 2, midHz: 2500, high: 0 }], ...LOUD_BASE,
  },
  "nu-metal-wall": {
    label: "2000年代のニューメタル（平らで太い壁・刻みの止めがそろう）",
    description: "試作。レクチファイア系の深めの歪みを、ゲートで刻みの止めをそろえる（伸ばした音の途中では閉じない浅さ）。V30 の明るいマイクと暗いマイクを半々、右は Greenback を混ぜる。250Hz を引き 800Hz を少し出し、高域は暗め。",
    amp: "namDD", ampDrive: 0.9, ampGate: 45, ampTight: 0.3, ampTightHz: 80, ampCabIr: "dd-v30-2x12-cap-1in+dd-v30-2x12-mix-deep", double: { irR: "dd-v30-2x12-mix-deep+jd-greenback-4x12-03" },
    fx: [{ type: "eq", low: 0, mid: -2, midHz: 250, high: -2 }, { type: "eq", low: 0, mid: 1.5, midHz: 800, high: 0 }], ...LOUD_BASE,
  },
  "jpop-rock-drive": {
    label: "J-POP のギターロックの歪み（浅め・コードが聞こえる）",
    description: "試作。ラウドロックより明らかに浅い歪みで、1音1音とコードの響きが聞こえる量。低音は 140Hz から締め、300Hz を引いて 1.2kHz を少し出し、高域は少し落とす（歌の場所を空ける）。左 V30／右 Greenback の別テイク。サビの歪みのバッキング向き。",
    amp: "namDD", ampDrive: 0.35, ampGate: 15, ampTight: 0.5, ampTightHz: 140, ampCabIr: "dd-v30-2x12-mix-balanced", double: { irR: "jd-greenback-4x12-01" },
    fx: [{ type: "eq", low: 0, mid: -2.5, midHz: 300, high: -1.5 }, { type: "eq", low: 0, mid: 2, midHz: 1200, high: 0 }], ...LOUD_BASE,
  },
  "electro-rock": {
    label: "エレクトロとロックの混ざったリフ（中域が太い歪み・乾いた音）",
    description: "採用（2026-10-21 人間「1つ目はよい」。BOOM BOOM SATELLITES の音の作り方の調査から）。ライン録り＋アンプのプラグインの考え方。中域（700Hz〜2kHz）が太い、ゲインは高すぎない歪み。110Hz から下と 8kHz から上を切り、ギター本体は乾いた音（残響は送りで少しだけ）。左右に別テイク。",
    amp: "namDD", ampDrive: 0.5, ampGate: 25, ampTight: 0.6, ampTightHz: 110, ampCabIr: "jd-brutal-4x12-03", double: { irR: "jd-greenback-4x12-04" },
    fx: [{ type: "eq", low: -2, mid: 2, midHz: 1200, high: -3 }, { type: "filter", kind: "lowpass", freq: 8000, q: 0.7 }], ...LOUD_BASE,
  },
  "electro-rock-gated": {
    label: "拍で刻んだ加工ギター（ファズ＋帯域を絞る＋ビットを落とす＋16分のゲート）",
    description: "曲調によって使う（2026-10-21 人間「わるくはない」）。残響はほぼなし。主役のリフより 8〜10dB 小さく混ぜる「味付け」の層。前段のファズ → キャビネットなし → 1.2kHz の帯域 → 8ビット → 16分のトランスゲート（pattern は曲に合わせて書きかえる）。区間の頭から入れる（弾いている途中で急に切らない）。",
    amp: "direct", ampCabIr: "none",
    fx: [{ type: "fuzz", gain: 20, tone: 3500, level: -12, pre: true }, { type: "filter", kind: "bandpass", freq: 1200, q: 1.5 }, { type: "bitcrusher", bits: 8, mix: 0.25 },
      { type: "transgate", beats: 0.25, pattern: "x.xxx.x.x.xx.x.x", depth: 0.9 }], humanPitch: 0, noScoop: true, di: "emily",
    // 2026-10-21 人間「曲調によってはよいかも。エコー強いかな」: 残響の送りをほぼなくし、刻みを乾いた音にする
    reverb: 0.03,
  },
  "warm-lead-a": {
    label: "響く温かいリード（浅い歪み・中域が太い）",
    description:
      "lead アンプの浅い歪みで、中域（1〜2kHz）が太く、耳に刺さる 2〜4kHz を丸めたリード。ディレイ（0.75拍）とプレートの残響で響かせる。" +
      "ビブラート・チョーキング・自動のしゃくりなし（banned-sounds 17）。2026-10-15『ネオンハートビート』の聞き比べ A。旋律・ソロ向き。",
    amp: "lead",
    ampDrive: 1.0,
    ampTone: -3,
    reverb: 0.32,
    chorus: 0,
    humanPitch: 0,
    fx: RINGING_FX,
    noRestrike: true,
    noScoop: true,
  },
  "warm-lead-b": {
    label: "こもった軽い歪みのリード（丸いキャビネット）",
    description:
      "オーバードライブの軽い歪みに、高音が控えめな録音キャビネット（dfc-ampmix。David Fau Casquel、CC BY 3.0）を通した、少しこもった丸いリード。" +
      "中域（500Hz〜2kHz）が厚い。ディレイとプレートで響かせる。ビブラート・チョーキング・自動のしゃくりなし。2026-10-15『ネオンハートビート』の聞き比べ B。",
    amp: "overdrive",
    ampDrive: 1.2,
    ampTone: -4,
    ampCabIr: "dfc-ampmix",
    reverb: 0.32,
    chorus: 0,
    humanPitch: 0,
    fx: RINGING_FX,
    noRestrike: true,
    noScoop: true,
  },
};

/** プリセットの項目を、パートに書かれていない所だけ入れる。知らない名前は注意を出してそのまま返す。 */
export function applyGuitarTone<T extends Record<string, unknown>>(part: T, where: string, warnings: string[]): T {
  const name = part.guitarTone;
  if (typeof name !== "string" || !name) return part;
  const tone = GUITAR_TONES[name];
  if (!tone) {
    warnings.push(`${where}: guitarTone「${name}」はありません（使える名前: ${Object.keys(GUITAR_TONES).join("・")}）`);
    return part;
  }
  const out: Record<string, unknown> = { ...part };
  if (tone.partDi && out.di === undefined) out.di = tone.partDi;
  for (const key of ["amp", "ampDrive", "ampTone", "ampCabIr", "reverb", "chorus", "humanPitch", "fx", "noRestrike", "ampGate", "ampGateHz", "ampTight", "ampTightHz", "double", "powerChord", "stringNoise"] as const) {
    if (out[key] === undefined && tone[key] !== undefined) out[key] = Array.isArray(tone[key]) ? (tone[key] as AiFx[]).map((f) => ({ ...f })) : tone[key];
  }
  return out as T;
}
