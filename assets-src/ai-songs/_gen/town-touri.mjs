import { build } from './lib.mjs';

const pick = ['r:0.5 f:0.5 t+:0.5 f:0.5 r:0.5 f:0.5 t+:0.5 f:0.5', 'r:1 t:0.5 f:0.5 r+:1 f:0.5 t:0.5'];
const bass = 'r:1 f:1 r:1 f:0.5 a:0.5';
const bassB = 'r:1 r:0.5 f:0.5 r:1 t:0.5 a:0.5';
const cnt = 't:2 f:2';
const str = 'f:4';
const strB = 't:2 f:2';

const melA = [
  'D5:1.5 B4:0.5 G4:1 B4:1', 'D5:1 F#5:1 E5:1 D5:1', 'E5:1.5 D5:0.5 C5:1 B4:1', 'D5:2 R:1 D5:0.5 E5:0.5',
  'G5:1 E5:1 B4:1 E5:1', 'C5:1 E5:1 A5:1 G5:1', 'F#5:1.5 E5:0.5 D5:1 A4:1', 'D5:2.5 R:0.5 D5:0.5 E5:0.5',
];
const melB = [
  'E5:1 G5:1 E5:1 C5:1', 'F#5:1.5 A5:0.5 F#5:1 D5:1', 'D5:1 F#5:1 B5:1 A5:1', 'G5:2 E5:1 B4:1',
  'C5:1 E5:1 G5:1 B5:1', 'A5:1.5 G5:0.5 E5:1 C5:1', 'D5:1 F#5:1 A5:1 F#5:0.5 E5:0.5', 'G5:3 R:1',
];
const melA2 = [
  'D5:1 B4:0.5 D5:0.5 G5:1.5 D5:0.5', 'F#5:1 D5:1 B4:1 D5:1', 'E5:1 G5:1 B5:1 G5:1', 'D5:3 D5:0.5 E5:0.5',
  'G5:1.5 E5:0.5 G5:1 B5:1', 'A5:1 G5:1 E5:1 C5:1', 'F#5:1 A5:1 D6:1 A5:1', 'D6:2 B5:1 A5:1',
];
const melB2 = [...melB.slice(0, 7), 'G5:2 D5:2'];

build({
  id: 'town-touri', title: '灯里の朝',
  description: 'G長調のやさしいフォークバンド曲（灯里の町）。ピアノのメロディを、指弾きふうのクリーンギターとベース、軽いドラム、うすい弦が包む。二回目のAメロでは音が高くなり、サビで少し明るく広がる、朝の町のあたたかい曲。',
  bpm: 96, beats: 4, tonic: 'G', mode: 'major', feel: 'ballad', tone: 'prs',
  parts: [
    { id: 'pf', instrument: 'piano', role: 'メロディ', volume: 0.26, pan: 0.05 },
    { id: 'gtr', instrument: 'guitar', role: 'クリーンギター（指弾き）', volume: 0.17, pan: -0.4, amp: 'clean', base: 43 },
    { id: 'echo', instrument: 'echoGuitar', role: '対旋律', volume: 0.1, pan: 0.45, amp: 'clean', base: 60 },
    { id: 'str', instrument: 'strings', role: 'うすい弦', volume: 0.1, pan: -0.15, base: 48 },
    { id: 'bass', instrument: 'bass', role: 'ベース', volume: 0.2, base: 28 },
    { id: 'kick', instrument: 'kick', role: 'キック', volume: 0.2 },
    { id: 'snare', instrument: 'snare', role: 'スネア', volume: 0.16 },
    { id: 'hat', instrument: 'hihat', role: 'ハイハット', volume: 0.09 },
  ],
  drums: {
    soft: { k: 'x.......x.......', h: 'x.x.x.x.x.x.x.x.' },
    verse: { k: 'x.......x.......', s: '....x.......x...', h: 'x.x.x.x.x.x.x.x.' },
    chorus: { k: 'x.....x.x.x.....', s: '....x.......x...', h: 'x.x.x.x.x.x.x.x.' },
    end: { k: 'x...............' },
  },
  sections: [
    { name: 'intro', chords: 'G D', p: { pf: ['R:4', 'A4:1 D5:1 F#5:2'], gtr: pick, str } },
    { name: 'A', chords: 'G Bm Cmaj7 G Em Am7 D D', dr: 'soft', fill: 8, ft: 'c', p: { pf: melA, gtr: pick, str, bass: [bass] } },
    { name: 'B', chords: 'C D Bm7 Em7 Cmaj7 Am7 D G', dr: 'chorus', ft: 'c', p: { pf: melB, gtr: pick, echo: cnt, str: strB, bass: bassB } },
    { name: 'A2', chords: 'G Bm Cmaj7 G Em Am7 D D', dr: 'verse', fill: 8, ft: 'c', p: { pf: melA2, gtr: pick, echo: cnt, str, bass: bass } },
    { name: 'B2', chords: 'C D Bm7 Em7 Cmaj7 Am7 D G', dr: 'chorus', ft: 'c', p: { pf: melB2, gtr: pick, echo: cnt, str: strB, bass: bassB } },
    { name: 'outro', chords: 'Cmaj7 D', dr: 'soft', nofill: true, p: { pf: ['E5:2 G5:2', 'F#5:2 A5:2'], gtr: pick, str, bass: 'r:2 f:1 a:1' } },
    { name: 'end', chords: 'G', dr: 'end', nofill: true, p: { pf: 'G5:4', gtr: 'r:4', str: 'r:4', bass: 'r:4' } },
  ],
});
