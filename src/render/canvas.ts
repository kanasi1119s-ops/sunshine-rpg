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

/**
 * 実際の描画の細かさ（論理の1ドットを、キャンバスの何ピクセルで描くか）を、表示の大きさから決める。
 * 2〜4倍。論理の大きさ（400×225）のまま描いて拡大すると、10ドットの文字（とくに漢字）がつぶれて読みにくかった
 * （人間の指摘「ゲーム画面の文字が読みにくい」2026-10-04）。細かく描けば、文字はくっきりし、ドット絵は最近傍で拡大されるので見た目は変わらない。
 */
export function renderScaleFor(displayWidth: number, devicePixelRatio: number): number {
  const k = Math.round((displayWidth / LOGICAL_WIDTH) * devicePixelRatio);
  return Math.max(2, Math.min(4, k));
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
  let scale = 0;

  function resize(): void {
    const { width, height } = computeDisplaySize(
      container.clientWidth,
      container.clientHeight,
    );
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    // 描く細かさを変えたときは、キャンバスの大きさと拡大の設定をやり直す（大きさを変えると設定が消えるため）
    const k = renderScaleFor(width, typeof window !== "undefined" ? window.devicePixelRatio || 1 : 1);
    if (k !== scale) {
      scale = k;
      canvas.width = LOGICAL_WIDTH * k;
      canvas.height = LOGICAL_HEIGHT * k;
      ctx!.setTransform(k, 0, 0, k, 0, 0);
      ctx!.imageSmoothingEnabled = false;
    }
  }

  return { canvas, ctx, resize };
}
