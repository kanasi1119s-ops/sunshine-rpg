/**
 * 決定ボタン（会話を進める・調べる）。移動キーと違い「押した瞬間」だけを1回拾いたいので、
 * 押しっぱなし状態ではなく「前回確認してから押されたか」を保持する。
 */
export class ActionButton {
  private justPressed = false;

  press(): void {
    this.justPressed = true;
  }

  /** 押されていたかを返し、内部状態はリセットする（1回だけ反応させるため）。 */
  consume(): boolean {
    const pressed = this.justPressed;
    this.justPressed = false;
    return pressed;
  }
}
