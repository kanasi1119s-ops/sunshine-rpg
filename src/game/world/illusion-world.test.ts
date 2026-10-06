import { describe, expect, it } from "vitest";
import { createEventRunner } from "../event/event-runner";
import type { EventCommand, Flags } from "../event/types";
import { collectBattleIds, collectWarpTargets } from "../event/inspect";
import { ILLUSION_MAPS, ILLUSION_NPCS } from "./illusion-world";
import { HIDDEN_PATH } from "../map/illusion/illusion-maps";

/** 会話を流す。choose に、選択肢ごとに選ぶ番号を順に入れる。 */
function run(commands: EventCommand[], flags: Flags, choose: number[] = []): string[] {
  const texts: string[] = [];
  const runner = createEventRunner(commands, flags);
  let r = runner.next();
  while (!r.done && r.step) {
    if (r.step.kind === "message") {
      texts.push(r.step.text);
      r = runner.next({ kind: "advance" });
    } else {
      r = runner.next({ kind: "choose", index: choose.shift() ?? 0 });
    }
  }
  return texts;
}
const npc = (mapId: string, id: string) => ILLUSION_NPCS[mapId].find((n) => n.id === id)!;

describe("幻想の禁域「まぼろしの回廊」", () => {
  it("1階: 詩のとおり（西=赤・まん中=青・東=緑）に柱の色を合わせると、扉が開く", () => {
    const flags: Flags = {};
    expect(run(npc("illusion-1", "illusion1-gate").commands, flags).join("")).toContain("そろっていない");
    run(npc("illusion-1", "illusion-pedestal-1").commands, flags, [0]);
    run(npc("illusion-1", "illusion-pedestal-2").commands, flags, [2]);
    run(npc("illusion-1", "illusion-pedestal-3").commands, flags, [2]);
    expect(flags.illusion1_open).toBeUndefined();
    run(npc("illusion-1", "illusion-pedestal-2").commands, flags, [1]);
    run(npc("illusion-1", "illusion1-gate").commands, flags);
    expect(flags.illusion1_open).toBe(true);
  });

  it("2階: 見えない道は、南の島から北の島までつながっていて、歩ける", () => {
    const m = ILLUSION_MAPS["illusion-2"];
    const walk = (x: number, y: number) => x >= 0 && y >= 0 && x < m.width && y < m.height && m.collision![y * m.width + x] !== 1;
    const seen = new Set<string>();
    const q: [number, number][] = [[10, 12]];
    while (q.length) {
      const [x, y] = q.shift()!;
      const k = `${x},${y}`;
      if (seen.has(k) || !walk(x, y)) continue;
      seen.add(k);
      for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) q.push([x + dx, y + dy]);
    }
    expect(seen.has("10,3")).toBe(true);
    for (const [x, y] of HIDDEN_PATH) expect(m.layers[0].data[y * m.width + x]).toBe(7);
  });

  it("3階: 問いに正しく答えると扉を通れ、まちがえると、まぼろしの影と戦う", () => {
    const door = npc("illusion-3", "illusion-door-1").commands;
    expect(collectBattleIds(door)).toEqual(new Set(["illusion-phantom"]));
    const flags: Flags = {};
    run(door, flags, [0]);
    expect(flags.illusion_q1_ok).toBeUndefined();
    run(door, flags, [1]);
    expect(flags.illusion_q1_ok).toBe(true);
    expect(collectWarpTargets(door)).toEqual(new Set(["illusion-3"]));
    // 2つ目の扉は、1つ目に答えるまで問いかけない
    expect(run(npc("illusion-3", "illusion-door-2").commands, {}).join("")).toContain("まだ");
  });

  it("入口は、初源の歪みを倒したあとに現れる", () => {
    const entrance = ILLUSION_NPCS["kyotoukyu-court"][0];
    expect(entrance.showWhenFlag).toBe("deep_yugami_defeated");
    expect(collectWarpTargets(entrance.commands)).toEqual(new Set(["illusion-1"]));
  });
});
