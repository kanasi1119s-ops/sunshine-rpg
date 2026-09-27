import type { ActionButton } from "./action-button";
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

const ACTION_KEYS = new Set(["Enter", " ", "z", "Z"]);

/** キーボードの矢印キー／WASDと、決定キー（Enter/Space/Z）を入力状態に反映する。 */
export function attachKeyboard(input: InputState, action: ActionButton): void {
  window.addEventListener("keydown", (event) => {
    const direction = KEY_TO_DIRECTION[event.key];
    if (direction) {
      input.press(direction);
      return;
    }
    if (!event.repeat && ACTION_KEYS.has(event.key)) {
      action.press();
    }
  });
  window.addEventListener("keyup", (event) => {
    const direction = KEY_TO_DIRECTION[event.key];
    if (direction) {
      input.release(direction);
    }
  });
}
