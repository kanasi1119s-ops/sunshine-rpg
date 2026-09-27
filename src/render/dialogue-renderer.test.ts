import { describe, expect, it } from "vitest";
import { renderDialogue } from "./dialogue-renderer";

class FakeContext {
  fillStyle = "";
  strokeStyle = "";
  font = "";
  textBaseline = "";
  texts: string[] = [];

  fillRect(): void {}
  strokeRect(): void {}
  fillText(text: string): void {
    this.texts.push(text);
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
});
