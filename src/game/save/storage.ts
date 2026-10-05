import { deserializeSaveData, serializeSaveData } from "./serializer";
import type { SaveData } from "./types";

/** localStorage と同じ形。テストでは本物の代わりに簡易な実装を渡せる。 */
export interface KeyValueStore {
  getItem(key: string): string | null;
  setItem(key: string, value: string): void;
  removeItem(key: string): void;
}

export type SaveSlotId = "slot1" | "slot2" | "slot3" | "slot4" | "slot5" | "autosave";

/** 自分でセーブする場所（5か所）。自動セーブ（`autosave`）は別に1つある。 */
export const MANUAL_SLOTS: readonly SaveSlotId[] = ["slot1", "slot2", "slot3", "slot4", "slot5"];

const KEY_PREFIX = "sunshine-rpg:save:";

function keyFor(slot: SaveSlotId): string {
  return `${KEY_PREFIX}${slot}`;
}

type SaveListener = (key: string, raw: string | null) => void;
let saveListener: SaveListener | null = null;
/** セーブ・削除のたびに呼ばれる関数を決める（アーティファクトのデータベースへの写し用）。 */
export function setSaveListener(fn: SaveListener | null): void {
  saveListener = fn;
}

export function saveToSlot(store: KeyValueStore, slot: SaveSlotId, data: SaveData): void {
  const raw = serializeSaveData(data);
  store.setItem(keyFor(slot), raw);
  saveListener?.(keyFor(slot), raw);
}

/** 読み込みに失敗した場合（壊れたデータ・非対応バージョンなど）はnullを返す。 */
export function loadFromSlot(store: KeyValueStore, slot: SaveSlotId): SaveData | null {
  const raw = store.getItem(keyFor(slot));
  if (!raw) {
    return null;
  }
  try {
    return deserializeSaveData(raw);
  } catch {
    return null;
  }
}

export function hasSlot(store: KeyValueStore, slot: SaveSlotId): boolean {
  return store.getItem(keyFor(slot)) !== null;
}

export function deleteSlot(store: KeyValueStore, slot: SaveSlotId): void {
  store.removeItem(keyFor(slot));
  saveListener?.(keyFor(slot), null);
}

/** テスト・デバッグ用の、メモリ上だけで完結するKeyValueStore。 */
export function createMemoryStore(): KeyValueStore {
  const map = new Map<string, string>();
  return {
    getItem: (key) => map.get(key) ?? null,
    setItem: (key, value) => {
      map.set(key, value);
    },
    removeItem: (key) => {
      map.delete(key);
    },
  };
}
