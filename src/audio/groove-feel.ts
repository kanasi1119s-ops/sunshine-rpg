/**
 * ノリ（グルーヴ）の道具。docs/sound/rhythm-groove-guide.md §10 の提案1・2・3・8・9。
 * - パート別の human の倍率（`Track.human`／`Score.humanRoles`）と、役割・ジャンルごとの表。
 * - ミリ秒で書く push（`Track.pushMs`）と、ジャンル・ノリ（tight／laidback／pushed）ごとの標準のずれ。
 * - swing の分離（8分の裏 `swing`／16分の裏 `swing16`、パートごとの上書き）。
 * 数字は docs/sound/rhythm-groove-guide.md §3.1・§7.2 の「出発点」で、耳で確かめる前のもの。
 */
import type { Instrument, Score, Track } from "./score";

/** ミリ秒 → 拍。push = ms × bpm ÷ 60000。 */
export const msToBeats = (ms: number, bpm: number): number => (ms * bpm) / 60000;
/** 拍 → ミリ秒。ms = push × 60000 ÷ bpm。 */
export const beatsToMs = (beats: number, bpm: number): number => (beats * 60000) / bpm;

export type GrooveRole = "kick" | "snare" | "hihat" | "cymbal" | "bass" | "sub" | "rhythm" | "lead" | "other";

/** 楽器 → ノリの役割。 */
export function grooveRoleOf(inst: Instrument | undefined): GrooveRole {
  switch (inst) {
    case "kick": return "kick";
    case "snare": return "snare";
    case "hihat": return "hihat";
    case "crash": case "tom": return "cymbal";
    case "bass": case "slap": return "bass";
    case "sub808": return "sub";
    case "guitar": case "echoGuitar": case "crunch": case "distGuitar": case "keys": case "piano": case "harpsichord": case "strings": case "pad": case "choir": case "bell": return "rhythm";
    case "lead": case "leadGuitar": case "brass": return "lead";
    default: return "other";
  }
}

// ---- パート別 human ----------------------------------------------------

/** 役割ごとの human の倍率の既定（提案1）。曲の human に掛ける。 */
export const ROLE_HUMAN_DEFAULT: Record<GrooveRole, number> = { kick: 0.5, snare: 0.8, hihat: 1.2, cymbal: 1.0, bass: 0.8, sub: 1.0, rhythm: 1.0, lead: 1.2, other: 1.0 };

/** ジャンルごとの、パート別 human 倍率の表（「パートごとのhuman表」）。書かれていない役割は ROLE_HUMAN_DEFAULT。 */
export const GENRE_HUMAN_ROLES: Record<string, Partial<Record<GrooveRole, number>>> = {
  // 機械の正確さが音楽の一部: キックとベースはほとんど動かさず、ハットとリードで少し人間味
  metal: { kick: 0.4, snare: 0.5, hihat: 0.7, bass: 0.5, rhythm: 0.6, lead: 1.0 },
  trap: { kick: 0.3, snare: 0.4, hihat: 0.6, bass: 0.3, sub: 0, rhythm: 0.6, lead: 0.8 },
  dnb: { kick: 0.3, snare: 0.4, hihat: 0.6, bass: 0.4, rhythm: 0.6, lead: 0.8 },
  dubstep: { kick: 0.3, snare: 0.4, hihat: 0.6, bass: 0.3, rhythm: 0.6, lead: 0.8 },
  house: { kick: 0.2, snare: 0.4, hihat: 0.8, bass: 0.4, rhythm: 0.6, lead: 0.8 },
  disco: { kick: 0.3, snare: 0.5, hihat: 0.8, bass: 0.6, rhythm: 0.8, lead: 1.0 },
  vocaloid: { kick: 0.4, snare: 0.5, hihat: 0.7, bass: 0.6, rhythm: 0.7, lead: 0.9 },
  battle: { kick: 0.5, snare: 0.6, hihat: 0.8, bass: 0.6, rhythm: 0.8, lead: 1.0 },
  boss: { kick: 0.4, snare: 0.5, hihat: 0.7, bass: 0.5, rhythm: 0.7, lead: 1.0 },
  // 余裕のあるノリ: ハットと楽器を大きめに、キックは控えめ
  ballad: { kick: 0.6, snare: 0.9, hihat: 1.3, bass: 1.0, rhythm: 1.1, lead: 1.3 },
  jazz: { kick: 0.5, snare: 1.0, hihat: 1.3, bass: 1.0, rhythm: 1.2, lead: 1.4 },
  reggae: { kick: 0.6, snare: 0.9, hihat: 1.2, bass: 1.0, rhythm: 1.1, lead: 1.2 },
  bossa: { kick: 0.5, snare: 0.9, hihat: 1.2, bass: 0.9, rhythm: 1.1, lead: 1.2 },
  rnb: { kick: 0.6, snare: 0.9, hihat: 1.3, bass: 1.0, rhythm: 1.1, lead: 1.3 },
  field: { kick: 0.6, snare: 0.9, hihat: 1.2, bass: 0.9, rhythm: 1.1, lead: 1.3 },
  funk: { kick: 0.6, snare: 0.9, hihat: 1.2, bass: 0.9, rhythm: 1.0, lead: 1.2 },
};

/** ジャンルの、パート別 human 倍率の表（全役割ぶん）。ジャンルが無い・知らないときは既定。 */
export function humanTableFor(genre?: string): Record<GrooveRole, number> {
  return { ...ROLE_HUMAN_DEFAULT, ...(genre ? GENRE_HUMAN_ROLES[genre] ?? {} : {}) };
}

