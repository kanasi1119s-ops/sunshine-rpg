import { build, rep } from './lib.mjs';

const arp8 = 'r:0.5 f:0.5 r+:0.5 t+:0.5 f:0.5 t+:0.5 r+:0.5 f:0.5';
const gA = 'r:0.5 t:0.5 f:0.5 t:0.5 r+:0.5 t:0.5 f:0.5 t:0.5';
const gC = 'r:0.25 f:0.25 t+:0.25 f:0.25 r:0.25 f:0.25 t+:0.25 f:0.25 r:0.25 f:0.25 t+:0.25 f:0.25 r:0.25 f:0.25 t+:0.25 f:0.25';
const bV = 'r:1.5 r:0.5 f:1 a:1';
const bB = 'r:1 r:0.5 r:0.5 f:0.5 r:0.5 o:0.5 a:0.5';
const bC = 'r:0.5 r:0.5 o:0.5 r:0.5 r:0.5 r:0.5 o:0.5 a:0.5';
const pStab = 'R:0.5 f+:0.5 R:0.5 f+:0.5 R:0.5 f+:0.5 R:0.5 f+:0.5';
const pHold = 'f:2 t+:2';

const melA = [
  'E5:1 G5:0.5 E5:0.5 D5:1 C5:1', 'B4:1 E5:1.5 D5:0.5 B4:1', 'A4:1 C5:1 E5:1 D5:0.5 C5:0.5', 'E5:2 R:1 G4:0.5 A4:0.5',
  'A4:1 C5:0.5 E5:1.5 D5:0.5 C5:0.5', 'D5:1 F5:1 A5:1 G5:0.5 F5:0.5', 'G5:1.5 F5:0.5 E5:1 D5:1', 'D5:2 R:1 D5:0.5 E5:0.5',
];
const melB = [
  'C5:1 E5:1 A5:1 G5:1', 'G5:1.5 E5:0.5 B4:1 E5:1', 'A5:1 G5:0.5 F5:0.5 E5:1 C5:1', 'D5:2 F5:1 A5:1',
  'C6:1 A5:1 F5:1 A5:1', 'B5:1.5 G5:0.5 E5:2', 'F5:1 A5:1 D6:1 C6:0.5 B5:0.5', 'B5:2 R:1 G5:0.5 A5:0.5',
];
const melC = [
  'C6:1.5 A5:0.5 F5:1 A5:1', 'G5:1.5 B5:0.5 D6:2', 'E6:1 D6:0.5 B5:0.5 G5:1 B5:1', 'C6:1 B5:0.5 A5:0.5 E5:2',
  'D6:1.5 C6:0.5 A5:1 F5:1', 'D6:1 Bb5:1 F5:1 D5:1', 'B5:1 D6:1 E6:1.5 D6:0.5', 'E6:3 R:1',
];
const melC2 = [...melC.slice(0, 7), 'E6:2 C6:1 G5:1'];
const melI = ['A5:0.5 C6:0.5 E6:1 D6:0.5 C6:0.5 A5:1', 'C6:1 A5:1 F5:1 A5:1', 'D6:1.5 C6:0.5 A5:1 F5:1', 'B5:1 D6:1 E6:2'];
const melO = ['A5:1.5 G5:0.5 F5:2', 'G5:2 B5:1 D6:1', 'E6:2 C6:1 G5:1', 'C6:4'];

const introMel = ['R:4', 'R:4', 'R:4', 'E5:0.5 G5:0.5 C6:1 G5:0.5 E5:0.5 D5:1'];

build({
  id: 'title', title: '灯りの約束',
  description: '明るい J-POP 調のバンド曲（タイトル画面）。ピアノとクリーンギターのアルペジオで始まり、サビでドラムとベースが走り出す。リードギターが「ミ・ソ・ミ・レ」の動機をくり返す、希望を感じる一曲。',
  bpm: 132, beats: 4, tonic: 'C', mode: 'major', feel: 'pop', tone: 'prs',
  parts: [
    { id: 'lead', instrument: 'leadGuitar', role: 'メロディ', volume: 0.27, pan: 0.1, amp: 'prs' },
    { id: 'gtr', instrument: 'guitar', role: 'クリーンギター', volume: 0.15, pan: -0.4, amp: 'clean', base: 43 },
    { id: 'pf', instrument: 'piano', role: 'ピアノ', volume: 0.15, pan: 0.3, base: 48 },
    { id: 'bass', instrument: 'bass', role: 'ベース', volume: 0.22, pan: 0, amp: 'auto', base: 28 },
    { id: 'kick', instrument: 'kick', role: 'キック', volume: 0.3 },
    { id: 'snare', instrument: 'snare', role: 'スネア', volume: 0.26 },
    { id: 'hat', instrument: 'hihat', role: 'ハイハット', volume: 0.12 },
    { id: 'crash', instrument: 'crash', role: 'クラッシュ', volume: 0.16 },
  ],
  drums: {
    intro: { k: 'x.......x.......', h: 'x.x.x.x.x.x.x.x.' },
    verse: { k: 'x.......x.x.....', s: '....x.......x...', h: 'x.x.x.x.x.x.x.x.' },
    pre: { k: 'x...x...x...x...', s: '....x.......x...', h: 'x.x.x.x.x.x.x.x.' },
    chorus: { k: 'x...x.x.x...x.x.', s: '....x.......x...', h: 'x.x.x.x.x.x.x.x.' },
    end: { k: 'x...............', c: 'x...............' },
  },
  sections: [
    { name: 'intro', chords: 'C G Fmaj7 G', dr: 'intro', crash: false, p: { lead: introMel, gtr: gA, pf: arp8, bass: ['R:4', 'R:4', 'r:2 r:1 a:1', 'r:2 r:1 a:1'] } },
    { name: 'A', chords: 'C Em Fmaj7 C Am Dm7 Gsus4 G', dr: 'verse', crash: true, p: { lead: melA, gtr: gA, pf: pHold, bass: bV } },
    { name: 'B', chords: 'Am Em Fmaj7 Dm7 Fmaj7 Em Dm7 G', dr: 'pre', ft: 'b', p: { lead: melB, gtr: gA, pf: arp8, bass: bB } },
    { name: 'chorus', chords: 'Fmaj7 G Em Am Dm7 Bb G C', dr: 'chorus', crash: true, p: { lead: melC, gtr: gC, pf: pStab, bass: bC } },
    { name: 'inter', chords: 'Am Fmaj7 Dm7 G', dr: 'pre', ft: 'b', p: { lead: melI, gtr: gA, pf: arp8, bass: bB } },
    { name: 'chorus2', chords: 'Fmaj7 G Em Am Dm7 Bb G C', dr: 'chorus', crash: true, p: { lead: melC2, gtr: gC, pf: pStab, bass: bC } },
    { name: 'outro', chords: 'Fmaj7 G C C', dr: 'verse', ft: 'c', p: { lead: melO, gtr: gA, pf: pHold, bass: bV } },
    { name: 'end', chords: 'C', dr: 'end', nofill: true, p: { lead: 'C5:4', gtr: 'r:4', pf: 'r:4', bass: 'r:4' } },
  ],
});
