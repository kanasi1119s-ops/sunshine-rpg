import { describe, expect, it } from "vitest";
import { BattleController, COMMANDS } from "./battle-controller";
import type { Combatant } from "./types";

function makeCombatant(overrides: Partial<Combatant> & { id: string }): Combatant {
  return {
    name: overrides.id,
    maxHp: 30,
    hp: 30,
    maxMp: 10,
    mp: 10,
    attack: 20,
    defense: 0,
    speed: 10,
    isEnemy: false,
    guarding: false,
    ...overrides,
  };
}

const testSkill = { id: "test-skill", name: "とくぎ（テスト）", mpCost: 3, powerMultiplier: 1.5 };
const item = { id: "herb", name: "やくそう", healAmount: 20 };
/** テストで使う味方ID（hero / a / b）はすべて同じとくぎを持つことにする。 */
const skills = { hero: testSkill, a: testSkill, b: testSkill };

describe("BattleController", () => {
  it("最初はパーティ1人目のコマンド選択から始まる", () => {
    const controller = new BattleController(
      [makeCombatant({ id: "hero" })],
      [makeCombatant({ id: "slime", isEnemy: true, hp: 1000, speed: 1 })],
      () => 0.5,
      { skills, item },
    );
    expect(controller.getUiState()).toEqual({ kind: "command", actorId: "hero", cursor: 0 });
  });

  it("attackを選ぶと対象選択に移り、確定するとメッセージが出る", () => {
    const controller = new BattleController(
      [makeCombatant({ id: "hero" })],
      [makeCombatant({ id: "slime", isEnemy: true, hp: 1000, speed: 1 })],
      () => 0.5,
      { skills, item },
    );

    expect(COMMANDS[0].kind).toBe("attack");
    controller.confirm(); // attackを選択
    expect(controller.getUiState()).toMatchObject({ kind: "target", commandKind: "attack" });

    controller.confirm(); // 対象（slime）を確定
    expect(controller.getUiState().kind).toBe("message");
  });

  it("defendとfleeは対象選択なしで即座に次の人へ進む", () => {
    const controller = new BattleController(
      [makeCombatant({ id: "a" }), makeCombatant({ id: "b" })],
      [makeCombatant({ id: "slime", isEnemy: true, hp: 1000, speed: 1 })],
      () => 0.5,
      { skills, item },
    );

    const defendIndex = COMMANDS.findIndex((c) => c.kind === "defend");
    controller.moveCursor(defendIndex); // aのコマンドをdefendに合わせる
    controller.confirm();

    expect(controller.getUiState()).toEqual({ kind: "command", actorId: "b", cursor: 0 });
  });

  it("敵を倒すと最終的にfinished(won)になる", () => {
    const controller = new BattleController(
      [makeCombatant({ id: "hero", attack: 999, speed: 100 })],
      [makeCombatant({ id: "slime", isEnemy: true, hp: 1, defense: 0, speed: 1 })],
      () => 0.5,
      { skills, item },
    );

    controller.confirm(); // attack
    controller.confirm(); // target slime

    // メッセージを最後まで送る。
    let guard = 0;
    while (controller.getUiState().kind === "message" && guard < 20) {
      controller.confirm();
      guard++;
    }

    expect(controller.getUiState().kind).toBe("finished");
    expect(controller.getUiState()).toMatchObject({ outcome: "won" });
  });

  it("味方が全滅するとfinished(lost)になる", () => {
    const controller = new BattleController(
      [makeCombatant({ id: "hero", hp: 1, defense: 0, speed: 1 })],
      [makeCombatant({ id: "slime", isEnemy: true, attack: 999, speed: 100 })],
      () => 0.5,
      { skills, item },
    );

    const defendIndex = COMMANDS.findIndex((c) => c.kind === "defend");
    controller.moveCursor(defendIndex);
    controller.confirm(); // defend（enemyのAI攻撃で倒れるはず）

    let guard = 0;
    while (controller.getUiState().kind === "message" && guard < 20) {
      controller.confirm();
      guard++;
    }

    expect(controller.getUiState()).toMatchObject({ kind: "finished", outcome: "lost" });
  });

  it("味方ごとに別のとくぎを使える（複数人パーティ対応）", () => {
    const skillA = { id: "skill-a", name: "とくぎA", mpCost: 3, powerMultiplier: 2 };
    const skillB = { id: "skill-b", name: "とくぎB", mpCost: 3, powerMultiplier: 5 };
    const controller = new BattleController(
      [makeCombatant({ id: "a" }), makeCombatant({ id: "b" })],
      [makeCombatant({ id: "slime", isEnemy: true, hp: 1000, defense: 0, speed: 1 })],
      () => 0.5,
      { skills: { a: skillA, b: skillB }, item },
    );

    const skillIndex = COMMANDS.findIndex((c) => c.kind === "skill");

    // aのとくぎ（威力2倍）を選択→対象確定
    controller.moveCursor(skillIndex);
    controller.confirm();
    controller.confirm();
    // bのとくぎ（威力5倍）を選択→対象確定（ここでラウンドが解決される）
    controller.moveCursor(skillIndex);
    controller.confirm();
    controller.confirm();

    const messages: string[] = [];
    let guard = 0;
    while (controller.getUiState().kind === "message" && guard < 10) {
      const state = controller.getUiState();
      if (state.kind === "message") {
        messages.push(state.text);
      }
      controller.confirm();
      guard++;
    }

    expect(messages.some((m) => m.includes("とくぎA"))).toBe(true);
    expect(messages.some((m) => m.includes("とくぎB"))).toBe(true);
  });
  it("ジョブの特技があると、とくぎで一覧が出て、選んだ特技が使われる", () => {
    const jobSkill = { id: "job:x", name: "踏み込み斬り", mpCost: 2, powerMultiplier: 2 };
    const controller = new BattleController(
      [makeCombatant({ id: "hero" })],
      [makeCombatant({ id: "slime", isEnemy: true, hp: 1000, speed: 1 })],
      () => 0.5,
      { skills, item, extraSkills: { hero: [jobSkill] } },
    );
    controller.moveCursor(1);
    controller.confirm();
    const list = controller.getUiState();
    expect(list.kind).toBe("skillList");
    if (list.kind !== "skillList") return;
    expect(list.skills.map((x) => x.name)).toEqual(["とくぎ（テスト）", "踏み込み斬り"]);
    controller.moveCursor(1);
    controller.confirm();
    controller.confirm();
    let text = "";
    for (let i = 0; i < 6; i++) {
      const ui = controller.getUiState();
      if (ui.kind === "message") text += ui.text;
      controller.confirm();
    }
    expect(text).toContain("踏み込み斬り");
  });

  it("ジョブの特技がなければ、従来どおりすぐ対象選択になる", () => {
    const controller = new BattleController(
      [makeCombatant({ id: "hero" })],
      [makeCombatant({ id: "slime", isEnemy: true, hp: 1000, speed: 1 })],
      () => 0.5,
      { skills, item, extraSkills: { hero: [] } },
    );
    controller.moveCursor(1);
    controller.confirm();
    expect(controller.getUiState().kind).toBe("target");
  });
});

