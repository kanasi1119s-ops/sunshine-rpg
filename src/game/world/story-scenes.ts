import type { EventCommand, Flags } from "../event/types";
import { CH0_SCENES } from "./scenes/ch0-scenes";
import { CH1_SCENES } from "./scenes/ch1-scenes";
import { CH2_SCENES } from "./scenes/ch2-scenes";
import { CH3_SCENES } from "./scenes/ch3-scenes";
import { CH4_SCENES } from "./scenes/ch4-scenes";
import { CH5_SCENES } from "./scenes/ch5-scenes";
import { CH6_SCENES } from "./scenes/ch6-scenes";
import { CH7_SCENES } from "./scenes/ch7-scenes";
import { CH8_SCENES } from "./scenes/ch8-scenes";
import { CH9_SCENES } from "./scenes/ch9-scenes";

/**
 * 小説（長編版『陽だまり紀行』）の場面を、ゲームの中で「読む」ための場面（2026-10-05、人間の指示
 * 「もっと小説の内容入れて、物語を読む部分を厚くしたい。イベント少なすぎる」）。
 * 場面は、地図に入ったとき（`at: "enter"`）か、決まった範囲に足を踏み入れたとき（`at: {x0,y0,x1,y1}`）に、条件がそろっていれば一度だけ流れる。
 * 条件: `requires` のフラグがすべて立っていて、`blockedBy` のフラグがどれも立っていないこと。流れたら `scene_<id>_seen` が立つ。
 * 物語の進み（依頼・ボス・報告）は、これまでどおり章のNPCが受け持つ。場面は、そのあいだを埋める会話・回想・情景で、進み具合のフラグは変えない
 * （例外として、場面の中で小さなフラグを立ててもよいが、章の進行に使うフラグは立てない）。
 */
export interface StoryScene {
  /** 一意な名前（例 "ch0-harbor-morning"）。流れたかどうかのフラグ名に使う。 */
  id: string;
  mapId: string;
  /** すべて立っているときだけ流れる。 */
  requires?: string[];
  /** どれか1つでも立っていると流れない（その場面の「時期」が過ぎたら出さない）。 */
  blockedBy?: string[];
  /** 地図に入ったとき、または範囲（両端を含むマス）に足を踏み入れたとき。 */
  at: "enter" | { x0: number; y0: number; x1: number; y1: number };
  commands: EventCommand[];
  /** 元にした小説の節（docs/novel/本編/...）。 */
  source?: string;
}

export const STORY_SCENES: StoryScene[] = [
  ...CH0_SCENES,
  ...CH1_SCENES,
  ...CH2_SCENES,
  ...CH3_SCENES,
  ...CH4_SCENES,
  ...CH5_SCENES,
  ...CH6_SCENES,
  ...CH7_SCENES,
  ...CH8_SCENES,
  ...CH9_SCENES,
];

export function sceneSeenFlag(id: string): string {
  return `scene_${id}_seen`;
}

/** いま流すべき場面（無ければ null）。tile はプレイヤーの足もとのマス。 */
export function pendingScene(mapId: string, tile: { x: number; y: number }, flags: Flags, scenes: readonly StoryScene[] = STORY_SCENES): StoryScene | null {
  for (const s of scenes) {
    if (s.mapId !== mapId || flags[sceneSeenFlag(s.id)]) continue;
    if (s.requires && !s.requires.every((f) => flags[f])) continue;
    if (s.blockedBy && s.blockedBy.some((f) => flags[f])) continue;
    if (s.at !== "enter") {
      const a = s.at;
      if (tile.x < a.x0 || tile.x > a.x1 || tile.y < a.y0 || tile.y > a.y1) continue;
    }
    return s;
  }
  return null;
}
