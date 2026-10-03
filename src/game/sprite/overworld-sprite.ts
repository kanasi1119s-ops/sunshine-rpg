import { shadeColor } from "../color-utils";
import { ARCHETYPES, WALKERS } from "./walker-data.generated";

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

export function buildSpritePixels(spec: SpriteSpec, dir: SpriteDir, frame: SpriteFrame): SpritePixels {
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
