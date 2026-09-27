import { describe, expect, it } from "vitest";
import { DialogueController } from "./dialogue-controller";
import type { EventCommand } from "../event/types";

describe("DialogueController", () => {
  it("開始直後はメッセージが未表示（0文字）で、時間経過で文字が増える", () => {
    const controller = new DialogueController({}, { charsPerSecond: 30 });
    controller.start([{ type: "message", text: "こんにちは" }]);

    expect(controller.isActive()).toBe(true);
    expect(controller.getRenderState()).toEqual({
      kind: "message",
      speaker: undefined,
      visibleText: "",
      fullyShown: false,
    });

    controller.update(100); // 30文字/秒 * 0.1秒 = 3文字
    expect(controller.getRenderState()).toEqual({
      kind: "message",
      speaker: undefined,
      visibleText: "こんに",
      fullyShown: false,
    });
  });

  it("文字送り中にconfirmすると全部表示され、もう一度confirmすると次に進む", () => {
    const commands: EventCommand[] = [
      { type: "message", text: "こんにちは" },
      { type: "message", text: "またね" },
    ];
    const controller = new DialogueController({});
    controller.start(commands);

    controller.update(10);
    controller.confirm(); // 全部表示
    expect(controller.getRenderState()).toEqual({
      kind: "message",
      speaker: undefined,
      visibleText: "こんにちは",
      fullyShown: true,
    });

    controller.confirm(); // 次のメッセージへ
    expect(controller.getRenderState()?.kind).toBe("message");
    if (controller.getRenderState()?.kind === "message") {
      expect((controller.getRenderState() as { visibleText: string }).visibleText).toBe("");
    }
  });

  it("最後まで進めるとisActiveがfalseになる", () => {
    const controller = new DialogueController({});
    controller.start([{ type: "message", text: "やあ" }]);
    controller.confirm(); // 全部表示
    controller.confirm(); // 終了
    expect(controller.isActive()).toBe(false);
    expect(controller.getRenderState()).toBeNull();
  });

  it("選択肢をmoveChoiceで選び、confirmで確定できる", () => {
    const flags = {};
    const commands: EventCommand[] = [
      {
        type: "choice",
        text: "どっち？",
        options: [
          { label: "A", commands: [{ type: "setFlag", flag: "chose_a", value: true }] },
          { label: "B", commands: [{ type: "setFlag", flag: "chose_b", value: true }] },
        ],
      },
    ];
    const controller = new DialogueController(flags);
    controller.start(commands);

    controller.moveChoice(1);
    expect(controller.getRenderState()).toMatchObject({ selectedIndex: 1 });

    controller.confirm();
    expect((flags as Record<string, boolean>).chose_b).toBe(true);
    expect(controller.isActive()).toBe(false);
  });

  it("warpコマンドに達したらonWarpを呼び、UIは止めずに終了する", () => {
    const warps: { mapId: string }[] = [];
    const controller = new DialogueController(
      {},
      { onWarp: (w) => warps.push({ mapId: w.mapId }) },
    );
    controller.start([{ type: "warp", mapId: "room", tileX: 1, tileY: 1 }]);

    expect(warps).toEqual([{ mapId: "room" }]);
    expect(controller.isActive()).toBe(false);
  });
});
