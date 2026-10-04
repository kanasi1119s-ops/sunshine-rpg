/**
 * 「はじめから」のあとに流れるオープニング（あらすじのムービー）。絵の上に文字が1文字ずつ出て、場面が切りかわる。
 * 決定: 文字を全部出す → 次の場面へ。キャンセル（x・Esc）や画面のボタンで、まるごと飛ばせる。
 * 仮: 絵は戦闘の背景のドット絵をゆっくり動かしたもの。曲はタイトルの曲（`title`）のまま。ネタバレになる内容は書かない（序章までの設定だけ）。
 */
export type OpeningArt = "void2" | "sea1" | "meadow" | "prophecy" | "sea2" | "title";
export type OpeningSprites = "none" | "party" | "hero";

export interface OpeningScene {
  art: OpeningArt;
  lines: string[];
  /** 絵の前を歩く人たち（仮のドット絵）。 */
  sprites: OpeningSprites;
  /** 光の粒の色（空を漂う）。 */
  sparkle: string;
}

export const OPENING_SCENES: OpeningScene[] = [
  {
    art: "void2",
    lines: ["むかし、空をわたる巨大な光の柱があった。", "人々はそれを「灯の環」とよんだ。"],
    sprites: "none",
    sparkle: "#8ad8ff",
  },
  {
    art: "sea1",
    lines: ["環は地上へ降りて砕け、", "そのかけらは山となり、海となり、", "暮らしを照らす「灯り石」になった。"],
    sprites: "none",
    sparkle: "#f2c14e",
  },
  {
    art: "meadow",
    lines: ["それから長い時がすぎ、統暦412年。", "大陸アルテシアは、おだやかな日々の", "なかにあった。"],
    sprites: "party",
    sparkle: "#f2c14e",
  },
  {
    art: "prophecy",
    lines: ["ところが近ごろ、各地で「歪み」とよばれる", "ふしぎな異変が起きはじめる。", "水が涸れ、荷が消え、坑道が崩れる……。"],
    sprites: "none",
    sparkle: "#c890ff",
  },
  {
    art: "sea2",
    lines: ["港町・灯里。「灯りの相談所」に入ったばかりの", "ユーリは、祖父から受け継いだ灯り石の腕輪を", "手に、ひとつ目の依頼へ向かう。"],
    sprites: "hero",
    sparkle: "#ffe9a0",
  },
  {
    art: "title",
    lines: ["ひなたの下で、少しずつ、", "真実に近づく旅が、はじまる。"],
    sprites: "none",
    sparkle: "#f2c14e",
  },
];

/** 1文字が出るまでの時間（ms）。 */
export const OPENING_CHAR_MS = 55;
/** 文字が全部出たあと、次へ進むまで待つ時間（ms）。 */
export const OPENING_HOLD_MS = 2200;
/** 場面の頭の、暗い状態から絵が現れるまでの時間（ms）。 */
export const OPENING_FADE_MS = 700;

export interface OpeningState {
  open: boolean;
  scene: number;
  /** 場面が始まってからの時間（ms）。 */
  elapsedMs: number;
}

export function createOpeningState(): OpeningState {
  return { open: false, scene: 0, elapsedMs: 0 };
}

export function startOpening(): OpeningState {
  return { open: true, scene: 0, elapsedMs: 0 };
}

function totalChars(scene: OpeningScene): number {
  return scene.lines.reduce((sum, line) => sum + line.length, 0);
}

/** 場面の文字が全部出るまでの時間（ms）。 */
export function revealDurationMs(scene: OpeningScene): number {
  return OPENING_FADE_MS + totalChars(scene) * OPENING_CHAR_MS;
}

/** 場面の長さ（ms）。 */
export function sceneDurationMs(scene: OpeningScene): number {
  return revealDurationMs(scene) + OPENING_HOLD_MS;
}

/** いま出ている文字の数（場面全体の通し）。 */
export function visibleChars(scene: OpeningScene, elapsedMs: number): number {
  return Math.max(0, Math.min(totalChars(scene), Math.floor((elapsedMs - OPENING_FADE_MS) / OPENING_CHAR_MS)));
}

function nextScene(state: OpeningState): OpeningState {
  if (state.scene + 1 >= OPENING_SCENES.length) {
    return { ...state, open: false };
  }
  return { open: true, scene: state.scene + 1, elapsedMs: 0 };
}

export function updateOpening(state: OpeningState, dtMs: number): OpeningState {
  if (!state.open) {
    return state;
  }
  const elapsedMs = state.elapsedMs + dtMs;
  if (elapsedMs >= sceneDurationMs(OPENING_SCENES[state.scene])) {
    return nextScene(state);
  }
  return { ...state, elapsedMs };
}

/** 決定: 文字が途中なら全部出す。全部出ていれば次の場面へ。 */
export function advanceOpening(state: OpeningState): OpeningState {
  if (!state.open) {
    return state;
  }
  const scene = OPENING_SCENES[state.scene];
  if (state.elapsedMs < revealDurationMs(scene)) {
    return { ...state, elapsedMs: revealDurationMs(scene) };
  }
  return nextScene(state);
}

/** まるごと飛ばす。 */
export function skipOpening(state: OpeningState): OpeningState {
  return { ...state, open: false };
}
