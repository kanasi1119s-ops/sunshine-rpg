import { describe, expect, it } from "vitest";
import { cycleDifficulty, loadDifficulty, saveDifficulty } from "./difficulty";

describe("difficulty", () => {
  it("切りかえて、保存・読みこみができる。わからない値はイージー", () => {
    expect(cycleDifficulty("easy", 1)).toBe("normal");
    expect(cycleDifficulty("normal", 1)).toBe("easy");
    const store: Record<string, string> = {};
    const storage = { getItem: (k: string) => store[k] ?? null, setItem: (k: string, v: string) => { store[k] = v; } };
    expect(loadDifficulty(storage)).toBe("easy");
    saveDifficulty(storage, "normal");
    expect(loadDifficulty(storage)).toBe("normal");
    store["sunshine-rpg-difficulty"] = "hard";
    expect(loadDifficulty(storage)).toBe("easy");
  });
});
