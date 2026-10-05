import { deserializeSaveData, serializeSaveData } from "../game/save/serializer";
import type { SaveData } from "../game/save/types";

function fileNameFor(data: SaveData): string {
  return `sunshine-rpg-save-${data.savedAt.replace(/[:.]/g, "-")}.json`;
}

interface DownloadsCap { save(req: { filename: string; data: string }): Promise<unknown> }

/**
 * セーブデータをJSONファイルとしてダウンロードさせる。アーティファクトでは、`downloads` 機能で保存する
 * （ふつうのダウンロードがふさがれていることがあるため）。成功したら true。
 */
export async function downloadSaveFile(data: SaveData): Promise<boolean> {
  const json = serializeSaveData(data);
  const claude = (globalThis as { claude?: { use(n: string): Promise<unknown> } }).claude;
  if (claude) {
    try {
      const cap = (await claude.use("downloads")) as DownloadsCap | null;
      if (cap) {
        await cap.save({ filename: fileNameFor(data), data: json });
        return true;
      }
    } catch {
      return false;
    }
  }
  const blob = new Blob([json], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = fileNameFor(data);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
  return true;
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
