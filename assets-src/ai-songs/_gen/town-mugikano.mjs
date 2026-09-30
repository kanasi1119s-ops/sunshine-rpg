import { build } from './lib.mjs';

const gtr = 'r:1 f:0.5 t+:0.5 f:0.5 t+:0.5';
const gtrB = 'r:0.5 f:0.5 t+:0.5 f:0.5 t+:0.5 f:0.5';
const bass = 'r:1 f:1 f:0.5 a:0.5';
const bassB = 'r:1 R:0.5 f:0.5 r+:0.5 a:0.5';
const cr = 'R:1 t+:1 f+:1';
const R3 = 'R:3';
const bellB = 'f:1 t+:1 r+:1';

const melA = ['A4:1 C5:1 F5:1', 'E5:2 C5:1', 'D5:1 F5:1 Bb5:1', 'A5:2 F5:1', 'D5:1 F5:1 A5:1', 'G5:1.5 F5:0.5 D5:1', 'E5:1 G5:1 C6:1', 'F5:2 E5:1'];
const melB = ['Bb5:1 A5:1 F5:1', 'G5:1 E5:1 G5:1', 'A5:1 C6:1 A5:1', 'A5:1 F5:1 D5:1', 'Bb5:1 G5:1 D5:1', 'G5:1.5 E5:0.5 C5:1', 'A5:1 C6:1 A5:1', 'F5:3'];
const melB2 = [...melB.slice(0, 7), 'F5:2 C5:1'];
const melBr = ['F4:1 A4:1 D5:1', 'E5:1 C5:1 A4:1', 'D5:1 F5:1 D5:1', 'C5:2 A4:1', 'Bb4:1 D5:1 G5:1', 'F5:1 A5:1 F5:1', 'F5:2 E5:1', 'G5:1 E5:1 C5:1'];
const melA2 = ['C5:1 F5:1 A5:1', 'C6:2 A5:1', 'Bb5:1 F5:1 D5:1', 'F5:1.5 G5:0.5 A5:1', 'A5:1 F5:1 A5:1', 'Bb5:1 A5:0.5 G5:0.5 F5:1', 'G5:1 C6:1 G5:1', 'F5:1 G5:1 E5:1'];

build({
  id: 'town-mugikano', title: '麦香野の風車',
  description: 'F長調の3拍子のフォークバンド曲（麦香野の村）。エレピが歌う「ラ・ド・ファ」の上がり調子は、風車がゆっくり回る動き。クリーンギターのアルペジオ、ベース、やさしいブラシふうのドラムに、きらきらした鐘が風車の羽のようにまわる。',
  bpm: 104, beats: 3, tonic: 'F', mode: 'major', flat: true, feel: 'ballad', tone: 'prs',
  parts: [
    { id: 'keys', instrument: 'keys', role: 'メロディ', volume: 0.25, pan: 0.05 },
    { id: 'gtr', instrument: 'guitar', role: 'クリーンギター', volume: 0.17, pan: -0.4, amp: 'clean', base: 43 },
    { id: 'cr', instrument: 'crunch', role: 'うらうちギター', volume: 0.1, pan: 0.4, amp: 'crunch', base: 43 },
    { id: 'bell', instrument: 'bell', role: '風車の鐘', volume: 0.1, pan: 0.5, base: 60 },
    { id: 'bass', instrument: 'bass', role: 'ベース', volume: 0.2, base: 28 },
    { id: 'kick', instrument: 'kick', role: 'キック', volume: 0.2 },
    { id: 'snare', instrument: 'snare', role: 'スネア', volume: 0.14 },
    { id: 'hat', instrument: 'hihat', role: 'ハイハット', volume: 0.08 },
  ],
  drums: {
    A: { k: 'x...........', s: '....x...x...', h: 'x.x.x.x.x.x.' },
    B: { k: 'x.....x.....', s: '....x...x...', h: 'x.x.x.x.x.x.' },
    end: { k: 'x...........' },
  },
  sections: [
    { name: 'intro', chords: 'F Dm Bb C', p: { keys: [R3, R3, 'D5:1 F5:1 Bb5:1', 'G5:2 E5:1'], gtr: gtr, bell: 'r:1 f:1 t+:1' } },
    { name: 'A', chords: 'F Am Bb F Dm Gm7 C Csus4', dr: 'A', ft: 'c', fill: 8, p: { keys: melA, gtr: gtr, bass: bass, bell: R3 } },
    { name: 'B', chords: 'Bb C Am Dm Gm7 C F F', dr: 'B', ft: 'c', p: { keys: melB, gtr: gtrB, cr: cr, bass: bassB, bell: bellB } },
    { name: 'A2', chords: 'F Am Bb F Dm Gm7 C Csus4', dr: 'A', ft: 'c', fill: 8, p: { keys: melA2, gtr: gtr, cr: cr, bass: bass, bell: bellB } },
    { name: 'bridge', chords: 'Dm Am Bb F Gm7 Dm Csus4 C', dr: 'A', ft: 'c', p: { keys: melBr, gtr: gtr, bass: 'r:3', bell: R3 } },
    { name: 'B2', chords: 'Bb C Am Dm Gm7 C F F', dr: 'B', ft: 'c', p: { keys: melB2, gtr: gtrB, cr: cr, bass: bassB, bell: bellB } },
    { name: 'outro', chords: 'Bb Gm7 C', dr: 'A', nofill: true, p: { keys: ['D5:1 F5:1 Bb5:1', 'Bb5:1 G5:1 D5:1', 'G5:1 E5:1 C5:1'], gtr: gtr, bass: 'r:1 f:1 a:1', bell: R3 } },
    { name: 'end', chords: 'F', dr: 'end', nofill: true, p: { keys: 'F5:3', gtr: 'r:3', bass: 'r:3', bell: 'f+:3' } },
  ],
});
