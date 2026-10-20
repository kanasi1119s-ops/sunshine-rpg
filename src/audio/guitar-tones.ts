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
  double?: boolean | { spread?: number; irR?: string; timing?: number };
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
  for (const key of ["amp", "ampDrive", "ampTone", "ampCabIr", "reverb", "chorus", "humanPitch", "fx", "noRestrike", "ampGate", "ampGateHz", "ampTight", "ampTightHz", "double", "powerChord"] as const) {
    if (out[key] === undefined && tone[key] !== undefined) out[key] = Array.isArray(tone[key]) ? (tone[key] as AiFx[]).map((f) => ({ ...f })) : tone[key];
  }
  return out as T;
}
