import { shadeColor } from "../color-utils";
import { ARCHETYPES, WALKERS } from "./walker-data.generated";
import { MOB_TEMPLATES } from "./mob-walker-data.generated";

/**
 * マップを歩くキャラクターのドット絵（16×32、4方向×3コマ）。`docs/design/pixel-character-guide.md` 第7・8節、
 * `docs/decisions.md`（2026-09-30、案B=16×32に決定）。髪・肌・服の色を変えるだけで、何人でも作れる「素体＋色」の作り方。
 * 絵は、体の部品をプログラムで置いていき、最後に外周へ暗い縁取りを自動でつける。既存作品の絵は参照していない。
 * 256×256の立ち絵・顔グラフィックと同じ人物に見えるよう、色は `PortraitSpec`（髪・肌・服）から取る。
 */
export type SpriteDir = "down" | "up" | "left" | "right";
export type SpriteFrame = 0 | 1 | 2;
export type SpriteHairStyle = "short" | "long" | "twin";

export interface SpriteSpec {
  skin: string;
  hair: string;
  /** 上着の色。 */
  top: string;
  /** ズボン・スカートの色。 */
  bottom: string;
  /** 帯・襟などの目印の色。 */
  accent: string;
  hairStyle: SpriteHairStyle;
  headband?: boolean;
  /** 手描きの絵（`walker-data.generated.ts`）がある人物の名前。あれば、素体＋色の代わりにそれを使う。 */
  handKey?: string;
  /** 町の人（モブ）の2頭身の素体の名前（`mob-walker-data.generated.ts`）。あれば、主要キャラと同じ作りの絵を、髪・肌・服の色で塗り替えて使う。 */
  mobTemplate?: string;
  /** 物を売る人（商人）。エプロン・はちまき・小銭入れを足して、商人らしく見せる（`applyMerchant`）。 */
  merchant?: boolean;
  /** 戦士（兵士・衛兵など）。兜と鎧を足して、戦士らしく見せる（`applyWarrior`）。 */
  warrior?: boolean;
}

export const SPRITE_WIDTH = 16;
export const SPRITE_HEIGHT = 32;
/** 足元（靴の底）の行。これより下は影。 */
export const SPRITE_FEET_ROW = 28;

const OUTLINE = "#221a30";
const SHADOW = "rgba(0, 0, 0, 0.28)";

export type SpritePixels = (string | null)[][];

function emptyGrid(): SpritePixels {
  return Array.from({ length: SPRITE_HEIGHT }, () => new Array<string | null>(SPRITE_WIDTH).fill(null));
}

function rect(grid: SpritePixels, x: number, y: number, w: number, h: number, color: string): void {
  for (let yy = y; yy < y + h; yy++) {
    for (let xx = x; xx < x + w; xx++) {
      if (yy >= 0 && yy < SPRITE_HEIGHT && xx >= 0 && xx < SPRITE_WIDTH) {
        grid[yy][xx] = color;
      }
    }
  }
}

/** 外周の透明なマスのうち、体に接するものを、暗い色で縁取る。影は縁取りの対象にしない。 */
function addOutline(grid: SpritePixels): void {
  const marks: [number, number][] = [];
  for (let y = 0; y < SPRITE_HEIGHT; y++) {
    for (let x = 0; x < SPRITE_WIDTH; x++) {
      if (grid[y][x] !== null) {
        continue;
      }
      for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
        const c = grid[y + dy]?.[x + dx];
        if (c && c !== SHADOW && c !== OUTLINE) {
          marks.push([x, y]);
          break;
        }
      }
    }
  }
  for (const [x, y] of marks) {
    grid[y][x] = OUTLINE;
  }
}

/** 歩きの3コマ（0=立ち、1=左足を出す、2=右足を出す）から、脚・腕の動きを決める。 */
function swing(frame: SpriteFrame): { leftLeg: number; rightLeg: number; leftArm: number; rightArm: number; stride: number } {
  if (frame === 1) {
    return { leftLeg: -1, rightLeg: 0, leftArm: 1, rightArm: -1, stride: 2 };
  }
  if (frame === 2) {
    return { leftLeg: 0, rightLeg: -1, leftArm: -1, rightArm: 1, stride: -2 };
  }
  return { leftLeg: 0, rightLeg: 0, leftArm: 0, rightArm: 0, stride: 0 };
}

