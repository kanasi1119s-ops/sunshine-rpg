import { findScale, type Scale } from "./scales";

/**
 * 場面（scene）ごとのおすすめの音階（2026-10-11、docs/sound/scales-world-guide.md 5-2 の表と提案 9）。
 * 強制ではなく、推奨の外の音階を書いたときに注意を出す。fanfare・title は表になかったので、似た場面から補った。
 */
export const SCENE_SCALES: Record<string, string[]> = {
  village: ["ro", "major-pentatonic", "ionian"],
  town: ["ionian", "mixolydian"],
  field: ["mixolydian", "lydian"],
  mystery: ["lydian", "dorian-b2"],
  shrine: ["ritsu", "lydian", "iwato"],
  castle: ["lydian", "aeolian", "dorian"],
  dungeon: ["phrygian", "harmonic-minor", "diminished-wh", "whole-tone", "todi"],
  battle: ["aeolian", "phrygian", "harmonic-minor"],
  boss: ["harmonic-minor", "phrygian", "diminished-wh", "hungarian-minor"],
  finalBoss: ["harmonic-minor", "phrygian", "diminished-wh", "whole-tone", "hungarian-minor"],
  sad: ["aeolian", "hirajoshi", "dorian"],
  inn: ["dorian", "mixolydian", "major-pentatonic"],
  ending: ["aeolian", "ionian", "lydian", "major-pentatonic"],
  fanfare: ["ionian", "mixolydian", "lydian"],
  title: ["lydian", "ionian", "aeolian", "dorian"],
};

/** 場面に合うおすすめの音階（Scale の並び）。 */
export function scalesForScene(scene: string): Scale[] {
  return (SCENE_SCALES[scene] ?? []).map((id) => findScale(id)!).filter(Boolean);
}

/** 曲の scale が場面の推奨の外なら注意の文章（内なら null）。 */
export function sceneScaleWarning(scene: string, scale: Scale): string | null {
  const rec = SCENE_SCALES[scene];
  if (!rec || rec.includes(scale.id)) return null;
  return `注意 scene「${scene}」のおすすめの音階は ${rec.map((id) => findScale(id)!.name).join("・")} です（${scale.name}は推奨の外。意図があれば、そのままで構いません）`;
}
