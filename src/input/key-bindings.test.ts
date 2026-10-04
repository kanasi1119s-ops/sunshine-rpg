import { describe, expect, it } from "vitest";
import {
  actionsForKey,
  DEFAULT_BINDINGS,
  describeBinding,
  isDefaultBindings,
  keyLabel,
  loadBindings,
  rebind,
  resetBindings,
  saveBindings,
} from "./key-bindings";

describe("操作キーの設定", () => {
  it("初期設定は、これまでのキー（矢印・WASD、Enter/Space/Z、X、Tab/Esc）", () => {
    const b = resetBindings();
    expect(isDefaultBindings(b)).toBe(true);
    expect(actionsForKey(b, "w")).toEqual(["up"]);
    expect(actionsForKey(b, "Escape")).toEqual(["menu"]);
    expect(actionsForKey(b, "Enter")).toEqual(["confirm"]);
  });

  it("動作にキーを割り当てると、その動作はそのキーだけになり、元のキーは使えなくなる", () => {
    const b = rebind(resetBindings(), "confirm", "j");
    expect(b.confirm).toEqual(["j"]);
    expect(actionsForKey(b, "Enter")).toEqual([]);
    expect(actionsForKey(b, "J")).toEqual(["confirm"]); // 大文字小文字は区別しない
    expect(isDefaultBindings(b)).toBe(false);
  });

  it("ほかの動作が使っているキーを選ぶと、そちらからはずれる", () => {
    const b = rebind(resetBindings(), "back", "z");
    expect(b.back).toEqual(["z"]);
    expect(b.confirm).toEqual(["Enter", " "]);
  });

  it("もとにもどす", () => {
    expect(isDefaultBindings(resetBindings())).toBe(true);
    const changed = rebind(resetBindings(), "job", "q");
    expect(changed.job).toEqual(["q"]);
    expect(DEFAULT_BINDINGS.job).toEqual(["c"]); // 初期設定そのものは変わらない
  });

  it("保存して、読み込める。こわれた保存は初期設定になる", () => {
    const mem: Record<string, string> = {};
    const storage = { getItem: (k: string) => mem[k] ?? null, setItem: (k: string, v: string) => { mem[k] = v; } };
    saveBindings(storage, rebind(resetBindings(), "menu", "m"));
    expect(loadBindings(storage).menu).toEqual(["m"]);
    mem["sunshine-rpg-key-bindings"] = "{こわれた";
    expect(isDefaultBindings(loadBindings(storage))).toBe(true);
  });

  it("キーの名前をわかりやすく出す", () => {
    expect(keyLabel("ArrowUp")).toBe("↑");
    expect(keyLabel(" ")).toBe("スペース");
    expect(keyLabel("z")).toBe("Z");
    expect(describeBinding(resetBindings(), "up")).toBe("↑ / W");
  });
});