function drawHairFront(grid: SpritePixels, spec: SpriteSpec, back: boolean): void {
  const hair = spec.hair;
  const hairDark = shadeColor(hair, -0.25);
  rect(grid, 4, 2, 8, 1, hair);
  rect(grid, 3, 3, 10, 4, hair);
  rect(grid, 4, 3, 8, 1, shadeColor(hair, 0.18));
  if (back) {
    rect(grid, 3, 7, 10, 6, hair);
    rect(grid, 4, 12, 8, 1, hairDark);
  } else {
    rect(grid, 3, 7, 2, 3, hair);
    rect(grid, 11, 7, 2, 3, hair);
    rect(grid, 5, 6, 6, 1, hairDark);
  }
  if (spec.hairStyle === "long") {
    rect(grid, 3, 10, 2, 8, hair);
    rect(grid, 11, 10, 2, 8, hair);
  } else if (spec.hairStyle === "twin") {
    rect(grid, 2, 9, 2, 6, hair);
    rect(grid, 12, 9, 2, 6, hair);
    rect(grid, 2, 14, 2, 1, hairDark);
    rect(grid, 12, 14, 2, 1, hairDark);
  }
  if (spec.headband && !back) {
    rect(grid, 3, 6, 10, 1, spec.accent);
  }
}

function drawFront(spec: SpriteSpec, frame: SpriteFrame, back: boolean): SpritePixels {
  const grid = emptyGrid();
  const s = swing(frame);
  const skinDark = shadeColor(spec.skin, -0.18);
  const topDark = shadeColor(spec.top, -0.22);
  const bottomDark = shadeColor(spec.bottom, -0.25);
  const boot = shadeColor(spec.bottom, -0.55);
  // 影
  rect(grid, 4, 29, 8, 2, SHADOW);
  // 脚（奥に沈む足は1ドット短い）
  rect(grid, 5, 23 + s.leftLeg, 3, 5 - s.leftLeg, spec.bottom);
  rect(grid, 8, 23 + s.rightLeg, 3, 5 - s.rightLeg, spec.bottom);
  rect(grid, 5, 27, 3, 1, boot);
  rect(grid, 8, 27, 3, 1, boot);
  rect(grid, 5, 28 + s.leftLeg, 3, 1, boot);
  rect(grid, 8, 28 + s.rightLeg, 3, 1, boot);
  rect(grid, 7, 23, 2, 1, bottomDark);
  // 胴・腕
  rect(grid, 4, 15, 8, 8, spec.top);
  rect(grid, 4, 21, 8, 1, topDark);
  rect(grid, 4, 21, 8, 1, spec.accent);
  rect(grid, 2, 16 + s.leftArm, 2, 6, spec.top);
  rect(grid, 12, 16 + s.rightArm, 2, 6, spec.top);
  rect(grid, 2, 22 + s.leftArm, 2, 2, spec.skin);
  rect(grid, 12, 22 + s.rightArm, 2, 2, spec.skin);
  if (!back) {
    rect(grid, 6, 15, 4, 1, spec.accent);
  }
  // 首・顔
  rect(grid, 7, 14, 2, 1, skinDark);
  if (!back) {
    rect(grid, 4, 7, 8, 7, spec.skin);
    rect(grid, 4, 13, 8, 1, skinDark);
    rect(grid, 5, 10, 1, 2, "#2a1f30");
    rect(grid, 10, 10, 1, 2, "#2a1f30");
    rect(grid, 7, 12, 2, 1, shadeColor(spec.skin, -0.35));
  }
  drawHairFront(grid, spec, back);
  addOutline(grid);
  return grid;
}

