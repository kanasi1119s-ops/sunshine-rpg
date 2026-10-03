import { describe, expect, it } from "vitest";
import type { PlayerState } from "./player";
import { GAP_CRUMBS, PartyTrail } from "./party-trail";

function at(x: number, y: number, dir: PlayerState["direction"] = "right"): PlayerState {
  return { x, y, width: 12, height: 14, direction: dir, moving: true, animationMs: 0 };
}

describe("隊列（仲間が後ろをついてくる）", () => {
  it("主人公が歩くと、仲間は通った道すじの上を、間をあけてついてくる", () => {
    const trail = new PartyTrail();
    trail.reset(at(0, 0));
    for (let x = 1; x <= 100; x++) trail.update(at(x, 0), 16, 2);
    const a = trail.followerAt(0)!, b = trail.followerAt(1)!;
    expect(a.y).toBe(0);
    expect(100 - a.x).toBeGreaterThanOrEqual(GAP_CRUMBS * 2 - 4);
    expect(a.x - b.x).toBeGreaterThanOrEqual(GAP_CRUMBS * 2 - 4);
    expect(a.dir).toBe("right");
  });

  it("主人公が止まると、仲間は追いついて止まる（動いている間だけ moving）", () => {
    const trail = new PartyTrail();
    trail.reset(at(0, 0));
    for (let x = 1; x <= 100; x++) trail.update(at(x, 0), 16, 1);
    for (let i = 0; i < 200; i++) trail.update(at(100, 0), 16, 1);
    const f = trail.followerAt(0)!;
    expect(f.moving).toBe(false);
    expect(100 - f.x).toBeLessThanOrEqual(GAP_CRUMBS * 2 + 2);
    expect(100 - f.x).toBeGreaterThanOrEqual(GAP_CRUMBS * 2 - 3);
  });

  it("とつぜん遠くへ移ったら（マップ切り替え）、その場にそろう", () => {
    const trail = new PartyTrail();
    trail.reset(at(0, 0));
    for (let x = 1; x <= 60; x++) trail.update(at(x, 0), 16, 1);
    trail.update(at(300, 200), 16, 1);
    const f = trail.followerAt(0)!;
    expect(f.x).toBe(300);
    expect(f.y).toBe(200);
  });

  it("人数が0のときは、仲間はいない", () => {
    const trail = new PartyTrail();
    trail.update(at(5, 5), 16, 0);
    expect(trail.followerAt(0)).toBeNull();
    expect(trail.count).toBe(0);
  });
});
