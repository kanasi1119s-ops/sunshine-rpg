import { describe, expect, it } from "vitest";
import { addItem, createInventory, getQuantity, removeItem } from "./inventory";

describe("inventory", () => {
  it("最初は何も持っていない", () => {
    expect(getQuantity(createInventory(), "herb")).toBe(0);
  });

  it("addItemで所持数が増える", () => {
    let inventory = createInventory();
    inventory = addItem(inventory, "herb", 2);
    inventory = addItem(inventory, "herb", 1);
    expect(getQuantity(inventory, "herb")).toBe(3);
  });

  it("removeItemで所持数が減り、0になったら一覧から消える", () => {
    let inventory = addItem(createInventory(), "herb", 2);
    inventory = removeItem(inventory, "herb", 2);
    expect(getQuantity(inventory, "herb")).toBe(0);
    expect(inventory).toEqual([]);
  });

  it("所持数が足りないremoveItemは何もしない", () => {
    const inventory = addItem(createInventory(), "herb", 1);
    const result = removeItem(inventory, "herb", 5);
    expect(getQuantity(result, "herb")).toBe(1);
  });
});
