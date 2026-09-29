import { arrange, type Section } from "./compose";
import type { Score } from "./score";

/**
 * 楽器と曲調を広げた新曲（各1〜1分半）。ロック・メタル・クラシック・空間系・キーボード主体・不思議・不協和音。
 * 旋律・コード進行・リズムはすべてオリジナル。既存曲の旋律や進行の丸写しはしていない。
 * 伴奏は `compose.ts` の型（パターン）から作り、旋律は手で書いた。どの場面に使うかは未定（`docs/sound/tracks.md`）。
 */

const rep = (s: string, n: number): string => Array(n).fill(s).join(" ");

// ── 1. ロック調「旅立ちの街道」（132BPM・44小節＝約80秒） ─────────────────────────
const ROCK_DRUM_VERSE = { kick: "x.......x.x.....", snare: "....x.......x...", hat: "x.x.x.x.x.x.x.x." };
const ROCK_DRUM_CHORUS = { kick: "x.....x.x.x...x.", snare: "....x.......x...", hat: "xxxxxxxxxxxxxxxx" };
const CRASH_4 = "x............... ................ ................ ................";
const ROCK_A = "B4:1 E5:1.5 G5:0.5 B5:1 G5:1 E5:1 C5:2 D5:1 G5:1 B5:1 D6:1 A5:2 F#5:2 B4:1 E5:1.5 G5:0.5 B5:1 C6:1 B5:1 G5:2 A5:1 F#5:1 D5:1 F#5:1 E5:1 F#5:1 A5:2";
const ROCK_CHORUS = "E5:0.5 G5:0.5 C6:1 E6:2 D6:1 B5:1 G5:2 A5:1 D6:1 F#6:2 E6:3 D6:1 C6:1 E6:1 G6:2 B5:1 D6:1 G6:2 ";
const rockSections: Section[] = [
  {
    chords: "Em Em C D",
    parts: { kick: "x.......x.x.....", snare: "....x.......x...", hat: "x.x.x.x.x.x.x.x.", crash: CRASH_4, bass: "R.RR.R.R", crunch: "R.RR.RR." },
    melody: { gtr: "E5:2 G5:1 B5:1 B5:2 A5:1 G5:1 G5:2 E5:1 G5:1 F#5:4" },
  },
  ...[0, 1].map((): Section => ({
    chords: "Em C G D Em C D D",
    parts: { ...ROCK_DRUM_VERSE, crash: CRASH_4, bass: "R.RR.R.R", crunch: "R.RR.RR.", arp: "abcbabcb" },
    melody: { lead: ROCK_A },
  })),
  {
    chords: "Am Am7 C D Am C B7 B7",
    parts: { ...ROCK_DRUM_CHORUS, crash: CRASH_4, bass: "R-R-R-5-", crunch: "R-------", arp: "abcdcbcd", k1: "a-------", k2: "b-------", k3: "c-------" },
    melody: { lead: "E5:2 A5:2 G5:2 E5:2 E5:1 G5:1 C6:2 D6:2 A5:2 C6:2 A5:2 G5:2 E5:2 D#5:1 F#5:1 A5:1 B5:1 B5:4" },
  },
  {
    chords: "C G D Em C G D D",
    parts: { ...ROCK_DRUM_CHORUS, crash: CRASH_4, bass: "RRRRRRRR", crunch: "R-R-R-R-", arp: "abcdcbcd", k1: "a-------", k2: "b-------", k3: "c-------" },
    melody: { gtr: ROCK_CHORUS + "F#6:1 E6:1 D6:1 A5:1 D6:3 R:1" },
  },
  {
    chords: "C G D Em C G D Em",
    parts: { ...ROCK_DRUM_CHORUS, crash: CRASH_4, bass: "RRRRRRRR", crunch: "R-R-R-R-", arp: "abcdcbcd", k1: "a-------", k2: "b-------", k3: "c-------" },
    melody: { gtr: ROCK_CHORUS + "F#6:1 E6:1 D6:1 A5:1 E6:4" },
  },
];
export const STYLE_ROCK_ROAD: Score = arrange({
  tempoBpm: 132,
  beatsPerBar: 4,
  sections: rockSections,
  parts: {
    kick: { instrument: "kick", waveform: "sine", volume: 0.3, octave: 2, step: 0.25, fixed: "C2" },
    snare: { instrument: "snare", waveform: "sine", volume: 0.26, octave: 2, step: 0.25, fixed: "C3" },
    hat: { instrument: "hihat", waveform: "sine", volume: 0.12, octave: 2, step: 0.25, fixed: "C6" },
    crash: { instrument: "crash", waveform: "sine", volume: 0.16, octave: 2, step: 0.25, fixed: "C5" },
    bass: { instrument: "bass", waveform: "triangle", volume: 0.3, octave: 2, step: 0.5 },
    crunch: { instrument: "crunch", waveform: "sawtooth", volume: 0.2, octave: 3, step: 0.5 },
    arp: { instrument: "guitar", waveform: "sawtooth", volume: 0.15, octave: 4, step: 0.5 },
    k1: { instrument: "keys", waveform: "sine", volume: 0.1, octave: 4, step: 0.5 },
    k2: { instrument: "keys", waveform: "sine", volume: 0.1, octave: 4, step: 0.5 },
    k3: { instrument: "keys", waveform: "sine", volume: 0.1, octave: 4, step: 0.5 },
  },
  melodies: {
    lead: { instrument: "lead", waveform: "square", volume: 0.13 },
    gtr: { instrument: "leadGuitar", waveform: "sawtooth", volume: 0.17 },
  },
});

