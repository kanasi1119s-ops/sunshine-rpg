import { deserializeSaveData, serializeSaveData } from "../game/save/serializer";
import type { SaveData } from "../game/save/types";

function fileNameFor(data: SaveData): string {
  return `sunshine-rpg-save-${data.savedAt.replace(/[:.]/g, "-")}.json`;
}

/** セーブデータをJSONファイルとしてダウンロードさせる。 */
export function downloadSaveFile(data: SaveData): void {
  const json = serializeSaveData(data);
  const blob = new Blob([json], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = fileNameFor(data);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

/** ファイルからセーブデータを読み込む。形式が不正なら例外を投げる。 */
export function readSaveFile(file: File): Promise<SaveData> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      try {
        resolve(deserializeSaveData(String(reader.result)));
      } catch (error) {
        reject(error instanceof Error ? error : new Error(String(error)));
      }
    };
    reader.onerror = () => reject(reader.error ?? new Error("ファイルを読み込めませんでした"));
    reader.readAsText(file);
  });
}
