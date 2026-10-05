/**
 * ゲームの中の時間（昼と夜）。町・村・世界地図などの外を歩いている間だけ進み（メニュー・会話・戦闘のあいだは止まる）、
 * 1日は実時間で8分。夜になると、画面が青く暗くなり、ぶらぶら歩いている町の人が減る。宿にとまると、朝になる。
 * 0＝朝（夜明け）から始まり、1日の割合 f（0〜1）で、昼 → 夕方 → 夜 → 夜明け と移る。
 */
export const DAY_MS = 8 * 60 * 1000;

export function dayFraction(clockMs: number): number {
  return (((clockMs % DAY_MS) + DAY_MS) % DAY_MS) / DAY_MS;
}

/** 夜の深さ（0＝昼、1＝真夜中）。夕方にだんだん暗くなり、夜明けにだんだん明るくなる。 */
export function nightness(f: number): number {
  if (f < 0.5) return 0;
  if (f < 0.66) return ((f - 0.5) / 0.16) * 0.9;     // 夕方
  if (f < 0.68) return 0.9 + ((f - 0.66) / 0.02) * 0.1;
  if (f < 0.88) return 1;                              // 夜
  return Math.max(0, 1 - (f - 0.88) / 0.12);           // 夜明け
}

/** 夕方・夜明けのあかね色の強さ（0〜1）。 */
export function warmGlow(f: number): number {
  const dusk = Math.max(0, 1 - Math.abs(f - 0.56) / 0.1);
  const dawn = Math.max(0, 1 - Math.abs(f - 0.95) / 0.06);
  return Math.max(dusk, dawn * 0.7);
}

export function isNight(clockMs: number): boolean {
  return nightness(dayFraction(clockMs)) >= 0.7;
}

/** つぎの朝（0）の時刻。宿にとまったときに、ここまで進める。 */
export function nextMorning(clockMs: number): number {
  return (Math.floor(clockMs / DAY_MS) + 1) * DAY_MS;
}

/** 場面の時間帯（小説の場面で「夕暮れ」「その夜」などと書いてあるとき、時計をそこへ合わせる）。 */
export type SceneTime = "morning" | "day" | "dusk" | "night";

/** その時間帯の、まん中あたりの1日の割合。 */
export const SCENE_TIME_FRACTION: Record<SceneTime, number> = { morning: 0.03, day: 0.25, dusk: 0.56, night: 0.76 };

export function sceneTimeOf(clockMs: number): SceneTime {
  const f = dayFraction(clockMs);
  if (f >= 0.88 || f < 0.1) return "morning";
  if (f < 0.5) return "day";
  if (f < 0.66) return "dusk";
  return "night";
}

/** 時計を、つぎにその時間帯になる時刻まで進める（もうその時間帯なら、そのまま。時計は戻さない）。 */
export function advanceClockTo(clockMs: number, time: SceneTime): number {
  if (sceneTimeOf(clockMs) === time) return clockMs;
  const day = Math.floor(clockMs / DAY_MS) * DAY_MS;
  let target = day + SCENE_TIME_FRACTION[time] * DAY_MS;
  if (target <= clockMs) target += DAY_MS;
  return target;
}

export function periodLabel(clockMs: number): string {
  const f = dayFraction(clockMs);
  if (nightness(f) >= 0.7) return "夜";
  if (f >= 0.5 && f < 0.66) return "夕方";
  if (f >= 0.88) return "朝";
  return "昼";
}

/** 夜に外へ出ている町の人か（ぶらぶら歩く人は、およそ3人に1人だけ残る）。同じ人は、いつも同じ結果。 */
export function staysOutAtNight(npcId: string): boolean {
  let h = 0;
  for (let i = 0; i < npcId.length; i++) h = (h * 31 + npcId.charCodeAt(i)) >>> 0;
  return h % 3 === 0;
}

/** 夜の色をかける外の地図か（世界地図・町・村）。建物の中・ダンジョンは対象外。 */
export function isOutdoorMap(mapId: string): boolean {
  return mapId === "world-map" || /-(town|village)$/.test(mapId) || /^village-/.test(mapId);
}