// ── 2. メタル調「鋼の咆哮」（172BPM・60小節＝約84秒） ─────────────────────────────
const METAL_CHUG = "R.RR.RR.R.RR.RR.";
const METAL_HIT = "R-------R---R---";
const M_DRUMS_V = { kick: "x.xx..x.x.xx..x.", snare: "....x.......x...", hat: "x.x.x.x.x.x.x.x." };
const M_DRUMS_C = { kick: "x.x.x.x.x.x.x.x.", snare: "....x.......x...", hat: "x.x.x.x.x.x.x.x.", crash: CRASH_4 };
const M_SOLO = [
  "D6:0.5 F6:0.5 A6:0.5 F6:0.5 D6:0.5 F6:0.5 A6:0.5 D7:0.5",
  "D7:0.5 Bb6:0.5 F6:0.5 D6:0.5 Bb5:0.5 D6:0.5 F6:0.5 Bb6:0.5",
  "C7:0.5 G6:0.5 E6:0.5 G6:0.5 C6:0.5 E6:0.5 G6:0.5 C7:0.5",
  "C#7:0.5 A6:0.5 E6:0.5 A6:0.5 C#6:0.5 E6:0.5 A6:0.5 C#7:0.5",
  "D7:1 A6:1 F6:1 D6:1",
  "Bb6:2 F6:1 D6:1",
  "E6:1 C#6:1 A5:1 E6:1",
  "A5:4",
].join(" ");
const METAL_CHORUS = "A5:1 D6:1 F6:2 D6:1 F6:1 Bb5:2 C6:1 F6:1 A6:2 G6:2 E6:2 F6:1 D6:1 A5:2 Bb5:1 D6:1 F6:2 E6:2 C#6:2 E6:2 C#6:1 A5:1";
const metalSections: Section[] = [
  {
    chords: "Dm Dm Bb A5",
    parts: { ...M_DRUMS_V, crash: CRASH_4, gtrs: METAL_HIT, bass: "R.R.R.R.R.R.R.R." },
    melody: { gtr: "D6:4 A5:2 F5:2 Bb5:4 C#6:4" },
  },
  {
    chords: "Dm Dm Bb C Dm Dm Gm A",
    parts: { ...M_DRUMS_V, gtrs: METAL_CHUG, bass: "R.R.R.R.R.R.R.R." },
    melody: { lead: "D5:1 D5:1 F5:1 A5:1 G5:2 F5:1 E5:1 D5:1 F5:1 Bb5:2 G5:2 E5:1 G5:1 A5:1 A5:1 D6:1 C6:1 A5:2 F5:2 G5:1 Bb5:1 D6:2 A5:1 C#6:1 E6:2" },
  },
  {
    chords: "Bb C Dm Dm Bb C A A",
    parts: { ...M_DRUMS_V, gtrs: METAL_CHUG, bass: "R.R.R.R.R.R.R.R.", s1: "a-------a-------", s2: "b-------b-------", s3: "c-------c-------" },
    melody: { lead: "D5:2 F5:2 E5:2 G5:2 F5:2 A5:2 D6:4 Bb5:2 D6:2 C6:2 E6:2 E6:2 C#6:2 A5:4" },
  },
  {
    chords: "Dm Bb F C Dm Bb A A",
    parts: { ...M_DRUMS_C, gtrs: METAL_HIT, bass: "R.R.R.R.R.R.R.R.", s1: "a---------------", s2: "b---------------", s3: "c---------------" },
    melody: { gtr: METAL_CHORUS },
  },
  {
    chords: "Dm Bb Gm A Dm Bb Gm A",
    parts: { pn: "a...b...c...b...", bass: "R---------------", s1: "a---------------", s2: "b---------------", s3: "c---------------" },
    melody: { pn: "F5:2 D5:2 D5:2 F5:2 Bb5:2 G5:2 A5:2 E5:2 F5:2 A5:2 D6:2 Bb5:2 G5:2 D5:2 C#5:2 E5:2" },
  },
  {
    chords: "Dm Bb C A Dm Bb A A",
    parts: { ...M_DRUMS_C, gtrs: METAL_CHUG, bass: "R.R.R.R.R.R.R.R." },
    melody: { gtr: M_SOLO },
  },
  {
    chords: "Dm Bb F C Dm Bb A A",
    parts: { ...M_DRUMS_C, gtrs: METAL_HIT, bass: "R.R.R.R.R.R.R.R.", s1: "a---------------", s2: "b---------------", s3: "c---------------" },
    melody: { gtr: METAL_CHORUS },
  },
  {
    chords: "Dm Bb C Dm Dm Bb A Dm",
    parts: { ...M_DRUMS_C, gtrs: METAL_CHUG, bass: "R.R.R.R.R.R.R.R." },
    melody: { gtr: "D6:2 A5:2 Bb5:2 F5:2 C6:2 G5:2 D6:4 D6:2 F6:2 Bb5:2 D6:2 C#6:2 E6:2 D6:4" },
  },
];
export const STYLE_METAL_ROAR: Score = arrange({
  tempoBpm: 172,
  beatsPerBar: 4,
  sections: metalSections,
  parts: {
    kick: { instrument: "kick", waveform: "sine", volume: 0.3, octave: 2, step: 0.25, fixed: "C2" },
    snare: { instrument: "snare", waveform: "sine", volume: 0.27, octave: 2, step: 0.25, fixed: "C3" },
    hat: { instrument: "hihat", waveform: "sine", volume: 0.11, octave: 2, step: 0.25, fixed: "C6" },
    crash: { instrument: "crash", waveform: "sine", volume: 0.15, octave: 2, step: 0.25, fixed: "C5" },
    gtrs: { instrument: "distGuitar", waveform: "sawtooth", volume: 0.2, octave: 2, step: 0.25 },
    bass: { instrument: "bass", waveform: "triangle", volume: 0.3, octave: 2, step: 0.25 },
    s1: { instrument: "strings", waveform: "sawtooth", volume: 0.07, octave: 4, step: 0.25 },
    s2: { instrument: "strings", waveform: "sawtooth", volume: 0.07, octave: 4, step: 0.25 },
    s3: { instrument: "strings", waveform: "sawtooth", volume: 0.07, octave: 4, step: 0.25 },
    pn: { instrument: "piano", waveform: "triangle", volume: 0.1, octave: 4, step: 0.25 },
  },
  melodies: {
    lead: { instrument: "lead", waveform: "square", volume: 0.12 },
    gtr: { instrument: "leadGuitar", waveform: "sawtooth", volume: 0.17 },
    pn: { instrument: "piano", waveform: "triangle", volume: 0.14 },
  },
});

