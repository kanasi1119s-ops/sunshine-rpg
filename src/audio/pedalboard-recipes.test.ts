import { describe, expect, it } from "vitest";
// @ts-ignore（node の型定義がないので import に付ける。melody-craft.test.ts と同じ）
import fs from "node:fs";
import { aiSongToScore } from "./ai-song";
import { FX_TYPES } from "./fx-chain";

/** docs/sound/band-ensemble/pedalboard-signal-chain.md の「```json recipe」ブロックを取り出す。 */
const DOC = new URL("../../docs/sound/band-ensemble/pedalboard-signal-chain.md", import.meta.url);
const blocks = [...fs.readFileSync(DOC, "utf8").matchAll(/```json recipe\n([\s\S]*?)\n```/g)].map((m) => m[1]);

const FX_KEYS = new Set(["type", "mix", "ms", "beats", "feedback", "rate", "depth", "freq", "q", "gain", "level", "low", "mid", "midHz", "high", "threshold", "ratio", "bits", "size", "tone", "attack", "release", "kind", "pre"]);
const PART_KEYS = new Set(["amp", "ampDrive", "ampLevel", "ampTone", "fx"]);
const base = { title: "レシピ", description: "テスト", bpm: 120, beats: 4, chords: "C G Am F", barsPerChord: 1, repeats: 1, autoAccompaniment: false, feel: "rock", tone: "rock" } as const;

describe("pedalboard-signal-chain.md のレシピ（JSON）", () => {
  it("レシピが20個以上あり、すべて JSON として読める", () => {
    expect(blocks.length).toBeGreaterThanOrEqual(20);
    for (const b of blocks) expect(() => JSON.parse(b)).not.toThrow();
  });

  it("使っているキーは、パートの amp 系と fx のつまみだけ。fx の種類は実在する", () => {
    for (const b of blocks) {
      const part = JSON.parse(b) as Record<string, unknown>;
      for (const k of Object.keys(part)) expect(PART_KEYS.has(k), `${k} は想定外のパートのキー`).toBe(true);
      for (const f of (part.fx ?? []) as Record<string, unknown>[]) {
        expect(FX_TYPES as readonly string[], `fx の種類 ${String(f.type)}`).toContain(f.type);
        for (const k of Object.keys(f)) expect(FX_KEYS.has(k), `${String(f.type)} の ${k} は想定外のつまみ`).toBe(true);
      }
    }
  });

  it("実際に AI ソングとして読ませても、アンプやエフェクターの警告が出ない", () => {
    for (const b of blocks) {
      const part = JSON.parse(b) as Record<string, unknown>;
      const { score, warnings } = aiSongToScore({ ...base, parts: [{ instrument: "guitar", role: "ギター", volume: 0.2, pan: 0, notes: "C4:4 D4:4", ...part }] });
      const bad = warnings.filter((w) => w.includes("アンプ「") || w.includes("エフェクター「"));
      expect(bad, JSON.stringify(part)).toEqual([]);
      expect(score.tracks[0].fx?.length ?? 0).toBe(((part.fx as unknown[] | undefined) ?? []).length);
    }
  });

  it("ギターにコーラスを付けていない（banned-sounds.md 6）", () => {
    for (const b of blocks) {
      const part = JSON.parse(b) as { amp?: string; fx?: { type: string }[] };
      expect((part.fx ?? []).some((f) => f.type === "chorus")).toBe(false);
    }
  });
});
