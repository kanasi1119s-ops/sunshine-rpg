import type { Direction } from "./direction";
import type { InputState } from "./input-state";

const KEY_TO_DIRECTION: Record<string, Direction> = {
  ArrowUp: "up",
  ArrowDown: "down",
  ArrowLeft: "left",
  ArrowRight: "right",
  w: "up",
  s: "down",
  a: "left",
  d: "right",
};

/** キーボードの矢印キー／WASDを入力状態に反映する。 */
export function attachKeyboard(input: InputState): void {
  window.addEventListener("keydown", (event) => {
    const direction = KEY_TO_DIRECTION[event.key];
    if (direction) {
      input.press(direction);
    }
  });
  window.addEventListener("keyup", (event) => {
    const direction = KEY_TO_DIRECTION[event.key];
    if (direction) {
      input.release(direction);
    }
  });
}