// ── 3. クラシック調「白亜の宮廷」（96BPM・3拍子・44小節＝約83秒） ────────────────────
const C_A = "B5:1 D6:1 G6:1 F#6:2 A5:1 G6:1 E6:1 B5:1 C6:1 E6:1 G6:1 D6:1.5 B5:0.5 G5:1 A5:1 C6:1 F#6:1 G6:2 B5:1 G5:3";
const classicSections: Section[] = [
  {
    chords: "G D Em C",
    parts: { cello: "R-----", hpsi: "abcbcb" },
    melody: { violin: "D6:3 A5:3 B5:3 G5:3" },
  },
  ...[0, 1].map((i): Section => ({
    chords: "G D Em C G D G G",
    parts: { cello: "R--R--", hpsi: "abcbcb", v1: "a-----", v2: "b-----", v3: "c-----" },
    melody: i === 0 ? { piano: C_A } : { violin: C_A, piano: C_A },
  })),
  {
    chords: "Em Am D G Em Am D D",
    parts: { cello: "R-----", hpsi: "abcbcb", v1: "a-----", v2: "b-----", v3: "c-----" },
    melody: { violin: "E6:2 G6:1 E6:1 C6:1 A5:1 D6:2 F#6:1 G6:1 B5:1 D6:1 E6:2 B5:1 C6:1 E6:1 A6:1 F#6:1.5 E6:0.5 D6:1 D6:3" },
  },
  {
    chords: "Bm G Em Am D D G D",
    parts: { cello: "R--R--", hpsi: "abcbcb", v1: "a-----", v2: "b-----", v3: "c-----" },
    melody: { hpsi2: "D6:1 F#6:1 B6:1 B5:1 D6:1 G6:1 G6:2 E6:1 A5:1 C6:1 E6:1 F#6:1 A6:1 D7:1 C7:1.5 A6:0.5 F#6:1 G6:2 B6:1 A6:2 F#6:1", piano: "B4:3 G4:3 E4:3 A4:3 D5:3 D5:3 B4:3 A4:3" },
  },
  {
    chords: "G D Em C G D G G",
    parts: { cello: "R--R--", hpsi: "abcbcb", v1: "a-----", v2: "b-----", v3: "c-----" },
    melody: { violin: C_A, piano: C_A },
  },
];
export const STYLE_CLASSIC_PALACE: Score = arrange({
  tempoBpm: 96,
  beatsPerBar: 3,
  sections: classicSections,
  parts: {
    cello: { instrument: "strings", waveform: "sawtooth", volume: 0.16, octave: 2, step: 0.5 },
    hpsi: { instrument: "harpsichord", waveform: "sawtooth", volume: 0.12, octave: 4, step: 0.5 },
    v1: { instrument: "strings", waveform: "sawtooth", volume: 0.07, octave: 4, step: 0.5 },
    v2: { instrument: "strings", waveform: "sawtooth", volume: 0.07, octave: 4, step: 0.5 },
    v3: { instrument: "strings", waveform: "sawtooth", volume: 0.07, octave: 4, step: 0.5 },
  },
  melodies: {
    violin: { instrument: "strings", waveform: "sawtooth", volume: 0.14 },
    piano: { instrument: "piano", waveform: "triangle", volume: 0.13 },
    hpsi2: { instrument: "harpsichord", waveform: "sawtooth", volume: 0.14 },
  },
});

