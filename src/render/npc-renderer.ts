import type { Npc } from "../game/npc";
import type { TileMap } from "../game/map/tile-map";
import type { Camera } from "./camera";
import { npcLook, spriteSpecForNpc } from "../game/sprite/character-specs";
import { shadeColor } from "../game/color-utils";
import { SPRITE_FEET_ROW } from "../game/sprite/overworld-sprite";
import { drawSprite } from "./sprite-renderer";

/** NPCの足元のy（ワールド座標）。プレイヤーとの前後（奥のものを先に描く）を決めるのに使う。 */
export function npcFeetY(npc: Npc, tileHeight: number): number {
  return npc.tileY * tileHeight + tileHeight;
}

/**
 * NPCのドット絵（16×32、正面向き）を、そのマスの足元にそろえて描く（頭は上のマスにはみ出す）。
 * 顔グラフィックのある人は、その色。名前の無い人は、IDから髪・肌・髪型を決めた色替え。
 * `filter` で、描くNPCを絞れる（プレイヤーより奥・手前に分けて描くため）。
 */
export function renderNpcs(
  ctx: CanvasRenderingContext2D,
  npcs: Npc[],
  map: TileMap,
  camera: Camera,
  filter: (npc: Npc) => boolean = () => true,
): void {
  const { tileWidth, tileHeight } = map.data;
  for (const npc of npcs) {
    if (!filter(npc)) {
      continue;
    }
    const x = npc.tileX * tileWidth - camera.x;
    const feetY = npcFeetY(npc, tileHeight) - camera.y;
    const look = npcLook(npc);
    if (look === "person") {
      drawSprite(ctx, spriteSpecForNpc(npc), "down", 0, x + (tileWidth - 16) / 2, feetY - SPRITE_FEET_ROW - 1);
    } else {
      drawMarker(ctx, npc.color, look === "monster", x, feetY - tileHeight, tileWidth, tileHeight);
    }
  }
}

/** 物・仕掛け・敵のしるし（人ではないもの）。物は縁取りつきの小さな箱、敵は暗い結晶のような形。 */
function drawMarker(ctx: CanvasRenderingContext2D, color: string, monster: boolean, x: number, y: number, w: number, h: number): void {
  const dark = "#221a30";
  if (monster) {
    // 暗い菱形（結晶）に、赤く光る芯。
    const cx = x + w / 2;
    for (let row = 0; row < h; row++) {
      const half = Math.round(((row < h / 2 ? row : h - 1 - row) + 1) * (w / h));
      ctx.fillStyle = dark;
      ctx.fillRect(Math.round(cx - half - 1), y + row, half * 2 + 2, 1);
      ctx.fillStyle = shadeColor(color, -0.45);
      ctx.fillRect(Math.round(cx - half), y + row, half * 2, 1);
    }
    ctx.fillStyle = "#ff6a6a";
    ctx.fillRect(Math.round(cx - 1), y + Math.floor(h / 2) - 1, 2, 2);
    return;
  }
  ctx.fillStyle = dark;
  ctx.fillRect(x + 1, y + 2, w - 2, h - 3);
  ctx.fillStyle = color;
  ctx.fillRect(x + 2, y + 3, w - 4, h - 5);
  ctx.fillStyle = shadeColor(color, 0.4);
  ctx.fillRect(x + 3, y + 4, w - 8, 2);
  ctx.fillStyle = shadeColor(color, -0.35);
  ctx.fillRect(x + 2, y + h - 4, w - 4, 1);
}
