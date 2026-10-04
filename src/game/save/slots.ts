import { loadFromSlot, MANUAL_SLOTS, type KeyValueStore, type SaveSlotId } from "./storage";
import type { SaveData } from "./types";

/** セーブ・ロード画面の1行ぶん。 */
export interface SlotSummary {
  id: SaveSlotId;
  /** 「セーブ1」「じどうセーブ」など。 */
  label: string;
  empty: boolean;
  /** 場所・レベル・日時（からっぽのときは無い）。 */
  text?: string;
  savedAt?: string;
}

const PLACE_BY_PREFIX: Array<[string, string]> = [
  ["world-map", "世界地図"], ["touri", "灯里"], ["mugikano", "麦香野"], ["garasuko", "硝子湖"], ["tetsukusari", "鉄鎖"],
  ["sanone", "砂音"], ["kiri", "霧断崖"], ["shimohara", "霜原"], ["fushima", "浮嶼"], ["toushin", "灯芯都"],
];

export function placeName(mapId: string): string {
  return PLACE_BY_PREFIX.find(([prefix]) => mapId.startsWith(prefix))?.[1] ?? "旅の途中";
}

function pad(n: number): string {
  return String(n).padStart(2, "0");
}

/** 「灯里　ユーリ Lv3　42灯貨　10/05 22:30」のような説明。 */
export function describeSave(data: SaveData): string {
  const d = new Date(data.savedAt);
  const when = Number.isNaN(d.getTime()) ? "" : `　${pad(d.getMonth() + 1)}/${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
  return `${placeName(data.player.mapId)}　ユーリ Lv${data.hero.stats.level}　${data.gold ?? 0}灯貨${when}`;
}

const LABELS: Record<SaveSlotId, string> = { autosave: "じどうセーブ", slot1: "セーブ1", slot2: "セーブ2", slot3: "セーブ3", slot4: "セーブ4", slot5: "セーブ5" };

/** 画面に並べる行。ロードのときは自動セーブも入れる（先頭）。 */
export function summarizeSlots(store: KeyValueStore, includeAuto: boolean): SlotSummary[] {
  const ids: SaveSlotId[] = includeAuto ? ["autosave", ...MANUAL_SLOTS] : [...MANUAL_SLOTS];
  return ids.map((id) => {
    const data = loadFromSlot(store, id);
    return data ? { id, label: LABELS[id], empty: false, text: describeSave(data), savedAt: data.savedAt } : { id, label: LABELS[id], empty: true };
  });
}

/** いちばん新しくセーブした場所（自動セーブも含む）。なければ null。全滅したとき、ここからやりなおす。 */
export function latestSaveSlot(store: KeyValueStore): SaveSlotId | null {
  let best: { id: SaveSlotId; time: number } | null = null;
  for (const s of summarizeSlots(store, true)) {
    if (s.empty || !s.savedAt) continue;
    const time = new Date(s.savedAt).getTime();
    if (Number.isNaN(time)) continue;
    if (!best || time > best.time) best = { id: s.id, time };
  }
  return best?.id ?? null;
}
