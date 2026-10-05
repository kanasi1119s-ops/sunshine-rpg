import { afterEach, describe, expect, it } from "vitest";
import { startCloudSaves } from "./cloud-saves";
import { createMemoryStore, setSaveListener, saveToSlot } from "./storage";
import type { SaveData } from "./types";

function fakeClaude(remote: Record<string, string>) {
  const docs = new Map<string, Record<string, unknown>>(Object.entries(remote).map(([k, raw]) => [k, { raw }]));
  const db = { collection: () => ({ doc: (id: string) => ({
    get: async () => ({ exists: docs.has(id), data: () => docs.get(id) }),
    set: async (d: Record<string, unknown>) => { docs.set(id, d); },
    delete: async () => { docs.delete(id); },
  }) }) };
  (globalThis as unknown as { claude: unknown }).claude = { use: async (n: string) => (n === "db" ? db : { id: async () => "u1" }) };
  return docs;
}
const raw = (t: string) => JSON.stringify({ savedAt: t });

afterEach(() => { delete (globalThis as { claude?: unknown }).claude; setSaveListener(null); });

describe("アーティファクトのセーブ保管", () => {
  it("データベースのセーブが新しければ、localStorageに戻す", async () => {
    fakeClaude({ slot1: raw("2026-10-05T10:00:00Z") });
    const store = createMemoryStore();
    let called = false;
    await startCloudSaves(store, () => { called = true; });
    expect(store.getItem("sunshine-rpg:save:slot1")).toBe(raw("2026-10-05T10:00:00Z"));
    expect(called).toBe(true);
  });
  it("セーブすると、データベースにも写る", async () => {
    const docs = fakeClaude({});
    const store = createMemoryStore();
    await startCloudSaves(store, () => undefined);
    saveToSlot(store, "slot2", { savedAt: "2026-10-05T11:00:00Z" } as SaveData);
    await new Promise((r) => setTimeout(r, 0));
    expect(docs.get("slot2")?.raw).toContain("2026-10-05T11:00:00Z");
  });
  it("dbが無い場所では、何もしない", async () => {
    await expect(startCloudSaves(createMemoryStore(), () => undefined)).resolves.toBeUndefined();
  });
});
