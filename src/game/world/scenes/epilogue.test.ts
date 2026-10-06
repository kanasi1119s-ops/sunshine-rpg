import { describe, expect, it } from "vitest";
import { createEventRunner } from "../../event/event-runner";
import type { EventCommand, Flags } from "../../event/types";
import { WORLD_MAPS } from "../world";
import { EPILOGUE_AFTER_ROLL, EPILOGUE_BEFORE_ROLL, EPILOGUE_SEEN_FLAG } from "./epilogue";

describe("エンディングのあとのエピローグ", () => {
  it("最後まで流れ、見たしるしと、終章の場面の「見た」しるしが立つ", () => {
    const flags: Flags = { chapter9_cleared: true };
    const warps: string[] = [];
    const times: string[] = [];
    let rolls = 0;
    let messages = 0;
    for (const part of [EPILOGUE_BEFORE_ROLL, EPILOGUE_AFTER_ROLL]) {
      const runner = createEventRunner(part, flags, {
        onWarp: (w) => warps.push(w.mapId),
        onTime: (t) => times.push(t),
        onStaffRoll: () => rolls++,
      });
      for (let step = runner.next(); !step.done; step = runner.next({ kind: "advance" })) messages++;
      if (part === EPILOGUE_BEFORE_ROLL) {
        expect(rolls).toBe(1);
        expect(flags[EPILOGUE_SEEN_FLAG]).toBeUndefined();
      }
    }
    expect(rolls).toBe(1);
    expect(messages).toBeGreaterThan(120);
    expect(flags[EPILOGUE_SEEN_FLAG]).toBe(true);
    for (const id of ["ch9-keeper-thanks", "ch9-return-sea", "ch9-return-brothers", "ch9-touri-pier"]) {
      expect(flags[`scene_${id}_seen`]).toBe(true);
    }
    expect(warps).toEqual(["touri-town", "yuri-home", "yuri-home-attic"]);
    expect(times.at(-1)).toBe("morning");
  });

  it("移る先は、どれも歩ける場所", () => {
    const warps = [...EPILOGUE_BEFORE_ROLL, ...EPILOGUE_AFTER_ROLL].filter((c): c is Extract<EventCommand, { type: "warp" }> => c.type === "warp");
    for (const w of warps) {
      const data = WORLD_MAPS[w.mapId];
      expect(data, w.mapId).toBeDefined();
      expect(data.collision?.[w.tileY * data.width + w.tileX], `${w.mapId} (${w.tileX},${w.tileY})`).not.toBe(1);
    }
  });
});
