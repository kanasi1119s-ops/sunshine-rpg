/**
 * ゲームを起動したときのオープニング。
 *  1. splash: 「サンシャインソフトウェア」と「決定でスタート」（ブラウザは、音を鳴らす前に操作が要るので、ここで1回押してもらう）
 *  2. logo:   曲が鳴りはじめ、ロゴが上から落ちてきて、光る
 *  3. story:  ロゴが上へ上がり、あらすじが下から上へ流れる
 *  4. 終わると（決定でとばしても）、タイトル画面へ
 * 時間の進みだけを持つ。絵は `render/boot-opening-renderer.ts`。
 * （既存作品のロゴ・演出のまねはしない。ロゴは本作の名前を、金色の文字と光で見せるオリジナルのもの。）
 */
export type BootPhase = "splash" | "logo" | "story";

export interface BootOpeningState {
  open: boolean;
  phase: BootPhase;
  /** その段が始まってからの時間（ms）。 */
  ms: number;
}

/** ロゴが落ちて、光って、落ち着くまでの時間（ms）。 */
export const LOGO_MS = 4600;
/** あらすじの流れる速さ（論理のドット／秒）と、1行の高さ。 */
export const STORY_SPEED = 20;
export const STORY_LINE_HEIGHT = 17;

export const STORY_LINES: string[] = [
  "大陸アルテシア。",
  "空をわたる巨大な光の環「灯の環」は、",
  "いつの日か砕けて地上へ降り、",
  "そのかけらは山となり、海となり、",
  "人々の暮らしを照らす「灯り石」となった。",
  "",
  "統暦412年。",
  "平和に見えた世界の各地で、",
  "「歪み」とよばれる異変が、目を覚ます。",
  "水は涸れ、荷は消え、大地は崩れ落ちる。",
  "",
  "港町・灯里の「灯りの相談所」に入った",
  "新人調査員ユーリは、祖父から受け継いだ",
  "灯り石の腕輪を手に、最初の依頼へ向かう。",
  "",
  "ひなたの下で、少しずつ、",
  "真実に近づく旅が、いま、はじまる――。",
];

export function startBootOpening(): BootOpeningState {
  return { open: true, phase: "splash", ms: 0 };
}

/** あらすじが全部流れきるまでの時間（ms）。画面の高さぶんの余白を含む。 */
export function storyDurationMs(screenHeight: number): number {
  return ((STORY_LINES.length * STORY_LINE_HEIGHT + screenHeight) / STORY_SPEED) * 1000;
}

export function updateBootOpening(state: BootOpeningState, dtMs: number, screenHeight: number): BootOpeningState {
  if (!state.open || state.phase === "splash") return state;
  const ms = state.ms + dtMs;
  if (state.phase === "logo") {
    return ms >= LOGO_MS ? { ...state, phase: "story", ms: 0 } : { ...state, ms };
  }
  return ms >= storyDurationMs(screenHeight) ? { ...state, open: false } : { ...state, ms };
}

/** 決定: スタート → ロゴ（曲がはじまる）→ あらすじ → タイトル。 */
export function advanceBootOpening(state: BootOpeningState): BootOpeningState {
  if (!state.open) return state;
  if (state.phase === "splash") return { ...state, phase: "logo", ms: 0 };
  if (state.phase === "logo") return { ...state, phase: "story", ms: 0 };
  return { ...state, open: false };
}

/** ロゴの高さ（0=画面の上の外、1=落ち着いた位置）。落ちて、はずんで、止まる。 */
export function logoDrop(ms: number): number {
  const fall = 900;
  if (ms <= 0) return 0;
  if (ms < fall) {
    const t = ms / fall;
    return t * t; // だんだん速く落ちる
  }
  // 着地のあと、2回はずむ
  const t = (ms - fall) / 900;
  if (t >= 1) return 1;
  const bounce = Math.exp(-4 * t) * Math.abs(Math.sin(t * Math.PI * 2.5));
  return 1 - 0.18 * bounce;
}

/** 着地の瞬間（ms）。光と画面のゆれの合図に使う。 */
export const LOGO_LAND_MS = 900;