// ── 4. 空間系「星海の回廊」（72BPM・24小節＝約80秒） ──────────────────────────────
const SPACE_PADS = { p1: "a-------", p2: "b-------", p3: "c-------", p4: "d-------", sub: "R-------", bells: "a..c..b." };
const spaceSections: Section[] = [
  {
    chords: "Am7 Fmaj7 Cmaj7 Gmaj7 Am7 Fmaj7 Cmaj7 Gmaj7",
    parts: SPACE_PADS,
    melody: { echo: "E5:3 G5:1 A5:4 G5:2 E5:2 D5:3 R:1 C5:2 E5:2 F5:3 C5:1 E5:4 B4:2 D5:2" },
  },
  {
    chords: "Dm7 Fmaj7 Am7 Em7 Dm7 Fmaj7 Am7 Em7",
    parts: SPACE_PADS,
    melody: { echo: "F5:3 A5:1 A5:2 C6:2 E6:4 G5:2 B5:2 D6:3 C6:1 A5:4 E5:2 G5:2 B4:4" },
  },
  {
    chords: "Fmaj7 Cmaj7 Am7 Em7 Fmaj7 Cmaj7 Dm7 Am7",
    parts: SPACE_PADS,
    melody: { echo: "C6:4 E6:3 D6:1 C6:2 A5:2 B5:4 A5:2 C6:2 G5:4 F5:2 A5:2 E5:4" },
  },
];
export const STYLE_SPACE_CORRIDOR: Score = arrange({
  tempoBpm: 72,
  beatsPerBar: 4,
  sections: spaceSections,
  parts: {
    p1: { instrument: "pad", waveform: "sine", volume: 0.09, octave: 3, step: 0.5 },
    p2: { instrument: "pad", waveform: "sine", volume: 0.09, octave: 3, step: 0.5 },
    p3: { instrument: "pad", waveform: "sine", volume: 0.09, octave: 4, step: 0.5 },
    p4: { instrument: "pad", waveform: "sine", volume: 0.08, octave: 4, step: 0.5 },
    sub: { instrument: "pad", waveform: "sine", volume: 0.13, octave: 2, step: 0.5 },
    bells: { instrument: "bell", waveform: "sine", volume: 0.07, octave: 5, step: 0.5 },
  },
  melodies: { echo: { instrument: "echoGuitar", waveform: "sawtooth", volume: 0.14 } },
});

