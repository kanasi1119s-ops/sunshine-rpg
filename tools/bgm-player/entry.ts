// BGMプレイヤー用の入り口。ゲーム本体と同じ再生エンジン（AudioEngine）と曲データをそのまま使う。
import { AudioEngine } from "../../src/audio/audio-engine";
import { getScoreDurationSec, type Score } from "../../src/audio/score";
import { CATALOG, getTrack } from "../../src/audio/catalog";
import { SE_LIBRARY } from "../../src/audio/se-library";

interface Entry { group: string; title: string; score: Score; scene?: string; style?: string }
const bgm: Entry[] = CATALOG.map((e) => ({ group: e.group, title: e.title, scene: e.scene, style: e.styleLabel, score: getTrack(e.id) }));
const effects: Entry[] = SE_LIBRARY.map((e) => ({ group: e.group, title: e.name, score: e.score }));
const engine = new AudioEngine();
(window as unknown as { BGM: unknown }).BGM = {
  bgm: bgm.map((e) => ({ group: e.group, title: e.title, scene: e.scene, style: e.style, bpm: e.score.tempoBpm, sec: getScoreDurationSec(e.score) })),
  effects: effects.map((e) => ({ group: e.group, title: e.title })),
  play: (i: number, offset = 0) => engine.playBgm(bgm[i].score, offset),
  pos: () => engine.getBgmPositionSec(),
  stop: () => engine.stopBgm(),
  playSe: (i: number) => engine.playSe(effects[i].score),
  volume: (v: number) => engine.setBgmVolume(v),
};
