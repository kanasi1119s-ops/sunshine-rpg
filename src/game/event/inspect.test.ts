import { describe, expect, it } from "vitest";
import { collectBattleIds, collectReferencedFlags, collectSetFlags, collectWarpTargets } from "./inspect";
import type { EventCommand } from "./types";

const SAMPLE: EventCommand[] = [
  { type: "message", text: "hello" },
  { type: "setFlag", flag: "met_villager", value: true },
  {
    type: "choice",
    text: "どうする？",
    options: [
      {
        label: "はい",
        commands: [
          { type: "setFlag", flag: "chose_yes", value: true },
          { type: "warp", mapId: "town-a", tileX: 1, tileY: 1 },
        ],
      },
      {
        label: "いいえ",
        commands: [
          {
            type: "if",
            flag: "already_fought",
            equals: true,
            then: [{ type: "message", text: "また？" }],
            else: [{ type: "startBattle", battleId: "boss-1" }],
          },
        ],
      },
    ],
  },
];

describe("collectSetFlags", () => {
  it("choiceやifの中身も含めて、すべてのsetFlagを集める", () => {
    expect(collectSetFlags(SAMPLE)).toEqual(new Set(["met_villager", "chose_yes"]));
  });
});

describe("collectReferencedFlags", () => {
  it("ifで参照されているフラグを集める", () => {
    expect(collectReferencedFlags(SAMPLE)).toEqual(new Set(["already_fought"]));
  });
});

describe("collectWarpTargets", () => {
  it("choiceの中のwarpも見つける", () => {
    expect(collectWarpTargets(SAMPLE)).toEqual(new Set(["town-a"]));
  });
});

describe("collectBattleIds", () => {
  it("if/elseの中のstartBattleも見つける", () => {
    expect(collectBattleIds(SAMPLE)).toEqual(new Set(["boss-1"]));
  });
});
