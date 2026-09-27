import { createSampleMapData, SAMPLE_MAP_SPAWN } from "../map/sample-map";
import { createSampleRoomData } from "../map/sample-room";
import type { TileMapData } from "../map/types";
import type { Npc } from "../npc";

/**
 * エンジンの動作確認用の仮の世界（マップ2枚＋NPC1人）。
 * 本物の町・ダンジョン・キャラクターはフェーズ2以降で作る。
 */
export const SAMPLE_MAPS: Record<string, TileMapData> = {
  "sample-field": createSampleMapData(),
  "sample-room": createSampleRoomData(),
};

export const SAMPLE_NPCS: Record<string, Npc[]> = {
  "sample-field": [],
  "sample-room": [
    {
      id: "test-villager",
      tileX: 2,
      tileY: 2,
      color: "#e07a5f",
      commands: [
        { type: "message", text: "やあ、これは動作確認用のNPCだよ。", speaker: "村人（仮）" },
        {
          type: "choice",
          text: "調子はどう？",
          options: [
            {
              label: "元気だよ",
              commands: [
                { type: "setFlag", flag: "greeted_villager_well", value: true },
                { type: "message", text: "それはよかった！", speaker: "村人（仮）" },
              ],
            },
            {
              label: "まあまあ",
              commands: [{ type: "message", text: "無理しないでね。", speaker: "村人（仮）" }],
            },
          ],
        },
        {
          type: "if",
          flag: "greeted_villager_well",
          equals: true,
          then: [{ type: "message", text: "また元気な顔を見せてね。", speaker: "村人（仮）" }],
          else: [{ type: "message", text: "また来てね。", speaker: "村人（仮）" }],
        },
      ],
    },
  ],
};

export const SAMPLE_START = {
  mapId: "sample-field",
  tileX: SAMPLE_MAP_SPAWN.tileX,
  tileY: SAMPLE_MAP_SPAWN.tileY,
};
