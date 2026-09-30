import { build } from './lib.mjs';

const gal = 'r:0.5 r:0.25 r:0.25 r:0.5 r:0.25 r:0.25 r:0.5 r:0.25 r:0.25 r:0.5 r:0.25 r:0.25';
const drive = 'r:0.5 r:0.5 r:0.5 r:0.5 r:0.5 r:0.5 r:0.5 r:0.5';
const pow = 'r:1 f:0.5 r:0.5 o:1 f:0.5 r:0.5';
const rifB = 'r:0.5 r:0.5 R:0.5 r:0.5 r:0.5 R:0.5 f:0.5 o:0.5';
const brk = 'r:1 R:1 r:0.5 r:0.5 R:1';
const bGal = 'r:0.5 r:0.5 r:0.5 r:0.5 r:0.5 r:0.5 r:0.5 a:0.5';
const bCh = 'r:0.5 o:0.5 r:0.5 o:0.5 r:0.5 o:0.5 r:0.5 a:0.5';
const bBrk = 'r:2 R:1 r:1';
const R4 = 'R:4';
const bSol = 'F#5:0.5 B5:0.5 D#6:1 B5:1 F#5:1';

const melA = [R4, R4, R4, R4, R4, R4, 'D5:0.5 G5:0.5 B5:1 A5:0.5 G5:0.5 D5:1', bSol];
const melB = [
  'A4:1 C5:1 E5:1 A5:1', 'G5:1 E5:1 C5:1 E5:1', 'F#5:1 A5:1 D6:1 A5:1', 'G5:1.5 B5:0.5 E6:2',
  'E6:1 C6:1 A5:1 E5:1', 'G5:1 C6:1 E6:1 C6:1', 'D#6:1 B5:1 F#5:1 B5:1', 'D#6:2 F#5:1 R:1',
];
const melC = [
  'E5:1 G5:0.5 C6:0.5 E6:2', 'D6:1 B5:1 G5:2', 'A5:1 D6:1 C#6:1 A5:1', 'B5:1.5 G5:0.5 E5:2',
  'E5:1 G5:0.5 C6:0.5 E6:2', 'D6:1 B5:0.5 D6:0.5 G5:2', 'F#5:1 B5:1 D#6:1 B5:1', 'E6:2 B5:1 G5:1',
];
const melC2 = [...melC.slice(0, 7), 'E6:2 G5:1 E5:1'];
const melA2 = [
  'B4:0.5 E5:0.5 G5:0.5 E5:0.5 B5:1 G5:1', 'F#5:0.5 A5:0.5 B5:1 G5:1 E5:1', 'C5:0.5 E5:0.5 G5:0.5 E5:0.5 C6:1 G5:1',
  'D5:0.5 F#5:0.5 A5:0.5 F#5:0.5 D6:1 A5:1', 'E5:0.5 G5:0.5 B5:0.5 G5:0.5 E6:1 B5:1', 'D6:0.5 B5:0.5 G5:1 E5:1 G5:1',
  'G5:0.5 B5:0.5 D6:1 B5:1 G5:1', bSol,
];
const melSolo = [
  'E5:0.25 G5:0.25 B5:0.25 G5:0.25 E6:0.5 B5:0.5 G5:0.5 B5:0.5 E6:1', 'D6:0.5 B5:0.5 G5:0.5 B5:0.5 D6:1 C6:0.5 B5:0.5',
  'F#5:0.5 A5:0.5 D6:1 C#6:0.5 D6:0.5 E6:1', 'E6:1 C#6:1 A5:1 E5:1',
  'B5:0.5 E6:0.5 B5:0.5 G5:0.5 E5:1 G5:1', 'D6:1 B5:0.5 G5:0.5 B5:1 D6:1',
  'E6:0.5 D6:0.5 C6:0.5 G5:0.5 E5:1 C5:1', 'D#6:1 B5:1 F#5:1 D#5:1',
];
const melBrk = ['E5:1 R:1 E5:0.5 G5:0.5 B5:1', 'E6:2 D6:1 B5:1', 'G5:1 R:1 G5:0.5 B5:0.5 D6:1', 'D#6:1 F#5:1 B5:2'];
const melO = ['E5:1 G5:0.5 C6:0.5 E6:2', 'D6:1 A5:1 F#5:2', 'G5:1 B5:1 E6:2', 'E6:4'];

