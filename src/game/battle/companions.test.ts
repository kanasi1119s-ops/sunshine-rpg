import { describe, expect, it } from "vitest";
import { COMPANIONS, createCompanionCombatant, RETO } from "./companions";

describe("companions", () => {
  it("COMPANIONSにレトが登録されている", () => {
    expect(COMPANIONS[RETO.id]).toBe(RETO);
  });

  it("createCompanionCombatantが現在のステータスを反映したCombatantを作る", () => {
    const stats = RETO.createInitialStats();
    const combatant = createCompanionCombatant(RETO, stats);
    expect(combatant.id).toBe("reto");
    expect(combatant.name).toBe("レト Lv1");
    expect(combatant.maxHp).toBe(stats.maxHp);
    expect(combatant.isEnemy).toBe(false);
  });
});
