import { build } from './lib.mjs';

const dA = 'r:0.5 R:0.25 r:0.25 r:0.5 R:0.5 r:0.25 r:0.25 r:0.5 o:0.5 R:0.5';
const dB = 'r:0.25 r:0.25 r:0.5 r:0.25 r:0.25 r:0.5 r:0.25 r:0.25 r:0.5 r:0.25 r:0.25 r:0.5';
const dC = 'r:1 R:0.5 r:0.5 o:1 f:1';
const dBr = 'r:0.5 r:0.5 r:0.5 R:0.5 r:0.5 r:0.5 r:0.5 R:0.5';
const dBrk = 'r:0.25 r:0.25 R:0.5 R:1 r:0.25 r:0.25 R:0.5 R:1';
const bA = 'r:0.5 R:0.25 r:0.25 o:0.5 R:0.25 f:0.25 r:0.5 R:0.25 r:0.25 o:0.5 a:0.5';
const bC = 'r:0.5 r:0.5 o:0.5 r:0.5 r:0.5 o:0.5 f:0.5 a:0.5';
const k8 = 'r:0.5 f:0.5 t+:0.5 f:0.5 r+:0.5 f:0.5 t+:0.5 f:0.5';
const k16 = 'r:0.25 f:0.25 t+:0.25 f:0.25 r:0.25 f:0.25 t+:0.25 f:0.25 r:0.25 f:0.25 t+:0.25 f:0.25 r:0.25 f:0.25 t+:0.25 f:0.25';
const kC = 'r+:0.75 r+:0.75 r+:0.5 R:0.5 f+:0.5 R:0.5 f+:0.5';
const R4 = 'R:4';
const iA = 'D6:0.75 D6:0.75 Bb5:0.5 F5:1 R:1';
const iC = 'E6:0.75 E6:0.75 C6:0.5 G5:1 R:1';
const melA5 = ['A5:0.5 A5:0.5 D6:0.5 F6:0.5 E6:0.5 D6:0.5 A5:1', 'F6:0.5 E6:0.5 D6:0.5 A5:0.5 F5:1 A5:1', 'G5:0.5 Bb5:0.5 D6:0.5 Bb5:0.5 G6:1 D6:1', 'C#6:0.5 E6:0.5 A6:1 G6:0.5 E6:0.5 C#6:1'];

const melA = [R4, 'R:3 A5:0.5 C6:0.5', iA, iC, ...melA5];
const melA2 = ['D6:0.5 D6:0.5 R:0.5 A5:0.5 D6:1 F6:1', 'E6:0.5 D6:0.5 A5:0.5 F5:0.5 A5:2', iA, iC, ...melA5];
const melB = ['D6:1 F6:1 Bb6:1 A6:1', 'G6:1 E6:1 C6:1 E6:1', 'F6:1 D6:1 A5:1 D6:1', 'A6:1 F6:1 C6:1 F6:1',
  'D6:0.5 F6:0.5 Bb6:1 F6:1 D6:1', 'E6:0.5 G6:0.5 C7:1 G6:1 E6:1', 'C#6:0.5 E6:0.5 A6:1 E6:0.5 C#6:0.5 A5:1', 'E6:2 C#6:1 A5:1'];
const melC = ['D6:1 A5:0.5 D6:0.5 F6:1 E6:0.5 D6:0.5', 'C6:1 A5:0.5 C6:0.5 F6:2', 'E6:1 G6:0.5 E6:0.5 C6:2', 'Bb5:1 D6:0.5 Bb5:0.5 G6:2',
  'F6:1 D6:0.5 F6:0.5 Bb6:2', 'A6:1 F6:0.5 A6:0.5 C7:2', 'C#6:1 E6:1 A6:1 G6:0.5 E6:0.5', 'D6:3 R:1'];
const melC2 = [...melC.slice(0, 7), 'D6:2 A5:1 D6:1'];
const melBr = ['G5:0.25 Bb5:0.25 D6:0.25 Bb5:0.25 G6:0.5 D6:0.5 Bb5:0.5 D6:0.5 G6:1', 'F6:0.5 D6:0.5 Bb5:0.5 G5:0.5 D6:1 Bb5:1',
  'A5:0.25 D6:0.25 F6:0.25 D6:0.25 A6:0.5 F6:0.5 D6:0.5 F6:0.5 A6:1', 'G6:0.5 F6:0.5 E6:0.5 D6:0.5 A5:2',
  'D6:0.5 F6:0.5 Bb6:0.5 F6:0.5 D6:0.5 F6:0.5 Bb6:1', 'A6:0.5 F6:0.5 D6:0.5 Bb5:0.5 F5:2',
  'C#6:0.25 E6:0.25 A6:0.25 E6:0.25 C#6:0.5 E6:0.5 A6:1 E6:1', 'E6:0.5 C#6:0.5 A5:0.5 E5:0.5 A5:2'];
