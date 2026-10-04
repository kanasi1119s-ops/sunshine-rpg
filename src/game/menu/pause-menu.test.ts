import { describe, expect, it } from "vitest";
import { backPauseMenu, confirmPauseMenu, movePauseCursor, openPauseMenu, PAUSE_ITEMS } from "./pause-menu";

describe("ゲーム中のメニュー", () => {
  it("開くと先頭の「つよさ」にカーソルがある。上下でつながって動く", () => {
    let state = openPauseMenu();
    expect(PAUSE_ITEMS[state.cursor].id).toBe("status");
    state = movePauseCursor(state, -1);
    expect(PAUSE_ITEMS[state.cursor].id).toBe("close");
    state = movePauseCursor(state, 1);
    expect(PAUSE_ITEMS[state.cursor].id).toBe("status");
  });

  it("つよさを開いて、決定またはXでメニューへ戻る。メニューでXを押すと閉じる", () => {
    const status = confirmPauseMenu(openPauseMenu()).state;
    expect(status.screen).toBe("status");
    expect(confirmPauseMenu(status).state.screen).toBe("main");
    expect(backPauseMenu(status).screen).toBe("main");
    expect(backPauseMenu(backPauseMenu(status)).open).toBe(false);
  });

  it("「セーブする」は動作を返して開いたまま。「タイトルへ戻る」は動作を返して閉じる。「とじる」は何も返さず閉じる", () => {
    const at = (index: number) => movePauseCursor(openPauseMenu(), index);
    const equip = confirmPauseMenu(at(1));
    expect(equip.action).toBe("equip");
    expect(equip.state.open).toBe(true);
    const save = confirmPauseMenu(at(2));
    expect(save.action).toBe("save");
    expect(save.state.open).toBe(true);
    const title = confirmPauseMenu(at(3));
    expect(title.action).toBe("title");
    expect(title.state.open).toBe(false);
    const close = confirmPauseMenu(at(4));
    expect(close.action).toBeNull();
    expect(close.state.open).toBe(false);
  });
});
