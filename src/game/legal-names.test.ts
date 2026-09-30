import { describe, expect, it } from "vitest";

/**
 * 既存作品の固有名詞チェック（CLAUDE.md 1-1、roles.md 3-11）。
 * 会話文だけでなく、ゲームのデータ（モンスター・呪文・特技・アイテム・地名）を書いたソース全体を調べる。
 * 「絶対に入れてはいけない語」の一覧なので、ここに書いた語がほかのファイルに出てきたらテストが落ちる。
 */
const FORBIDDEN = [
  "ドラゴンクエスト", "ドラクエ", "空の軌跡", "英雄伝説", "閃の軌跡", "ファイナルファンタジー", "ゼルダの伝説", "ポケットモンスター", "ポケモン",
  "スライム", "ドラキー", "ゴーレム", "メタルスライム", "はぐれメタル", "ホイミ", "ベホイミ", "ベホマ", "ザオラル", "ザオリク", "メラゾーマ", "ギラ", "イオナズン", "ギガデイン",
  "ルーラ", "リレミト", "キアリー", "バギクロス", "ラリホー", "スカラ", "ルカニ", "バイキルト", "ロトの", "ゾーマ", "ラーミア", "こうもりのつばさ",
];
/** このテスト自身は語の一覧を持つので除く */
const SKIP = ["legal-names.test.ts", "text-lint.test.ts"];

const SOURCES = import.meta.glob("./**/*.ts", { eager: true, query: "?raw", import: "default" }) as Record<string, string>;

describe("既存作品の固有名詞が、ゲームのソースに混ざっていない", () => {
  const files = Object.keys(SOURCES).filter((f) => !SKIP.some((n) => f.endsWith(n)));

  it("調べるソースが十分にある", () => {
    expect(files.length).toBeGreaterThan(100);
  });

  it("禁止語がひとつも出てこない", () => {
    const hits: string[] = [];
    for (const file of files) {
      const text = SOURCES[file];
      for (const word of FORBIDDEN) {
        if (text.includes(word)) {
          hits.push(`${file}: ${word}`);
        }
      }
    }
    expect(hits).toEqual([]);
  });
});
