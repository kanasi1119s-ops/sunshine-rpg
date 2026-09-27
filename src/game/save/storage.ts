import { deserializeSaveData, serializeSaveData } from "./serializer";
import type { SaveData } from "./types";

/** localStorage と同じ形。テストでは本物の代わりに簡易な実装を渡せる。 */
export interface KeyValueStore {
  getItem(key: string): string | null;
  setItem(key: string, value: string): void;
  removeItem(key: string): void;
}

export type SaveSlotId = "slot1" | "slot2" | "slot3" | "autosave";

const KEY_PREFIX = "sunshine-rpg:save:";

function keyFor(slot: SaveSlotId): string {
  return `${KEY_PREFIX}${slot}`;
}

export function saveToSlot(store: KeyValueStore, slot: SaveSlotId, data: SaveData): void {
  store.setItem(keyFor(slot), serializeSaveData(data));
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
