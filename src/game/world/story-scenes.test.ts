import { describe, expect, it } from "vitest";
import type { EventCommand } from "../event/types";
import { pendingScene, sceneSeenFlag, STORY_SCENES, type StoryScene } from "./story-scenes";
import { WORLD_MAPS, WORLD_NPCS } from "./world";

/** ゲームの中で、どこかで立てられるフラグ（NPCの会話・場面の setFlag）。 */
function collectSetFlags(): Set<string> {
  const out = new Set<string>();
  const walk = (cmds: EventCommand[]): void => {
    for (const c of cmds) {
      if (c.type === "setFlag") out.add(c.flag);
      if (c.type === "if") {
        walk(c.then);
        if (c.else) walk(c.else);
      }
      if (c.type === "choice") for (const o of c.options) walk(o.commands);
    }
  };
  for (const npcs of Object.values(WORLD_NPCS)) for (const n of npcs) walk(n.commands);
  for (const s of STORY_SCENES) walk(s.commands);
  return out;
}
/** main.ts などのコードの側で立つフラグ（勝利・章のはじまり・乗り物・場面）。 */
const CODE_FLAG = /^(chapter\d+_intro_seen|.*_defeated|scene_.*_seen|has_ship|has_airship|vortex_route_open|tower_gate_open)$/;

function messages(cmds: EventCommand[]): string[] {
  const out: string[] = [];
  for (const c of cmds) {
    if (c.type === "message") out.push(c.text);
    if (c.type === "if") out.push(...messages(c.then), ...messages(c.else ?? []));
    if (c.type === "choice") for (const o of c.options) out.push(...messages(o.commands));
  }
  return out;
}
function setFlagsIn(cmds: EventCommand[]): string[] {
  const out: string[] = [];
  for (const c of cmds) {
    if (c.type === "setFlag") out.push(c.flag);
    if (c.type === "if") out.push(...setFlagsIn(c.then), ...setFlagsIn(c.else ?? []));
    if (c.type === "choice") for (const o of c.options) out.push(...setFlagsIn(o.commands));
  }
  return out;
}

describe("小説の場面（story-scenes）", () => {
  const known = collectSetFlags();

  it("場面の名前は重ならない", () => {
    const ids = STORY_SCENES.map((s) => s.id);
    expect(new Set(ids).size).toBe(ids.length);
  });

  it("地図は実在し、範囲は地図の中で、歩ける所をふくむ", () => {
    for (const s of STORY_SCENES) {
      const m = WORLD_MAPS[s.mapId];
      expect(m, `${s.id}: 地図 ${s.mapId}`).toBeDefined();
      if (s.at === "enter") continue;
      const a = s.at;
      expect(a.x0 >= 0 && a.y0 >= 0 && a.x1 < m.width && a.y1 < m.height && a.x0 <= a.x1 && a.y0 <= a.y1, `${s.id}: 範囲`).toBe(true);
      let open = false;
      for (let y = a.y0; y <= a.y1; y++) for (let x = a.x0; x <= a.x1; x++) if (!m.collision || m.collision[y * m.width + x] === 0) open = true;
      expect(open, `${s.id}: 範囲に歩ける所が無い`).toBe(true);
    }
  });

  it("条件のフラグは、ゲームのどこかで本当に立つものだけ", () => {
    for (const s of STORY_SCENES) {
      for (const f of [...(s.requires ?? []), ...(s.blockedBy ?? [])]) {
        expect(known.has(f) || CODE_FLAG.test(f), `${s.id}: 立つことの無いフラグ ${f}`).toBe(true);
      }
    }
  });

  it("場面は章の進み（依頼・報告・仲間）を変えない（立てるのは scene_・novel_ のフラグだけ）", () => {
    for (const s of STORY_SCENES) {
      for (const f of setFlagsIn(s.commands)) expect(/^(scene_|novel_)/.test(f), `${s.id}: ${f}`).toBe(true);
      expect(s.commands.some((c) => c.type === "startBattle" || c.type === "warp"), `${s.id}: 戦闘・移動は入れない`).toBe(false);
    }
  });

  it("文は空でなく、会話欄に収まる長さ（110字まで）", () => {
    for (const s of STORY_SCENES) {
      const ms = messages(s.commands);
      expect(ms.length, `${s.id}: 会話が無い`).toBeGreaterThan(0);
      for (const t of ms) {
        expect(t.trim().length, `${s.id}: 空の文`).toBeGreaterThan(0);
        expect(t.length, `${s.id}: 長すぎる「${t.slice(0, 20)}…」`).toBeLessThanOrEqual(110);
      }
    }
  });

  it("pendingScene: 条件がそろったときだけ、まだ見ていない場面を返す", () => {
    const scenes: StoryScene[] = [
      { id: "t-enter", mapId: "m", requires: ["a"], blockedBy: ["z"], at: "enter", commands: [{ type: "message", text: "x" }] },
      { id: "t-area", mapId: "m", at: { x0: 2, y0: 2, x1: 3, y1: 3 }, commands: [{ type: "message", text: "y" }] },
    ];
    expect(pendingScene("m", { x: 0, y: 0 }, {}, scenes)).toBeNull();
    expect(pendingScene("m", { x: 0, y: 0 }, { a: true }, scenes)?.id).toBe("t-enter");
    expect(pendingScene("m", { x: 0, y: 0 }, { a: true, z: true }, scenes)).toBeNull();
    expect(pendingScene("m", { x: 2, y: 3 }, { [sceneSeenFlag("t-enter")]: true }, scenes)?.id).toBe("t-area");
    expect(pendingScene("other", { x: 2, y: 3 }, {}, scenes)).toBeNull();
  });
});
