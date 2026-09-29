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
const bgm: Entry[] = allEntries().map((e) => ({ group: e.group, title: e.title, scene: e.scene, style: e.styleLabel, score: getTrack(e.id) }));
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
