import { CATALOG, EXTRA_ENTRIES, type CatalogEntry } from "./catalog";
import { songFileToEntry, USER_SONGS } from "./user-songs";

/**
 * 過去に作った曲の保管庫（songs-archive/）。BGMプレイヤー・作曲ソフトにだけ入れる。
 * ゲーム本体（main.ts）はこのファイルを読み込まないので、dist/ の容量予算には入らない。
 * ゲームの場面で使う曲は、songs/ に移す。
 */
const files = import.meta.glob("./songs-archive/*.sunshine-song.json", { eager: true, import: "default" }) as Record<string, unknown>;

function loadAll(): CatalogEntry[] {
  const taken = new Set([...CATALOG, ...EXTRA_ENTRIES].map((e) => e.id));
  for (const e of USER_SONGS) taken.add(e.id);
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

export const ARCHIVE_SONGS: CatalogEntry[] = loadAll();

EXTRA_ENTRIES.push(...ARCHIVE_SONGS);
