import { migrateSaveData } from "./migrate";
import type { SaveData } from "./types";

export function serializeSaveData(data: SaveData): string {
  return JSON.stringify(data);
}

export function deserializeSaveData(json: string): SaveData {
  const parsed: unknown = JSON.parse(json);
  return migrateSaveData(parsed);
}
