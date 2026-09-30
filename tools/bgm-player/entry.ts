// BGMプレイヤー用の入り口。ゲーム本体と同じ再生エンジン（AudioEngine）と曲データをそのまま使う。
import soundfontUrl from "../../src/audio/soundfont/game.sf3?url";
import processorUrl from "spessasynth_lib/dist/spessasynth_processor.min.js?url";
import { AudioEngine } from "../../src/audio/audio-engine";
import { getScoreDurationSec, type Score } from "../../src/audio/score";
import { allEntries, getTrack } from "../../src/audio/catalog";
import "../../src/audio/user-songs";
import { ps2Edition } from "../../src/audio/ps2-edition";
import { realEdition } from "../../src/audio/real-edition";
import { SE_LIBRARY } from "../../src/audio/se-library";

interface Entry { group: string; title: string; score: Score; scene?: string; style?: string }
// 章ごとに並べる: グループ（章）は、組み込みの曲の並び（序章→各章→終章→クリア後→イベント）の順、追加した曲のグループは最後。
// 同じ章の中では、元の曲のすぐ後ろに、従来版（-old）・きれいな版（-clean）・クリーン連打版（-cleanpick）・空間版（-space）を並べる。
const all = allEntries();
const baseOf = (id: string): string => id.replace(/-(old|clean|cleanpick|space)$/, "");
const variantRank = (id: string): number => (id.endsWith("-old") ? 1 : id.endsWith("-cleanpick") ? 2 : id.endsWith("-space") ? 3 : id.endsWith("-clean") ? 4 : 0);
// 変種（きれいな版・クリーン連打版・空間版・従来版）は、元の曲と同じ章に入れる
const groupOfId = new Map(all.map((e) => [e.id, e.group]));
const chapterOf = (e: { id: string; group: string }): string => (baseOf(e.id) !== e.id ? groupOfId.get(baseOf(e.id)) ?? e.group : e.group);
// 章の並び: 序章 → 第1〜8章 → 終章 → 共通 → クリア後 → イベント → 追加した曲
const groupRank = (g: string): number => {
  if (g.startsWith("序章")) return 0;
  const m = /^第(\d+)章/.exec(g);
  if (m) return Number(m[1]);
  if (g.startsWith("終章")) return 10;
  if (g.startsWith("共通")) return 11 + (["共通・フィールド", "共通・町", "共通・ダンジョン", "共通・戦闘", "共通・イベント"].indexOf(g) + 1);
  if (g === "クリア後") return 20;
  if (g === "イベント") return 21;
  return 30;
};
const firstIndex = new Map<string, number>();
all.forEach((e, i) => { const b = baseOf(e.id); if (!firstIndex.has(b)) firstIndex.set(b, i); });
const sorted = all.map((e) => ({ ...e, group: chapterOf(e) })).sort((a, b) => groupRank(a.group) - groupRank(b.group) || (a.group < b.group ? -1 : a.group > b.group ? 1 : 0) || (firstIndex.get(baseOf(a.id)) ?? 0) - (firstIndex.get(baseOf(b.id)) ?? 0) || variantRank(a.id) - variantRank(b.id));
const bgm: Entry[] = sorted.map((e) => ({ group: e.group, title: e.title, scene: e.scene, style: e.styleLabel, score: getTrack(e.id) }));
const effects: Entry[] = SE_LIBRARY.map((e) => ({ group: e.group, title: e.name, score: e.score }));
// 1ファイルのHTMLでは外部ファイルを読み込めないので、埋め込んだ素材（データURL）を、録音音源の再生に渡す
function bytesOf(dataUrl: string): Uint8Array {
  const bin = atob(dataUrl.slice(dataUrl.indexOf(",") + 1));
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}
try {
  globalThis.__sampledAssets = {
    soundfont: bytesOf(soundfontUrl).buffer as ArrayBuffer,
    // データURLのまま渡す（file:// で開いたときも読める。Blob URLだと読み込めないことがある）
    processorUrl,
  };
} catch (error) {
  console.warn("録音音源の埋め込みを読めませんでした:", error);
}
const engine = new AudioEngine();
let edition: "modern" | "ps2" | "real" = "modern";
const bgmPs2 = bgm.map((e) => ps2Edition(e.score));
const bgmReal = bgm.map((e) => realEdition(e.score));
(window as unknown as { BGM: unknown }).BGM = {
  bgm: bgm.map((e) => ({ group: e.group, title: e.title, scene: e.scene, style: e.style, bpm: e.score.tempoBpm, sec: getScoreDurationSec(e.score) })),
  effects: effects.map((e) => ({ group: e.group, title: e.title })),
  play: (i: number, offset = 0) => engine.playBgm(edition === "ps2" ? bgmPs2[i] : edition === "real" ? bgmReal[i] : bgm[i].score, offset),
  setEdition: (name: "modern" | "ps2" | "real") => {
    edition = name;
  },
  pos: () => engine.getBgmPositionSec(),
  seek: (sec: number) => engine.seekBgm(sec),
  stop: () => engine.stopBgm(),
  playSe: (i: number) => engine.playSe(effects[i].score),
  volume: (v: number) => engine.setBgmVolume(v),
  synthOnly: (on: boolean) => engine.setSynthOnly(on),
  sampled: () => engine.isSampledReady(),
};