// ── 5. キーボード主体「夕暮れのカフェ通り」（108BPM・40小節＝約89秒） ────────────────
const CAFE_DRUMS = { kick: "x.......x.x.....", snare: "....x.......x...", hat: "x.x.x.x.x.x.x.x." };
const CAFE_COMP = { k1: "a--a--a-", k2: "b--b--b-", k3: "c--c--c-", k4: "d--d--d-" };
const CAFE_A = "E5:1 G5:1 E5:1 D5:1 C5:2 E5:2 F5:1 A5:1 D6:2 B5:2 G5:2 G5:1 B5:1 E6:2 C#6:1 E6:1 A5:2 D6:2 F5:1 A5:1 G5:3 R:1";
const CAFE_B = "A5:2 C6:2 B5:1 G5:1 E5:2 F5:2 D5:2 E5:2 G5:2 C6:1 A5:1 F5:2 D6:2 B5:2 G5:2 E5:1 G5:1 A5:4";
const cafeSections: Section[] = [
  {
    chords: "Cmaj7 Am7 Dm7 G7",
    parts: { bass: "abcb", ...CAFE_COMP, hat: "x.x.x.x.x.x.x.x." },
    melody: { keysm: "E5:2 G5:1 B5:1 C6:2 A5:2 F5:2 A5:1 C6:1 B5:3 R:1" },
  },
  {
    chords: "Cmaj7 Am7 Dm7 G7 Em7 A7 Dm7 G7",
    parts: { ...CAFE_DRUMS, bass: "abcb", ...CAFE_COMP },
    melody: { gtr: CAFE_A },
  },
  {
    chords: "Fmaj7 Em7 Dm7 Cmaj7 Fmaj7 G7 Em7 Am7",
    parts: { ...CAFE_DRUMS, bass: "abcb", ...CAFE_COMP, arp: "abcdcbcd" },
    melody: { lead: CAFE_B },
  },
  {
    chords: "Cmaj7 Am7 Dm7 G7 Em7 A7 Dm7 G7",
    parts: { ...CAFE_DRUMS, bass: "abcb", ...CAFE_COMP, arp: "abcdcbcd" },
    melody: { keysm: CAFE_A },
  },
  {
    chords: "Fmaj7 Em7 Dm7 Cmaj7 Fmaj7 G7 Em7 Am7",
    parts: { ...CAFE_DRUMS, bass: "abcb", ...CAFE_COMP, arp: "abcdcbcd", st1: "a-------", st2: "b-------", st3: "c-------" },
    melody: { lead: CAFE_B },
  },
  {
    chords: "Fmaj7 G7 Cmaj7 Cmaj7",
    parts: { bass: "abcb", ...CAFE_COMP, kick: "x...............", snare: "................", hat: "x.x.x.x.x.x.x.x." },
    melody: { keysm: "A5:2 F5:2 B5:2 D6:2 C6:2 E6:2 G6:4" },
  },
];
export const STYLE_KEYS_CAFE: Score = arrange({
  tempoBpm: 108,
  beatsPerBar: 4,
  sections: cafeSections,
  parts: {
    kick: { instrument: "kick", waveform: "sine", volume: 0.24, octave: 2, step: 0.25, fixed: "C2" },
    snare: { instrument: "snare", waveform: "sine", volume: 0.18, octave: 2, step: 0.25, fixed: "C3" },
    hat: { instrument: "hihat", waveform: "sine", volume: 0.1, octave: 2, step: 0.25, fixed: "C6" },
    bass: { instrument: "bass", waveform: "triangle", volume: 0.3, octave: 2, step: 1 },
    k1: { instrument: "keys", waveform: "sine", volume: 0.09, octave: 4, step: 0.5 },
    k2: { instrument: "keys", waveform: "sine", volume: 0.09, octave: 4, step: 0.5 },
    k3: { instrument: "keys", waveform: "sine", volume: 0.09, octave: 4, step: 0.5 },
    k4: { instrument: "keys", waveform: "sine", volume: 0.08, octave: 4, step: 0.5 },
    arp: { instrument: "guitar", waveform: "sawtooth", volume: 0.12, octave: 4, step: 0.5 },
    st1: { instrument: "strings", waveform: "sawtooth", volume: 0.06, octave: 4, step: 0.5 },
    st2: { instrument: "strings", waveform: "sawtooth", volume: 0.06, octave: 4, step: 0.5 },
    st3: { instrument: "strings", waveform: "sawtooth", volume: 0.06, octave: 4, step: 0.5 },
  },
  melodies: {
    keysm: { instrument: "keys", waveform: "sine", volume: 0.15 },
    gtr: { instrument: "guitar", waveform: "sawtooth", volume: 0.17 },
    lead: { instrument: "lead", waveform: "square", volume: 0.11 },
  },
});

