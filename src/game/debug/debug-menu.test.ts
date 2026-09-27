import { describe, expect, it } from "vitest";
import { createDebugMenuState, moveMenuCursor, toggleMenu } from "./debug-menu";

describe("toggleMenu", () => {
  it("最初は閉じていて、1回呼ぶと開く", () => {
    const state = createDebugMenuState();
    expect(state.open).toBe(false);
    const opened = toggleMenu(state, 5);
    expect(opened.open).toBe(true);
  });

  it("もう一度呼ぶと閉じる", () => {
    let state = toggleMenu(createDebugMenuState(), 5);
    state = toggleMenu(state, 5);
    expect(state.open).toBe(false);
  });

  it("項目数が減っていてもカーソルが範囲外にならない", () => {
    const state = { open: false, cursor: 4 };
    const opened = toggleMenu(state, 2);
    expect(opened.cursor).toBe(1);
  });
});

describe("moveMenuCursor", () => {
  it("閉じているときは動かない", () => {
    const state = createDebugMenuState();
    expect(moveMenuCursor(state, 1, 5)).toEqual(state);
  });

  it("下に動かすとカーソルが進む", () => {
    const state = toggleMenu(createDebugMenuState(), 3);
    const moved = moveMenuCursor(state, 1, 3);
    expect(moved.cursor).toBe(1);
  });

  it("末尾から下に動かすと先頭に戻る", () => {
    let state = toggleMenu(createDebugMenuState(), 3);
    state = moveMenuCursor(state, -1, 3); // 0 -> 2 (wrap)
    expect(state.cursor).toBe(2);
  });
});
