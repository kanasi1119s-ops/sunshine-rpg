import { describe, expect, it } from "vitest";
import type { PlayerState } from "./player";
import { CRUMB_SPACING, GAP_CRUMBS, PartyTrail } from "./party-trail";

function at(x: number, y: number, dir: PlayerState["direction"] = "right"): PlayerState {
  return { x, y, width: 12, height: 14, direction: dir, moving: true, animationMs: 0 };
}

const GAP_PX = GAP_CRUMBS * CRUMB_SPACING;

describe("隊列（仲間が後ろをついてくる）", () => {
  it("主人公が歩くと、仲間は通った道すじの上を、間をあけてついてくる", () => {
    const trail = new PartyTrail();
    trail.reset(at(0, 0));
    for (let x = 1; x <= 100; x++) trail.update(at(x, 0), 16, 2);
    const a = trail.followerAt(0)!, b = trail.followerAt(1)!;
    expect(a.y).toBe(0);
    expect(100 - a.x).toBeGreaterThanOrEqual(GAP_PX - 4);
    expect(a.x - b.x).toBeGreaterThanOrEqual(GAP_PX - 4);
    expect(a.dir).toBe("right");
  });

  it("主人公が止まると、仲間は追いついて止まる（動いている間だけ moving）", () => {
    const trail = new PartyTrail();
    trail.reset(at(0, 0));
    for (let x = 1; x <= 100; x++) trail.update(at(x, 0), 16, 1);
    for (let i = 0; i < 200; i++) trail.update(at(100, 0), 16, 1);
    const f = trail.followerAt(0)!;
    expect(f.moving).toBe(false);
    expect(100 - f.x).toBeLessThanOrEqual(GAP_PX + 2);
    expect(100 - f.x).toBeGreaterThanOrEqual(GAP_PX - 3);
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

  it("歩いている間は、仲間の歩く絵が止まったり動いたりをくり返さない（ブレない）", () => {
    const trail = new PartyTrail();
    trail.reset(at(0, 0));
    for (let x = 1; x <= 80; x++) trail.update(at(x, 0), 16, 2);
    let flicker = 0;
    let lastX = trail.followerAt(0)!.x;
    for (let x = 81; x <= 200; x++) {
      trail.update(at(x, 0), 16, 2);
      const f = trail.followerAt(0)!;
      if (!f.moving) flicker++;
      // 毎フレーム、1〜2ドットずつなめらかに進む
      expect(f.x - lastX).toBeLessThanOrEqual(2.5);
      lastX = f.x;
    }
    expect(flicker).toBe(0);
  });

  it("人数が0のときは、仲間はいない", () => {
    const trail = new PartyTrail();
    trail.update(at(5, 5), 16, 0);
    expect(trail.followerAt(0)).toBeNull();
    expect(trail.count).toBe(0);
  });
});
