import { EXTRA_ENTRIES, type CatalogEntry } from "./catalog";
import type { Score } from "./score";

/** 作曲ソフトが書き出す「ゲームの曲」のファイル形式。 */
export interface GameSongFile {
  format: "sunshine-game-song";
  version: 1;
  id: string;
  title: string;
  scene: string;
  group?: string;
  score: Score;
}

const ID_RULE = /^[a-z0-9][a-z0-9-]*$/;

/** ファイルの中身を確かめて、曲の一覧の1件にする。おかしければ理由つきでエラー。 */
export function songFileToEntry(data: unknown, taken: Set<string>): CatalogEntry {
  const f = data as Partial<GameSongFile> | null;
  if (!f || f.format !== "sunshine-game-song" || !f.score || !Array.isArray(f.score.tracks) || f.score.tracks.length === 0) {
    throw new Error("ゲームの曲のファイル形式ではありません");
  }
  if (typeof f.id !== "string" || !ID_RULE.test(f.id)) {
    throw new Error(`曲のIDは、英小文字・数字・「-」だけにしてください: ${String(f.id)}`);
  }
  if (taken.has(f.id)) {
    throw new Error(`曲のIDが重なっています: ${f.id}`);
  }
  const score: Score = { ...f.score };
  delete score.namModels;
  // 録音トラック（実際の楽器の音）は大きいので、ゲームには入れない
  delete score.audioTracks;
  score.tracks = score.tracks.map((t) => {
    if (t.amp?.type === "nam") {
      const amp = { ...t.amp, type: "auto" as const };
      delete amp.model;
      return { ...t, amp };
    }
    return t;
  });
  return { id: f.id, title: f.title || f.id, scene: f.scene || "（未割り当て）", styleLabel: "作曲ソフトで作った曲", group: f.group || "オリジナル追加曲", handmade: score };
}

const files = import.meta.glob("./songs/*.sunshine-song.json", { eager: true, import: "default" }) as Record<string, unknown>;

function loadAll(): CatalogEntry[] {
  // 組み込みの曲と同じIDは「バンド版への差し替え」として認める（catalog.ts の allEntries が差し替える）。ファイルどうしの重なりだけを弾く。
  const taken = new Set<string>();
  const out: CatalogEntry[] = [];
  for (const [path, data] of Object.entries(files).sort(([a], [b]) => a.localeCompare(b))) {
    try {
      const entry = songFileToEntry(data, taken);
      taken.add(entry.id);
      out.push(entry);
    } catch (e) {
      console.warn(`曲を読み込めませんでした（${path}）:`, (e as Error).message);
    }
  }
  return out;
}

/** 作曲ソフトで作って登録した曲。 */
export const USER_SONGS: CatalogEntry[] = loadAll();

EXTRA_ENTRIES.push(...USER_SONGS);