describe("BattleController: もどる（cancel）", () => {
  const enemy = () => makeCombatant({ id: "slime", isEnemy: true, hp: 1000, speed: 1 });

  it("対象選択でもどるとコマンド選択に戻る", () => {
    const c = new BattleController([makeCombatant({ id: "hero" })], [enemy()], () => 0.5, { skills, item });
    c.confirm();
    expect(c.getUiState().kind).toBe("target");
    c.cancel();
    expect(c.getUiState()).toEqual({ kind: "command", actorId: "hero", cursor: 0 });
  });

  it("2人目のコマンドでもどると、1人目の行動を取り消して選び直せる", () => {
    const c = new BattleController([makeCombatant({ id: "hero" }), makeCombatant({ id: "a" })], [enemy()], () => 0.5, { skills, item });
    c.confirm(); // heroがたたかう
    c.confirm(); // 対象
    expect(c.getUiState()).toEqual({ kind: "command", actorId: "a", cursor: 0 });
    c.cancel();
    expect(c.getUiState()).toEqual({ kind: "command", actorId: "hero", cursor: 0 });
    // もう一度選べて、最後まで進める
    c.confirm();
    c.confirm();
    c.confirm();
    c.confirm();
    expect(c.getUiState().kind).toBe("message");
  });

  it("最初のコマンドでは、もどっても何も起きない", () => {
    const c = new BattleController([makeCombatant({ id: "hero" })], [enemy()], () => 0.5, { skills, item });
    c.cancel();
    expect(c.getUiState()).toEqual({ kind: "command", actorId: "hero", cursor: 0 });
  });
});

describe("オートモード", () => {
  it("autoCommand で、全員ぶんのコマンドが自動で決まりターンが進む", () => {
    const c = new BattleController(
      [makeCombatant({ id: "hero" }), makeCombatant({ id: "a" })],
      [makeCombatant({ id: "slime", isEnemy: true, hp: 1000, speed: 1 })],
      () => 0.9,
      { skills, item },
    );
    c.autoCommand();
    expect(c.getUiState()).toMatchObject({ kind: "command", actorId: "a" });
    c.autoCommand();
    expect(c.getUiState().kind).toBe("message");
  });
  it("コマンド選択以外では何もしない", () => {
    const c = new BattleController(
      [makeCombatant({ id: "hero" })],
      [makeCombatant({ id: "slime", isEnemy: true, hp: 1000, speed: 1 })],
      () => 0.9,
      { skills, item },
    );
    c.autoCommand();
    const before = c.getUiState();
    c.autoCommand();
    expect(c.getUiState()).toEqual(before);
  });
});