function drawSide(spec: SpriteSpec, frame: SpriteFrame): SpritePixels {
  // 左向き。右向きは、あとで左右を入れ替えて作る。
  const grid = emptyGrid();
  const s = swing(frame);
  const skinDark = shadeColor(spec.skin, -0.18);
  const topDark = shadeColor(spec.top, -0.22);
  const bottomDark = shadeColor(spec.bottom, -0.25);
  const boot = shadeColor(spec.bottom, -0.55);
  const hair = spec.hair;
  rect(grid, 4, 29, 8, 2, SHADOW);
  // 脚（奥の足は暗く、手前の足は明るく。歩幅で前後に開く）
  const back = 6 - s.stride / 2;
  const front = 7 + s.stride / 2;
  rect(grid, back, 23, 3, 5, bottomDark);
  rect(grid, back, 27, 3, 2, shadeColor(boot, -0.1));
  rect(grid, front, 23, 3, 5, spec.bottom);
  rect(grid, front - 1, 27, 4, 2, boot);
  // 胴・腕
  rect(grid, 5, 15, 6, 8, spec.top);
  rect(grid, 5, 21, 6, 1, spec.accent);
  rect(grid, 9, 15, 2, 8, topDark);
  const armX = 6 + Math.round(s.stride / 2);
  rect(grid, armX, 16, 2, 6, spec.top);
  rect(grid, armX, 22, 2, 2, spec.skin);
  // 首・頭（左を向く）
  rect(grid, 6, 14, 3, 1, skinDark);
  rect(grid, 3, 7, 7, 7, spec.skin);
  rect(grid, 3, 13, 7, 1, skinDark);
  rect(grid, 4, 10, 1, 2, "#2a1f30");
  rect(grid, 2, 11, 1, 1, skinDark);
  // 髪（後ろと上）
  rect(grid, 4, 2, 8, 1, hair);
  rect(grid, 3, 3, 10, 4, hair);
  rect(grid, 4, 3, 7, 1, shadeColor(hair, 0.18));
  rect(grid, 9, 7, 4, 6, hair);
  rect(grid, 3, 6, 4, 1, shadeColor(hair, -0.25));
  if (spec.hairStyle === "long") {
    rect(grid, 9, 12, 4, 6, hair);
  } else if (spec.hairStyle === "twin") {
    rect(grid, 11, 9, 2, 6, hair);
  }
  if (spec.headband) {
    rect(grid, 3, 6, 10, 1, spec.accent);
  }
  addOutline(grid);
  return grid;
}

function mirror(grid: SpritePixels): SpritePixels {
  return grid.map((row) => [...row].reverse());
}

const LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

/** 手描きの素体（役割色の番号で持つ）を、髪・肌・服・帯の色で塗り替える。 */
function recolorArchetype(
  arch: { fixed: string[]; frames: Record<string, string[]> },
  spec: SpriteSpec,
  dir: SpriteDir,
  frame: SpriteFrame,
): SpritePixels {
  const roles = [
    shadeColor(spec.hair, -0.35), spec.hair, shadeColor(spec.hair, 0.3),
    shadeColor(spec.skin, -0.18), spec.skin, shadeColor(spec.skin, 0.15),
    shadeColor(spec.top, -0.3), spec.top, shadeColor(spec.top, 0.3),
    shadeColor(spec.bottom, -0.2), spec.bottom, shadeColor(spec.bottom, 0.25),
    "#2a1a12", "#4a2c1a", "#6a4228",
    shadeColor(spec.accent, -0.3), spec.accent, shadeColor(spec.accent, 0.3),
    shadeColor(spec.hair, -0.7), shadeColor(spec.skin, -0.55), shadeColor(spec.top, -0.7),
    shadeColor(spec.bottom, -0.7), "#140c08", shadeColor(spec.accent, -0.7),
  ];
  return arch.frames[`${dir}${frame}`].map((row) =>
    [...row].map((ch) => {
      if (ch === ".") {
        return null;
      }
      const index = LETTERS.indexOf(ch);
      return index < 24 ? roles[index] : arch.fixed[index - 24];
    }),
  );
}

/** 町の人の2頭身の素体を、髪・肌・服・飾りの色で塗り替える。同じ役割の色の明暗の差は、そのまま保つ。 */
function recolorMob(spec: SpriteSpec, dir: SpriteDir, frame: SpriteFrame): SpritePixels | null {
  const tpl = spec.mobTemplate ? MOB_TEMPLATES[spec.mobTemplate] : undefined;
  if (!tpl) return null;
  const base: Record<string, string> = { hair: spec.hair, skin: spec.skin, top: spec.top, bottom: spec.bottom || spec.top, accent: spec.accent };
  const colors = tpl.palette.map((c, i) => (tpl.roles[i] === "fixed" ? c : shadeColor(base[tpl.roles[i]] ?? c, tpl.shade[i])));
  const grid = tpl.frames[`${dir}${frame}`].map((row) => [...row].map((ch) => (ch === "." ? null : colors[LETTERS.indexOf(ch)])));
  if (spec.warrior) {
    const down = tpl.frames["down0"];
    const skinLetters = new Set(tpl.roles.map((r, i) => (r === "skin" ? LETTERS[i] : "")).filter(Boolean));
    let faceTop = 8;
    for (let y = 0; y < down.length; y++) {
      if ([...down[y]].some((ch) => skinLetters.has(ch))) {
        faceTop = y;
        break;
      }
    }
    applyWarrior(grid, dir, spec, faceTop, tpl.roles.map((r, i) => (r === "hair" ? colors[i] : "")).filter(Boolean));
  } else if (spec.merchant) {
    // 顔の上のへり（髪の生えぎわ）の段: 肌の色の画素がいちばん上にある段
    const down = tpl.frames[`down0`];
    const skinLetters = new Set(tpl.roles.map((r, i) => (r === "skin" ? LETTERS[i] : "")).filter(Boolean));
    let faceTop = 8;
    for (let y = 0; y < down.length; y++) {
      if ([...down[y]].some((ch) => skinLetters.has(ch))) {
        faceTop = y;
        break;
      }
    }
    applyMerchant(grid, dir, spec, faceTop, tpl.roles.map((r, i) => (r === "hair" ? colors[i] : "")).filter(Boolean));
  }
  return grid;
}