// ── 6. 不協和音「歪みの囁き」（70BPM・24小節＝約82秒）: 心を不安にさせる曲 ──────────────
// 半音でぶつかる持続音（うなり）、悪魔の音程（3全音）の鐘、止まりかけた心臓のような低いキック。
const unease = (n: number): string => rep("Edim", n);
export const STYLE_DISCORD_WHISPER: Score = arrange({
  tempoBpm: 70,
  beatsPerBar: 4,
  sections: [
    {
      chords: unease(8),
      parts: { heart: "x.x............." },
      melody: {
        c1: "E3:16 E3:16",
        c2: "F3:16 F3:16",
        b1: "R:4 B5:0.5 R:7.5 F6:0.5 R:7.5 B5:0.5 R:11.5",
        w1: "R:8 D#4:8 R:4 E4:4 R:8",
      },
    },
    {
      chords: unease(8),
      parts: { heart: "x.x............." },
      melody: {
        c1: "E3:8 G3:8 E3:8 Bb3:8",
        c2: "F3:8 Ab3:8 F3:8 B3:8",
        b1: "B5:0.5 R:3.5 F6:0.5 R:3.5 F#6:0.5 R:7.5 C6:0.5 R:3.5 F6:0.5 R:3.5 B5:0.5 R:7.5",
        w1: "D#5:2 E5:2 F5:4 E5:4 D#5:4 F#5:2 F5:2 E5:4 D#5:2 R:6",
      },
    },
    {
      chords: unease(8),
      parts: { heart: "x.x.x.x.x.x.x.x." },
      melody: {
        c1: "E3:32",
        c2: "F3:8 F#3:8 G3:8 F#3:8",
        b1: "B5:0.5 R:1.5 F6:0.5 R:1.5 B5:0.5 R:1.5 F6:0.5 R:1.5 B5:0.5 R:1.5 F6:0.5 R:1.5 B5:0.5 R:1.5 F6:0.5 R:1.5 B5:4 F6:4 R:8",
        w1: "E5:8 F5:8 E5:4 Eb5:4 E5:8",
      },
    },
  ],
  parts: {
    heart: { instrument: "kick", waveform: "sine", volume: 0.22, octave: 2, step: 0.25, fixed: "C2" },
  },
  melodies: {
    c1: { instrument: "pad", waveform: "sine", volume: 0.12 },
    c2: { instrument: "pad", waveform: "sine", volume: 0.12 },
    b1: { instrument: "bell", waveform: "sine", volume: 0.1 },
    w1: { instrument: "strings", waveform: "sawtooth", volume: 0.09 },
  },
});

