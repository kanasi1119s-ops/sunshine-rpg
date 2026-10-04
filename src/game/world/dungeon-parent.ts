/**
 * 「町とボスの間に足したダンジョン」の登録表（`dungeon-extensions.ts` が地図を作るときに埋める）。
 * 曲・戦闘の背景・エンカウントを、元のボスの地図にならうために、軽い別ファイルに分けてある。
 */
/** 足した地図 → その章のボスの地図。 */
export const DUNGEON_PARENT: Record<string, string> = {};
/** 足した地図 → 戦闘の背景の種類。 */
export const DUNGEON_BIOME: Record<string, string> = {};
