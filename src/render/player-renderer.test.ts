import { describe, expect, it } from "vitest";
import { renderPlayer } from "./player-renderer";
import { createPlayer } from "../game/player";
import { createCamera } from "./camera";

class FakeContext {
  fillStyle = "";
  rectCalls: { x: number; y: number; w: number; h: number }[] = [];
  pathCalls = 0;

  fillRect(x: number, y: number, w: number, h: number): void {
    this.rectCalls.push({ x, y, w, h });
  }
  beginPath(): void {
    this.pathCalls++;
  }
  moveTo(): void {}
  lineTo(): void {}
  closePath(): void {}
  fill(): void {}
}

describe("renderPlayer", () => {
  it("ドット絵のプレイヤーを描く（単色の四角1回だけではない）", () => {
    const ctx = new FakeContext();
    const player = createPlayer(0, 0);
    const camera = createCamera(400, 225);

    renderPlayer(ctx as unknown as CanvasRenderingContext2D, player, camera);

    expect(ctx.rectCalls.length).toBeGreaterThan(1);
    expect(ctx.pathCalls).toBe(1);
  });

  it("向きが変わっても描画エラーにならない", () => {
    const camera = createCamera(400, 225);
    for (const direction of ["up", "down", "left", "right"] as const) {
      const ctx = new FakeContext();
      const player = { ...createPlayer(5, 5), direction };
      expect(() => renderPlayer(ctx as unknown as CanvasRenderingContext2D, player, camera)).not.toThrow();
    }
  });
});
