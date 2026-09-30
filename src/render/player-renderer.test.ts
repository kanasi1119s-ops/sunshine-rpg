import { describe, expect, it } from "vitest";
import { renderPlayer } from "./player-renderer";
import { createPlayer } from "../game/player";
import { createCamera } from "./camera";

class FakeContext {
  fillStyle = "";
  rectCalls: { x: number; y: number; w: number; h: number }[] = [];

  fillRect(x: number, y: number, w: number, h: number): void {
    this.rectCalls.push({ x, y, w, h });
  }
}

describe("renderPlayer", () => {
  it("16×32のドット絵を、判定の足元の中央にそろえて描く（頭は上のマスにはみ出す）", () => {
    const ctx = new FakeContext();
    const player = createPlayer(48, 48); // 判定は 12×14
    renderPlayer(ctx as unknown as CanvasRenderingContext2D, player, createCamera(400, 225));
    expect(ctx.rectCalls.length).toBeGreaterThan(20);
    const minY = Math.min(...ctx.rectCalls.map((r) => r.y));
    const maxY = Math.max(...ctx.rectCalls.map((r) => r.y));
    const minX = Math.min(...ctx.rectCalls.map((r) => r.x));
    const maxX = Math.max(...ctx.rectCalls.map((r) => r.x + r.w));
    expect(maxY).toBeLessThanOrEqual(48 + 14 + 1); // 足元（判定の下端）まで。影が下に2行
    expect(minY).toBeLessThan(48 - 10); // 頭は判定より上にはみ出す
    expect(maxX - minX).toBeLessThanOrEqual(16);
  });

  it("向きが変わっても、歩いていても、描画エラーにならない", () => {
    const camera = createCamera(400, 225);
    for (const direction of ["up", "down", "left", "right"] as const) {
      for (const moving of [false, true]) {
        const ctx = new FakeContext();
        const player = { ...createPlayer(5, 5), direction, moving, animationMs: 300 };
        expect(() => renderPlayer(ctx as unknown as CanvasRenderingContext2D, player, camera)).not.toThrow();
        expect(ctx.rectCalls.length).toBeGreaterThan(20);
      }
    }
  });
});
