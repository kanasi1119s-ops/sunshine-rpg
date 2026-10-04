/**
 * ゲームを起動したときのオープニング。
 *  1. splash: 「SUNSHINE SOFTWARE PRESENTS」（英語のみ）。タップ・決定で、オープニングがはじまる
 *     （ブラウザは、操作がないと音を鳴らせないので、このタップが音のはじまりにもなる）
 *  2. story:  曲がはじまり、星空の上を、あらすじが下から上へ流れる
 *  3. reveal: 光が集まってリングになり、曲のクライマックスの一撃で、文字が輝きながら現れる（タイトルは最後に出る）
 *  4. hold:   ロゴを見せたまま、決定ボタンが押されるまで、曲もロゴもそのまま流れつづける
 *  5. 決定でタイトル画面へ（途中で押すと、ひとつ先へとばす）
 * 時間の進みだけを持つ。絵は `render/boot-opening-renderer.ts`。
 * （既存作品のロゴ・演出のまねはしない。）
 */
export type BootPhase = "splash" | "story" | "reveal" | "hold";

export interface BootOpeningState {
  open: boolean;
  phase: BootPhase;
  /** その段が始まってからの時間（ms）。 */
  ms: number;
}

/** あらすじの流れる速さ（論理のドット／秒）と、1行の高さ。 */
export const STORY_SPEED = 20;
export const STORY_LINE_HEIGHT = 17;

/** 曲の最初の一撃（ティンパニと金管）が鳴る時刻（ms。曲のはじまりから）。星空が光る。 */
export const OPENING_HIT_MS = 900;

/** 光が集まる → 文字が現れる → サブタイトルが出る、の時刻（revealの頭から、ms）と、全体の長さ。 */
export const REVEAL = { gatherEnd: 3000, lettersEnd: 4300, subtitleEnd: 5500, total: 6500 } as const;

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
  if (state.phase === "story") {
    return ms >= storyDurationMs(screenHeight) ? { ...state, phase: "reveal", ms: 0 } : { ...state, ms };
  }
  if (state.phase === "reveal") {
    return ms >= REVEAL.total ? { ...state, phase: "hold", ms: 0 } : { ...state, ms };
  }
  // hold: ボタンが押されるまで、そのまま流れつづける
  return { ...state, ms };
}

/** 決定: タップでスタート → あらすじ → （ロゴの登場を見せる）→ ロゴ → タイトル。途中で押すと、ひとつ先へ。 */
export function advanceBootOpening(state: BootOpeningState): BootOpeningState {
  if (!state.open) return state;
  if (state.phase === "splash") return { ...state, phase: "story", ms: 0 };
  if (state.phase === "story") return { ...state, phase: "reveal", ms: 0 };
  if (state.phase === "reveal") return { ...state, phase: "hold", ms: REVEAL.total };
  return { ...state, open: false };
}
