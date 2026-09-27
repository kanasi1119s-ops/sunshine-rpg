import { resolveDirection, type Direction } from "./direction";

/**
 * キーボードと画面ボタンの両方から書き込める、共有の入力状態。
 * JSのSetは挿入順を保つため、あとから押した方向を優先する resolveDirection と相性がよい。
 */
export class InputState {
  private pressed = new Set<Direction>();

  press(direction: Direction): void {
    this.pressed.delete(direction);
    this.pressed.add(direction);
  }

  release(direction: Direction): void {
    this.pressed.delete(direction);
  }

  getDirection(): Direction | null {
    return resolveDirection(this.pressed);
  }
}
