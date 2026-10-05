import { MANUAL_SLOTS, setSaveListener, type KeyValueStore } from "./storage";

/**
 * アーティファクト（claude.ai に公開したページ）で遊ぶときの、セーブデータの保管。
 * ブラウザのlocalStorageは、ページを開き直すと空になることがあるため、セーブのたびに、アーティファクトのデータベース（`db`）の
 * 自分専用の場所（`data/users/<自分のid>/saves`）にも写しておき、起動したとき、こちらが新しければlocalStorageに戻す。
 * `db` が使えない場所（ふつうのWeb公開・開発中）では、何もしない（これまでどおりlocalStorageだけ）。
 */
interface DocRef { get(): Promise<{ exists: boolean; data(): Record<string, unknown> | undefined }>; set(d: Record<string, unknown>): Promise<void>; delete(): Promise<void> }
interface Db { collection(path: string): { doc(id: string): DocRef } }
interface ClaudeRuntime { use(name: string): Promise<unknown> }

const PREFIX = "sunshine-rpg:save:";

function savedAtOf(raw: string | null): number {
  if (!raw) return 0;
  try {
    const t = new Date((JSON.parse(raw) as { savedAt?: string }).savedAt ?? "").getTime();
    return Number.isNaN(t) ? 0 : t;
  } catch {
    return 0;
  }
}

/** 起動時に1回呼ぶ。localStorageに戻したセーブがあれば、`onRestored` を呼ぶ。 */
export async function startCloudSaves(store: KeyValueStore, onRestored: () => void): Promise<void> {
  const claude = (globalThis as { claude?: ClaudeRuntime }).claude;
  if (!claude) return;
  try {
    const db = (await claude.use("db")) as Db | null;
    const user = (await claude.use("user")) as { id(): Promise<string | null> } | null;
    const id = user ? await user.id() : null;
    if (!db || !id) return;
    const saves = db.collection(`data/users/${id}/saves`);
    const keyOf = (k: string): string => k.slice(PREFIX.length);
    let restored = false;
    for (const slot of [...MANUAL_SLOTS, "autosave"] as const) {
      const key = PREFIX + slot;
      try {
        const snap = await saves.doc(slot).get();
        const remote = snap.exists ? (snap.data() as { raw?: string } | undefined)?.raw : undefined;
        const local = store.getItem(key);
        if (remote && savedAtOf(remote) > savedAtOf(local)) {
          store.setItem(key, remote);
          restored = true;
        } else if (local && !remote) {
          await saves.doc(slot).set({ raw: local });
        }
      } catch {
        /* このスロットだけ飛ばす */
      }
    }
    // これから先のセーブ・削除を、データベースにも写す
    setSaveListener((key, raw) => {
      const slot = keyOf(key);
      const doc = saves.doc(slot);
      (raw === null ? doc.delete() : doc.set({ raw })).catch(() => undefined);
    });
    if (restored) onRestored();
  } catch {
    /* db が使えない場所では、何もしない */
  }
}
