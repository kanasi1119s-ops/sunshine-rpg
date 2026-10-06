import type { Flags } from "../event/types";
import type { TileMapData } from "../map/types";
import { propFootprintTiles, propOverhangTiles } from "../map/map-props";
import type { Npc } from "../npc";
import { PORTRAITS } from "../portrait/portraits";
import { firstSpeaker } from "../sprite/character-specs";
import { isVoiceOnly, sceneSpeakers, STORY_SCENES, type StoryScene } from "./story-scenes";

/**
 * 物語の場面で話す人を、その町に「いる人」にする（2026-10-06、人間の指示「会話イベントもドットキャラは近づくときは歩いてきて、
 * 必ず町にいるようにしてください」）。
 * - 場面で話す人のうち、仲間（ユーリと、ついてくる仲間）・声だけの人・その町にすでにいる同じ名前の人をのぞいた人を、
 *   その場面の地図に置く。場面の時期（requires がそろい、blockedBy が立っていないあいだ）だけ、そこにいる。
 * - 置く所: 場面が始まる所（範囲の場面はその範囲、入ったときの場面は町のまんなか）から 4〜8 マスはなれた、
 *   まわり8マスがすべて通れるマス（道をふさがない）。せまい部屋で見つからなければ、あいているマスならよい。
 *   出入り口・ほかの人・飾り（家・木・井戸など）のまわりはさける。世界地図には置かない。
 * - 話しかけると、その人が場面でさいごに言ったセリフを言う。
 * 場面が始まると、この人たちが主人公のそばまで歩いてくる（main.ts の bringSceneActors）。
 */

/** 物語でいつも仲間として出てくる人（町に置かない）。 */
export const PARTY_NAMES = new Set(["ユーリ", "レト", "ミナ", "ガイド", "オルカ", "アヤメ"]);

export interface SceneWindow {
  requires?: string[];
  blockedBy?: string[];
}

/** その人がいま町にいるか（どれか1つの場面の時期にあてはまれば、いる）。 */
export function residentVisible(windows: readonly SceneWindow[], flags: Flags): boolean {
  return windows.some((w) => (!w.requires || w.requires.every((f) => flags[f])) && !(w.blockedBy && w.blockedBy.some((f) => flags[f])));
}

function lastLineOf(commands: StoryScene["commands"], name: string): string | null {
  let last: string | null = null;
  const walk = (cmds: StoryScene["commands"]): void => {
    for (const c of cmds) {
      if (c.type === "message" && c.speaker === name) last = c.text;
      if (c.type === "if") {
        walk(c.then);
        if (c.else) walk(c.else);
      }
      if (c.type === "choice") for (const o of c.options) walk(o.commands);
    }
  };
  walk(commands);
  return last;
}

function hashOf(s: string): number {
  let h = 0;
  for (const ch of s) h = (h * 31 + ch.charCodeAt(0)) >>> 0;
  return h;
}

/** 場面の地図ごとに、町に置く人を作る。npcs は、その地図にもともといる人（重なりと名前の確認に使う）。 */
export function sceneResidentsFor(mapId: string, data: TileMapData, npcs: readonly Npc[], scenes: readonly StoryScene[] = STORY_SCENES): Npc[] {
  // 世界地図には置かない（旅の途中の場面。話す人は、少しはなれた所から歩いてくる）
  if (mapId === "world-map") return [];
  const here = scenes.filter((s) => s.mapId === mapId);
  if (here.length === 0) return [];
  const w = data.width, h = data.height;
  const col = data.collision ?? [];
  const exits = data.exits ?? [];
  const open = (x: number, y: number): boolean => x > 0 && y > 0 && x < w - 1 && y < h - 1 && col[y * w + x] === 0;
  const taken = new Set<number>();
  for (const n of npcs) for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) taken.add((Math.round(n.tileY) + dy) * w + Math.round(n.tileX) + dx);
  for (const e of exits) for (let dy = -2; dy <= 2; dy++) for (let dx = -2; dx <= 2; dx++) taken.add((e.tileY + dy) * w + e.tileX + dx);
  // 飾り（家・木・井戸など）の絵がかかるマス（絵の上にはみ出す所もふくめ、まわり1マス）にも置かない
  for (const prop of data.props ?? []) {
    const tiles = propFootprintTiles(prop);
    const top = Math.min(...tiles.map((t) => t.y)) - propOverhangTiles(prop.kind, data.tileHeight);
    const xs = tiles.map((t) => t.x);
    for (let y = top - 1; y <= prop.tileY + 1; y++) for (let x = Math.min(...xs) - 1; x <= Math.max(...xs) + 1; x++) taken.add(y * w + x);
  }
  const roomy = (x: number, y: number): boolean => {
    for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) if (!open(x + dx, y + dy)) return false;
    return !taken.has(y * w + x);
  };
  const existing = new Set(npcs.map((n) => firstSpeaker(n.commands).speaker).filter((s): s is string => !!s));
  // 町のまんなか（通れるマスの重心）
  let sx = 0, sy = 0, cnt = 0;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) if (open(x, y)) { sx += x; sy += y; cnt++; }
  const center = cnt ? { x: Math.round(sx / cnt), y: Math.round(sy / cnt) } : { x: Math.floor(w / 2), y: Math.floor(h / 2) };
  const people = new Map<string, { windows: SceneWindow[]; line: string; anchor: { x: number; y: number } }>();
  for (const s of here) {
    const anchor = s.at === "enter" ? center : { x: Math.round((s.at.x0 + s.at.x1) / 2), y: Math.round((s.at.y0 + s.at.y1) / 2) };
    for (const name of sceneSpeakers(s.commands)) {
      if (PARTY_NAMES.has(name) || isVoiceOnly(name) || existing.has(name)) continue;
      const p = people.get(name);
      const win = { requires: s.requires, blockedBy: s.blockedBy };
      if (p) {
        p.windows.push(win);
      } else {
        people.set(name, { windows: [win], line: lastLineOf(s.commands, name) ?? "……", anchor });
      }
    }
  }
  const out: Npc[] = [];
  for (const [name, p] of people) {
    const hash = hashOf(name);
    let best: { x: number; y: number; score: number } | null = null;
    // まわりまで広い所がなければ（せまい部屋）、そのマスがあいていればよい（少しだけ点を悪くする）
    const usable = (x: number, y: number): number => (roomy(x, y) ? 0 : open(x, y) && !taken.has(y * w + x) ? 50 : -1);
    for (let y = 1; y < h - 1; y++) {
      for (let x = 1; x < w - 1; x++) {
        const u = usable(x, y);
        if (u < 0) continue;
        const d = Math.abs(x - p.anchor.x) + Math.abs(y - p.anchor.y);
        const score = u + (d >= 4 && d <= 8 ? 0 : 100 + Math.abs(d - 6) * 10) + ((x * 7 + y * 13 + hash) % 97) / 100;
        if (!best || score < best.score) best = { x, y, score };
      }
    }
    if (!best) continue;
    for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) taken.add((best.y + dy) * w + best.x + dx);
    out.push({
      id: `resident-${mapId}-${hash.toString(36)}`,
      tileX: best.x,
      tileY: best.y,
      color: "#a08870",
      ...(PORTRAITS[name] ? { spriteName: name } : {}),
      commands: [{ type: "message", speaker: name, text: p.line }],
      sceneWindows: p.windows,
    });
  }
  return out;
}