const STEEL_LIGHT = "#d4dae4";
const STEEL = "#9aa4b4";
const STEEL_DARK = "#6a7484";
const STEEL_DEEP = "#454e5e";

/** 戦士らしく: 兜（髪の上を鉄の色に。てっぺんに飾り）・胸当て・肩当て・ベルト。 */
function applyWarrior(grid: SpritePixels, dir: SpriteDir, spec: SpriteSpec, faceTop: number, hairColors: string[]): void {
  const w = grid[0].length;
  const put = (x: number, y: number, c: string): void => {
    if (y >= 0 && y < grid.length && x >= 0 && x < w && grid[y][x] !== null) grid[y][x] = c;
  };
  const isHair = (c: string | null): boolean => !!c && hairColors.includes(c);
  // 兜: 生えぎわより上の髪を鉄に（左上が明るい）。生えぎわのへりは暗く
  for (let y = 0; y < faceTop + 1; y++) {
    for (let x = 0; x < w; x++) {
      if (!isHair(grid[y][x])) continue;
      const c = y === faceTop ? STEEL_DEEP : y === faceTop - 1 ? STEEL_DARK : y <= 5 && x < w / 2 ? STEEL_LIGHT : x < w / 2 ? STEEL : STEEL_DARK;
      grid[y][x] = c;
    }
  }
  // 兜の側面（耳のあたり）も鉄に
  for (let y = faceTop + 1; y <= faceTop + 3; y++) for (let x = 0; x < w; x++) if (isHair(grid[y][x])) grid[y][x] = x < w / 2 ? STEEL : STEEL_DARK;
  // 兜のてっぺんの飾り（かざりの色）
  let topY = -1;
  for (let y = 0; y < grid.length && topY < 0; y++) if (grid[y].some((c) => c !== null && c !== "#1a1018")) topY = y;
  if (topY >= 0 && dir !== "left" && dir !== "right") {
    put(7, topY, spec.accent); put(8, topY, spec.accent);
  } else if (topY >= 0) {
    put(dir === "left" ? 7 : 8, topY, spec.accent);
  }
  // 胸当て・肩当て・ベルト
  const x0 = dir === "down" || dir === "up" ? 4 : 5;
  const x1 = dir === "down" || dir === "up" ? 11 : 10;
  for (let y = 19; y <= 22; y++) {
    for (let x = x0; x <= x1; x++) {
      const light = x < (x0 + x1) / 2;
      put(x, y, y === 19 ? STEEL_LIGHT : y === 22 ? STEEL_DARK : light ? STEEL : STEEL_DARK);
    }
  }
  if (dir === "down") {
    for (let y = 20; y <= 21; y++) { put(7, y, STEEL_LIGHT); put(8, y, STEEL); } // 胸の中央の筋
  }
  if (dir === "up") {
    for (let y = 20; y <= 21; y++) put(7, y, STEEL_DEEP);
  }
  put(x0 - 1, 19, STEEL); put(x0 - 1, 20, STEEL_DARK); put(x1 + 1, 19, STEEL); put(x1 + 1, 20, STEEL_DARK); // 肩当て
  for (let x = x0; x <= x1; x++) put(x, 23, "#5a4026");
  if (dir === "down") { put(7, 23, "#e8c048"); put(8, 23, "#e8c048"); }
}

const APRON = "#f0e8d4";
const APRON_SHADE = "#cfc2a0";
const APRON_DARK = "#a89a78";

