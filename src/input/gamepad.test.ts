import { describe, expect, it } from "vitest";
import { buttonEdges, createGamepadPoller, directionsFromPad } from "./gamepad";
import { InputState } from "./input-state";

const btns = (...on: number[]): boolean[] => Array.from({ length: 17 }, (_, i) => on.includes(i));

describe("コントローラー", () => {
  it("十字キーとスティックから、方向を出す", () => {
    expect([...directionsFromPad({ buttons: btns(12), axes: [0, 0] })]).toEqual(["up"]);
    expect([...directionsFromPad({ buttons: btns(), axes: [0.9, 0.1] })]).toEqual(["right"]);
    expect([...directionsFromPad({ buttons: btns(), axes: [-0.2, -0.3] })]).toEqual([]); // 小さな傾きは無視
    expect([...directionsFromPad({ buttons: btns(), axes: [0.6, 0.9] })]).toEqual(["down"]); // 斜めは大きいほう
  });

  it("A=決定、B=もどる、スタート=メニュー。押した瞬間だけ拾う", () => {
    expect(buttonEdges(btns(), btns(0)).pressed).toEqual(["confirm"]);
    expect(buttonEdges(btns(0), btns(0)).pressed).toEqual([]);
    expect(buttonEdges(btns(0), btns()).released).toEqual(["confirm"]);
    expect(buttonEdges(btns(), btns(1, 9)).pressed.sort()).toEqual(["back", "menu"]);
  });

  it("つながっていれば、入力状態に方向とボタンがそそがれ、抜けると離される", () => {
    const input = new InputState();
    const events: string[] = [];
    let pad: Partial<Gamepad> | null = { connected: true, buttons: btns(14).map((pressed) => ({ pressed }) as GamepadButton), axes: [0, 0] };
    const poller = createGamepadPoller(input, (a, down) => events.push(`${a}:${down}`), () => [pad as Gamepad]);
    poller.poll();
    expect(input.getDirection()).toBe("left");
    pad = { connected: true, buttons: btns(0).map((pressed) => ({ pressed }) as GamepadButton), axes: [0, 0] };
    poller.poll();
    expect(input.getDirection()).toBeNull();
    expect(events).toEqual(["confirm:true"]);
    pad = null;
    poller.poll();
    expect(input.getDirection()).toBeNull();
  });
});
