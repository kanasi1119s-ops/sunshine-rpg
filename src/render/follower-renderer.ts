import type { Camera } from "./camera";
import type { PartyTrail } from "../game/party-trail";
import type { SpriteSpec } from "../game/sprite/overworld-sprite";
import { frameAt, SPRITE_FEET_ROW, SPRITE_WIDTH } from "../game/sprite/overworld-sprite";
import { drawSprite } from "./sprite-renderer";

/** 主人公の当たり判定（12×14）と同じ大きさのものとして、足元をそろえる。 */
const BODY_W = 12;
const BODY_H = 14;

/** ついてくる仲間の足元のy（前後の順の判定用）。 */
export function followerFeetY(trail: PartyTrail, i: number): number {
  const f = trail.followerAt(i);
  return f ? f.y + BODY_H : -Infinity;
}

/** ついてくる仲間を描く。`filter` で足元のyによって、主人公より奥・手前に分けて描ける。 */
export function renderFollowers(ctx: CanvasRenderingContext2D, trail: PartyTrail, specs: SpriteSpec[], camera: Camera, filter: (feetY: number) => boolean = () => true): void {
  for (let i = trail.count - 1; i >= 0; i--) {
    const f = trail.followerAt(i);
    const spec = specs[i];
    if (!f || !spec || !filter(f.y + BODY_H)) {
      continue;
    }
    const feetX = f.x + BODY_W / 2 - camera.x;
    const feetY = f.y + BODY_H - camera.y;
    drawSprite(ctx, spec, f.dir, frameAt(f.moving, f.animMs), feetX - SPRITE_WIDTH / 2, feetY - SPRITE_FEET_ROW - 1);
  }
}
