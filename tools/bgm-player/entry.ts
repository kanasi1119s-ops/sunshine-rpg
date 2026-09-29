// BGMプレイヤー用の入り口。ゲーム本体と同じ再生エンジン（AudioEngine）と曲データをそのまま使う。
import { AudioEngine } from "../../src/audio/audio-engine";
import { getScoreDurationSec, type Score } from "../../src/audio/score";
import * as c0 from "../../src/audio/chapter0-tracks";
import * as c1 from "../../src/audio/chapter1-tracks";
import * as c2 from "../../src/audio/chapter2-tracks";
import * as c3 from "../../src/audio/chapter3-tracks";
import * as c4 from "../../src/audio/chapter4-tracks";
import * as c5 from "../../src/audio/chapter5-tracks";
import * as c6 from "../../src/audio/chapter6-tracks";
import { STYLE_TRACKS } from "../../src/audio/style-tracks";
import { SE_LIBRARY } from "../../src/audio/se-library";

interface Entry { group: string; title: string; score: Score }
const bgm: Entry[] = [
  { group: "序章 灯里", title: "タイトル・灯りのテーマ", score: c0.CHAPTER0_TITLE_THEME },
  { group: "序章 灯里", title: "灯里の町", score: c0.CHAPTER0_TOWN_THEME },
  { group: "序章 灯里", title: "町外れ", score: c0.CHAPTER0_OUTSKIRTS_THEME },
  { group: "序章 灯里", title: "通常戦闘", score: c0.CHAPTER0_BATTLE_THEME },
  { group: "序章 灯里", title: "ボス戦「灯里の歪み」", score: c0.CHAPTER0_BOSS_THEME },
  { group: "第1章 麦香野", title: "麦香野の村", score: c1.CHAPTER1_VILLAGE_THEME },
  { group: "第1章 麦香野", title: "水源", score: c1.CHAPTER1_WATER_SOURCE_THEME },
  { group: "第1章 麦香野", title: "ボス戦「水涸れの歪み」", score: c1.CHAPTER1_BOSS_THEME },
  { group: "第2章 硝子湖", title: "硝子湖の町", score: c2.CHAPTER2_TOWN_THEME },
  { group: "第2章 硝子湖", title: "密輸倉庫", score: c2.CHAPTER2_WAREHOUSE_THEME },
  { group: "第2章 硝子湖", title: "ボス戦「積荷の歪み」", score: c2.CHAPTER2_BOSS_THEME },
  { group: "第3章 鉄鏈鉱山", title: "鉄鏈鉱山の町", score: c3.CHAPTER3_TOWN_THEME },
  { group: "第3章 鉄鏈鉱山", title: "坑内", score: c3.CHAPTER3_MINE_THEME },
  { group: "第3章 鉄鏈鉱山", title: "ボス戦「実験の歪み」", score: c3.CHAPTER3_BOSS_THEME },
  { group: "第4章 砂音", title: "砂音の町", score: c4.CHAPTER4_TOWN_THEME },
  { group: "第4章 砂音", title: "隊商の野営地", score: c4.CHAPTER4_CAMP_THEME },
  { group: "第4章 砂音", title: "ボス戦「砂嵐の歪み」", score: c4.CHAPTER4_BOSS_THEME },
  { group: "第5章 霧断崖", title: "霧断崖の町", score: c5.CHAPTER5_TOWN_THEME },
  { group: "第5章 霧断崖", title: "記録の間", score: c5.CHAPTER5_ARCHIVE_THEME },
  { group: "第5章 霧断崖", title: "ボス戦「予言の歪み」", score: c5.CHAPTER5_BOSS_THEME },
  { group: "第6章 霜原", title: "霜原の町", score: c6.CHAPTER6_TOWN_THEME },
  { group: "第6章 霜原", title: "戦跡の施設", score: c6.CHAPTER6_FACILITY_THEME },
  { group: "第6章 霜原", title: "ボス戦「試作機の歪み」", score: c6.CHAPTER6_BOSS_THEME },
];
bgm.push(...STYLE_TRACKS.map((t) => ({ group: "新曲・スタイル別", title: `${t.title}（${t.style}）`, score: t.score })));
const effects: Entry[] = SE_LIBRARY.map((e) => ({ group: e.group, title: e.name, score: e.score }));
const engine = new AudioEngine();
(window as unknown as { BGM: unknown }).BGM = {
  bgm: bgm.map((e) => ({ group: e.group, title: e.title, bpm: e.score.tempoBpm, sec: getScoreDurationSec(e.score) })),
  effects: effects.map((e) => ({ group: e.group, title: e.title })),
  play: (i: number, offset = 0) => engine.playBgm(bgm[i].score, offset),
  pos: () => engine.getBgmPositionSec(),
  stop: () => engine.stopBgm(),
  playSe: (i: number) => engine.playSe(effects[i].score),
  volume: (v: number) => engine.setBgmVolume(v),
};
