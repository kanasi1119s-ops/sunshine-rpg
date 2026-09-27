/** ゲーム内部の論理解像度。この大きさで描画し、画面には拡大縮小して表示する。 */
export const LOGICAL_WIDTH = 400;
export const LOGICAL_HEIGHT = 225;

/** コンテナの実サイズに合わせて、アスペクト比を保ったまま最大の表示サイズを計算する。 */
export function computeDisplaySize(
  containerWidth: number,
  containerHeight: number,
): { width: number; height: number } {
  const scale = Math.min(
    containerWidth / LOGICAL_WIDTH,
    containerHeight / LOGICAL_HEIGHT,
  );
  return {
    width: LOGICAL_WIDTH * scale,
    height: LOGICAL_HEIGHT * scale,
  };
}

export interface GameCanvas {
  canvas: HTMLCanvasElement;
  ctx: CanvasRenderingContext2D;
  /** コンテナのサイズが変わったときに呼ぶ。表示サイズを再計算する。 */
  resize: () => void;
}

/** PC・スマホ両対応のドット絵向けCanvasを作り、containerに挿入する。 */
export function createGameCanvas(container: HTMLElement): GameCanvas {
  const canvas = document.createElement("canvas");
  canvas.width = LOGICAL_WIDTH;
  canvas.height = LOGICAL_HEIGHT;
  canvas.style.imageRendering = "pixelated";
  canvas.style.display = "block";
  canvas.style.touchAction = "none";
  container.appendChild(canvas);

  const ctx = canvas.getContext("2d");
  if (!ctx) {
    throw new Error("2D描画コンテキストを取得できません");
  }
  ctx.imageSmoothingEnabled = false;

  function resize(): void {
    const { width, height } = computeDisplaySize(
      container.clientWidth,
      container.clientHeight,
    );
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
  }

  return { canvas, ctx, resize };
}
