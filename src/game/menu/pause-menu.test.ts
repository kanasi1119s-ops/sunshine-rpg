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
    const idx = (id: string): number => PAUSE_ITEMS.findIndex((i) => i.id === id);
    const items = confirmPauseMenu(at(1));
    expect(items.state.screen).toBe("items");
    expect(confirmPauseMenu(items.state).state.screen).toBe("main");
    expect(backPauseMenu(items.state).screen).toBe("main");
    const equip = confirmPauseMenu(at(idx("equip")));
    expect(equip.action).toBe("equip");
    expect(equip.state.open).toBe(true);
    const keys = confirmPauseMenu(at(idx("keys")));
    expect(keys.action).toBe("keys");
    expect(keys.state.open).toBe(true);
    const save = confirmPauseMenu(at(idx("save")));
    expect(save.action).toBe("save");
    expect(save.state.open).toBe(true);
    const title = confirmPauseMenu(at(idx("title")));
    expect(title.action).toBe("title");
    expect(title.state.open).toBe(false);
    const close = confirmPauseMenu(at(idx("close")));
    expect(close.action).toBeNull();
    expect(close.state.open).toBe(false);
  });
});

describe("ならびかえ", () => {
  it("1人目を選び、2人目を選ぶと入れかえる。同じ人を選ぶとやめる。戻るで選びなおし", () => {
    let s = { ...openPauseMenu(), cursor: PAUSE_ITEMS.findIndex((i) => i.id === "order") };
    s = confirmPauseMenu(s).state;
    expect(s.screen).toBe("order");
    s = confirmPauseMenu(s).state;                    // 1人目（0番）
    expect(s.orderPick).toBe(0);
    s = movePauseCursor(s, 1, 4);
    s = movePauseCursor(s, 1, 4);
    const r = confirmPauseMenu(s);                      // 2人目（2番）
    expect(r.action).toBe("swap");
    expect(r.swap).toEqual([0, 2]);
    s = confirmPauseMenu(r.state).state;
    expect(confirmPauseMenu(s).state.orderPick).toBeNull();
    s = backPauseMenu(s);
    expect(s.orderPick).toBeNull();
    expect(s.screen).toBe("order");
    expect(backPauseMenu(s).screen).toBe("main");
  });
});
