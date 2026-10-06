import { describe, expect, it } from "vitest";
import type { EventCommand } from "../event/types";
import { pendingScene, sceneSeenFlag, sceneSleptFlag, sleptFlagsAfterInn, STORY_SCENES, type StoryScene } from "./story-scenes";
import { advanceClockTo, DAY_MS, sceneTimeOf } from "../time-of-day";
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
      // 移動は、さいごに同じ町のユーリの家へ帰るときだけ（「ch0-night-home」。家の中で夕食の場面が流れる）
      const homeWarp = (c: (typeof s.commands)[number], i: number): boolean => c.type === "warp" && c.mapId === "yuri-home" && s.mapId === "touri-town" && i === s.commands.length - 1;
      expect(s.commands.some((c, i) => c.type === "startBattle" || (c.type === "warp" && !homeWarp(c, i))), `${s.id}: 戦闘・移動は入れない`).toBe(false);
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

  it("宿にとまったあとの場面: 条件がそろったあとで同じ町の宿にとまるまでは流れない", () => {
    const scenes: StoryScene[] = [
      { id: "t-morning", mapId: "inn-x-town-1f", requires: ["a"], at: "enter", afterSleep: true, commands: [{ type: "message", text: "朝" }] },
    ];
    expect(pendingScene("inn-x-town-1f", { x: 0, y: 0 }, { a: true }, scenes)).toBeNull();
    expect(sleptFlagsAfterInn("inn-x-town-2f", {}, scenes)).toEqual([]);              // 条件がそろう前にとまっても、しるしはつかない
    expect(sleptFlagsAfterInn("inn-y-town-1f", { a: true }, scenes)).toEqual([]);     // 別の町の宿
    const slept = sleptFlagsAfterInn("inn-x-town-2f", { a: true }, scenes);
    expect(slept).toEqual([sceneSleptFlag("t-morning")]);
    expect(pendingScene("inn-x-town-1f", { x: 0, y: 0 }, { a: true, [slept[0]]: true }, scenes)?.id).toBe("t-morning");
  });

  it("霜原の朝の場面は、宿にとまって目がさめたあとに流れ、女将が話す", () => {
    const s = STORY_SCENES.find((x) => x.id === "ch6-inn-preparations")!;
    expect(s.afterSleep).toBe(true);
    expect(s.mapId.startsWith("inn-shimohara-town")).toBe(true);
    expect(s.commands.some((c) => c.type === "message" && c.speaker === "宿の女将")).toBe(true);
  });

  it("最初の地の文が夕暮れ・夕焼け・夕日・日暮れの場面は、時間帯も夕暮れ（dusk）", () => {
    /** 最初の地の文（話し手のない文）。if・choice の中も、出てくる順にたどる。 */
    const firstNarration = (cmds: readonly EventCommand[]): string | null => {
      for (const c of cmds) {
        if (c.type === "message" && !c.speaker) return c.text;
        const inner: EventCommand[][] =
          c.type === "if" ? [c.then, c.else ?? []] : c.type === "choice" ? c.options.map((o) => o.commands) : [];
        for (const sub of inner) {
          const t = firstNarration(sub);
          if (t !== null) return t;
        }
      }
      return null;
    };
    const duskScenes = STORY_SCENES.filter((s) => /夕暮れ|夕焼け|夕日|日暮れ/.test(firstNarration(s.commands) ?? ""));
    expect(duskScenes.length, "夕暮れではじまる場面が1つも見つからない").toBeGreaterThan(0);
    for (const s of duskScenes) expect(s.time, `${s.id}: 夕暮れの場面なのに時間帯が ${s.time ?? "なし"}`).toBe("dusk");
  });

  it("場面の時間帯: 時計は前へだけ進み、その時間帯になる", () => {
    const noon = DAY_MS * 3 + DAY_MS * 0.25;
    const dusk = advanceClockTo(noon, "dusk");
    expect(sceneTimeOf(dusk)).toBe("dusk");
    expect(dusk).toBeGreaterThan(noon);
    expect(advanceClockTo(dusk, "dusk")).toBe(dusk);                 // もう夕暮れなら、そのまま
    const night = DAY_MS * 3 + DAY_MS * 0.8;
    const nextDusk = advanceClockTo(night, "dusk");                    // 夜のあとの夕暮れは、つぎの日
    expect(sceneTimeOf(nextDusk)).toBe("dusk");
    expect(nextDusk).toBeGreaterThan(night);
    expect(sceneTimeOf(advanceClockTo(night, "morning"))).toBe("morning");
  });
});
