export interface Camera {
  /** ワールド座標（ピクセル）でのカメラ左上の位置。 */
  x: number;
  y: number;
  viewportWidth: number;
  viewportHeight: number;
}

export function createCamera(viewportWidth: number, viewportHeight: number): Camera {
  return { x: 0, y: 0, viewportWidth, viewportHeight };
}

function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max);
}

/**
 * targetX/targetY（ワールド座標）が画面の中央に来るようにカメラを動かす。
 * マップの外側が映り込まないよう、マップの範囲内に収める。
 */
export function centerCameraOn(
  camera: Camera,
  targetX: number,
  targetY: number,
  mapWidthPx: number,
  mapHeightPx: number,
): Camera {
  const rawX = targetX - camera.viewportWidth / 2;
  const rawY = targetY - camera.viewportHeight / 2;

  const maxX = Math.max(0, mapWidthPx - camera.viewportWidth);
  const maxY = Math.max(0, mapHeightPx - camera.viewportHeight);

  return {
    ...camera,
    // 小数のままだとタイルの継ぎ目に黒い線が出るので、ピクセルの整数位置にそろえる。
    x: Math.round(clamp(rawX, 0, maxX)),
    y: Math.round(clamp(rawY, 0, maxY)),
  };
}
