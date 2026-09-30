import { build } from './lib.mjs';

const R4 = 'R:4';
const gA = 'r:1 f:1 t+:1 f:1';
const gB = 'r:0.5 f:0.5 t+:1 f:0.5 t+:0.5 r+:1';
const melA = ['E5:1.5 R:0.5 C5:1 A4:1', 'A4:1 C5:1 E5:2', 'D5:1.5 F5:0.5 A5:2', 'E5:2 R:2', 'C5:1 E5:1 A5:2', 'G5:1 F5:1 C5:2', 'F5:2 G5:1 E5:1', 'G#5:1 B5:1 E6:2'];
const melB = ['F5:1 A5:1 C6:2', 'E6:1.5 C6:0.5 A5:2', 'C6:1 A5:1 F5:2', 'G5:1 C6:1 E6:2', 'D6:2 C6:1 A5:1', 'A5:1 E5:1 C6:1 A5:1', 'B5:1 G#5:1 E5:2', 'G#5:1 B5:1 E6:1 D6:1'];
const melR = ['E5:1.5 C5:0.5 A4:2', 'A4:1 C5:1 F5:2', 'G#4:1 B4:1 E5:2', 'A4:4'];

build({
  id: 'water-source', title: '涸れゆく水源',
  description: 'Am のゆっくりとした自然音楽ふうバンド曲（水源・採掘跡）。ピアノが、ぽつり、ぽつりと水のしずくのように旋律を落とし、エコーのギター、クリーンギターのアルペジオ、パッドが乾いた空気を作る。ドラムはキックと低いタムだけの静かなリズム。中ほどで音が高く広がり、最後はしずくが止まるように終わる。',
  bpm: 64, beats: 4, tonic: 'A', mode: 'minor', feel: 'ballad', tone: 'prs',
  parts: [
    { id: 'pf', instrument: 'piano', role: 'メロディ（しずく）', volume: 0.22, pan: 0.1 },
    { id: 'echo', instrument: 'echoGuitar', role: 'エコーギター', volume: 0.12, pan: 0.45, amp: 'shoegaze', base: 60 },
    { id: 'gtr', instrument: 'guitar', role: 'クリーンアルペジオ', volume: 0.13, pan: -0.4, amp: 'clean', base: 43 },
    { id: 'pad', instrument: 'pad', role: 'パッド', volume: 0.12, base: 48 },
    { id: 'bass', instrument: 'bass', role: 'ベース', volume: 0.17, base: 28 },
    { id: 'kick', instrument: 'kick', role: 'キック', volume: 0.16 },
    { id: 'tom', instrument: 'tom', role: '低いタム', volume: 0.15 },
    { id: 'hat', instrument: 'hihat', role: 'ハイハット', volume: 0.06 },
  ],
  drums: {
    A: { k: 'x...............', t: '........x.......' },
    B: { k: 'x.......x.......', t: '..x.......x.....', h: 'x...x...x...x...' },
    end: { k: 'x...............' },
  },
  sections: [
    { name: 'intro', chords: 'Am Fmaj7', p: { echo: ['A4:4', 'C5:4'], gtr: gA, pad: 't:4' } },
    { name: 'A', chords: 'Am Fmaj7 Dm7 Am Am Fmaj7 Csus4 E', dr: 'A', fill: 8, ft: 'a', p: { pf: melA, echo: [R4, R4, R4, R4, 't+:4', 'f:4', 't+:4', 'f:4'], gtr: gA, pad: 't:4', bass: 'r:4' } },
    { name: 'B', chords: 'Dm7 Am Fmaj7 C Dm7 Am E E', dr: 'B', fill: 8, ft: 'b', p: { pf: melB, echo: 't+:2 f+:2', gtr: gB, pad: 'f:4', bass: 'r:2 f:1.5 a:0.5' } },
    { name: 'reprise', chords: 'Am Fmaj7 E Am', dr: 'A', nofill: true, p: { pf: melR, echo: 'f:4', gtr: gA, pad: 't:4', bass: 'r:4' } },
    { name: 'end', chords: 'Dm7 Am', dr: 'end', nofill: true, p: { pf: ['D5:2 F5:2', 'A4:4'], echo: ['A4:4', 'E5:4'], gtr: ['r:4', 'r:4'], pad: 'f:4', bass: 'r:4' } },
  ],
});
