import { describe, expect, it } from "vitest";
import { confirmControlsMenu, CONTROLS_ROW_COUNT, finishCapture, moveControlsCursor, openControlsMenu } from "./controls-menu";

describe("そうさ設定の画面", () => {
  it("動作を選んで決定すると、新しいキーを待つ。待っている間はカーソルが動かない", () => {
    let s = openControlsMenu();
    s = moveControlsCursor(s, 4); // 決定・調べる
    const r = confirmControlsMenu(s);
    expect(r.choice).toEqual({ kind: "capture", action: "confirm" });
    expect(r.state.capturing).toBe(true);
    expect(moveControlsCursor(r.state, 1).cursor).toBe(s.cursor);
    expect(finishCapture(r.state, "決定を Jに した").capturing).toBe(false);
  });

  it("「もとにもどす」と「とじる」", () => {
    let s = openControlsMenu();
    s = moveControlsCursor(s, -2); // いちばん下から2番目 = もとにもどす
    expect(s.cursor).toBe(CONTROLS_ROW_COUNT - 2);
    expect(confirmControlsMenu(s).choice).toEqual({ kind: "reset" });
    s = moveControlsCursor(s, 1);
    const closed = confirmControlsMenu(s);
    expect(closed.choice).toEqual({ kind: "close" });
    expect(closed.state.open).toBe(false);
  });
});
