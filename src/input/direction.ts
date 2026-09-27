export type Direction = "up" | "down" | "left" | "right";

/**
 * 現在押されている方向の集合から、実際に移動する向きを1つ決める。
 * 斜め入力は許可せず、縦方向を優先する（王道RPGの4方向移動）。
 * 一番最近押された方向を優先したいので、呼び出し側は「押した順」を維持したSetを渡す。
 */
export function resolveDirection(pressed: ReadonlySet<Direction>): Direction | null {
  const order: Direction[] = Array.from(pressed);
  if (order.length === 0) {
    return null;
  }
  return order[order.length - 1] ?? null;
}
