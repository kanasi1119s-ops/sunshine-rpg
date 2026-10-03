import { describe, expect, it } from "vitest";
import { buildSpritePixels, frameAt, SPRITE_FEET_ROW, SPRITE_HEIGHT, SPRITE_WIDTH, spriteRuns, type SpriteDir, type SpriteFrame, type SpriteSpec } from "./overworld-sprite";

const SPEC: SpriteSpec = { skin: "#f2c9a0", hair: "#3a2a20", top: "#3a6ab0", bottom: "#4a4a60", accent: "#f2c14e", hairStyle: "short" };
const DIRS: SpriteDir[] = ["down", "up", "left", "right"];
const FRAMES: SpriteFrame[] = [0, 1, 2];

function colorCount(pixels: (string | null)[][]): number {
  return new Set(pixels.flat().filter(Boolean)).size;
}
function bottomRow(pixels: (string | null)[][]): number {
  for (let y = SPRITE_HEIGHT - 1; y >= 0; y--) {
    if (pixels[y].some((c) => c && c !== "rgba(0, 0, 0, 0.28)")) {
      return y;
    }
  }
  return -1;
}

describe("マップを歩くキャラクターのドット絵（16×32）", () => {
  it("すべての向き・コマで、16×32の絵ができ、体と縁取りがある", () => {
    for (const dir of DIRS) {
      for (const frame of FRAMES) {
        const px = buildSpritePixels(SPEC, dir, frame);
        expect(px).toHaveLength(SPRITE_HEIGHT);
        expect(px.every((row) => row.length === SPRITE_WIDTH)).toBe(true);
        expect(px.flat().filter(Boolean).length, `${dir}${frame}`).toBeGreaterThan(150);
        expect(px.flat().some((c) => c && c !== "rgba(0, 0, 0, 0.28)" && parseInt(c.slice(1, 3), 16) + parseInt(c.slice(3, 5), 16) + parseInt(c.slice(5, 7), 16) < 150), `${dir}${frame} の縁取り`).toBe(true);
      }
    }
  });

  it("色数が多すぎない（手描きの素体＋役割色で40色以内）", () => {
    for (const dir of DIRS) {
      for (const frame of FRAMES) {
        expect(colorCount(buildSpritePixels(SPEC, dir, frame))).toBeLessThanOrEqual(40);
      }
    }
  });

  it("正面・後ろ・横で高さがそろい、足元は同じ行（歩いても、足元の線が1ドットしか動かない）", () => {
    const bottoms = DIRS.flatMap((dir) => FRAMES.map((frame) => bottomRow(buildSpritePixels(SPEC, dir, frame))));
    for (const b of bottoms) {
      expect(Math.abs(b - (SPRITE_FEET_ROW + 1))).toBeLessThanOrEqual(1); // 縁取りが1行ぶん下に出る
    }
  });

  it("4方向（下・上・左・右）が別々の絵で、歩きのコマで絵が変わる", () => {
    const sets = DIRS.map((dir) => JSON.stringify(buildSpritePixels(SPEC, dir, 0)));
    expect(new Set(sets).size).toBe(4);
    expect(buildSpritePixels(SPEC, "down", 1)).not.toEqual(buildSpritePixels(SPEC, "down", 0));
    expect(buildSpritePixels(SPEC, "left", 1)).not.toEqual(buildSpritePixels(SPEC, "left", 2));
  });

  it("正面には顔（目）があり、後ろ向きには無い", () => {
    const eye = "#1a1420";
    const count = (px: (string | null)[][]): number => px.flat().filter((c) => c === eye).length;
    expect(count(buildSpritePixels(SPEC, "down", 0))).toBeGreaterThan(count(buildSpritePixels(SPEC, "up", 0)));
  });

  it("髪型（短い・長い・ツインテール）で、絵が変わる", () => {
    const short = buildSpritePixels(SPEC, "down", 0);
    expect(buildSpritePixels({ ...SPEC, hairStyle: "long" }, "down", 0)).not.toEqual(short);
    expect(buildSpritePixels({ ...SPEC, hairStyle: "twin" }, "down", 0)).not.toEqual(short);
  });

  it("同じ色が続く部分は、矩形にまとまる（描く回数が、ドットの数より少ない）", () => {
    const px = buildSpritePixels(SPEC, "down", 0);
    expect(spriteRuns(px).length).toBeLessThan(px.flat().filter(Boolean).length * 0.7);
  });

  it("歩きのコマ: 止まっていれば立ち、歩くと立ち→左足→立ち→右足と回る", () => {
    expect(frameAt(false, 999)).toBe(0);
    const frames = [0, 140, 280, 420, 560].map((ms) => frameAt(true, ms));
    expect(frames).toEqual([0, 1, 0, 2, 0]);
  });
});
