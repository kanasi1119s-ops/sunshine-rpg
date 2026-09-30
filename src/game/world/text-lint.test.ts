import { describe, expect, it } from "vitest";
import { WORLD_NPCS } from "./world";
import { CHAPTER0_OPENING_COMMANDS } from "./chapter0-world";
import { CHAPTER7_OPENING_COMMANDS } from "./chapter7-world";
import { CHAPTER8_OPENING_COMMANDS } from "./chapter8-world";
import { CHAPTER9_OPENING_COMMANDS } from "./chapter9-world";
import type { EventCommand } from "../event/types";

/**
 * 会話文の表記ゆれ・禁止語のチェック（roadmap 7-3）。すべてのNPCの会話・場面つなぎの文を集めて調べる。
 * - 日本語の直後に半角の「!」「?」を置かない（全角の「！」「？」にそろえる）
 * - 「。。」「、、」など、句読点の重なりがない
 * - 既存作品の固有名詞（`CLAUDE.md` 1-1）が混ざっていない
 */
function collectTexts(commands: EventCommand[], out: string[]): void {
  for (const command of commands) {
    switch (command.type) {
      case "message":
        out.push(command.text);
        if (command.speaker) {
          out.push(command.speaker);
        }
        break;
      case "choice":
        out.push(command.text);
        for (const option of command.options) {
          out.push(option.label);
          collectTexts(option.commands, out);
        }
        break;
      case "if":
        collectTexts(command.then, out);
        collectTexts(command.else ?? [], out);
        break;
      default:
        break;
    }
  }
}

const TEXTS: string[] = (() => {
  const out: string[] = [];
  for (const npcs of Object.values(WORLD_NPCS)) {
    for (const npc of npcs) {
      collectTexts(npc.commands, out);
    }
  }
  for (const opening of [CHAPTER0_OPENING_COMMANDS, CHAPTER7_OPENING_COMMANDS, CHAPTER8_OPENING_COMMANDS, CHAPTER9_OPENING_COMMANDS]) {
    collectTexts(opening, out);
  }
  return out;
})();

const FORBIDDEN = ["ドラゴンクエスト", "ドラクエ", "空の軌跡", "英雄伝説", "ファイナルファンタジー", "ゼルダ", "ポケモン", "ホイミ", "メラ", "ベホマ", "ザオラル"];

describe("会話文の表記チェック", () => {
  it("十分な数の文を集めている", () => {
    expect(TEXTS.length).toBeGreaterThan(1500);
  });

  it("日本語の直後に、半角の「!」「?」がない（全角にそろえる）", () => {
    const bad = TEXTS.filter((t) => /[ぁ-んァ-ヶ一-龠ー」）…、。][!?]/.test(t));
    expect(bad.slice(0, 5)).toEqual([]);
  });

  it("句読点の重なり（。。、、）や、行頭・行末の空白がない", () => {
    const bad = TEXTS.filter((t) => /。。|、、|^\s|\s$/.test(t));
    expect(bad.slice(0, 5)).toEqual([]);
  });

  it("既存作品の固有名詞が混ざっていない", () => {
    const bad = TEXTS.filter((t) => FORBIDDEN.some((w) => t.includes(w)));
    expect(bad).toEqual([]);
  });

  it("空の文がない", () => {
    expect(TEXTS.filter((t) => t.trim() === "")).toEqual([]);
  });
});
