/**
 * ギターの音色プリセット（2026-10-15、人間の指示「この音自体も保存して使いまわせるようにして」）。
 * AIソング形式のパートに `"guitarTone": "warm-lead-b"` のように書くと、アンプ・歪み・高音・キャビネット・残響・ディレイを
 * まとめて入れる。パートに同じ項目を書いたときは、パートの値が優先（プリセットは「出発点」）。
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
  /** true なら、曲の autoScoop（長い音を半音下から持ち上げる自動のしゃくり）を、曲に書いていなければ止める。 */
  noScoop?: boolean;
}

/** 響かせるリードのディレイと残響（『ネオンハートビート』で決めた組み合わせ）。 */
const RINGING_FX: AiFx[] = [
  { type: "delay", beats: 0.75, mix: 0.18, feedback: 0.35 },
  { type: "plate", mix: 0.16 },
];

export const GUITAR_TONES: Record<string, GuitarTone> = {
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
  for (const key of ["amp", "ampDrive", "ampTone", "ampCabIr", "reverb", "chorus", "humanPitch", "fx"] as const) {
    if (out[key] === undefined && tone[key] !== undefined) out[key] = Array.isArray(tone[key]) ? (tone[key] as AiFx[]).map((f) => ({ ...f })) : tone[key];
  }
  return out as T;
}
