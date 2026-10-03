import { describe, expect, it } from "vitest";
import { renderDialogue } from "./dialogue-renderer";
import { PORTRAIT_PIXEL_WIDTH } from "./portrait-renderer";

class FakeContext {
  fillStyle = "";
  strokeStyle = "";
  font = "";
  textBaseline = "";
  texts: string[] = [];
  textPositions: number[] = [];
  rectCalls: { x: number; y: number; w: number; h: number }[] = [];

  fillRect(x: number, y: number, w: number, h: number): void {
    this.rectCalls.push({ x, y, w, h });
  }
  strokeRect(): void {}
  createLinearGradient(): { addColorStop: () => void } {
    return { addColorStop: () => undefined };
  }
  fillText(text: string, x: number): void {
    this.texts.push(text);
    this.textPositions.push(x);
  }
  measureText(text: string): { width: number } {
    return { width: text.length * 6 };
  }
}

describe("renderDialogue", () => {
  it("話者名とメッセージ本文を描画する", () => {
    const ctx = new FakeContext();
    renderDialogue(
      ctx as unknown as CanvasRenderingContext2D,
      { kind: "message", speaker: "村人（仮）", visibleText: "こんにちは", fullyShown: true },
      400,
      225,
    );
    expect(ctx.texts).toContain("村人（仮）");
    expect(ctx.texts.some((t) => t.includes("こんにちは"))).toBe(true);
    expect(ctx.texts).toContain("▼");
  });

  it("選択中の項目にカーソルを付けて描画する", () => {
    const ctx = new FakeContext();
    renderDialogue(
      ctx as unknown as CanvasRenderingContext2D,
      { kind: "choice", text: "どうする？", labels: ["はい", "いいえ"], selectedIndex: 1 },
      400,
      225,
    );
    expect(ctx.texts).toContain("▶ いいえ");
    expect(ctx.texts).toContain("  はい");
  });

  it("顔グラフィックが登録されている話者は、ドット絵を描いたうえで文字を右にずらす", () => {
    const withPortrait = new FakeContext();
    renderDialogue(
      withPortrait as unknown as CanvasRenderingContext2D,
      { kind: "message", speaker: "ユーリ", visibleText: "こんにちは", fullyShown: false },
      400,
      225,
    );
    const withoutPortrait = new FakeContext();
    renderDialogue(
      withoutPortrait as unknown as CanvasRenderingContext2D,
      { kind: "message", speaker: "村人（仮）", visibleText: "こんにちは", fullyShown: false },
      400,
      225,
    );
    // どちらも背景枠の1回は描くが、顔グラフィックがある方はドットの分だけ多く描く。
    expect(withPortrait.rectCalls.length).toBeGreaterThan(withoutPortrait.rectCalls.length);

    const nameIndexWithPortrait = withPortrait.texts.indexOf("ユーリ");
    const nameIndexWithoutPortrait = withoutPortrait.texts.indexOf("村人（仮）");
    expect(withPortrait.textPositions[nameIndexWithPortrait]).toBe(
      withoutPortrait.textPositions[nameIndexWithoutPortrait] + PORTRAIT_PIXEL_WIDTH + 4,
    );
  });
});
