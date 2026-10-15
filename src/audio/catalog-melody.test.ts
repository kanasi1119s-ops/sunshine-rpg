/**
 * ゲームの組み込み曲（自動作曲・特別曲）の音符が、知らないうちに変わっていないかを見張る（2026-10-16）。
 * 10/07 に作曲エンジンを直したとき、曲のデータは同じでも乱数の流れが変わり、49曲のメロディが変わってしまった（人間の指摘「明らかにメロディが変わってる」）。
 * 作曲エンジン（songwriter.ts・finale.ts・compose.ts など）を直すときは、新しい動きをオプションにして、既存の曲では使わないこと。
 * わざと曲を変えたときだけ（人間の承認が要る）、失敗の表示に出る新しい値で catalog-melody.fixture.json を書きかえる。
 */
import { describe, expect, it } from "vitest";
import saved from "./catalog-melody.fixture.json";
import { allEntries, getTrackEdition } from "./catalog";

/** 文字列の指紋（FNV-1a 32bit を2本）。 */
function fnv(text: string, seed: number): string {
  let h = seed >>> 0;
  for (let i = 0; i < text.length; i++) { h ^= text.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; }
  return h.toString(16).padStart(8, "0");
}
function fingerprint(id: string): string {
  let all = "";
  for (const ed of ["modern", "real", "ps2"] as const) {
    const s = getTrackEdition(id, ed);
    all += JSON.stringify(s.tracks.map((t) => [t.instrument ?? null, t.notes.map((n) => [n.note, n.durationBeats, n.velocity ?? null])]));
  }
  return fnv(all, 2166136261) + fnv(all, 0x9747b28c);
}

describe("組み込み曲の音符", () => {
  it("記録（10/07 より前の、人間が聴いてきた音符）と同じ", () => {
    const now: Record<string, string> = {};
    for (const e of allEntries()) if (!e.handmade) now[e.id] = fingerprint(e.id);
    for (const [id, fp] of Object.entries(saved as Record<string, string>)) expect(now[id], id).toBe(fp);
  });
});
