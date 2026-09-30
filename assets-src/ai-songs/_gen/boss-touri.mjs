import { build } from './lib.mjs';

const rA = 'r:0.75 r:0.75 r:0.5 R:0.5 r:0.5 f:0.5 r:0.5';
const rA2 = 'r:0.75 r:0.75 f:0.5 R:0.5 o:0.5 f:0.5 r:0.5';
const rB = 'r:0.5 R:0.5 r:0.5 r:0.5 o:0.5 R:0.5 r:0.5 o:0.5';
const rC = 'r:1.5 r:0.5 f:1 o:0.5 f:0.5';
const rBrk = 'r:0.5 R:1.5 r:0.5 R:1.5';
const rBr = 'r:2 f:2';
const bA = 'r:0.75 r:0.75 r:0.5 R:0.5 r:0.5 f:0.5 a:0.5';
const bB = 'r:1 r:0.5 o:0.5 r:1 f:0.5 a:0.5';
const bC = 'r:0.5 r:0.5 o:0.5 r:0.5 r:0.5 o:0.5 r:0.5 a:0.5';
const bBr = 'r:2 R:0.5 r:0.5 f:0.5 a:0.5';
const R4 = 'R:4';
const fin = 'G#5:0.5 B5:0.5 E6:1 B5:1 G#5:1';

const melA = [R4, 'R:2 A4:0.5 C5:0.5 E5:1', 'G5:0.75 G5:0.75 E5:0.5 C5:0.5 E5:0.5 G5:1', 'B5:0.75 A5:0.75 G5:0.5 D5:2',
  'A5:0.75 A5:0.75 E5:0.5 C5:0.5 E5:0.5 A5:1', 'G5:1 E5:1 C5:1 E5:1', 'A5:1 F5:1 C5:1 F5:0.5 A5:0.5', 'G#5:1 B5:1 E6:2'];
const melB = ['C6:1 A5:1 F5:1 A5:1', 'D6:1 B5:1 G5:1 B5:1', 'E6:1 C6:1 A5:1 C6:1', 'E6:0.5 D6:0.5 C6:1 G5:1 E5:1',
  'C6:1 F5:1 A5:1 C6:1', 'D6:1 G5:1 B5:1 D6:1', 'G#5:0.5 B5:0.5 E6:1 D6:0.5 B5:0.5 G#5:1', 'B5:2 G#5:1 E5:1'];
const melC = ['A5:1.5 C6:0.5 E6:2', 'D6:1 C6:1 G5:1 E5:1', 'B5:1.5 D6:0.5 G5:2', 'A5:1 D6:1 F#5:1 A5:1',
  'A5:1.5 C6:0.5 A5:1 F5:1', 'D6:1 B5:1 G5:1 D6:1', 'E6:1 D6:0.5 B5:0.5 G#5:1 B5:1', 'A5:3 R:1'];
const melC2 = [...melC.slice(0, 7), 'A5:2 E5:1 A5:1'];
const melA2 = ['E5:0.5 E5:0.5 D5:0.5 C5:1 A4:0.5 C5:0.5 E5:0.5', 'A5:0.75 G5:0.75 E5:0.5 C5:2', 'G5:0.5 G5:0.5 E5:0.5 C5:1.5 E5:0.5 G5:0.5',
  'B5:0.5 D6:0.5 B5:0.5 G5:1.5 D5:1', 'C6:1 A5:0.5 C6:0.5 E6:2', 'D6:0.5 C6:0.5 A5:1 E5:1 A5:1', 'A5:0.5 C6:0.5 F5:1 A5:1 C6:1',
  'B5:0.5 G#5:0.5 E5:0.5 G#5:0.5 B5:1 E6:1'];
const melBr = ['A5:2 C6:2', 'E6:3 D6:1', 'D6:2 B5:2', 'C6:2 A5:1 E5:1', 'F5:1.5 A5:0.5 C6:2', 'E6:2 G5:1 E5:1', 'G#5:1 B5:1 E6:2', 'D6:0.5 B5:0.5 G#5:1 E5:2'];
const melBrk = ['A4:1 R:1 A4:0.5 C5:0.5 E5:1', 'A5:2 G5:1 E5:1', 'F5:1 R:1 A5:1 C6:1', 'G#5:1 B5:1 E6:2'];
const melO = ['C6:1 A5:1 F5:2', 'D6:1 B5:1 G5:2', 'G#5:1 B5:1 E6:2', 'A5:4'];

