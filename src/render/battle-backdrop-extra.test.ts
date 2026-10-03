import { describe, expect, it } from "vitest";
import { EXTRA_BIOMES, paintExtraBackdrop } from "./battle-backdrop-extra";

const W = 400;
const H = 225;

/** fillRect だけを記録するにせの描画先（ブラウザ以外ではCanvasが無いため）。 */
function fakeCtx(): { ctx: CanvasRenderingContext2D; covered: Uint8Array; calls: () => number } {
  const covered = new Uint8Array(W * H);
  let calls = 0;
  const target: Record<string, unknown> = {
    fillStyle: "#000",
    imageSmoothingEnabled: true,
    fillRect(x: number, y: number, w: number, h: number) {
      calls++;
      for (let yy = Math.max(0, y); yy < Math.min(H, y + h); yy++) {
        for (let xx = Math.max(0, x); xx < Math.min(W, x + w); xx++) {
          covered[yy * W + xx] = 1;
        }
      }
    },
    createRadialGradient() {
      return { addColorStop() {} };
    },
  };
  return { ctx: target as unknown as CanvasRenderingContext2D, covered, calls: () => calls };
}

describe("paintExtraBackdrop", () => {
  for (const kind of EXTRA_BIOMES) {
    it(`${kind} は例外なく描け、400×225のどこも塗り残さない`, () => {
      const { ctx, covered, calls } = fakeCtx();
      expect(() => paintExtraBackdrop(kind, ctx, W, H)).not.toThrow();
      expect(calls()).toBeGreaterThan(1000);
      const missing = covered.reduce((n, v) => n + (v === 0 ? 1 : 0), 0);
      expect(missing).toBe(0);
    });
  }

  it("同じ種類を2回描いても同じ呼び出し回数になる（乱数を使わない）", () => {
    const a = fakeCtx();
    const b = fakeCtx();
    paintExtraBackdrop("forest", a.ctx, W, H);
    paintExtraBackdrop("forest", b.ctx, W, H);
    expect(a.calls()).toBe(b.calls());
  });
});
