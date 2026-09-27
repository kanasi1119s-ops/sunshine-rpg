export interface GameLoopCallbacks {
  update: (dtMs: number) => void;
  render: (interpolation: number) => void;
}

export interface GameLoopOptions {
  /** 1回の update が進める時間（ミリ秒）。既定は 60fps 相当。 */
  stepMs?: number;
  /** タブ切り替え等で経過時間が異常に大きくなったときの上限（ミリ秒）。 */
  maxDeltaMs?: number;
}

export interface GameLoop {
  /** requestAnimationFrame から渡される現在時刻（ミリ秒）を渡して呼ぶ。 */
  tick: (nowMs: number) => void;
  /** 直近1秒間に tick が呼ばれた回数。 */
  getFps: () => number;
}

/**
 * 固定時間ステップのゲームループ。
 * update は常に stepMs 刻みで呼ばれるため、描画のフレームレートが揺れても
 * ゲームの中身（戦闘計算・移動など）の進み方は一定になる。
 */
export function createGameLoop(
  callbacks: GameLoopCallbacks,
  options: GameLoopOptions = {},
): GameLoop {
  const stepMs = options.stepMs ?? 1000 / 60;
  const maxDeltaMs = options.maxDeltaMs ?? 250;

  let lastTime: number | null = null;
  let accumulator = 0;
  let frameCount = 0;
  let fpsTimer = 0;
  let fps = 0;

  function tick(nowMs: number): void {
    if (lastTime === null) {
      lastTime = nowMs;
    }
    let delta = nowMs - lastTime;
    lastTime = nowMs;
    if (delta > maxDeltaMs) {
      delta = maxDeltaMs;
    }

    accumulator += delta;
    while (accumulator >= stepMs) {
      callbacks.update(stepMs);
      accumulator -= stepMs;
    }
    callbacks.render(accumulator / stepMs);

    frameCount += 1;
    fpsTimer += delta;
    if (fpsTimer >= 1000) {
      fps = frameCount;
      frameCount = 0;
      fpsTimer -= 1000;
    }
  }

  return { tick, getFps: () => fps };
}