build({
  id: 'boss-touri', title: '灯里の歪みとの決戦',
  description: 'Am の重く力強いロック調バンド曲（最初のボス戦）。3・3・2 のはずむディストーションリフに、弦の緊張が重なる。リードギターは「ミ・ミ・レ・ド」の動機で攻め、サビで高く駆け上がる。中盤は歌うように長く伸ばすギターの見せ場、ブレイクを経て最後のサビへ。',
  bpm: 172, beats: 4, tonic: 'A', mode: 'minor', feel: 'rock', tone: 'rock',
  parts: [
    { id: 'lead', instrument: 'leadGuitar', role: 'リードギター', volume: 0.26, pan: 0.2, amp: 'hardrock' },
    { id: 'dist', instrument: 'distGuitar', role: 'リフ', volume: 0.17, pan: -0.35, amp: 'hardrock', base: 40 },
    { id: 'bass', instrument: 'bass', role: 'ベース', volume: 0.22, amp: 'overdrive', base: 28 },
    { id: 'str', instrument: 'strings', role: '弦（緊張）', volume: 0.11, pan: 0, base: 48 },
    { id: 'kick', instrument: 'kick', role: 'キック', volume: 0.3 },
    { id: 'snare', instrument: 'snare', role: 'スネア', volume: 0.26 },
    { id: 'hat', instrument: 'hihat', role: 'ハイハット', volume: 0.11 },
    { id: 'crash', instrument: 'crash', role: 'クラッシュ', volume: 0.17 },
  ],
  drums: {
    intro: { k: 'x.......x.......', s: '....x.......x...', h: 'x.x.x.x.x.x.x.x.' },
    A: { k: 'x..x..x...x.x...', s: '....x.......x...', h: 'x.x.x.x.x.x.x.x.' },
    B: { k: 'x.x...x.x.x...x.', s: '....x.......x...', h: 'x.x.x.x.x.x.x.x.' },
    C: { k: 'x.x.x...x.x.x.x.', s: '....x.......x...', h: 'x.x.x.x.x.x.x.x.', c: 'x.......x.......' },
    bridge: { k: 'x.......x.......', s: '........x.......', h: 'x.x.x.x.x.x.x.x.' },
    brk: { k: 'x.....x.x.......', s: '........x.......' },
    end: { k: 'x...............', c: 'x...............' },
  },
  sections: [
    { name: 'intro', chords: 'Am F G E', dr: 'intro', ft: 'b', crash: false, p: { lead: [R4, R4, R4, fin], dist: rA, bass: bA, str: 'f:4' } },
    { name: 'A', chords: 'Am Am C G Am Am F E', dr: 'A', crash: true, ft: 'a', p: { lead: melA, dist: rA, bass: bA, str: R4 } },
    { name: 'B', chords: 'F G Am C F G E E', dr: 'B', ft: 'b', p: { lead: melB, dist: rB, bass: bB, str: 't:4' } },
    { name: 'C', chords: 'Am C G D F G E Am', dr: 'C', crash: true, ft: 'a', p: { lead: melC, dist: rC, bass: bC, str: 'f:2 r+:2' } },
    { name: 'A2', chords: 'Am Am C G Am Am F E', dr: 'A', crash: true, ft: 'a', p: { lead: melA2, dist: rA2, bass: bA, str: 't:4' } },
    { name: 'bridge', chords: 'F C G Am F C E E', dr: 'bridge', crash: true, ft: 'a', p: { lead: melBr, dist: rBr, bass: bBr, str: 'f:4' } },
    { name: 'break', chords: 'Am Am F E', dr: 'brk', crash: true, ft: 'b', p: { lead: melBrk, dist: rBrk, bass: 'r:2 R:1 r:1', str: 'f:4' } },
    { name: 'C2', chords: 'Am C G D F G E Am', dr: 'C', crash: true, ft: 'a', p: { lead: melC2, dist: rC, bass: bC, str: 'f:2 r+:2' } },
    { name: 'outro', chords: 'F G E Am', dr: 'C', ft: 'b', p: { lead: melO, dist: rC, bass: bC, str: 'f:2 r+:2' } },
    { name: 'end', chords: 'Am', dr: 'end', nofill: true, p: { lead: 'E5:4', dist: 'r:4', bass: 'r:4', str: 'f:4' } },
  ],
});
