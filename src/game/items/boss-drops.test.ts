import { describe, expect, it } from "vitest";
import { runTurn } from "../battle/battle-engine";
import type { BattleState, Combatant } from "../battle/types";
import { DUNGEON_ENEMIES } from "../battle/chapter12-enemies";
import { GODS } from "../battle/chapter11-enemies";
import { ALL_ITEMS_BY_ID, shopStock, describeBonus } from "../economy/shop";
import { BOSS_DROP_ITEMS, bossDropFor } from "./boss-drops";
import { candidatesFor } from "./party-equipment";
import { applyTraits } from "./traits";
import { canEquip } from "./weapon-types";

const mk = (id: string, over: Partial<Combatant> = {}): Combatant => ({
  id, name: id, maxHp: 100, hp: 100, maxMp: 20, mp: 5, attack: 10, defense: 5, speed: 5, isEnemy: false, guarding: false, ...over,
});

describe("ボスが落とすかざり", () => {
  const battleIds = [
    "chapter0-yugami", "mugikano-yugami", "garasuko-yugami", "tetsukusari-yugami", "sanone-yugami", "kiri-yugami", "shimohara-yugami", "fushima-yugami",
    "toushin-yugami", "kyotoukyu-yugami", "deep3-yugami", "deep-yugami",
    ...DUNGEON_ENEMIES.map((e) => e.id),
    ...GODS.map((g) => g.id),
    "illusion-boss",
  ];
  it("すべてのボスの戦闘に、特殊効果つきのかざりが1つずつある", () => {
    for (const id of battleIds) {
      const drop = bossDropFor(id);
      expect(drop, `${id} が落とすかざりがない`).toBeDefined();
      const item = ALL_ITEMS_BY_ID[drop!];
      expect(item.category).toBe("accessory");
      expect((item as { traits?: unknown[] }).traits?.length ?? 0).toBeGreaterThan(0);
    }
    expect(BOSS_DROP_ITEMS).toHaveLength(battleIds.length);
    expect(new Set(BOSS_DROP_ITEMS.map((i) => i.name)).size).toBe(BOSS_DROP_ITEMS.length);
  });
  it("雑魚の戦闘は何も落とさない", () => {
    expect(bossDropFor("enc-touri-outskirts-0")).toBeUndefined();
  });
  it("装備すると、戦闘の本人に効果がつく", () => {
    const withTraits = applyTraits(mk("hero"), { accessory: "boss-deep-yugami" }, ALL_ITEMS_BY_ID);
    expect(withTraits.guards).toEqual(["poison", "sleep", "confuse"]);
    expect(withTraits.regenHp).toBeCloseTo(0.04);
    expect(withTraits.luck).toBeGreaterThan(5);
  });
  it("毎ターンの終わりに、HPとMPが回復する", () => {
    const hero = mk("a", { hp: 50, regenHp: 0.1, regenMp: 3 });
    const s: BattleState = { party: [hero], enemies: [mk("e", { isEnemy: true, attack: 1 })], log: [], fled: false };
    const next = runTurn(s, [{ type: "defend", actorId: "a" }], () => 0.5);
    expect(next.party[0].hp).toBeGreaterThanOrEqual(59);
    expect(next.party[0].mp).toBe(8);
  });
  it("状態異常をふせぐ装備なら、毒がかからない", () => {
    const poisoner = mk("e", { isEnemy: true, speed: 9, inflicts: { status: "poison", chance: 1, turns: 3 } });
    const s: BattleState = { party: [mk("a", { guards: ["poison"], defense: 99, maxHp: 999, hp: 999 })], enemies: [poisoner], log: [], fled: false };
    const next = runTurn(s, [{ type: "attack", actorId: "e", targetId: "a" }], () => 0.5);
    expect(next.party[0].poison).toBeUndefined();
  });
});

describe("たて・兜・頭巾", () => {
  it("各段の店に、たて・兜・頭巾が並ぶ", () => {
    for (let t = 1; t <= 9; t++) {
      const ids = shopStock(`tier-${t}`).map((i) => i.id);
      expect(ids).toContain(`shield-${t}`);
      expect(ids).toContain(`helm-${t}`);
      expect(ids).toContain(`hood-${t}`);
    }
  });
  it("たては杖のミナ・弓のコハクは持てず、頭巾はみんな、兜はミナ以外がつけられる", () => {
    const shield = ALL_ITEMS_BY_ID["shield-1"], helm = ALL_ITEMS_BY_ID["helm-1"], hood = ALL_ITEMS_BY_ID["hood-1"];
    expect(["hero", "reto", "orca", "ayame"].every((o) => canEquip(o, shield))).toBe(true);
    expect(canEquip("mina", shield)).toBe(false);
    expect(canEquip("guide", shield)).toBe(false);
    expect(canEquip("mina", helm)).toBe(false);
    expect(["hero", "reto", "mina", "guide", "orca", "ayame"].every((o) => canEquip(o, hood))).toBe(true);
  });
  it("持っていれば、部位ごとに選べる", () => {
    const inv = [{ itemId: "shield-1", quantity: 1 }, { itemId: "hood-1", quantity: 1 }];
    expect(candidatesFor("hero", "shield", {}, inv, ALL_ITEMS_BY_ID).map((c) => c.item.id)).toEqual(["shield-1"]);
    expect(candidatesFor("mina", "head", {}, inv, ALL_ITEMS_BY_ID).map((c) => c.item.id)).toEqual(["hood-1"]);
    expect(describeBonus(ALL_ITEMS_BY_ID["hood-1"] as never)).toContain("ぼうぎょ");
  });
});
