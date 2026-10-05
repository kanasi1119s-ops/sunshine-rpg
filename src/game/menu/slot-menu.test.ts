import { describe, expect, it } from "vitest";

import { isFileRow as _isFileRow, moveSlotCursor as _move, openSlotMenu as _open } from "./slot-menu";
describe("ファイル行", () => {
  it("いちばん下まで進むとファイル行になり、もう一度で先頭にもどる", () => {
    const rows = [{ id: "slot1", label: "セーブ1", empty: true }] as never;
    let s = _open("save", rows);
    expect(_isFileRow(s)).toBe(false);
    s = _move(s, 1);
    expect(_isFileRow(s)).toBe(true);
    s = _move(s, 1);
    expect(s.cursor).toBe(0);
  });
});
