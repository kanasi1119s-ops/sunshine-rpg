/**
 * 「はじめから」のあとに流れるオープニング（あらすじのムービー）。絵の上に文字が1文字ずつ出て、場面が切りかわる。
 * 決定: 文字を全部出す → 次の場面へ。キャンセル（x・Esc）や画面のボタンで、まるごと飛ばせる。
 * 仮: 絵は戦闘の背景のドット絵を動かしたものと、描いた演出（光の環・流星・稲妻）。曲は `fate`。ネタバレになる内容は書かない（序章までの設定だけ）。
 */
export type OpeningArt = "stars" | "void2" | "sea1" | "prophecy" | "sea2" | "meadow" | "title";
export type OpeningSprites = "none" | "party" | "hero";
/** 絵の上に重ねる演出。 */
export type OpeningOverlay = "ring" | "shatter" | "meteors" | "lightning" | "rays" | null;

export interface OpeningScene {
  art: OpeningArt;
  lines: string[];
  /** 絵の前を歩く人たち（仮のドット絵）。 */
  sprites: OpeningSprites;
  /** 光の粒の色（空を漂う）。 */
  sparkle: string;
  /** 絵の寄り（拡大率）の始めと終わり。 */
  zoom: [number, number];
  /** 絵の横ゆれ（ピクセル）の始めと終わり。 */
  pan: [number, number];
  overlay: OpeningOverlay;
  /** 画面のゆれの強さ（ピクセル）。0でゆれない。 */
  shake: number;
  /** 場面の頭に白くひらめく時間（ms）。0でひらめかない。 */
  flashMs: number;
  /** 絵の上に重ねる色（暗くする・赤みをつける）。 */
  tint?: string;
  /** 画面の中央に大きく出す一言。 */
  caption?: string;
}

/** 壮大に見せる（2026-10-05、人間の指示「もっと壮大なオープニングのがいい。優しすぎる」）。曲は `fate`（運命の扉）。 */
export const OPENING_SCENES: OpeningScene[] = [
  {
    art: "stars",
    lines: ["はるか昔、世界は、", "空をわたる巨大な光の環に抱かれていた。", "人々はそれを「灯の環」とよんだ。"],
    sprites: "none",
    sparkle: "#ffe9a0",
    zoom: [1, 1.15],
    pan: [0, 0],
    overlay: "ring",
    shake: 0,
    flashMs: 0,
  },
  {
    art: "void2",
    lines: ["だが、ある時、環は砕けた。", "無数の光のかけらが、", "流星のように地上へ降りそそいだ。"],
    sprites: "none",
    sparkle: "#8ad8ff",
    zoom: [1.25, 1],
    pan: [0, 0],
    overlay: "shatter",
    shake: 3,
    flashMs: 900,
    tint: "rgba(10, 0, 30, 0.35)",
  },
  {
    art: "sea1",
    lines: ["かけらは山となり、海となり、", "人々の暮らしを照らす「灯り石」となって、", "静かに世界を支えつづけた。"],
    sprites: "none",
    sparkle: "#f2c14e",
    zoom: [1.05, 1.18],
    pan: [-14, 14],
    overlay: "meteors",
    shake: 0,
    flashMs: 0,
  },
  {
    art: "stars",
    lines: ["統暦412年。", "大陸アルテシアは、", "かりそめの平和のなかにあった。"],
    sprites: "none",
    sparkle: "#8a8aa8",
    zoom: [1, 1],
    pan: [0, 0],
    overlay: "ring",
    shake: 0,
    flashMs: 0,
    caption: "それから、四百年。",
  },
  {
    art: "prophecy",
    lines: ["しかし今、各地で「歪み」が目を覚ます。", "水は涸れ、荷は消え、大地は崩れ落ちる。", "世界の灯りが、ひとつ、またひとつと消えていく。"],
    sprites: "none",
    sparkle: "#c890ff",
    zoom: [1, 1.2],
    pan: [8, -8],
    overlay: "lightning",
    shake: 2,
    flashMs: 0,
    tint: "rgba(60, 0, 20, 0.25)",
  },
  {
    art: "sea2",
    lines: ["港町・灯里。", "「灯りの相談所」の新人調査員ユーリの手で、", "祖父から受け継いだ腕輪が、かすかに光った。"],
    sprites: "hero",
    sparkle: "#ffe9a0",
    zoom: [1.15, 1],
    pan: [10, -10],
    overlay: null,
    shake: 0,
    flashMs: 0,
  },
  {
    art: "meadow",
    lines: ["出会い、ぶつかり、謎を追い、", "やがて旅は、世界のはての真実へつづいていく。"],
    sprites: "party",
    sparkle: "#f2c14e",
    zoom: [1, 1.2],
    pan: [0, 0],
    overlay: "meteors",
    shake: 0,
    flashMs: 0,
  },
  {
    art: "title",
    lines: ["ひなたの下で、少しずつ、", "真実に近づく旅が、いま、はじまる。"],
    sprites: "none",
    sparkle: "#f2c14e",
    zoom: [1, 1],
    pan: [0, 0],
    overlay: "rays",
    shake: 0,
    flashMs: 700,
  },
];

/** 1文字が出るまでの時間（ms）。 */
export const OPENING_CHAR_MS = 50;
/** 文字が全部出たあと、次へ進むまで待つ時間（ms）。 */
export const OPENING_HOLD_MS = 2600;
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