/** 商人らしく: はちまき（髪の生えぎわ）・エプロン・小銭入れ。 */
function applyMerchant(grid: SpritePixels, dir: SpriteDir, spec: SpriteSpec, faceTop: number, hairColors: string[]): void {
  const put = (x: number, y: number, c: string): void => {
    if (y >= 0 && y < grid.length && x >= 0 && x < grid[0].length && grid[y][x] !== null) grid[y][x] = c;
  };
  const isHair = (c: string | null): boolean => !!c && hairColors.includes(c);
  // はちまき: 生えぎわのすぐ上の段（髪の色の画素だけ）を、かざりの色に
  const bandY = faceTop - 1;
  for (let y = bandY; y <= bandY; y++) {
    for (let x = 0; x < grid[0].length; x++) if (isHair(grid[y]?.[x] ?? null)) grid[y][x] = spec.accent;
  }
  if (dir === "up") {
    for (let x = 0; x < grid[0].length; x++) if (isHair(grid[bandY + 1]?.[x] ?? null)) grid[bandY + 1][x] = shadeColor(spec.accent, -0.2);
  }
  // エプロン
  if (dir === "down") {
    for (let y = 17; y <= 25; y++) {
      const half = y <= 18 ? 2 : 3;
      for (let x = 8 - half; x < 8 + half; x++) put(x, y, x === 8 - half ? APRON_SHADE : APRON);
    }
    for (let x = 5; x <= 10; x++) put(x, 25, APRON_DARK); // すその影
    for (let x = 6; x <= 9; x++) put(x, 22, APRON_SHADE); // ポケットのふち
    put(5, 17, APRON_DARK); put(10, 17, APRON_DARK); // 肩のひも
    // 小銭入れ（腰の右）
    put(11, 22, "#b88a3a"); put(12, 22, "#b88a3a"); put(11, 23, "#8a6226"); put(12, 23, "#8a6226"); put(11, 21, "#e8c048");
  } else if (dir === "up") {
    for (let x = 4; x <= 11; x++) put(x, 20, APRON); // 腰のひも
    put(7, 21, APRON); put(8, 21, APRON); put(6, 22, APRON_SHADE); put(9, 22, APRON_SHADE);
  } else {
    // 横向き: からだの前（向いているほう）に、エプロンのへり
    const frontX = dir === "left" ? [4, 5, 6] : [9, 10, 11];
    for (let y = 18; y <= 25; y++) for (const x of frontX) put(x, y, y === 25 ? APRON_DARK : APRON);
  }
}

export function buildSpritePixels(spec: SpriteSpec, dir: SpriteDir, frame: SpriteFrame): SpritePixels {
  const mob = recolorMob(spec, dir, frame);
  if (mob) {
    return mob;
  }
  const arch = !spec.handKey ? ARCHETYPES[spec.hairStyle === "short" ? "short" : spec.hairStyle] : undefined;
  if (arch) {
    return recolorArchetype(arch, spec, dir, frame);
  }
  const hand = spec.handKey ? WALKERS[spec.handKey] : undefined;
  if (hand) {
    const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    return hand.frames[`${dir}${frame}`].map((row) => [...row].map((ch) => (ch === "." ? null : hand.palette[letters.indexOf(ch)])));
  }
  switch (dir) {
    case "down":
      return drawFront(spec, frame, false);
    case "up":
      return drawFront(spec, frame, true);
    case "left":
      return drawSide(spec, frame);
    case "right":
      return mirror(drawSide(spec, frame));
  }
}

/** 同じ色が横に続く部分をまとめた矩形（描画の回数を減らす）。 */
export interface SpriteRun {
  x: number;
  y: number;
  w: number;
  color: string;
}

export function spriteRuns(pixels: SpritePixels): SpriteRun[] {
  const runs: SpriteRun[] = [];
  pixels.forEach((row, y) => {
    let x = 0;
    while (x < row.length) {
      const color = row[x];
      if (!color) {
        x++;
        continue;
      }
      let w = 1;
      while (x + w < row.length && row[x + w] === color) {
        w++;
      }
      runs.push({ x, y, w, color });
      x += w;
    }
  });
  return runs;
}

/** 歩きのコマの並び（立ち→左足→立ち→右足）。`animationMs`から今のコマを決める。 */
export const WALK_CYCLE: SpriteFrame[] = [0, 1, 0, 2];
export const WALK_FRAME_MS = 140;

export function frameAt(moving: boolean, animationMs: number): SpriteFrame {
  if (!moving) {
    return 0;
  }
  return WALK_CYCLE[Math.floor(animationMs / WALK_FRAME_MS) % WALK_CYCLE.length];
}
