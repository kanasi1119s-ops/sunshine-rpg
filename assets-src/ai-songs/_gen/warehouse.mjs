import { build } from './lib.mjs';

const R4 = 'R:4';
const gA = 'r:0.5 f:0.5 t+:0.5 s+:0.5 f:0.5 t+:0.5 s+:0.5 f:0.5';
const gB = 'r:0.75 f:0.75 t+:0.5 R:0.5 s+:0.75 f:0.75';
const sA = 'r:1.5 R:0.5 r:0.5 R:0.5 r:1';
const sB = 'r:0.75 R:0.25 r:0.75 R:0.25 o:0.5 R:0.5 f:1';
const melA = ['R:1 B4:0.5 D5:0.5 E5:1.5 D5:0.5', 'E5:1 G5:0.5 E5:0.5 C5:2', 'C5:1 E5:0.5 G5:0.5 A5:1 G5:1', 'E5:2 R:1 B4:0.5 D5:0.5',
  'E5:0.5 G5:0.5 B5:1 A5:0.5 G5:0.5 E5:1', 'G5:1 E5:0.5 D5:0.5 C5:1 E5:1', 'D5:1 F#5:1 A5:1 F#5:1', 'D#5:1 F#5:1 A5:1 B5:1'];
const melB = ['E5:1 G5:1 B5:1 G5:1', 'F#5:1 A5:1 F#5:1 D5:1', 'G5:1.5 B5:0.5 G5:1 E5:1', 'F#5:1 D5:1 B4:2',
  'C6:1 B5:1 G5:1 E5:1', 'A5:1.5 G5:0.5 E5:1 C5:1', 'D#5:1 F#5:1 B5:2', 'A5:1 F#5:1 D#5:1 F#5:1'];
const melBr = ['G5:2 E5:2', 'C5:1 E5:1 G5:2', 'A5:1.5 G5:0.5 E5:2', 'D#5:1 F#5:1 A5:1 B5:1'];
const melB2 = ['G5:1 B5:1 C6:1 B5:1', 'A5:1 F#5:1 D5:2', 'B5:2 G5:1 E5:1', 'F#5:1 A5:1 F#5:1 D5:1', 'E5:1 G5:1 C6:2', 'C6:1 A5:1 G5:1 E5:1', 'F#5:2 D#5:2'];

build({
  id: 'warehouse', title: '夜の倉庫',
  description: 'Em のゆったりした R&B 調バンド曲（夜の密輸倉庫）。深い808の低音とハーフタイムのドラム、エレピのなめらかな旋律、ローファイなクリーンギターのアルペジオ。サビはコードが上へ流れ、ブリッジでいったん静まってから最後のサビへ。うしろめたい夜の空気の曲。',
  bpm: 84, beats: 4, tonic: 'E', mode: 'minor', feel: 'ballad', tone: 'prs',
  parts: [
    { id: 'keys', instrument: 'keys', role: 'エレピ（メロディ）', volume: 0.22, pan: 0.1 },
    { id: 'gtr', instrument: 'guitar', role: 'ローファイギター', volume: 0.14, pan: -0.4, amp: 'lofi', base: 43 },
    { id: 'echo', instrument: 'echoGuitar', role: 'エコーギター', volume: 0.1, pan: 0.45, amp: 'clean', base: 60 },
    { id: 'pad', instrument: 'pad', role: 'パッド', volume: 0.12, base: 48 },
    { id: 'sub', instrument: 'sub808', role: '808ベース', volume: 0.26, base: 24 },
    { id: 'kick', instrument: 'kick', role: 'キック', volume: 0.28 },
    { id: 'snare', instrument: 'snare', role: 'スネア', volume: 0.2 },
    { id: 'hat', instrument: 'hihat', role: 'ハイハット', volume: 0.08 },
  ],
  drums: {
    A: { k: 'x.....x..x......', s: '........x.......', h: 'x.x.x.x.x.x.x.x.' },
    B: { k: 'x.....x..x..x...', s: '....x.......x...', h: 'x.x.x.x.x.x.x.xx' },
    br: { k: 'x...............', s: '........x.......', h: 'x...x...x...x...' },
    end: { k: 'x...............' },
  },
  sections: [
    { name: 'intro', chords: 'Em7 Cmaj7', p: { gtr: gA, pad: 't:4', echo: ['R:4', 'f:4'] } },
    { name: 'A', chords: 'Em7 Cmaj7 Am7 Em7 Em7 Cmaj7 Bm7 B7', dr: 'A', ft: 'c', crash: false, p: { keys: melA, gtr: gA, pad: 't:4', sub: sA, echo: [R4, R4, R4, R4, 'f+:2 t+:2', 'f+:2 t+:2', 'f+:2 t+:2', 'f+:2 t+:2'] } },
    { name: 'B', chords: 'Cmaj7 D Em7 Bm7 Cmaj7 Am7 B7 B7', dr: 'B', ft: 'b', p: { keys: melB, gtr: gB, pad: 'f:4', sub: sB, echo: 'f+:2 t+:2' } },
    { name: 'bridge', chords: 'Cmaj7 Cmaj7 Am7 B7', dr: 'br', ft: 'c', p: { keys: melBr, gtr: gA, pad: 't:4', sub: 'r:4', echo: 'f+:4' } },
    { name: 'B2', chords: 'Cmaj7 D Em7 Bm7 Cmaj7 Am7 B7', dr: 'B', ft: 'b', nofill: false, p: { keys: melB2, gtr: gB, pad: 'f:4', sub: sB, echo: 'f+:2 t+:2' } },
    { name: 'end', chords: 'Em7', dr: 'end', nofill: true, p: { keys: 'E5:4', gtr: 'r:4', pad: 't:4', sub: 'r:4', echo: 'f:4' } },
  ],
});
