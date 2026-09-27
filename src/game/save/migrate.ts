import { SAVE_VERSION, type SaveData } from "./types";

/**
 * 読み込んだデータを、今のバージョンの形に変換する。
 * 将来バージョンが上がったら、ここに「vN → vN+1」の変換を追加していく
 * （例: version 1 のデータが来たら、まず v1→v2 の変換をしてから続きを見る）。
 */
export function migrateSaveData(data: unknown): SaveData {
  if (typeof data !== "object" || data === null || !("version" in data)) {
    throw new Error("セーブデータの形式が正しくありません");
  }
  const version = (data as { version: unknown }).version;

  if (version === SAVE_VERSION) {
    return data as SaveData;
  }

  throw new Error(`対応していないセーブデータのバージョンです: ${String(version)}`);
}
