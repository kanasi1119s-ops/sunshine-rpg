import { build } from './lib.mjs';

const walk = ['r:1 t:1 f:1 a:1', 'r:1 f:1 s:1 a:1'];
const kc = ['R:1.5 t+:1 f+:0.5 R:1', 'R:0.5 s+:1.5 R:1 t+:1'];
const gs = 'R:1 f:0.5 R:0.5 R:1 s:0.5 R:0.5';
const R4 = 'R:4';
const melA1 = ['D5:0.5 F5:0.5 A5:1 G5:0.5 F5:0.5 D5:1', 'D5:1 Bb5:1.5 G5:0.5 F5:1', 'Eb5:0.5 G5:0.5 Bb5:1 A5:0.5 G5:0.5 Eb5:1', 'A5:1 C6:1 Eb6:1 D6:1',
  'D6:1.5 Bb5:0.5 F5:1 A5:1', 'G5:0.5 Bb5:0.5 D6:1 C6:0.5 Bb5:0.5 G5:1', 'C6:1 Bb5:0.5 G5:0.5 Eb5:2', 'F5:1 A5:1 C6:1 R:1'];
const melA2 = ['F5:0.5 A5:0.5 D6:1 C6:0.5 A5:0.5 F5:1', 'G5:1 D6:1.5 Bb5:0.5 G5:1', 'G5:0.5 Bb5:0.5 Eb6:1 D6:0.5 C6:0.5 Bb5:1', 'A5:0.5 C6:0.5 Eb6:1 D6:0.5 C6:0.5 A5:1',
  'D6:1 C6:1 Bb5:1 A5:1', 'Bb5:0.5 D6:0.5 G5:1 Bb5:1 D6:1', 'C6:0.5 Eb6:0.5 D6:1 Bb5:1 G5:1', 'A5:0.5 C6:0.5 F5:1 A5:1 R:1'];
const melA3 = [...melA1.slice(0, 7), 'A5:1 C6:1 F5:2'];
const melB = ['D5:1 G5:1 Bb5:2', 'G5:1 E5:1 C5:1 E5:1', 'A5:2 F5:1 C5:1', 'D5:1 F5:1 A5:1 C6:1',
  'Bb5:1.5 A5:0.5 G5:1 D5:1', 'E5:1 G5:1 Bb5:1 G5:1', 'Eb5:1 G5:1 C6:1 Bb5:1', 'A5:2 C6:1 Eb6:1'];
const chA = 'Bbmaj7 Gm7 Cm7 F7 Bbmaj7 Ebmaj7 Cm7 F7';

build({
  id: 'town-garasuko', title: '硝子湖の港',
  description: 'B♭長調の軽いジャズバンド曲（硝子湖の港町）。ジャズ調のリードギターが港のゆれるような旋律を歌い、エレピのコンピング、歩くように動くウォーキングベース、ライドふうのハイハットが続く。中ほどはピアノが主役のブリッジ。おだやかな港の午後の曲。',
  bpm: 112, beats: 4, tonic: 'Bb', mode: 'major', flat: true, feel: 'pop', tone: 'prs',
  parts: [
    { id: 'lead', instrument: 'leadGuitar', role: 'ジャズギター（メロディ）', volume: 0.24, pan: 0.15, amp: 'jazz' },
    { id: 'pf', instrument: 'piano', role: 'ピアノ', volume: 0.17, pan: -0.25, base: 48 },
    { id: 'keys', instrument: 'keys', role: 'エレピ（コンピング）', volume: 0.14, pan: 0.35, base: 48 },
    { id: 'gtr', instrument: 'guitar', role: 'ミュートギター', volume: 0.1, pan: -0.5, amp: 'jazz', base: 43 },
    { id: 'bass', instrument: 'bass', role: 'ウォーキングベース', volume: 0.22, base: 28 },
    { id: 'kick', instrument: 'kick', role: 'キック', volume: 0.16 },
    { id: 'snare', instrument: 'snare', role: 'スネア（ブラシ）', volume: 0.1 },
    { id: 'hat', instrument: 'hihat', role: 'ライド', volume: 0.09 },
  ],
  drums: {
    A: { k: 'x...x...x...x...', s: '......x.......x.', h: 'x...x.x.x...x.x.' },
    B: { k: 'x.......x.......', s: '......x.......x.', h: 'x...x.x.x...x.x.' },
    end: { k: 'x...............' },
  },
  sections: [
    { name: 'intro', chords: 'Bbmaj7 Ebmaj7 Cm7 F7', dr: 'B', ft: 'c', p: { pf: [R4, R4, 'Eb5:1 G5:1 Bb5:2', 'A5:1 C6:1 Eb6:2'], keys: kc, gtr: gs, bass: [R4, R4, 'r:2 f:2', 'r:1 t:1 f:1 a:1'] } },
    { name: 'A', chords: chA, dr: 'A', ft: 'c', fill: 4, p: { lead: melA1, pf: R4, keys: kc, gtr: gs, bass: walk } },
    { name: 'A2', chords: chA, dr: 'A', ft: 'c', p: { lead: melA2, pf: 'R:3 f+:0.5 s+:0.5', keys: kc, gtr: gs, bass: walk } },
    { name: 'B', chords: 'Gm7 C7 Fmaj7 Dm7 Gm7 C7 Cm7 F7', dr: 'B', ft: 'c', p: { pf: melB, lead: R4, keys: kc, gtr: gs, bass: walk } },
    { name: 'A3', chords: chA, dr: 'A', ft: 'c', p: { lead: melA3, pf: R4, keys: kc, gtr: gs, bass: walk } },
    { name: 'outro', chords: 'Ebmaj7 Cm7 F7', dr: 'B', nofill: true, p: { lead: ['G5:1 Bb5:1 D6:2', 'Eb6:1 C6:1 G5:2', 'A5:1 C6:1 Eb6:2'], keys: kc, gtr: gs, bass: 'r:1 t:1 f:1 a:1' } },
    { name: 'end', chords: 'Bb', dr: 'end', nofill: true, p: { lead: 'D6:4', pf: 'r:4', keys: 'r:4', gtr: 'r:4', bass: 'r:4' } },
  ],
});