/** そのパートの human の倍率。`Track.human` ＞ `Score.humanRoles[役割]` ＞ 1（今までどおり）。0〜2。 */
export function trackHumanMult(score: Pick<Score, "humanRoles">, track: Pick<Track, "human" | "instrument">): number {
  const own = Number(track.human);
  if (track.human !== undefined && Number.isFinite(own)) return Math.max(0, Math.min(2, own));
  const role = score.humanRoles?.[grooveRoleOf(track.instrument)];
  return role !== undefined && Number.isFinite(Number(role)) ? Math.max(0, Math.min(2, Number(role))) : 1;
}

// ---- ミリ秒の push とノリ -------------------------------------------

export type GrooveFeel = "tight" | "laidback" | "pushed";
export const GROOVE_FEELS: readonly GrooveFeel[] = ["tight", "laidback", "pushed"];
type MsTable = Partial<Record<GrooveRole, number>>;

/** ノリの3種。ミリ秒（プラス＝あと乗り、マイナス＝前のめり）。キックは基準の 0。 */
export const GROOVE_FEEL_MS: Record<GrooveFeel, MsTable> = {
  tight: { snare: 0, hihat: -2, bass: 0, rhythm: 0, lead: 0 },
  laidback: { snare: 10, hihat: 2, bass: 8, rhythm: 6, lead: 5 },
  pushed: { snare: -3, hihat: -4, cymbal: -2, bass: 0, rhythm: 0, lead: -3 },
};

/** ジャンルごとの標準のずれ（ミリ秒。docs/sound/rhythm-groove-guide.md §3.1 の範囲の真ん中あたり）。 */
export const GENRE_GROOVE_MS: Record<string, MsTable> = {
  rock: { snare: 5, hihat: -2, bass: 2, rhythm: 3 },
  hardrock: { snare: 1, bass: 0, rhythm: 0 },
  metal: { snare: 1 },
  punk: { snare: 1, hihat: -2 },
  pop: { snare: 2, hihat: -2, rhythm: 2 },
  jpop: { snare: 2, hihat: -2, rhythm: 2 },
  vocaloid: { hihat: -1 },
  ballad: { snare: 8, hihat: 2, bass: 5, rhythm: 6, lead: 5 },
  funk: { snare: 8, hihat: -3, bass: 4, rhythm: 2 },
  rnb: { snare: 11, bass: 8, rhythm: 8, lead: 6 },
  hiphop: { kick: -5, snare: 14, hihat: 2, bass: 8, rhythm: 7 },
  jazz: { snare: 10, hihat: -3, bass: -2, rhythm: 10, lead: 5 },
  reggae: { snare: 5, bass: 10, rhythm: 10 },
  bossa: { snare: 4, bass: 2, rhythm: 5 },
  house: { snare: 2, hihat: -5 },
  disco: { snare: 2, hihat: -5 },
  field: { snare: 7, bass: 5, rhythm: 6 },
  battle: { snare: -3, hihat: -3 },
  boss: { snare: -3, hihat: -3 },
};

/** ジャンルに合うノリの種類（`grooveFeel: "genre"` のときの選び方）。表にないジャンルは tight。 */
export const GENRE_FEEL: Record<string, GrooveFeel> = {
  ballad: "laidback", rnb: "laidback", hiphop: "laidback", jazz: "laidback", reggae: "laidback", bossa: "laidback", funk: "laidback", field: "laidback",
  battle: "pushed", boss: "pushed",
};

/**
 * パートが書いた push・pushMs が無いときの、ノリ（grooveFeel）による標準のずれ（ミリ秒）。
 * feel が "genre" なら drumGenre の表（GENRE_GROOVE_MS）、それ以外は 3種の表。見つからなければ undefined。
 */
export function grooveFeelMs(feel: string | undefined, genre: string | undefined, role: GrooveRole): number | undefined {
  if (!feel) return undefined;
  const table = feel === "genre" ? (genre ? GENRE_GROOVE_MS[genre] : undefined) : GROOVE_FEEL_MS[feel as GrooveFeel];
  if (!table) return undefined;
  const v = table[role];
  return v === undefined ? (role === "kick" ? 0 : undefined) : v;
}

/** パートの push（拍）。push に pushMs を bpm で拍に直して足す。どちらも無ければ undefined（今までどおり）。 */
export function pushBeatsOf(track: Pick<Track, "push" | "pushMs">, bpm: number): number | undefined {
  const ms = Number(track.pushMs);
  if (!Number.isFinite(ms) || ms === 0) return track.push;
  const clamped = Math.max(-50, Math.min(50, ms));
  return (track.push ?? 0) + msToBeats(clamped, bpm);
}

// ---- swing の分離 ---------------------------------------------------

/** パートの swing（8分の裏）と swing16（16分の裏）。パートの指定 ＞ 曲の指定。swing16 は無ければ swing と同じ動き。 */
export function swingOf(score: Pick<Score, "swing" | "swing16">, track: Pick<Track, "swing" | "swing16">): { swing: number | undefined; swing16: number | undefined } {
  const swing = track.swing ?? score.swing;
  // パートの swing だけを書いたときは、16分の裏も同じ量。曲の swing16 は、パートが swing を書かないときだけ使う
  const swing16 = track.swing16 ?? (track.swing !== undefined ? undefined : score.swing16);
  return { swing, swing16 };
}

// ---- 三角分布 -------------------------------------------------------

/** 0.93〜1.07 の一様な値 u を、中心に寄りやすい三角分布（同じ幅）にするため、別の種の値と平均する。 */
export const triangular = (a: number, b: number): number => (a + b) / 2;
