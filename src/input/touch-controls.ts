import type { ActionButton } from "./action-button";
import type { Direction } from "./direction";
import type { InputState } from "./input-state";

/** スティックのまんなかから、これ以上かたむけたら、その向きに歩く（スティックの半径に対する割合）。 */
const DEADZONE = 0.28;

/** かたむけた量（-1〜1）から、向きを決める。たてよこで大きいほうの向き。小さければ null。 */
export function stickDirection(dx: number, dy: number): Direction | null {
  if (Math.hypot(dx, dy) < DEADZONE) return null;
  if (Math.abs(dx) > Math.abs(dy)) return dx > 0 ? "right" : "left";
  return dy > 0 ? "down" : "up";
}

/** スマホ・タブレット用の画面上スティックと決定ボタンを作り、containerに追加する。 */
export function createTouchControls(
  container: HTMLElement,
  input: InputState,
  action: ActionButton,
): HTMLElement {
  const pad = document.createElement("div");
  pad.className = "touch-stick";
  const knob = document.createElement("div");
  knob.className = "touch-stick__knob";
  pad.appendChild(knob);

  let activePointer: number | null = null;
  let current: Direction | null = null;
  const setDirection = (next: Direction | null): void => {
    if (next === current) return;
    if (current) input.release(current);
    if (next) input.press(next);
    current = next;
  };
  const update = (event: PointerEvent): void => {
    const rect = pad.getBoundingClientRect();
    const radius = rect.width / 2;
    let dx = (event.clientX - (rect.left + radius)) / radius;
    let dy = (event.clientY - (rect.top + radius)) / radius;
    const len = Math.hypot(dx, dy);
    if (len > 1) {
      dx /= len;
      dy /= len;
    }
    // つまみを、指のほうへ動かして見せる
    knob.style.transform = `translate(${dx * radius * 0.55}px, ${dy * radius * 0.55}px)`;
    setDirection(stickDirection(dx, dy));
  };
  const end = (event: PointerEvent): void => {
    if (event.pointerId !== activePointer) return;
    event.preventDefault();
    activePointer = null;
    knob.style.transform = "translate(0, 0)";
    setDirection(null);
  };
  pad.addEventListener("pointerdown", (event) => {
    if (activePointer !== null) return;
    event.preventDefault();
    activePointer = event.pointerId;
    pad.setPointerCapture?.(event.pointerId);
    update(event);
  });
  pad.addEventListener("pointermove", (event) => {
    if (event.pointerId !== activePointer) return;
    event.preventDefault();
    update(event);
  });
  pad.addEventListener("pointerup", end);
  pad.addEventListener("pointercancel", end);

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
