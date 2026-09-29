import { describe, expect, it } from "vitest";
import { AMP_PRESET_NAMES } from "./amp";
import { hasCode, presetToPlugin, validateAmpPlugin } from "./amp-plugins";

describe("アンプの追加のしくみ（アンプ定義ファイル）", () => {
  it("ジャンル別アンプ14種は、すべてアンプ定義の形で書ける", () => {
    for (const name of AMP_PRESET_NAMES) expect(validateAmpPlugin(presetToPlugin(name)).id).toBe(`genre-${name}`);
  });
  it("まちがいは、場所つきでまとめて知らせる", () => {
    const bad = { format: "sunshine-amp", version: 1, id: "Bad Id", label: "", stages: [{ type: "eq", kind: "weird", freq: 5 }, { type: "laser" }] };
    let msg = "";
    try {
      validateAmpPlugin(bad);
    } catch (e) {
      msg = (e as Error).message;
    }
    expect(msg).toMatch(/id は/);
    expect(msg).toMatch(/label/);
    expect(msg).toMatch(/stages\[0\]: kind/);
    expect(msg).toMatch(/stages\[0\]: freq/);
    expect(msg).toMatch(/stages\[1\]: 知らない段/);
    expect(() => validateAmpPlugin({ format: "other" })).toThrow(/アンプ定義ファイル/);
  });
  it("プログラムを含むかが分かる", () => {
    const def = validateAmpPlugin({ format: "sunshine-amp", version: 1, id: "my-amp", label: "自作", stages: [{ type: "worklet", name: "my-proc", code: "registerProcessor('my-proc', class extends AudioWorkletProcessor { process() { return true; } })" }] });
    expect(hasCode(def)).toBe(true);
    expect(hasCode(presetToPlugin("rock"))).toBe(false);
  });
});

describe("見本のアンプ定義ファイル", () => {
  it("assets-src/amp-plugins の見本は、すべて正しい形", () => {
    const files = import.meta.glob("../../assets-src/amp-plugins/*.sunshine-amp.json", { eager: true, import: "default" }) as Record<string, unknown>;
    expect(Object.keys(files).length).toBeGreaterThanOrEqual(2);
    for (const [path, data] of Object.entries(files)) expect(validateAmpPlugin(data).id).toBe(path.split("/").pop()!.replace(".sunshine-amp.json", ""));
  });
});
