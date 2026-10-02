import { describe, expect, it } from "vitest";
import { GROUPS, activeRmsDb, dryChain, gainForTarget, groupOf, mixPlan } from "./mix-plan";
import { GM_DRUM_NOTE, GM_PROGRAM } from "./gm-map";

describe("パート別ミックスの設計", () => {
  it("すべての楽器の音色が、どれかのパートに振り分けられる", () => {
    const names = new Set<string>([...Object.keys(GM_PROGRAM), ...Object.keys(GM_DRUM_NOTE), "distGuitar", "leadGuitar", "sub808", "slap", "sfxDown"]);
    for (const n of names) expect(GROUPS, n).toContain(groupOf(n));
    expect(groupOf("kick")).toBe("drums");
    expect(groupOf("distGuitar")).toBe("gtrRhythm");
    expect(groupOf("leadGuitar")).toBe("gtrLead");
    expect(groupOf("shamisen")).toBe("ethnic");
    expect(groupOf(undefined)).toBe("lead");
  });

  it("全パートに設計がある。数値が正常（低域<高域・音量の目標・残響0〜1）", () => {
    for (const style of [undefined, "metal", "classic", "electro", "phonk", "space"]) {
      const plan = mixPlan(style, ["loud", "orchestra", "wagakki"]);
      for (const g of GROUPS) {
        const m = plan[g];
        expect(m.hp).toBeLessThan(m.lp);
        expect(m.target).toBeLessThan(-10);
        expect(m.target).toBeGreaterThan(-45);
        expect(m.reverb).toBeGreaterThanOrEqual(0);
        expect(m.reverb).toBeLessThanOrEqual(1);
        expect(dryChain(m)).not.toMatch(/NaN|undefined|Infinity/);
      }
    }
  });

  it("曲調ごとの補正: メタルはギターが前、クラシックは弦が前、フォンクはベースが前（基準より）", () => {
    const base = mixPlan(undefined);
    expect(mixPlan("metal").gtrRhythm.target).toBeGreaterThan(base.gtrRhythm.target);
    expect(mixPlan("classic").orch.target).toBeGreaterThan(base.orch.target);
    expect(mixPlan("phonk").bass.target).toBeGreaterThan(base.bass.target);
    expect(mixPlan("rock", ["orchestra"]).orch.target).toBeGreaterThan(mixPlan("rock").orch.target);
  });

  it("設計の呼び出しが、元の表を書きかえない", () => {
    const a = mixPlan("metal");
    a.drums.target = 0;
    a.drums.eq[0].g = 99;
    expect(mixPlan("metal").drums.target).not.toBe(0);
    expect(mixPlan("metal").drums.eq[0].g).not.toBe(99);
  });

  it("音量の合わせ方: 目標に合わせる倍率（±18dBに制限）。鳴っていないパートは null", () => {
    expect(gainForTarget(-30, -24)).toBe(6);
    expect(gainForTarget(-60, -24)).toBe(18);
    expect(gainForTarget(-5, -30)).toBe(-18);
    expect(gainForTarget(null, -24)).toBeNull();
  });

  it("鳴っている間だけのRMSを測る（無音の窓は数えない）", () => {
    const sr = 1000;
    const l = new Float32Array(sr * 4);
    const r = new Float32Array(sr * 4);
    for (let i = 0; i < sr * 2; i++) {
      l[i] = 0.1;
      r[i] = 0.1;
    }
    expect(activeRmsDb(l, r, sr)).toBeCloseTo(-20, 1);
    expect(activeRmsDb(new Float32Array(sr), new Float32Array(sr), sr)).toBeNull();
  });
});
