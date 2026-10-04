import { describe, expect, it } from "vitest";
import { BattleController, COMMANDS } from "./battle-controller";
import type { Combatant } from "./types";

const c = (o: Partial<Combatant> & { id: string }): Combatant => ({ name: o.id, maxHp: 30, hp: 30, maxMp: 10, mp: 10, attack: 5, defense: 0, speed: 10, isEnemy: false, guarding: false, ...o });
const skill = { id: "s", name: "とくぎ", mpCost: 1, powerMultiplier: 1 };
const herb = { id: "herb", name: "灯り草", healAmount: 20 };
const dew = { id: "dew", name: "露の雫", healAmount: 0, mpAmount: 5 };
const itemIndex = COMMANDS.findIndex((x) => x.kind === "item");

function start(items: { item: typeof herb; quantity: number }[]) {
  return new BattleController([c({ id: "hero", hp: 5, mp: 2 })], [c({ id: "slime", isEnemy: true, hp: 1000, speed: 1, attack: 0 })], () => 0.5, { skills: { hero: skill }, items });
}
function pickItem(ctl: BattleController): void {
  ctl.moveCursor(itemIndex);
  ctl.confirm();
}

describe("戦闘の回復アイテム", () => {
  it("どうぐ→一覧→対象→使うと、数が減って回復する（HPもMPも）", () => {
    const ctl = start([{ item: herb, quantity: 2 }, { item: dew, quantity: 1 }]);
    pickItem(ctl);
    expect(ctl.getUiState().kind).toBe("itemList");
    ctl.confirm();                                      // 灯り草
    expect(ctl.getUiState().kind).toBe("target");
    ctl.confirm();                                      // ユーリに
    expect(ctl.getItemUsage()).toEqual({ herb: 1 });
    expect(ctl.getState().party[0].hp).toBeGreaterThanOrEqual(24);
  });
  it("MPを回復する雫", () => {
    const ctl = start([{ item: dew, quantity: 1 }]);
    pickItem(ctl);
    ctl.confirm();
    ctl.confirm();
    expect(ctl.getState().party[0].mp).toBe(7);
    expect(ctl.getState().log.join("\n")).toContain("MPが 5 回復した");
  });
  it("持っていないときは選べない。もどると、使った数は取り消される", () => {
    const none = start([]);
    expect(none.hasUsableItems()).toBe(false);
    pickItem(none);
    expect(none.getUiState().kind).toBe("command");
    const ctl = start([{ item: herb, quantity: 1 }]);
    pickItem(ctl);
    ctl.confirm();
    ctl.cancel();                                       // 対象選び→一覧
    expect(ctl.getUiState().kind).toBe("itemList");
    expect(ctl.getItemUsage()).toEqual({});
  });
});
