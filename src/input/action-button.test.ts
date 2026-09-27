import { describe, expect, it } from "vitest";
import { ActionButton } from "./action-button";

describe("ActionButton", () => {
  it("押していなければfalse", () => {
    const button = new ActionButton();
    expect(button.consume()).toBe(false);
  });

  it("押した後、1回だけtrueを返す", () => {
    const button = new ActionButton();
    button.press();
    expect(button.consume()).toBe(true);
    expect(button.consume()).toBe(false);
  });
});
