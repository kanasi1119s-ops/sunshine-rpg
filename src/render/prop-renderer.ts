import { proceduralPropCanvas } from "./tent-prop";
import type { MapProp, TileMapData } from "../game/map/types";
import { SPRITE_DATA } from "../game/art/sprite-data.generated";
import { getSpriteCanvas } from "../game/art/sprite";
import type { Camera } from "./camera";

/** 飾りの足元のy（ワールド座標）。プレイヤー・NPCとの前後（奥のものを先に描く）を決めるのに使う。 */
export function propFeetY(prop: MapProp, tileHeight: number): number {
  return prop.tileY * tileHeight + tileHeight;
}

/** 飾り（木・家）を、足元・中央のマスにそろえて描く。`filter` で、プレイヤーより奥・手前に分けて描ける。 */
export function renderProps(
  ctx: CanvasRenderingContext2D,
  data: TileMapData,
  camera: Camera,
  filter: (prop: MapProp) => boolean = () => true,
  /** 描く飾りを指定する（前後の並べ替えで1つずつ描くとき用）。省略すると地図の飾り全部。 */
  props: readonly MapProp[] | undefined = data.props,
): void {
  if (!props) {
    return;
  }
  ctx.imageSmoothingEnabled = false;
  for (const prop of props) {
    if (!filter(prop)) {
      continue;
    }
    const canvas = getSpriteCanvas(`prop:${prop.kind}`, SPRITE_DATA) ?? proceduralPropCanvas(prop);
    if (!canvas) {
      continue;
    }
    const x = prop.tileX * data.tileWidth + data.tileWidth / 2 - canvas.width / 2 - camera.x;
    const y = propFeetY(prop, data.tileHeight) - canvas.height - camera.y;
    ctx.drawImage(canvas, Math.round(x), Math.round(y));
  }
}