const melBrk = ['D6:1 R:1 A5:0.5 D6:0.5 F6:1', 'A6:2 F6:1 D6:1', 'Bb5:1 R:1 D6:0.5 F6:0.5 Bb6:1', 'C#6:1 E6:1 A6:2'];
const melO = ['D6:1 F6:1 Bb6:2', 'E6:1 G6:1 C7:2', 'C#6:1 E6:1 A6:2', 'D6:4'];

build({
  id: 'boss-mugikano', title: '水涸れの歪み',
  description: 'Dm のエレクトリックなバンド曲（ボス戦「水涸れの歪み」）。四つ打ちのキックにシンセのアルペジオ、はずむスラップベース、ディストーションの刻みが重なる。シンセリードの跳ねるフックが、サビで一気に高い音へ跳ぶ。ブリッジは16分音符の速弾き、ブレイクのあと最後のサビへ。',
  bpm: 176, beats: 4, tonic: 'D', mode: 'minor', flat: true, feel: 'rock', tone: 'rock',
  parts: [
    { id: 'lead', instrument: 'lead', role: 'シンセリード', volume: 0.22, pan: 0.15 },
    { id: 'dist', instrument: 'distGuitar', role: 'ギターの刻み', volume: 0.16, pan: -0.4, amp: 'distortion', base: 40 },
    { id: 'bass', instrument: 'slap', role: 'スラップベース', volume: 0.22, base: 28 },
    { id: 'keys', instrument: 'keys', role: 'シンセアルペジオ', volume: 0.13, pan: 0.4, base: 48 },
    { id: 'kick', instrument: 'kick', role: 'キック', volume: 0.3 },
    { id: 'snare', instrument: 'snare', role: 'スネア', volume: 0.25 },
    { id: 'hat', instrument: 'hihat', role: 'ハイハット', volume: 0.1 },
    { id: 'crash', instrument: 'crash', role: 'クラッシュ', volume: 0.16 },
  ],
  drums: {
    intro: { k: 'x...x...x...x...', h: '..x...x...x...x.' },
    A: { k: 'x...x...x...x...', s: '....x.......x...', h: '..x...x...x...x.' },
    B: { k: 'x...x...x...x...', s: '....x.......x...', h: 'xxxxxxxxxxxxxxxx' },
    C: { k: 'x...x...x...x.x.', s: '....x.......x...', h: 'x.x.x.x.x.x.x.x.', c: 'x.......x.......' },
    bridge: { k: 'x.......x.......', s: '....x.......x...', h: 'x.x.x.x.x.x.x.x.' },
    brk: { k: 'x.......x.x.....', s: '........x.......' },
    end: { k: 'x...............', c: 'x...............' },
  },
  sections: [
    { name: 'intro', chords: 'Dm Dm Bb C', dr: 'intro', ft: 'a', crash: false, p: { lead: [R4, R4, R4, 'E6:0.5 G6:0.5 C7:1 G6:1 E6:1'], keys: k8 } },
    { name: 'A', chords: 'Dm Dm Bb C Dm Dm Gm A', dr: 'A', crash: true, ft: 'a', p: { lead: melA, dist: dA, bass: bA, keys: k8 } },
    { name: 'B', chords: 'Bb C Dm F Bb C A A', dr: 'B', ft: 'b', p: { lead: melB, dist: dB, bass: bA, keys: k16 } },
    { name: 'C', chords: 'Dm F C Gm Bb F A Dm', dr: 'C', crash: true, ft: 'a', p: { lead: melC, dist: dC, bass: bC, keys: kC } },
    { name: 'A2', chords: 'Dm Dm Bb C Dm Dm Gm A', dr: 'A', crash: true, ft: 'a', p: { lead: melA2, dist: dA, bass: bA, keys: k16 } },
    { name: 'bridge', chords: 'Gm Gm Dm Dm Bb Bb A A', dr: 'bridge', crash: true, ft: 'a', p: { lead: melBr, dist: dBr, bass: bC, keys: k8 } },
    { name: 'break', chords: 'Dm Dm Bb A', dr: 'brk', crash: true, ft: 'b', p: { lead: melBrk, dist: dBrk, bass: 'r:2 R:1 r:1', keys: 'R:4' } },
    { name: 'C2', chords: 'Dm F C Gm Bb F A Dm', dr: 'C', crash: true, ft: 'a', p: { lead: melC2, dist: dC, bass: bC, keys: kC } },
    { name: 'outro', chords: 'Bb C A Dm', dr: 'C', ft: 'b', p: { lead: melO, dist: dC, bass: bC, keys: kC } },
    { name: 'end', chords: 'Dm', dr: 'end', nofill: true, p: { lead: 'D6:4', dist: 'r:4', bass: 'r:4', keys: 'r:4' } },
  ],
});
