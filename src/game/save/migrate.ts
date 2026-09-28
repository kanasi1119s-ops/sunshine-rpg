import { SAVE_VERSION, type SaveData } from "./types";

/** version 1（仲間データが無い頃）のセーブデータの形。 */
interface SaveDataV1 {
  version: 1;
  savedAt: string;
  player: SaveData["player"];
  hero: SaveData["hero"];
  inventory: SaveData["inventory"];
  flags: SaveData["flags"];
}

function migrateV1ToV2(data: SaveDataV1): SaveData {
  // v1のセーブには仲間の概念が無かったため、空の状態から始める
  // （仲間の加入フラグ自体は flags 側に残っているので、会話上の扱いに支障はない。
  // 　戦闘に参加させ直す場合、仲間はレベル1から再スタートになる）。
  return { ...data, version: 2, companions: {} };
}

/**
 * 読み込んだデータを、今のバージョンの形に変換する。
 * 将来バージョンが上がったら、ここに「vN → vN+1」の変換を追加していく
 * （例: version 1 のデータが来たら、まず v1→v2 の変換をしてから続きを見る）。
 */
export function migrateSaveData(data: unknown): SaveData {
  if (typeof data !== "object" || data === null || !("version" in data)) {
    throw new Error("セーブデータの形式が正しくありません");
  }
  let current = data as { version: unknown };

  if (current.version === 1) {
    current = migrateV1ToV2(current as unknown as SaveDataV1);
  }

  if (current.version === SAVE_VERSION) {
    return current as SaveData;
  }

  throw new Error(`対応していないセーブデータのバージョンです: ${String(current.version)}`);
}
