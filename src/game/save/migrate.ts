import { SAVE_VERSION, type SaveData } from "./types";

/** version 3（灯貨が無い頃）のセーブデータの形。 */
interface SaveDataV3 extends Omit<SaveData, "version" | "gold"> {
  version: 3;
}

/** version 2（ジョブが無い頃）のセーブデータの形。 */
interface SaveDataV2 extends Omit<SaveData, "version" | "jobs" | "gold"> {
  version: 2;
}

/** version 1（仲間データが無い頃）のセーブデータの形。 */
interface SaveDataV1 {
  version: 1;
  savedAt: string;
  player: SaveData["player"];
  hero: SaveData["hero"];
  inventory: SaveData["inventory"];
  flags: SaveData["flags"];
}

function migrateV1ToV2(data: SaveDataV1): SaveDataV2 {
  // v1のセーブには仲間の概念が無かったため、空の状態から始める
  // （仲間の加入フラグ自体は flags 側に残っているので、会話上の扱いに支障はない。
  // 　戦闘に参加させ直す場合、仲間はレベル1から再スタートになる）。
  return { ...data, version: 2, companions: {} };
}

function migrateV2ToV3(data: SaveDataV2): SaveDataV3 {
  // v2のセーブにはジョブの概念が無かったため、全員ジョブ未装備・熟練度0から始める。
  return { ...data, version: 3, jobs: {} };
}

function migrateV3ToV4(data: SaveDataV3): SaveData {
  // v3のセーブには灯貨の概念が無かったため、0から始める。
  return { ...data, version: 4, gold: 0 };
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

  if (current.version === 2) {
    current = migrateV2ToV3(current as unknown as SaveDataV2);
  }

  if (current.version === 3) {
    current = migrateV3ToV4(current as unknown as SaveDataV3);
  }

  if (current.version === SAVE_VERSION) {
    return current as SaveData;
  }

  throw new Error(`対応していないセーブデータのバージョンです: ${String(current.version)}`);
}
