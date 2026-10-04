import { describe, expect, it } from "vitest";
import { backEquipMenu, confirmEquipMenu, moveEquipCursor, openEquipMenu } from "./equip-menu";

const counts = { members: 3, slots: 3, items: 4 };

describe("そうび画面", () => {
  it("誰の → どの部位 → どの品 の順に進み、品で決定すると入れかえる", () => {
    let s = openEquipMenu();
    s = moveEquipCursor(s, 1, counts);
    expect(s.member).toBe(1);
    s = confirmEquipMenu(s).state;
    expect(s.stage).toBe("slot");
    s = moveEquipCursor(s, 2, counts);
    s = confirmEquipMenu(s).state;
    expect(s.stage).toBe("item");
    const done = confirmEquipMenu(moveEquipCursor(s, -1, counts));
    expect(done.apply).toBe(true);
    expect(done.state.stage).toBe("slot");
    expect(done.state.member).toBe(1);
  });

  it("もどるで1段ずつ戻り、最後は閉じる", () => {
    let s = confirmEquipMenu(confirmEquipMenu(openEquipMenu()).state).state;
    expect(s.stage).toBe("item");
    s = backEquipMenu(s);
    expect(s.stage).toBe("slot");
    s = backEquipMenu(s);
    expect(s.stage).toBe("member");
    expect(backEquipMenu(s).open).toBe(false);
  });

  it("カーソルは端でぐるっと回る", () => {
    const s = moveEquipCursor(openEquipMenu(), -1, counts);
    expect(s.member).toBe(2);
  });
});