// ── 7. 不思議「時計仕掛けの迷宮」（96BPM・32小節＝約80秒）: オルゴールと歯車の謎解き ─────────
const CLOCK_CHORDS_A = "Cdim Ebdim Gbdim Adim Cdim Ebdim Gbdim Adim";
const CLOCK_CHORDS_B = "Am Fdim G Ebdim Am Fdim E7 E7";
export const STYLE_MYSTERY_CLOCKWORK: Score = arrange({
  tempoBpm: 96,
  beatsPerBar: 4,
  sections: [
    {
      chords: CLOCK_CHORDS_A,
      parts: { tick: "x.x.x.x.x.x.x.x.", mb: "abcdcbab", pz: "R.......R.5.....", bass: "R---------------" },
    },
    {
      chords: CLOCK_CHORDS_A,
      parts: { tick: "x.x.x.x.x.x.x.x.", mb: "abcdcbab", pz: "R.R.5.R.R.R.5.R.", bass: "R---------------", pad: "a---------------" },
      melody: { harp: "C6:1 Eb6:1 Gb6:1 A6:1 Gb6:2 Eb6:2 Eb6:1 Gb6:1 A6:1 C7:1 A6:2 Gb6:2 Gb6:1 A6:1 C7:1 Eb7:1 C7:2 A6:2 A6:1 C7:1 Eb7:1 Gb7:1 Eb7:4" },
    },
    {
      chords: CLOCK_CHORDS_B,
      parts: { tick: "x.x.x.x.x.x.x.x.", mb: "abcbabcb", pz: "R.R.5.R.R.R.5.R.", bass: "R---------------", pad: "a---------------" },
      melody: { harp: "E6:2 C6:1 A5:1 F6:1 Ab5:1 C6:2 D6:2 B5:1 G5:1 Gb5:1 A5:1 C6:1 Eb6:1 A5:1 C6:1 E6:2 F6:1 Ab5:1 C6:2 G#5:1 B5:1 E6:2 E6:4" },
    },
    {
      chords: CLOCK_CHORDS_B,
      parts: { tick: "x.x.x.x.x.x.x.x.", mb: "abcbabcb", pz: "R.R.5.R.R.R.5.R.", bass: "R---------------", pad: "a---------------" },
      melody: { harp: "A6:1 E6:1 C6:1 A5:1 C6:1 Ab5:1 F5:2 B5:1 D6:1 G6:2 Gb6:1 Eb6:1 C6:1 A5:1 E6:1 C6:1 A5:2 F6:1 C6:1 Ab5:1 F5:1 G#5:1 B5:1 E6:1 G#6:1 A6:4" },
    },
  ],
  parts: {
    tick: { instrument: "hihat", waveform: "sine", volume: 0.09, octave: 2, step: 0.25, fixed: "C6" },
    mb: { instrument: "bell", waveform: "sine", volume: 0.07, octave: 5, step: 0.5 },
    pz: { instrument: "harpsichord", waveform: "sawtooth", volume: 0.1, octave: 3, step: 0.25 },
    bass: { instrument: "pad", waveform: "sine", volume: 0.1, octave: 2, step: 0.25 },
    pad: { instrument: "strings", waveform: "sawtooth", volume: 0.05, octave: 4, step: 0.25 },
  },
  melodies: { harp: { instrument: "bell", waveform: "sine", volume: 0.1 } },
});

/** 新曲の一覧（BGMプレイヤー・テスト用）。 */
export const STYLE_TRACKS: { id: string; title: string; style: string; score: Score }[] = [
  { id: "rock-road", title: "旅立ちの街道", style: "ロック調（ギター・ベース・ドラム・キーボード）", score: STYLE_ROCK_ROAD },
  { id: "metal-roar", title: "鋼の咆哮", style: "メタル調（歪んだギター・ツーバス風・ギターソロ）", score: STYLE_METAL_ROAR },
  { id: "classic-palace", title: "白亜の宮廷", style: "クラシック調（弦・ハープシコード・ピアノ、3拍子）", score: STYLE_CLASSIC_PALACE },
  { id: "space-corridor", title: "星海の回廊", style: "空間系（パッド・鈴・エコーのかかったギター）", score: STYLE_SPACE_CORRIDOR },
  { id: "keys-cafe", title: "夕暮れのカフェ通り", style: "キーボード主体（エレピ・ウォーキングベース）", score: STYLE_KEYS_CAFE },
  { id: "discord-whisper", title: "歪みの囁き", style: "不協和音（心を不安にさせる曲）", score: STYLE_DISCORD_WHISPER },
  { id: "mystery-clockwork", title: "時計仕掛けの迷宮", style: "不思議（オルゴールと歯車、減七の響き）", score: STYLE_MYSTERY_CLOCKWORK },
];
