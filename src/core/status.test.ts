import { describe, expect, it } from "vitest";
import { GAME_TITLE, getStatusMessage } from "./status";

describe("status", () => {
  it("タイトルが空でないこと", () => {
    expect(GAME_TITLE.length).toBeGreaterThan(0);
  });

  it("状態メッセージに「準備」という語が含まれること", () => {
    expect(getStatusMessage()).toContain("準備");
  });
});
