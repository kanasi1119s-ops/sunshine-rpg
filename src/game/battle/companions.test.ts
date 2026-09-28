import { describe, expect, it } from "vitest";
import { COMPANIONS, createCompanionCombatant, MINA, RETO } from "./companions";

describe("companions", () => {
  it("COMPANIONSにレトとミナが登録されている", () => {
    expect(COMPANIONS[RETO.id]).toBe(RETO);
    expect(COMPANIONS[MINA.id]).toBe(MINA);
  });

  it("createCompanionCombatantが現在のステータスを反映したCombatantを作る", () => {
    const stats = RETO.createInitialStats();
    const combatant = createCompanionCombatant(RETO, stats);
    expect(combatant.id).toBe("reto");
    expect(combatant.name).toBe("レト Lv1");
    expect(combatant.maxHp).toBe(stats.maxHp);
    expect(combatant.isEnemy).toBe(false);
  });

  it("ミナは水紋系の固有のとくぎを持つ", () => {
    expect(MINA.skill.name).toBe("水紋ノ波");
    const combatant = createCompanionCombatant(MINA, MINA.createInitialStats());
    expect(combatant.id).toBe("mina");
    expect(combatant.name).toBe("ミナ Lv1");
  });
});
