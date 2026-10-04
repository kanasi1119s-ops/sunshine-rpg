import { describe, expect, it } from "vitest";
import { backFieldUse, confirmFieldUse, moveFieldUse, openFieldUse, refreshFieldUse, type FieldUseOption } from "./field-use";

const item: FieldUseOption = { key: "i1", label: "灯り草", note: "HP20", itemId: "akarigusa" };
const all: FieldUseOption = { key: "s1", label: "慈雨", note: "MP5", casterId: "mina", skill: { id: "x", name: "慈雨", mpCost: 5, powerMultiplier: 1, effect: "healAll", healRatio: 2 } };

describe("field-use", () => {
  it("一覧→対象選び→使う、もどるで一覧へ", () => {
    let s = openFieldUse("items", [item]);
    let r = confirmFieldUse(s);
    expect(r.apply).toBeNull();
    s = moveFieldUse(r.state, 1, 3);
    expect(s.targetCursor).toBe(1);
    r = confirmFieldUse(s);
    expect(r.apply).toEqual({ option: item, targetIndex: 1 });
    expect(backFieldUse(s).stage).toBe("pick");
    expect(backFieldUse(backFieldUse(s)).open).toBe(false);
  });
  it("全員に効く魔法は、対象を選ばずに使う", () => {
    const r = confirmFieldUse(openFieldUse("spells", [all]));
    expect(r.apply).toEqual({ option: all, targetIndex: null });
  });
  it("空のとき・使い切ったとき", () => {
    expect(openFieldUse("items", []).message).toContain("もっていない");
    const s = refreshFieldUse(openFieldUse("items", [item]), [], "なくなった");
    expect(s.options).toHaveLength(0);
    expect(s.stage).toBe("pick");
  });
});
