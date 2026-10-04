import type { Direction } from "./direction";
import type { InputState } from "./input-state";
import type { ControlAction } from "./key-bindings";

/**
 * 外部のコントローラー（ゲームパッド）。標準的な配置のコントローラーを想定する。
 *  十字キー・左スティック = うごく ／ A（下のボタン）= 決定 ／ B（右のボタン）= もどる ／ X（左のボタン）= ジョブ画面
 *  ／ Y（上のボタン）= 世界地図の全体図 ／ スタート = メニュー ／ セレクト = もどる
 * 配置は固定。ブラウザは、コントローラーのボタンをひとつ押すまで、つながったことに気づかない（ブラウザの決まり）。
 */
export const PAD_BUTTON_ACTIONS: Record<number, ControlAction> = {
  0: "confirm",
  1: "back",
  2: "job",
  3: "map",
  8: "back",
  9: "menu",
};

export interface PadSnapshot {
  buttons: boolean[];
  axes: number[];
}

const STICK_THRESHOLD = 0.55;

/** コントローラーの状態から、いま押している方向（十字キー・左スティック）。 */
export function directionsFromPad(pad: PadSnapshot): Set<Direction> {
  const dirs = new Set<Direction>();
  if (pad.buttons[12]) dirs.add("up");
  if (pad.buttons[13]) dirs.add("down");
  if (pad.buttons[14]) dirs.add("left");
  if (pad.buttons[15]) dirs.add("right");
  const x = pad.axes[0] ?? 0;
  const y = pad.axes[1] ?? 0;
  // スティックは、いちばん大きくたおした向き1つだけ（斜めで迷わないように）
  if (Math.abs(x) >= STICK_THRESHOLD || Math.abs(y) >= STICK_THRESHOLD) {
    if (Math.abs(y) >= Math.abs(x)) dirs.add(y < 0 ? "up" : "down");
    else dirs.add(x < 0 ? "left" : "right");
  }
  return dirs;
}

/** 前回との差から、新しく押されたボタン・離されたボタンの動作を出す。 */
export function buttonEdges(prev: boolean[], now: boolean[]): { pressed: ControlAction[]; released: ControlAction[] } {
  const pressed: ControlAction[] = [];
  const released: ControlAction[] = [];
  for (const [indexText, action] of Object.entries(PAD_BUTTON_ACTIONS)) {
    const i = Number(indexText);
    if (now[i] && !prev[i]) pressed.push(action);
    if (!now[i] && prev[i]) released.push(action);
  }
  return { pressed, released };
}

export interface GamepadPoller {
  /** 毎フレーム呼ぶ。 */
  poll(): void;
}

/**
 * コントローラーの入力を、キーボードと同じ入力状態にそそぐ。
 * `onButton` には、押したとき(true)・離したとき(false)の動作を渡す（決定は main.ts の決定ボタン、そのほかはキーの合図）。
 */
export function createGamepadPoller(
  input: InputState,
  onButton: (action: ControlAction, down: boolean) => void,
  getPads: () => ArrayLike<Gamepad | null> | undefined = () => (typeof navigator !== "undefined" && navigator.getGamepads ? navigator.getGamepads() : undefined),
): GamepadPoller {
  let prevButtons: boolean[] = [];
  let held = new Set<Direction>();
  return {
    poll() {
      const pads = getPads();
      let pad: Gamepad | null = null;
      if (pads) {
        for (let i = 0; i < pads.length; i++) {
          if (pads[i]?.connected) {
            pad = pads[i];
            break;
          }
        }
      }
      if (!pad) {
        for (const d of held) input.release(d);
        held = new Set();
        prevButtons = [];
        return;
      }
      const snapshot: PadSnapshot = { buttons: pad.buttons.map((b) => b.pressed), axes: [...pad.axes] };
      const dirs = directionsFromPad(snapshot);
      for (const d of held) if (!dirs.has(d)) input.release(d);
      for (const d of dirs) if (!held.has(d)) input.press(d);
      held = dirs;
      const { pressed, released } = buttonEdges(prevButtons, snapshot.buttons);
      for (const a of pressed) onButton(a, true);
      for (const a of released) onButton(a, false);
      prevButtons = snapshot.buttons;
    },
  };
}
