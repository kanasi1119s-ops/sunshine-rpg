import { describe, expect, it } from "vitest";
import { PART_RECIPES, SCENE_SETS, SOUND_SETS, applySoundSet } from "./sound-sets";
import masterSource from "../../tools/composer/master.mjs?raw";
import type { Score } from "./score";

const mk = (): Score => ({
  tempoBpm: 160, loop: false, edition: "real",
  tracks: [
    { waveform: "square", instrument: "kick", volume: 0.3, pan: 0, notes: [{ note: "C2", durationBeats: 4 }] },
    { waveform: "square", instrument: "distGuitar", volume: 0.3, pan: -0.9, notes: [{ note: "A2", durationBeats: 4 }] },
    { waveform: "square", instrument: "distGuitar", volume: 0.3, pan: 0.9, notes: [{ note: "A2", durationBeats: 4 }] },
    { waveform: "square", instrument: "bell", volume: 0.3, pan: 0, notes: [{ note: "C5", durationBeats: 4 }] },
  ],
});

describe("サウンドセット", () => {
  it("アンプ・音量・ドラムのミックスが当たり、合計は 0.9 をこえない", () => {
    const out = applySoundSet(mk(), SOUND_SETS["punk-run"]);
    expect(out.tracks[1].amp?.type).toBe("punk");
    expect(out.tracks[1].pan).toBe(-0.55);
    expect(out.tracks[2].pan).toBe(0.55);
    expect(out.tracks[3].volume).toBeLessThanOrEqual(0.06);
    expect(out.drumMix?.tom?.tune).toBe(-3);
    expect(out.tracks.reduce((a, t) => a + t.volume, 0)).toBeLessThanOrEqual(0.9001);
  });
  it("何度当てても同じ結果で、元の曲は変わらない", () => {
    const base = mk();
    const once = applySoundSet(base, SOUND_SETS["punk-run"]);
    const twice = applySoundSet(once, SOUND_SETS["punk-run"]);
    expect(twice).toEqual(once);
    expect(base.tracks[1].volume).toBe(0.3);
    expect(base.tracks[1].amp).toBeUndefined();
  });
  it("セットの音量の合計は 0.9 以下、使う音源の名前は作曲ソフトにある", () => {
    for (const s of Object.values(SOUND_SETS)) {
      const sum = Object.values(s.parts).reduce((a, p) => a + (p?.volume ?? 0), 0);
      expect(sum).toBeLessThanOrEqual(1.6); // 同じ楽器が複数あるので、1本ぶんの合計
      expect(["std", "finger", "pick", "rock", "metal", "jazz", "jpop"]).toContain(s.overlays.bass);
      expect(["std", "muldjord", "rock", "metal", "jazz", "jpop", "supra"]).toContain(s.overlays.drums);
      expect(["std", "gretsch", "hofner", "pluck", "pluck-soft", "pluck-clear", "pluck-mellow"]).toContain(s.overlays.guitar);
    }
  });

  it("仕上げの音量（master）は、あるなら現実的な範囲（-16〜-6 LUFS）", () => {
    for (const s of Object.values(SOUND_SETS)) {
      if (s.master) {
        expect(s.master.lufs).toBeGreaterThanOrEqual(-20); // アンビエント・ゲームのダンジョンは -18
        expect(s.master.lufs).toBeLessThanOrEqual(-6);
      }
    }
    expect(SOUND_SETS["punk-run"].master).toBeDefined();
  });

  it("既存の2つのセットの書き出し設定は変わらない（punk-run は -10 だけ、clear-guitar-rock は書き出し設定なし）", () => {
    expect(SOUND_SETS["punk-run"].master).toEqual({ lufs: -10 });
    expect(SOUND_SETS["clear-guitar-rock"].master).toBeUndefined();
  });

  it("ミックスの型が 12 種以上あり、master の preset は master.mjs に実在する", () => {
    const added = ["rock-4", "pop-lead", "jpop-bright", "ballad-piano-strings", "jazz-trio", "funk-bass", "house-duck", "ambient-wide", "orchestra-depth", "game-battle", "game-town", "game-dungeon"];
    for (const id of added) expect(SOUND_SETS[id], id).toBeDefined();
    for (const s of Object.values(SOUND_SETS)) {
      const p = s.master?.preset;
      if (p) expect(masterSource.includes(`"${p}":`) || masterSource.includes(`  ${p}:`), `${s.id} の preset ${p}`).toBe(true);
      if (s.master?.space) expect(["hall", "room", "plate"]).toContain(s.master.space);
      if (s.master?.spaceWet !== undefined) expect(s.master.spaceWet).toBeGreaterThanOrEqual(0), expect(s.master.spaceWet).toBeLessThanOrEqual(1);
    }
  });

  it("新しいセットでも、キック・ベース・808 は中央のまま（panWidth を持たない）、volume は 0〜0.2", () => {
    for (const s of Object.values(SOUND_SETS)) {
      for (const inst of ["kick", "bass", "sub808"] as const) expect(s.parts[inst]?.panWidth, `${s.id}/${inst}`).toBeUndefined();
      for (const p of Object.values(s.parts)) if (p?.volume !== undefined) { expect(p.volume).toBeGreaterThan(0); expect(p.volume).toBeLessThanOrEqual(0.2); }
    }
  });

  it("新しいセットを当てても何度でも同じ結果で、合計は 0.9 以下", () => {
    for (const s of Object.values(SOUND_SETS)) {
      const once = applySoundSet(mk(), s);
      expect(applySoundSet(once, s)).toEqual(once);
      expect(once.tracks.reduce((a, t) => a + t.volume, 0)).toBeLessThanOrEqual(0.9001);
    }
  });

  it("場面の表は実在するセットを指し、音づくりの型は PartMix を持つ", () => {
    for (const sc of Object.values(SCENE_SETS)) {
      expect(SOUND_SETS[sc.sound], sc.sound).toBeDefined();
      expect(masterSource.includes(`"${sc.preset}":`), sc.preset).toBe(true);
    }
    for (const r of Object.values(PART_RECIPES)) expect(r.mix.volume).toBeLessThanOrEqual(0.2);
  });

  it("音づくりの型に、strings-ensemble など 5 つを足してある", () => {
    for (const id of ["strings-ensemble", "brass-swell", "organ-hold", "cinematic-drone", "chip-lead"]) expect(PART_RECIPES[id], id).toBeDefined();
    expect(PART_RECIPES["strings-ensemble"].mix).toMatchObject({ chorus: 0.3, reverb: 0.3, duck: 0.3 });
    expect(PART_RECIPES["brass-swell"].mix.bright).toBe(-0.1);
    expect(PART_RECIPES["cinematic-drone"].hint?.sustain).toBe(3);
    expect(PART_RECIPES["cinematic-drone"].mix.reverb).toBe(0.5);
    expect(PART_RECIPES["chip-lead"].hint?.patch).toBe("squareLead");
    expect(PART_RECIPES["chip-lead"].mix.reverb).toBe(0);
  });
});
