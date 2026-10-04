import { describe, expect, it } from "vitest";
import { backTitle, confirmTitle, createTitleState, moveTitleCursor, titleItemsFor } from "./title-menu";
import { CREDIT_LINES, HELP_LINES } from "./title-text";

describe("タイトル画面", () => {
  it("セーブがないときは「つづきから」が出ない。あるときは先頭に出る", () => {
    expect(titleItemsFor(false).map((i) => i.id)).toEqual(["new", "help", "keys", "credits"]);
    expect(titleItemsFor(true).map((i) => i.id)).toEqual(["continue", "new", "help", "keys", "credits"]);
  });

  it("カーソルは上下で動き、端でつながる", () => {
    let state = createTitleState(false);
    state = moveTitleCursor(state, -1);
    expect(titleItemsFor(false)[state.cursor].id).toBe("credits");
    state = moveTitleCursor(state, 1);
    expect(titleItemsFor(false)[state.cursor].id).toBe("new");
  });

  it("「はじめから」「つづきから」を決定すると、タイトルが閉じて、その動作が返る", () => {
    const withSave = createTitleState(true);
    const cont = confirmTitle(withSave);
    expect(cont.action).toBe("continue");
    expect(cont.state.open).toBe(false);
    const fresh = confirmTitle(moveTitleCursor(withSave, 1));
    expect(fresh.action).toBe("new");
    expect(fresh.state.open).toBe(false);
  });

  it("あそびかた・クレジットを開いて、決定またはXで、メニューへ戻る", () => {
    const start = createTitleState(false);
    const help = confirmTitle(moveTitleCursor(start, 1)).state;
    expect(help.screen).toBe("help");
    expect(help.open).toBe(true);
    expect(confirmTitle(help).state.screen).toBe("menu");
    const credits = confirmTitle(moveTitleCursor(start, 3)).state;
    expect(credits.screen).toBe("credits");
    expect(backTitle(credits).screen).toBe("menu");
  });

  it("文は、画面（400×？）に収まる行数と長さ", () => {
    for (const lines of [HELP_LINES, CREDIT_LINES]) {
      expect(lines.length).toBeLessThanOrEqual(17);
      for (const line of lines) {
        expect(line.length, line).toBeLessThanOrEqual(40);
      }
    }
  });

  it("クレジットに、使っている素材の表記が入っている（規約: `docs/assets-credits.md`）", () => {
    const text = CREDIT_LINES.join("");
    expect(text).toContain("ぴぽや");
    expect(text).toContain("Frank Wen");
    expect(text).toContain("Michael Cowgill");
    expect(text).toContain("spessasynth");
  });
});