build({
  id: 'battle', title: '戦いの合図',
  description: 'Em の疾走するハードコア調バンド曲（通常戦闘）。ギャロップのディストーションリフ、スキャンク（スネアが裏拍）のドラム、リードギターの「ミ・ソ・シ」の駆け上がり。サビで低音が2倍に刻み、中盤のギターソロ、ハーフタイムのブレイクダウンを経て最後のサビへなだれこむ。',
  bpm: 184, beats: 4, tonic: 'E', mode: 'minor', feel: 'rock', tone: 'metal',
  parts: [
    { id: 'lead', instrument: 'leadGuitar', role: 'リードギター', volume: 0.25, pan: 0.2, amp: 'metal' },
    { id: 'dist', instrument: 'distGuitar', role: 'リフ', volume: 0.17, pan: -0.35, amp: 'metal', base: 40 },
    { id: 'bass', instrument: 'bass', role: 'ベース', volume: 0.22, amp: 'overdrive', base: 28 },
    { id: 'kick', instrument: 'kick', role: 'キック', volume: 0.32 },
    { id: 'snare', instrument: 'snare', role: 'スネア', volume: 0.26 },
    { id: 'hat', instrument: 'hihat', role: 'ハイハット', volume: 0.1 },
    { id: 'crash', instrument: 'crash', role: 'クラッシュ', volume: 0.16 },
    { id: 'tom', instrument: 'tom', role: 'タム', volume: 0.2 },
  ],
  drums: {
    intro: { k: 'x.x.x.x.x.x.x.x.', s: '....x.......x...', h: 'x.x.x.x.x.x.x.x.' },
    A: { k: 'x.x.x...x.x.x...', s: '....x.......x...', h: 'x.x.x.x.x.x.x.x.' },
    B: { k: 'x.x.x.x.x.x.x.x.', s: '....x.......x...', h: 'x.x.x.x.x.x.x.x.' },
    C: { k: 'x...x...x...x...', s: '..x...x...x...x.', h: 'xxxxxxxxxxxxxxxx' },
    brk: { k: 'x.......x.x.....', s: '........x.......', h: 'x...x...x...x...' },
    end: { k: 'x...............', c: 'x...............' },
  },
  sections: [
    { name: 'intro', chords: 'Em C D B', dr: 'intro', ft: 'b', p: { lead: [R4, R4, R4, bSol], dist: gal, bass: bGal } },
    { name: 'A', chords: 'Em Em C D Em Em G B', dr: 'A', crash: true, ft: 'a', p: { lead: melA, dist: gal, bass: bGal } },
    { name: 'B', chords: 'Am C D Em Am C B B', dr: 'B', ft: 'b', p: { lead: melB, dist: rifB, bass: bGal } },
    { name: 'C', chords: 'C G D Em C G B Em', dr: 'C', crash: true, ft: 'a', p: { lead: melC, dist: pow, bass: bCh } },
    { name: 'A2', chords: 'Em Em C D Em Em G B', dr: 'A', crash: true, ft: 'a', p: { lead: melA2, dist: gal, bass: bGal } },
    { name: 'solo', chords: 'Em G D A Em G C B', dr: 'B', crash: true, ft: 'a', p: { lead: melSolo, dist: drive, bass: bGal } },
    { name: 'break', chords: 'Em Em Em B', dr: 'brk', crash: true, ft: 'b', p: { lead: melBrk, dist: brk, bass: bBrk } },
    { name: 'C2', chords: 'C G D Em C G B Em', dr: 'C', crash: true, ft: 'a', p: { lead: melC2, dist: pow, bass: bCh } },
    { name: 'outro', chords: 'C D Em Em', dr: 'C', ft: 'b', p: { lead: melO, dist: pow, bass: bCh } },
    { name: 'end', chords: 'Em', dr: 'end', nofill: true, p: { lead: 'E5:4', dist: 'r:4', bass: 'r:4' } },
  ],
});
