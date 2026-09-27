import type { ActionButton } from "./action-button";
import type { Direction } from "./direction";
import type { InputState } from "./input-state";

const LABELS: Record<Direction, string> = {
  up: "▲",
  down: "▼",
  left: "◀",
  right: "▶",
};

/** スマホ・タブレット用の画面上十字ボタンと決定ボタンを作り、containerに追加する。 */
export function createTouchControls(
  container: HTMLElement,
  input: InputState,
  action: ActionButton,
): HTMLElement {
  const pad = document.createElement("div");
  pad.className = "touch-dpad";

  (Object.keys(LABELS) as Direction[]).forEach((direction) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `touch-dpad__button touch-dpad__button--${direction}`;
    button.textContent = LABELS[direction];

    const press = (event: Event): void => {
      event.preventDefault();
      input.press(direction);
    };
    const release = (event: Event): void => {
      event.preventDefault();
      input.release(direction);
    };

    button.addEventListener("pointerdown", press);
    button.addEventListener("pointerup", release);
    button.addEventListener("pointercancel", release);
    button.addEventListener("pointerleave", release);

    pad.appendChild(button);
  });

  container.appendChild(pad);

  const actionButton = document.createElement("button");
  actionButton.type = "button";
  actionButton.className = "touch-action-button";
  actionButton.textContent = "決定";
  actionButton.addEventListener("pointerdown", (event) => {
    event.preventDefault();
    action.press();
  });
  container.appendChild(actionButton);

  return pad;
}
