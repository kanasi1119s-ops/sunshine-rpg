import { describe, expect, it } from "vitest";
import { SIDE_STORIES, SIDE_STORY_NPCS } from "../world/side-stories";
import { SIDE_REWARD_ITEMS, sideRewardFor } from "./side-rewards";
import { ALL_ITEMS_BY_ID } from "../economy/shop";

describe("サブストーリーのごほうびの装備", () => {
  it("どのサブストーリーにも、そこだけの装備が1つずつある（名前も重ならない）", () => {
    for (const s of SIDE_STORIES) expect(sideRewardFor(s.key), `${s.id} ${s.title}`).toBeDefined();
    expect(SIDE_REWARD_ITEMS).toHaveLength(SIDE_STORIES.length);
    const names = Object.values(ALL_ITEMS_BY_ID).map((i) => i.name);
    for (const item of SIDE_REWARD_ITEMS) {
      expect(names.filter((n) => n === item.name), item.name).toHaveLength(1);
      expect(item.price).toBe(0);
      expect(item.traits?.length ?? 0, `${item.name} に特殊効果がない`).toBeGreaterThan(0);
    }
  });
  it("報告すると、その装備をもらう（依頼人の会話に、装備をわたす命令が入っている）", () => {
    const all = JSON.stringify(SIDE_STORY_NPCS);
    for (const s of SIDE_STORIES) expect(all.includes(`"giveEquipment","itemId":"side-${s.key}"`), s.id).toBe(true);
  });
});

import { storyNote } from "../world/side-story";

describe("ごほうびの文", () => {
  it("品物の説明（〜をもらった）はのぞき、絆・手帳の記録は残す", () => {
    expect(storyNote("麦の穂の飾りをもらった。")).toBe("");
    expect(storyNote("ミナとの絆が深まった。")).toBe("ミナとの絆が深まった。");
    expect(storyNote("灯貨をもらった。（手帳に「静滅教団」の名が記録された）")).toBe("（手帳に「静滅教団」の名が記録された）");
  });
});
