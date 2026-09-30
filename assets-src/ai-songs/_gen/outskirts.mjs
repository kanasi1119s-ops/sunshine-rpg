import { build } from './lib.mjs';

const gA = 'r:1 f:1 t+:1 f:1';
const gB = 'r:0.5 f:0.5 t+:0.5 f:0.5 r+:0.5 f:0.5 t+:0.5 f:0.5';
const bellA = ['R:4', 'R:2 A6:0.5 R:1.5', 'R:4', 'R:3 E6:0.5 R:0.5'];
const bellB = ['R:1 D6:0.5 A6:0.5 R:2', 'R:4', 'R:2.5 F6:0.5 R:1', 'R:4'];

const melA = [
  'A4:2 D5:1.5 E5:0.5', 'F5:3 R:1', 'E5:1 F5:1 A5:2', 'G5:2 E5:1 C5:1',
  'D5:1 F5:1 A5:2', 'G5:1.5 F5:0.5 D5:2', 'D5:1 F5:1 A5:1.5 G5:0.5', 'F5:2 E5:2',
];
const melB = [
  'D6:2 C6:1 A5:1', 'G5:1.5 E5:0.5 G5:2', 'A5:1 F5:1 D5:2', 'C6:1.5 A5:0.5 F5:2',
  'Bb5:2 A5:1 G5:1', 'F5:1 A5:1 D6:2', 'C#6:2 E6:1 D6:1', 'D6:3 R:1',
];
const melC = ['D6:1.5 C6:0.5 A5:2', 'G5:2 Bb5:2', 'A5:1 F5:1 D5:2', 'C#5:2 E5:2', 'D5:4'];

build({
  id: 'outskirts', title: '町外れの風',
  description: 'Dm のひろびろとした自然音楽ふうバンド曲（町外れ）。エコーのかかったギターの長い旋律、ゆっくりしたクリーンギターのアルペジオ、うすいパッドと、風のようなハイハット、ぽつんと落ちる鐘の音。低いタムが遠くの足音のように鳴る。',
  bpm: 70, beats: 4, tonic: 'D', mode: 'minor', flat: true, feel: 'ballad', tone: 'prs',
  parts: [
    { id: 'echo', instrument: 'echoGuitar', role: 'メロディ（風）', volume: 0.24, pan: 0.15, amp: 'shoegaze' },
    { id: 'gtr', instrument: 'guitar', role: 'クリーンアルペジオ', volume: 0.14, pan: -0.4, amp: 'clean', base: 43 },
    { id: 'pad', instrument: 'pad', role: 'パッド', volume: 0.13, pan: 0, base: 48 },
    { id: 'bass', instrument: 'bass', role: 'ベース', volume: 0.18, base: 28 },
    { id: 'kick', instrument: 'kick', role: 'キック', volume: 0.18 },
    { id: 'tom', instrument: 'tom', role: 'タム', volume: 0.16 },
    { id: 'hat', instrument: 'hihat', role: 'ハイハット', volume: 0.07 },
    { id: 'bell', instrument: 'bell', role: '鐘', volume: 0.1, pan: 0.4 },
  ],
  drums: {
    A: { k: 'x...............', t: '........x.......', h: 'x...x...x...x...' },
    B: { k: 'x.......x.......', t: '....x.......x...', h: 'x.x.x.x.x.x.x.x.' },
    end: { k: 'x...............' },
  },
  sections: [
    { name: 'intro', chords: 'Dm Bbmaj7', p: { gtr: gA, pad: 'f:4', bell: ['R:3 A6:0.5 R:0.5', 'R:4'], echo: ['R:4', 'R:4'] } },
    { name: 'A', chords: 'Dm Bbmaj7 Fmaj7 C Dm Gm7 Bbmaj7 Csus4', dr: 'A', ft: 'a', p: { echo: melA, gtr: gA, pad: 'f:4', bass: 'r:2 f:1.5 a:0.5', bell: bellA } },
    { name: 'B', chords: 'Bbmaj7 C Dm F Gm7 Dm A Dm', dr: 'B', ft: 'b', p: { echo: melB, gtr: gB, pad: 't+:2 f+:2', bass: 'r:1 R:1 r:1 f:0.5 a:0.5', bell: bellB } },
    { name: 'C', chords: 'Bbmaj7 Gm7 Dm A Dm', dr: 'A', ft: 'a', p: { echo: melC, gtr: gA, pad: 'f:4', bass: 'r:2 f:1.5 a:0.5', bell: 'R:4' } },
    { name: 'end', chords: 'Dm', dr: 'end', nofill: true, p: { echo: 'A4:4', gtr: 'r:4', pad: 'f:4', bass: 'r:4', bell: 'A6:4' } },
  ],
});
