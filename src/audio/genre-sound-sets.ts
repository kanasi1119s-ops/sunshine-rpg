// ジャンル別のサウンドセット（docs/sound/drum-genre-guide.md §7 の 1）。drum-genres.ts の表（drumMix・ドラム音源・ベース音源・型）から作る。
// 音量（parts）は、clear-guitar-rock と同じ規模の出発点で、耳で調整する前の目安。録音の数値分析は取り込んでいない。
import { DRUM_GENRES } from "./drum-genres";
import type { PartMix, SoundSet } from "./sound-sets";
import type { Instrument } from "./score";

const ID_TO_GENRE: Record<string, { genre: string; tone: "rock" | "metal"; ampGuitar: string; bassDuck: number }> = {
  "rock-band": { genre: "rock", tone: "rock", ampGuitar: "crunch", bassDuck: 0.2 },
  metal: { genre: "metal", tone: "metal", ampGuitar: "loudmetal", bassDuck: 0.25 },
  "jpop-anime": { genre: "jpop", tone: "rock", ampGuitar: "clean", bassDuck: 0.2 },
  ballad: { genre: "ballad", tone: "rock", ampGuitar: "clean", bassDuck: 0.1 },
  "jazz-swing": { genre: "jazz", tone: "rock", ampGuitar: "clean", bassDuck: 0 },
  "funk-tight": { genre: "funk", tone: "rock", ampGuitar: "clean", bassDuck: 0.2 },
  "hiphop-boombap": { genre: "hiphop", tone: "rock", ampGuitar: "clean", bassDuck: 0.3 },
  trap: { genre: "trap", tone: "rock", ampGuitar: "clean", bassDuck: 0.35 },
  house: { genre: "house", tone: "rock", ampGuitar: "clean", bassDuck: 0.35 },
  dnb: { genre: "dnb", tone: "rock", ampGuitar: "clean", bassDuck: 0.3 },
  reggae: { genre: "reggae", tone: "rock", ampGuitar: "clean", bassDuck: 0.1 },
  bossa: { genre: "bossa", tone: "rock", ampGuitar: "clean", bassDuck: 0 },
  "game-battle": { genre: "battle", tone: "rock", ampGuitar: "crunch", bassDuck: 0.2 },
  "game-boss": { genre: "boss", tone: "metal", ampGuitar: "loudrock", bassDuck: 0.25 },
};

function build(id: string): SoundSet {
  const meta = ID_TO_GENRE[id];
  const g = DRUM_GENRES[meta.genre];
  const soft = ["ballad", "jazz", "bossa", "reggae", "field"].includes(meta.genre);
  const parts: Partial<Record<Instrument, PartMix>> = {
    kick: { volume: soft ? 0.06 : 0.09 }, snare: { volume: soft ? 0.045 : 0.065 }, hihat: { volume: 0.03 }, crash: { volume: 0.032 }, tom: { volume: 0.05 },
    bass: { volume: 0.095, bright: meta.genre === "reggae" ? -0.4 : 0.2, ...(meta.bassDuck ? { duck: meta.bassDuck } : {}) },
    sub808: { volume: 0.09, duck: meta.bassDuck },
    guitar: { volume: 0.16, amp: { type: "clean" }, reverb: 0.15, panWidth: 0.5 },
    crunch: { volume: 0.12, amp: { type: "crunch" }, panWidth: 0.55 },
    distGuitar: { volume: 0.09, amp: { type: meta.tone === "metal" ? "loudmetal" : "loudrock" }, panWidth: 0.8 },
    piano: { volume: 0.1, reverb: 0.2 }, keys: { volume: 0.08, reverb: 0.2 }, strings: { volume: 0.06, reverb: 0.5 }, bell: { volume: 0.05, reverb: 0.4 },
  };
  const grids = g.grids;
  return {
    id, label: `${g.label}（ジャンル別の出発点）`,
    description: `${g.label}の drumMix・ドラム音源（${g.drums}）・ベース音源（${g.bass}）をまとめて当てはめる。音量は出発点で、聴いて調整する。`,
    source: "docs/sound/drum-genre-guide.md §2（ジャンルの一般的な基本形を16分の位置に置き直したもの。特定の曲の写しではない）。録音の数値分析は取り込んでいない",
    overlays: { bass: g.bass, drums: g.drums, guitar: "gretsch" },
    tone: meta.tone, human: g.human,
    parts,
    drumMix: JSON.parse(JSON.stringify(g.drumMix)),
    tempoHint: g.bpm,
    drumPatterns: { [`${meta.genre}-kick`]: grids.kick, [`${meta.genre}-snare`]: grids.snare, [`${meta.genre}-hat`]: grids.hat },
  };
}

export const GENRE_SOUND_SETS: Record<string, SoundSet> = Object.fromEntries(Object.keys(ID_TO_GENRE).map((id) => [id, build(id)]));
