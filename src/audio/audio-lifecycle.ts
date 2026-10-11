/**
 * ブラウザの音まわりの安全対策（docs/sound/game-music-guide.md §7.4・§10 の提案4）。
 *  ・最初のユーザー操作（開始ボタン・タップ・キー）で resume する（unlockOnGesture）
 *  ・タブが隠れたら suspend、戻ったら resume する（バッテリーと、バックグラウンドで鳴り続ける事故の予防）
 *  ・電話・通知・他のアプリで止められた（state が suspended／interrupted になった）あと、次の操作で再開する
 *  ・起動時の読み込み表示のために、録音音源の準備ができるまで待つ（waitUntilReady）
 * ブラウザの型に依存しない最小の境目（CtxLike・DocLike）だけを使うので、そのままテストできる。
 */
export interface CtxLike {
  state: string;
  resume(): Promise<void>;
  suspend(): Promise<void>;
  addEventListener(type: "statechange", fn: () => void): void;
  removeEventListener(type: "statechange", fn: () => void): void;
}
export interface DocLike {
  hidden: boolean;
  addEventListener(type: string, fn: () => void): void;
  removeEventListener(type: string, fn: () => void): void;
}

export const GESTURE_EVENTS = ["pointerdown", "touchend", "keydown", "click"] as const;

export interface LifecycleOptions {
  /** 隠れたとき suspend しない（常に鳴らしたい場合）。 */
  keepPlayingInBackground?: boolean;
  /** 状態が変わったときに知らせる（画面の表示用）。 */
  onState?: (state: string) => void;
}

/** 開始ボタンなどの操作の中で呼ぶ。止まっていれば resume する。 */
export async function unlockAudio(ctx: CtxLike): Promise<boolean> {
  if (ctx.state === "running") return true;
  try { await ctx.resume(); } catch { return false; }
  return ctx.state === "running";
}

/** 安全対策をつなぐ。戻り値の関数で外せる。 */
export function attachAudioLifecycle(doc: DocLike, ctx: CtxLike, opts: LifecycleOptions = {}): () => void {
  /** 私たちが隠れたことで suspend したか（それなら戻ったとき resume する）。 */
  let suspendedByHide = false;
  /** 外から止められた（電話など）ので、次の操作で再開したいか。 */
  let needsGesture = false;

  const onVisibility = (): void => {
    if (doc.hidden) {
      if (opts.keepPlayingInBackground || ctx.state !== "running") return;
      suspendedByHide = true;
      void ctx.suspend().catch(() => undefined);
    } else if (suspendedByHide) {
      suspendedByHide = false;
      void ctx.resume().catch(() => { needsGesture = true; });
    } else if (ctx.state !== "running") {
      needsGesture = true;
      void ctx.resume().catch(() => undefined);
    }
  };
  const onState = (): void => {
    opts.onState?.(ctx.state);
    // 自分で止めたのではないのに running でなくなった（電話・他のアプリ・iOS の interrupted）
    if (ctx.state !== "running" && !suspendedByHide && !doc.hidden) needsGesture = true;
    if (ctx.state === "running") needsGesture = false;
  };
  const onGesture = (): void => {
    if (ctx.state !== "running" && (needsGesture || !suspendedByHide)) void ctx.resume().catch(() => undefined);
  };

  doc.addEventListener("visibilitychange", onVisibility);
  ctx.addEventListener("statechange", onState);
  for (const e of GESTURE_EVENTS) doc.addEventListener(e, onGesture);
  return () => {
    doc.removeEventListener("visibilitychange", onVisibility);
    ctx.removeEventListener("statechange", onState);
    for (const e of GESTURE_EVENTS) doc.removeEventListener(e, onGesture);
  };
}

/** 録音音源の準備ができるまで待つ（起動時の「読み込み中」表示用）。timeoutMs を過ぎたら false。 */
export function waitUntilReady(isReady: () => boolean, opts: { pollMs?: number; timeoutMs?: number; onTick?: (waitedMs: number) => void; setTimeout?: (fn: () => void, ms: number) => unknown } = {}): Promise<boolean> {
  const poll = opts.pollMs ?? 100, limit = opts.timeoutMs ?? 20000;
  const st = opts.setTimeout ?? ((fn, ms) => setTimeout(fn, ms));
  return new Promise((resolve) => {
    let waited = 0;
    const step = (): void => {
      if (isReady()) { resolve(true); return; }
      if (waited >= limit) { resolve(false); return; }
      opts.onTick?.(waited);
      waited += poll;
      st(step, poll);
    };
    step();
  });
}
