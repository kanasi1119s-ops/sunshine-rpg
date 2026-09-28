import { describe, expect, it } from "vitest";
import { hashCell, shadeColor } from "./color-utils";

describe("shadeColor", () => {
  it("正の値で明るくする", () => {
    expect(shadeColor("#808080", 0.5)).toBe("#c0c0c0");
  });

  it("負の値で暗くする", () => {
    expect(shadeColor("#808080", -0.5)).toBe("#404040");
  });

  it("0では変化しない", () => {
    expect(shadeColor("#5a9a4a", 0)).toBe("#5a9a4a");
  });

  it("範囲外にはみ出さない（0〜255にクランプする）", () => {
    expect(shadeColor("#ffffff", 0.5)).toBe("#ffffff");
    expect(shadeColor("#000000", -0.5)).toBe("#000000");
  });

  it("不正な形式はそのまま返す", () => {
    expect(shadeColor("not-a-color", 0.5)).toBe("not-a-color");
  });
});

describe("hashCell", () => {
  it("同じ座標なら常に同じ値を返す（フレームをまたいで模様が変わらない）", () => {
    expect(hashCell(3, 7)).toBe(hashCell(3, 7));
  });

  it("座標が違えば基本的に違う値になる", () => {
    expect(hashCell(0, 0)).not.toBe(hashCell(1, 0));
    expect(hashCell(0, 0)).not.toBe(hashCell(0, 1));
  });

  it("非負の整数を返す", () => {
    const value = hashCell(-5, 12345);
    expect(Number.isInteger(value)).toBe(true);
    expect(value).toBeGreaterThanOrEqual(0);
  });
});
