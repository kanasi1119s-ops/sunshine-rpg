import { describe, expect, it } from "vitest";
import { battleEffectFor, shakeOffset } from "./battle-effect";

const party = ["ユーリ", "レト"];

describe("battleEffectFor", () => {
  it("味方がダメージを受けたら画面がゆれる", () => {
    expect(battleEffectFor("灯里の歪み の体当たり！ ユーリ に 5 のダメージ", party)?.kind).toBe("shake");
  });
  it("敵に当てたら敵が光り、会心は強く光る", () => {
    expect(battleEffectFor("ユーリ の斬撃！ 灯里の歪み に 9 のダメージ", party)?.kind).toBe("hit");
    expect(battleEffectFor("ユーリ の斬撃！ 会心の一撃！ 灯里の歪み に 20 のダメージ", party)?.kind).toBe("crit");
  });
  it("回復は緑に光り、敵を倒したときは消える演出、味方が倒れたときは何もしない", () => {
    expect(battleEffectFor("ミナ のHPが 8 回復した", party)?.kind).toBe("heal");
    expect(battleEffectFor("灯里の歪み を倒した！", party)?.kind).toBe("down");
    expect(battleEffectFor("レト を倒した！", party)).toBeNull();
  });
  it("関係のない文では演出しない", () => {
    expect(battleEffectFor("敵があらわれた！", party)).toBeNull();
  });
  it("ゆれは時間とともに小さくなり、終わると0になる", () => {
    expect(shakeOffset(1, 500)).toBe(0);
    expect(Math.abs(shakeOffset(0.1, 25))).toBeLessThanOrEqual(4);
  });
});
