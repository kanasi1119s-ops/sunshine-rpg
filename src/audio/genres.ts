import type { MasterFxSettings } from "./master-fx";
import { REST, type Instrument, type NoteEvent, type Score, type Track } from "./score";
import type { SongSpec } from "./songwriter";

/**
 * 2020年代の最新ジャンル（トラップ、ドリル、ローファイ、フューチャーベース、ハイパーポップ、シンセウェイブ、シティポップ、ハウス、テクノ、トランス、ドラムンベース、
 * ダブステップ、UKガラージ、アマピアノ、レゲトン、ヴェイパーウェイブ、ハードスタイル、ジャージークラブ、ポップパンク、ベッドルームポップ、ニューディスコ、
 * ハイブリッド・トレイラー）の曲を、型（リズム・進行・音色・構成）から組み立てる。
 * 特定の曲・アーティストの旋律や進行はなぞらない。ジャンルに共通するテンポ・リズムの型・音色の使い方だけを使う（CLAUDE.md 1-1）。
 * すべて4拍子。同じ種（seed）なら同じ曲になる。
 */
export type ModernStyle =
  | "trap" | "drill" | "lofi" | "futurebass" | "hyperpop" | "synthwave" | "citypop" | "house" | "techno" | "trance"
  | "dnb" | "dubstep" | "ukgarage" | "amapiano" | "reggaeton" | "vaporwave" | "hardstyle" | "jerseyclub" | "poppunk" | "bedroompop" | "nudisco" | "trailer";

type Form = "club" | "hiphop" | "pop" | "cinema";
interface Sec { name: string; bars: number; drums: 0 | 1 | 2; bass: boolean; chords: boolean; lead: boolean; arp: boolean; pad: boolean; build?: boolean; }

const FORMS: Record<Form, Sec[]> = {
  club: [
    { name: "intro", bars: 8, drums: 1, bass: false, chords: false, lead: false, arp: false, pad: true },
    { name: "build", bars: 8, drums: 1, bass: false, chords: true, lead: false, arp: false, pad: true, build: true },
    { name: "drop", bars: 16, drums: 2, bass: true, chords: true, lead: true, arp: false, pad: false },
    { name: "break", bars: 8, drums: 0, bass: false, chords: true, lead: true, arp: false, pad: true },
    { name: "build", bars: 8, drums: 1, bass: false, chords: true, lead: false, arp: true, pad: true, build: true },
    { name: "drop", bars: 16, drums: 2, bass: true, chords: true, lead: true, arp: true, pad: false },
    { name: "outro", bars: 8, drums: 1, bass: true, chords: false, lead: false, arp: false, pad: true },
  ],
  hiphop: [
    { name: "intro", bars: 4, drums: 0, bass: false, chords: true, lead: true, arp: false, pad: true },
    { name: "verse", bars: 16, drums: 2, bass: true, chords: true, lead: false, arp: false, pad: true },
    { name: "hook", bars: 8, drums: 2, bass: true, chords: true, lead: true, arp: true, pad: true },
    { name: "verse", bars: 16, drums: 2, bass: true, chords: true, lead: false, arp: false, pad: true },
    { name: "hook", bars: 8, drums: 2, bass: true, chords: true, lead: true, arp: true, pad: true },
    { name: "outro", bars: 4, drums: 1, bass: false, chords: true, lead: true, arp: false, pad: true },
  ],
  pop: [
    { name: "intro", bars: 4, drums: 0, bass: false, chords: true, lead: false, arp: true, pad: true },
    { name: "verse", bars: 8, drums: 1, bass: true, chords: true, lead: true, arp: false, pad: false },
    { name: "pre", bars: 4, drums: 2, bass: true, chords: true, lead: true, arp: false, pad: true, build: true },
    { name: "chorus", bars: 8, drums: 2, bass: true, chords: true, lead: true, arp: true, pad: true },
    { name: "verse", bars: 8, drums: 2, bass: true, chords: true, lead: true, arp: false, pad: false },
    { name: "chorus", bars: 8, drums: 2, bass: true, chords: true, lead: true, arp: true, pad: true },
    { name: "bridge", bars: 8, drums: 1, bass: false, chords: true, lead: true, arp: false, pad: true },
    { name: "chorus", bars: 8, drums: 2, bass: true, chords: true, lead: true, arp: true, pad: true },
    { name: "outro", bars: 4, drums: 0, bass: false, chords: true, lead: false, arp: true, pad: true },
  ],
  cinema: [
    { name: "intro", bars: 8, drums: 0, bass: false, chords: true, lead: false, arp: true, pad: true },
    { name: "build", bars: 8, drums: 1, bass: true, chords: true, lead: false, arp: true, pad: true, build: true },
    { name: "hit", bars: 16, drums: 2, bass: true, chords: true, lead: true, arp: true, pad: true },
    { name: "break", bars: 8, drums: 0, bass: false, chords: true, lead: true, arp: false, pad: true },
    { name: "build", bars: 8, drums: 1, bass: true, chords: true, lead: false, arp: true, pad: true, build: true },
    { name: "finale", bars: 16, drums: 2, bass: true, chords: true, lead: true, arp: true, pad: true },
    { name: "outro", bars: 4, drums: 0, bass: false, chords: true, lead: false, arp: false, pad: true },
  ],
};

interface Genre {
  label: string; form: Form; bpm: [number, number]; minor: boolean;
  /** 16ステップ（1小節）のパターン。x=打つ、X=強く、.=休み、r=ロール（32分2連打）。 */
  kick: string[]; snare?: string[]; clap?: string[]; hat: string[]; open?: string; extra?: { inst: Instrument; pat: string; vol: number; pan: number };
  /** 進行（度数）。 */
  progs: number[][];
  bass: { inst: Instrument; pat: string; oct: number; walk?: boolean; vol: number };
  chord: { inst: Instrument; pat: string; oct: number; seventh: boolean; ninth?: boolean; vol: number; pan: number };
  arp?: { inst: Instrument; oct: number; vol: number; pan: number; up: number[] };
  lead: { inst: Instrument; oct: number; vol: number; rhythms: string[]; range: number };
  pad?: { inst: Instrument; vol: number };
  chops?: boolean; drumKit: number; pump: false | true | "all"; synth: boolean;
  riser: boolean; strings?: boolean; crashOnSection: boolean;
  /** ジャンルらしい、曲全体のエフェクト。 */
  fx?: MasterFxSettings;
}

const GENRES: Record<ModernStyle, Genre> = {
  trap: { label: "トラップ", form: "hiphop", bpm: [136, 148], minor: true, kick: ["x.....x...x.....", "x.....x..x..x..."], snare: ["........x......."], clap: ["........x......."], hat: ["x.x.x.x.x.x.x.x.", "x.x.x.xrx.x.rrrr", "xxx.x.x.x.xxx.xr"], open: "......x.......x.",
    progs: [[1, 6, 3, 7], [1, 1, 6, 7], [6, 7, 1, 1]], bass: { inst: "sub808", pat: "x.....x...x.....", oct: 1, vol: 0.34 }, chord: { inst: "pad", pat: "x...............", oct: 3, seventh: false, vol: 0.1, pan: 0 },
    arp: { inst: "bell", oct: 5, vol: 0.13, pan: 0.3, up: [0, 4, 7, 12, 7, 4] }, lead: { inst: "bell", oct: 5, vol: 0.14, rhythms: ["x..x..x.........", "x.....x...x....."], range: 5 }, pad: { inst: "strings", vol: 0.1 }, chops: true, drumKit: 25, pump: false, synth: true, riser: false, crashOnSection: true },
  drill: { label: "ドリル", form: "hiphop", bpm: [140, 146], minor: true, kick: ["x.......x.x.....", "x.....x...x....."], snare: ["............x..."], clap: ["............x..."], hat: ["x.xx.xx.x.xx.xx.", "xxx.xx.xxx.xx.xx"], open: "..x.............",
    progs: [[1, 1, 7, 6], [1, 6, 7, 7], [1, 3, 7, 6]], bass: { inst: "sub808", pat: "x...x..x..x.....", oct: 1, walk: true, vol: 0.34 }, chord: { inst: "strings", pat: "x...............", oct: 3, seventh: false, vol: 0.13, pan: 0 },
    arp: { inst: "piano", oct: 4, vol: 0.14, pan: -0.2, up: [0, 3, 7, 3, 12, 7] }, lead: { inst: "piano", oct: 5, vol: 0.15, rhythms: ["x..x..x.x.......", "x.x...x........."], range: 5 }, pad: { inst: "pad", vol: 0.09 }, drumKit: 25, pump: false, synth: false, riser: false, crashOnSection: false },
  lofi: { label: "ローファイ・ヒップホップ", form: "hiphop", bpm: [72, 86], minor: false, kick: ["x.....x.x.......", "x.....x...x....."], snare: ["....x.......x..."], hat: ["x.x.x.x.x.x.x.x."], open: "",
    progs: [[2, 5, 1, 6], [4, 3, 6, 1], [1, 6, 2, 5]], bass: { inst: "bass", pat: "x.....x.x.......", oct: 2, vol: 0.24 }, chord: { inst: "keys", pat: "x.....x...x.....", oct: 3, seventh: true, ninth: true, vol: 0.16, pan: -0.2 },
    arp: { inst: "guitar", oct: 3, vol: 0.12, pan: 0.3, up: [0, 4, 7, 11, 7, 4] }, lead: { inst: "keys", oct: 4, vol: 0.14, rhythms: ["..x...x.x.......", "x...x.....x....."], range: 4 }, pad: { inst: "pad", vol: 0.07 }, drumKit: 32, pump: false, synth: false, riser: false, crashOnSection: false, fx: { tape: 0.6, chorus: 0.35 } },
  futurebass: { label: "フューチャーベース", form: "club", bpm: [146, 158], minor: false, kick: ["x.......x......."], snare: ["........x......."], clap: ["........x......."], hat: ["x.x.x.x.x.x.x.x."], open: "..x...x...x...x.",
    progs: [[6, 4, 1, 5], [4, 5, 3, 6], [1, 5, 6, 4]], bass: { inst: "sub808", pat: "x.......x.......", oct: 1, vol: 0.34 }, chord: { inst: "lead", pat: "x..x..x.x.......", oct: 4, seventh: false, vol: 0.16, pan: 0 },
    arp: { inst: "bell", oct: 5, vol: 0.12, pan: 0.35, up: [0, 4, 7, 12, 16, 12, 7, 4] }, lead: { inst: "lead", oct: 5, vol: 0.18, rhythms: ["x..x..x.x..x....", "x.x.x...x......."], range: 6 }, pad: { inst: "pad", vol: 0.11 }, chops: true, drumKit: 24, pump: "all", synth: true, riser: true, crashOnSection: true },
  hyperpop: { label: "ハイパーポップ", form: "pop", bpm: [150, 172], minor: false, kick: ["x..x..x...x.x...", "x..x..x.x..x..x."], snare: ["....x.......x..."], clap: ["....x.......x..r"], hat: ["xxxxxxxxxxxxxxxx", "x.xxx.xxx.xxx.xr"], open: "..x...x...x...x.",
    progs: [[1, 5, 6, 4], [6, 4, 1, 5], [4, 1, 5, 6]], bass: { inst: "sub808", pat: "x..x..x.x..x..x.", oct: 1, vol: 0.3 }, chord: { inst: "lead", pat: "x..x..x...x.x...", oct: 4, seventh: false, vol: 0.14, pan: -0.2 },
    arp: { inst: "bell", oct: 6, vol: 0.11, pan: 0.4, up: [0, 7, 12, 16, 19, 16, 12, 7] }, lead: { inst: "lead", oct: 5, vol: 0.19, rhythms: ["x.xx.xx.x.xx.x..", "xx.xx.xx.x.x.xx."], range: 7 }, pad: { inst: "pad", vol: 0.08 }, chops: true, drumKit: 24, pump: "all", synth: true, riser: true, crashOnSection: true, fx: { bitcrush: 11, chorus: 0.2 } },
  synthwave: { label: "シンセウェイブ", form: "pop", bpm: [96, 112], minor: true, kick: ["x...x...x...x..."], snare: ["....x.......x..."], clap: ["....x.......x..."], hat: ["x.x.x.x.x.x.x.x.", "xxxxxxxxxxxxxxxx"], open: "..x...x...x...x.",
    progs: [[1, 6, 3, 7], [1, 7, 6, 7], [6, 7, 1, 1]], bass: { inst: "sub808", pat: "x.xxx.xxx.xxx.xx", oct: 1, vol: 0.28 }, chord: { inst: "pad", pat: "x...............", oct: 3, seventh: false, vol: 0.12, pan: 0 },
    arp: { inst: "lead", oct: 4, vol: 0.13, pan: 0.3, up: [0, 3, 7, 12, 7, 3, 0, 3] }, lead: { inst: "lead", oct: 5, vol: 0.17, rhythms: ["x...x.x.x.......", "x..x..x.x.x....."], range: 5 }, pad: { inst: "strings", vol: 0.1 }, drumKit: 24, pump: true, synth: true, riser: false, crashOnSection: true, fx: { chorus: 0.4, delay: { beats: 0.75, feedback: 0.35, mix: 0.2 } } },
  citypop: { label: "シティポップ", form: "pop", bpm: [104, 116], minor: false, kick: ["x.....x...x.x...", "x.....x..x..x..."], snare: ["....x.......x..."], hat: ["x.x.x.x.x.x.x.x."], open: "..x...x...x...x.",
    progs: [[4, 5, 3, 6], [2, 5, 1, 6], [1, 3, 4, 5]], bass: { inst: "slap", pat: "x..x.xx.x..x.xx.", oct: 2, walk: true, vol: 0.26 }, chord: { inst: "keys", pat: "x..x..x...x.x...", oct: 3, seventh: true, ninth: true, vol: 0.16, pan: -0.25 },
    arp: { inst: "guitar", oct: 3, vol: 0.12, pan: 0.3, up: [0, 4, 7, 11, 14, 11, 7, 4] }, lead: { inst: "brass", oct: 4, vol: 0.18, rhythms: ["x.x..x..x.x.....", "x..x.x..x......."], range: 6 }, pad: { inst: "strings", vol: 0.09 }, drumKit: 0, pump: false, synth: false, riser: false, crashOnSection: true, fx: { chorus: 0.3 } },
  house: { label: "ハウス", form: "club", bpm: [122, 128], minor: true, kick: ["x...x...x...x..."], clap: ["....x.......x..."], hat: ["x.x.x.x.x.x.x.x.", ".xx.xx.xxx.xx.xx"], open: "..x...x...x...x.",
    progs: [[1, 6, 4, 5], [1, 4, 6, 5], [6, 4, 1, 5]], bass: { inst: "sub808", pat: "..x...x...x...x.", oct: 1, vol: 0.3 }, chord: { inst: "piano", pat: "x..x..x...x.x...", oct: 4, seventh: true, vol: 0.17, pan: -0.15 },
    arp: { inst: "keys", oct: 4, vol: 0.11, pan: 0.3, up: [0, 4, 7, 4] }, lead: { inst: "lead", oct: 5, vol: 0.15, rhythms: ["x..x..x.x.......", "x.x...x........."], range: 5 }, pad: { inst: "pad", vol: 0.1 }, chops: true, drumKit: 24, pump: "all", synth: true, riser: true, crashOnSection: true },
  techno: { label: "テクノ", form: "club", bpm: [128, 138], minor: true, kick: ["x...x...x...x..."], clap: ["....x.......x..."], hat: [".x.x.x.x.x.x.x.x", "xx.xx.xx.xx.xx.x"], open: "..x...x...x...x.",
    progs: [[1, 1, 1, 1], [1, 1, 7, 7], [1, 1, 6, 7]], bass: { inst: "sub808", pat: "xxxxxxxxxxxxxxxx", oct: 1, vol: 0.26 }, chord: { inst: "lead", pat: "x..x..x...x.....", oct: 4, seventh: false, vol: 0.12, pan: -0.2 },
    arp: { inst: "lead", oct: 4, vol: 0.12, pan: 0.3, up: [0, 0, 7, 0, 12, 0, 7, 3] }, lead: { inst: "lead", oct: 5, vol: 0.13, rhythms: ["x.x.xx.x.x.xx.x.", "x..x..x..x..x..."], range: 4 }, pad: { inst: "pad", vol: 0.08 }, drumKit: 24, pump: "all", synth: true, riser: true, crashOnSection: true },
  trance: { label: "トランス", form: "club", bpm: [136, 142], minor: true, kick: ["x...x...x...x..."], clap: ["....x.......x..."], hat: ["..x...x...x...x.", "xxxxxxxxxxxxxxxx"], open: "..x...x...x...x.",
    progs: [[1, 6, 3, 7], [6, 7, 1, 1], [1, 7, 6, 7]], bass: { inst: "sub808", pat: ".xxx.xxx.xxx.xxx", oct: 1, vol: 0.27 }, chord: { inst: "pad", pat: "x...............", oct: 3, seventh: false, vol: 0.13, pan: 0 },
    arp: { inst: "lead", oct: 5, vol: 0.15, pan: 0.3, up: [0, 3, 7, 3, 12, 7, 3, 7] }, lead: { inst: "lead", oct: 5, vol: 0.18, rhythms: ["x...x...x...x...", "x.x.x...x...x.x."], range: 6 }, pad: { inst: "strings", vol: 0.1 }, drumKit: 24, pump: "all", synth: true, riser: true, crashOnSection: true },
  dnb: { label: "ドラムンベース", form: "club", bpm: [170, 176], minor: true, kick: ["x.........x....."], snare: ["....x.......x..."], hat: ["x.x.x.x.x.x.x.x.", "xxx.xxx.xxx.xxx."], open: "..x.......x.....",
    progs: [[1, 6, 7, 1], [1, 1, 7, 6], [6, 7, 1, 3]], bass: { inst: "sub808", pat: "x.....x...x.....", oct: 1, walk: true, vol: 0.3 }, chord: { inst: "pad", pat: "x...............", oct: 3, seventh: true, vol: 0.11, pan: 0 },
    arp: { inst: "keys", oct: 4, vol: 0.11, pan: 0.3, up: [0, 3, 7, 10, 7, 3] }, lead: { inst: "lead", oct: 5, vol: 0.15, rhythms: ["x..x..x.x..x....", "x.x..x..x......."], range: 5 }, pad: { inst: "strings", vol: 0.08 }, drumKit: 24, pump: true, synth: true, riser: true, crashOnSection: true },
  dubstep: { label: "ダブステップ", form: "club", bpm: [138, 144], minor: true, kick: ["x.........x....."], snare: ["........x......."], clap: ["........x......."], hat: ["x.x.x.x.x.x.x.x.", "..x...x...x...x."], open: "",
    progs: [[1, 1, 6, 7], [1, 7, 6, 7], [1, 3, 6, 7]], bass: { inst: "sub808", pat: "xxx.xxx.xxx.xxx.", oct: 1, walk: true, vol: 0.32 }, chord: { inst: "lead", pat: "x.......x.......", oct: 4, seventh: false, vol: 0.14, pan: 0 },
    arp: { inst: "bell", oct: 5, vol: 0.1, pan: 0.3, up: [0, 3, 7, 3] }, lead: { inst: "lead", oct: 4, vol: 0.16, rhythms: ["x..x..x.x.......", "x.....x.x...x..."], range: 5 }, pad: { inst: "pad", vol: 0.09 }, drumKit: 24, pump: "all", synth: true, riser: true, crashOnSection: true },
  ukgarage: { label: "UKガラージ", form: "club", bpm: [130, 136], minor: true, kick: ["x.......x.....x.", "x.....x.x......."], snare: ["....x.......x..."], clap: ["....x.......x..."], hat: ["x.xx.xx.xx.xx.xx", "..x..x..x..x..x."], open: "..x...x...x...x.",
    progs: [[1, 6, 4, 5], [6, 4, 1, 5], [2, 5, 1, 6]], bass: { inst: "sub808", pat: "x..x..x...x.x...", oct: 1, vol: 0.3 }, chord: { inst: "keys", pat: "x..x....x..x....", oct: 4, seventh: true, vol: 0.15, pan: -0.2 },
    arp: { inst: "bell", oct: 5, vol: 0.1, pan: 0.3, up: [0, 4, 7, 11] }, lead: { inst: "choir", oct: 4, vol: 0.15, rhythms: ["x..x..x.x..x....", "..x..x..x......."], range: 5 }, pad: { inst: "pad", vol: 0.09 }, chops: true, drumKit: 24, pump: true, synth: true, riser: true, crashOnSection: true },
  amapiano: { label: "アマピアノ", form: "hiphop", bpm: [108, 116], minor: true, kick: ["x.......x.......", "x.....x.x......."], snare: ["....x.......x..."], clap: ["....x.......x..."], hat: ["x.xxx.xxx.xxx.xx"], open: "..x...x...x...x.", extra: { inst: "hihat", pat: "xxxxxxxxxxxxxxxx", vol: 0.06, pan: 0.4 },
    progs: [[1, 6, 4, 5], [6, 4, 1, 5], [1, 4, 6, 5]], bass: { inst: "sub808", pat: "x..x..x.x..x..x.", oct: 1, walk: true, vol: 0.32 }, chord: { inst: "piano", pat: "x..x..x...x.x...", oct: 4, seventh: true, vol: 0.17, pan: -0.15 },
    arp: { inst: "piano", oct: 5, vol: 0.12, pan: 0.3, up: [0, 4, 7, 11, 7, 4] }, lead: { inst: "choir", oct: 4, vol: 0.14, rhythms: ["x..x..x.........", "..x..x..x......."], range: 5 }, pad: { inst: "pad", vol: 0.09 }, chops: true, drumKit: 24, pump: false, synth: false, riser: false, crashOnSection: false, fx: { tape: 0.2 } },
  reggaeton: { label: "レゲトン", form: "pop", bpm: [92, 100], minor: true, kick: ["x...x...x...x..."], snare: ["...x..x....x..x."], hat: ["x.x.x.x.x.x.x.x."], open: "..x...x...x...x.",
    progs: [[1, 7, 6, 7], [1, 4, 5, 1], [6, 7, 1, 1]], bass: { inst: "sub808", pat: "x..x..x.x..x..x.", oct: 1, vol: 0.3 }, chord: { inst: "keys", pat: "x..x..x...x.....", oct: 4, seventh: false, vol: 0.14, pan: -0.2 },
    arp: { inst: "bell", oct: 5, vol: 0.11, pan: 0.3, up: [0, 3, 7, 3] }, lead: { inst: "lead", oct: 5, vol: 0.16, rhythms: ["x..x..x.x..x....", "x.x..x..x......."], range: 5 }, pad: { inst: "pad", vol: 0.07 }, chops: true, drumKit: 25, pump: false, synth: true, riser: false, crashOnSection: true },
  vaporwave: { label: "ヴェイパーウェイブ", form: "hiphop", bpm: [62, 76], minor: false, kick: ["x.......x.......", "x.......x.x....."], snare: ["....x.......x..."], hat: ["x...x...x...x..."], open: "",
    progs: [[1, 4, 3, 6], [4, 3, 2, 1], [1, 6, 4, 5]], bass: { inst: "bass", pat: "x.......x.......", oct: 2, vol: 0.22 }, chord: { inst: "keys", pat: "x.......x.......", oct: 3, seventh: true, ninth: true, vol: 0.17, pan: -0.15 },
    arp: { inst: "bell", oct: 5, vol: 0.1, pan: 0.3, up: [0, 4, 7, 11, 14, 11] }, lead: { inst: "keys", oct: 4, vol: 0.14, rhythms: ["x.....x...x.....", "..x.....x......."], range: 4 }, pad: { inst: "pad", vol: 0.12 }, drumKit: 0, pump: false, synth: true, riser: false, crashOnSection: false, fx: { tape: 0.4, chorus: 0.6, delay: { beats: 0.75, feedback: 0.45, mix: 0.3 } } },
  hardstyle: { label: "ハードスタイル", form: "club", bpm: [148, 156], minor: true, kick: ["x...x...x...x..."], snare: ["....x.......x..."], clap: ["....x.......x..."], hat: ["..x...x...x...x."], open: "..x...x...x...x.",
    progs: [[1, 6, 7, 1], [1, 7, 6, 7], [6, 7, 1, 3]], bass: { inst: "sub808", pat: "..xx..xx..xx..xx", oct: 1, vol: 0.33 }, chord: { inst: "lead", pat: "x...x...x...x...", oct: 4, seventh: false, vol: 0.13, pan: 0 },
    arp: { inst: "lead", oct: 5, vol: 0.12, pan: 0.3, up: [0, 3, 7, 12] }, lead: { inst: "lead", oct: 5, vol: 0.2, rhythms: ["x..x..x.x..x..x.", "x.x.x.x.x...x..."], range: 6 }, pad: { inst: "pad", vol: 0.1 }, drumKit: 24, pump: "all", synth: true, riser: true, crashOnSection: true },
  jerseyclub: { label: "ジャージークラブ", form: "club", bpm: [136, 144], minor: true, kick: ["x..x..x...x.x...", "x..x..x..x..x..x"], clap: ["....x.......x..."], snare: ["....x.......x..r"], hat: ["x.x.x.x.x.x.x.x."], open: "",
    progs: [[1, 6, 3, 7], [1, 4, 6, 5], [6, 7, 1, 1]], bass: { inst: "sub808", pat: "x..x..x...x.x...", oct: 1, vol: 0.32 }, chord: { inst: "piano", pat: "x..x..x...x.....", oct: 4, seventh: false, vol: 0.16, pan: -0.15 },
    arp: { inst: "bell", oct: 5, vol: 0.11, pan: 0.3, up: [0, 3, 7, 12] }, lead: { inst: "choir", oct: 4, vol: 0.15, rhythms: ["x.x..x..x.x.....", "x..x..x.........", "..x.x.x.x......."], range: 5 }, pad: { inst: "pad", vol: 0.08 }, chops: true, drumKit: 24, pump: "all", synth: true, riser: true, crashOnSection: true },
  poppunk: { label: "ポップパンク", form: "pop", bpm: [164, 184], minor: false, kick: ["x.....x.x.....x.", "x.x...x.x.x...x."], snare: ["....x.......x..."], hat: ["x.x.x.x.x.x.x.x."], open: "..x...x...x...x.",
    progs: [[1, 5, 6, 4], [1, 4, 5, 5], [6, 4, 1, 5]], bass: { inst: "bass", pat: "x.x.x.x.x.x.x.x.", oct: 2, vol: 0.26 }, chord: { inst: "crunch", pat: "x.x.x.x.x.x.x.x.", oct: 3, seventh: false, vol: 0.15, pan: -0.4 },
    arp: { inst: "guitar", oct: 4, vol: 0.11, pan: 0.4, up: [0, 4, 7, 12] }, lead: { inst: "leadGuitar", oct: 4, vol: 0.2, rhythms: ["x.x.x.x.x.x.....", "x..x.x..x.x.x..."], range: 6 }, pad: { inst: "strings", vol: 0.07 }, drumKit: 16, pump: false, synth: false, riser: false, crashOnSection: true },
  bedroompop: { label: "ベッドルームポップ", form: "pop", bpm: [92, 108], minor: false, kick: ["x.....x.....x...", "x.....x...x....."], snare: ["....x.......x..."], hat: ["x.x.x.x.x.x.x.x."], open: "",
    progs: [[1, 5, 6, 4], [6, 4, 1, 5], [4, 1, 5, 6]], bass: { inst: "bass", pat: "x.....x.x.....x.", oct: 2, vol: 0.22 }, chord: { inst: "guitar", pat: "x..x..x...x.x...", oct: 3, seventh: true, vol: 0.15, pan: -0.3 },
    arp: { inst: "keys", oct: 4, vol: 0.11, pan: 0.3, up: [0, 4, 7, 11, 7, 4] }, lead: { inst: "keys", oct: 5, vol: 0.15, rhythms: ["x..x..x.x.......", "..x...x.x...x..."], range: 5 }, pad: { inst: "pad", vol: 0.09 }, drumKit: 0, pump: false, synth: false, riser: false, crashOnSection: false, fx: { tape: 0.3, chorus: 0.2 } },
  nudisco: { label: "ニューディスコ", form: "pop", bpm: [114, 122], minor: false, kick: ["x...x...x...x..."], snare: ["....x.......x..."], clap: ["....x.......x..."], hat: ["..x...x...x...x.", "x.x.x.x.x.x.x.x."], open: "..x...x...x...x.",
    progs: [[6, 4, 1, 5], [2, 5, 1, 4], [4, 5, 3, 6]], bass: { inst: "slap", pat: "x.xxx.xxx.xxx.xx", oct: 2, walk: true, vol: 0.26 }, chord: { inst: "guitar", pat: "x.xx.xx.x.xx.xx.", oct: 3, seventh: true, vol: 0.15, pan: -0.3 },
    arp: { inst: "keys", oct: 4, vol: 0.11, pan: 0.3, up: [0, 4, 7, 11] }, lead: { inst: "brass", oct: 4, vol: 0.18, rhythms: ["x.x..x..x.x.....", "x..x.x..x......."], range: 6 }, pad: { inst: "strings", vol: 0.09 }, drumKit: 0, pump: "all", synth: false, riser: false, crashOnSection: true },
  trailer: { label: "ハイブリッド・トレイラー", form: "cinema", bpm: [84, 100], minor: true, kick: ["x...............", "x.......x......."], snare: ["................", "........x......."], hat: ["................"], open: "",
    progs: [[1, 6, 3, 7], [1, 7, 6, 5], [6, 7, 1, 1]], bass: { inst: "sub808", pat: "x...............", oct: 1, vol: 0.32 }, chord: { inst: "strings", pat: "x.x.x.x.x.x.x.x.", oct: 3, seventh: false, vol: 0.14, pan: -0.2 },
    arp: { inst: "strings", oct: 4, vol: 0.1, pan: 0.3, up: [0, 7, 12, 7] }, lead: { inst: "brass", oct: 3, vol: 0.2, rhythms: ["x...............", "x.......x......."], range: 4 }, pad: { inst: "choir", vol: 0.12 }, drumKit: 16, pump: false, synth: false, riser: true, strings: true, crashOnSection: true, fx: { delay: { beats: 1.5, feedback: 0.3, mix: 0.12 } } },
};

export const MODERN_STYLE_LABEL = Object.fromEntries(Object.entries(GENRES).map(([k, v]) => [k, v.label])) as Record<ModernStyle, string>;
export const isModernStyle = (s: string): s is ModernStyle => s in GENRES;

const NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
const nm = (m: number): string => NAMES[((m % 12) + 12) % 12] + (Math.floor(m / 12) - 1);
const TONIC: Record<string, number> = { C: 0, "C#": 1, Db: 1, D: 2, "D#": 3, Eb: 3, E: 4, F: 5, "F#": 6, Gb: 6, G: 7, "G#": 8, Ab: 8, A: 9, "A#": 10, Bb: 10, B: 11 };
const MAJ = [0, 2, 4, 5, 7, 9, 11], MIN = [0, 2, 3, 5, 7, 8, 10];
function rngOf(seed: number): () => number { let a = seed >>> 0; return () => { a = (a + 0x6d2b79f5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }

/** ジャンルの曲を組み立てる（すべて4拍子）。 */
export function genreScore(spec: SongSpec): Score {
  const g = GENRES[spec.style as ModernStyle];
  const rng = rngOf(spec.seed);
  const pickOf = <T,>(a: T[]): T => a[Math.floor(rng() * a.length)];
  const tonic = TONIC[spec.tonic] ?? 0, minor = spec.minor, scale = minor ? MIN : MAJ;
  const bpm = Math.round(spec.bpm > 0 ? spec.bpm : (g.bpm[0] + g.bpm[1]) / 2);
  const degSemi = (d: number): number => Math.floor((d - 1) / 7) * 12 + scale[(((d - 1) % 7) + 7) % 7];
  const midiOf = (d: number, oct: number): number => 12 * (oct + 1) + tonic + degSemi(d);
  const chordTones = (d: number, seventh: boolean, ninth: boolean): number[] => { const t = [0, degSemi(d + 2) - degSemi(d), degSemi(d + 4) - degSemi(d)]; if (seventh) t.push(degSemi(d + 6) - degSemi(d)); if (ninth) t.push(degSemi(d + 8) - degSemi(d)); return t; };
  const secs = FORMS[g.form];
  const total = secs.reduce((n, s) => n + s.bars, 0), steps = total * 16;
  const prog = pickOf(g.progs), prog2 = pickOf(g.progs);
  const kickVar = pickOf(g.kick), hatVar = pickOf(g.hat);
  const cell = (arr: (null | { n: string; len: number })[], i: number, n: string, len = 1): void => { if (i >= 0 && i < steps) arr[i] = { n, len }; };
  const mk = (): (null | { n: string; len: number })[] => Array(steps).fill(null);
  const T: Record<string, (null | { n: string; len: number })[]> = { kick: mk(), snare: mk(), clap: mk(), hihat: mk(), openhat: mk(), crash: mk(), extra: mk(), riser: mk(), tom: mk(), bass: mk(), chord: mk(), arp: mk(), lead: mk(), pad: mk(), chop: mk(), strings: mk() };
  const stepsOf = (p: string): number[] => [...p].flatMap((c, i) => (c === "." ? [] : [i]));
  let bar = 0;
  secs.forEach((sec, si) => {
    const isLastOfSong = si === secs.length - 1;
    for (let i = 0; i < sec.bars; i++, bar++) {
      const b0 = bar * 16, p = (si % 2 === 0 ? prog : prog2)[(i >> (g.form === "hiphop" || g.form === "cinema" ? 1 : 0)) % 4] ?? 1;
      const d = p, lastBar = i === sec.bars - 1;
      // ドラム
      if (sec.drums >= 1) {
        for (const k of stepsOf(kickVar)) if (sec.drums === 2 || k % 4 === 0) cell(T.kick, b0 + k, "x");
        if (sec.drums === 1 && !stepsOf(kickVar).some((k) => k % 4 === 0)) cell(T.kick, b0, "x");
        for (const [k, c] of [...hatVar].entries()) { if (c === "x" && (sec.drums === 2 || k % 4 === 2)) cell(T.hihat, b0 + k, "x"); else if (c === "r" && sec.drums === 2) { cell(T.hihat, b0 + k, "x", 1); } }
      }
      if (sec.drums === 2) {
        const sn = g.snare ? pickOf(g.snare) : "", cl = g.clap ? pickOf(g.clap) : "";
        for (const k of stepsOf(sn)) cell(T.snare, b0 + k, "x"); for (const k of stepsOf(cl)) cell(T.clap, b0 + k, "x");
        if (g.open) for (const k of stepsOf(g.open)) cell(T.openhat, b0 + k, "x");
        if (g.extra) for (const k of stepsOf(g.extra.pat)) cell(T.extra, b0 + k, "x");
        if (g.crashOnSection && i === 0) cell(T.crash, b0, "x");
        if (lastBar && !isLastOfSong) for (let k = 12; k < 16; k++) cell(T.tom, b0 + k, "x");
      }
      // ビルド: ライザー（区間全体で1音）とスネアロール（最後の4小節で、だんだん細かく）
      if (sec.build && g.riser && i === 0) cell(T.riser, b0, nm(midiOf(1, 5)), sec.bars * 16);
      if (sec.build) { if (i >= sec.bars - 4) for (let k = 0; k < 16; k += i >= sec.bars - 2 ? 1 : 2) cell(T.snare, b0 + k, "x"); if (lastBar) cell(T.crash, b0 + 16, "x"); }
      if (sec.build && lastBar) { for (let k = 0; k < 16; k++) if (k >= 12) T.kick[b0 + k] = null; }
      // ベース
      if (sec.bass) { const pat = g.bass.pat; stepsOf(pat).forEach((k, n, all) => { const next = all[n + 1] ?? 16; let note = midiOf(d, g.bass.oct); if (g.bass.walk && n % 3 === 2) note += minor ? 7 : 7; if (g.bass.walk && n % 4 === 3) note += 12; cell(T.bass, b0 + k, nm(note), Math.max(1, next - k)); }); }
      // 和音
      if (sec.chords) { const tones = chordTones(d, g.chord.seventh, !!g.chord.ninth); const pat = sec.drums === 0 && g.form !== "cinema" ? "x..............." : g.chord.pat; stepsOf(pat).forEach((k, n, all) => { const next = all[n + 1] ?? 16; const idx = n % tones.length; cell(T.chord, b0 + k, nm(midiOf(d, g.chord.oct) + tones[idx] + (idx >= 3 ? 0 : 0)), Math.max(1, Math.min(4, next - k))); }); }
      // パッド（1小節の長い音）
      if (sec.pad && g.pad) { const tones = chordTones(d, false, false); cell(T.pad, b0, nm(midiOf(d, 4) + tones[2]), 16); }
      if (sec.pad && g.strings) cell(T.strings, b0, nm(midiOf(d, 3) + chordTones(d, false, false)[1]), 16);
      // アルペジオ
      if (sec.arp && g.arp) { const tones = chordTones(d, false, false); for (let k = 0; k < 16; k += 2) { const u = g.arp.up[(k / 2) % g.arp.up.length]; const base = tones[(u === 0 ? 0 : u <= 4 ? 1 : 2)] ?? 0; cell(T.arp, b0 + k, nm(midiOf(d, g.arp.oct) + base + (u >= 12 ? 12 : 0)), 2); } }
      // リード: 2小節ごとにリズムを選び、コードの音を軸に階段状に動く
      if (sec.lead) { const rhy = g.lead.rhythms[(bar >> 1) % g.lead.rhythms.length]; let deg = d + (rng() < 0.5 ? 0 : 2); stepsOf(rhy).forEach((k, n, all) => { const next = all[n + 1] ?? 16; if (n > 0) deg += pickOf([-2, -1, 1, 1, 2]); deg = Math.max(d - 2, Math.min(d + g.lead.range, deg)); if (n === 0) deg = d + pickOf([0, 2, 4]); cell(T.lead, b0 + k, nm(midiOf(deg, g.lead.oct)), Math.max(1, Math.min(6, next - k))); }); }
      // ボーカルチョップ風（休符をはさむ短い合唱）
      if (g.chops && sec.lead && sec.drums === 2 && i % 2 === 1) { const tones = chordTones(d, false, false); for (const k of [3, 6, 11]) cell(T.chop, b0 + k, nm(midiOf(d, 4) + tones[k === 6 ? 2 : 1]), 2); }
    }
  });
  // 曲の最後は、根音の長い音で締める
  const endStep = (total - 1) * 16;
  for (const key of ["kick", "snare", "clap", "hihat", "openhat", "extra", "tom", "riser", "bass", "chord", "arp", "lead", "chop"]) for (let k = 0; k < 16; k++) T[key][endStep + k] = null;
  cell(T.kick, endStep, "x"); cell(T.crash, endStep, "x"); cell(T.bass, endStep, nm(midiOf(1, g.bass.oct)), 16); cell(T.pad, endStep, nm(midiOf(1, 4) + (minor ? 3 : 4)), 16);
  const toNotes = (arr: (null | { n: string; len: number })[]): NoteEvent[] => {
    const out: NoteEvent[] = []; let i = 0;
    const rest = (b: number): void => { while (b > 0) { const x = Math.min(b, 16); out.push({ note: REST, durationBeats: x }); b -= x; } };
    while (i < steps) { const e = arr[i]; if (!e) { let j = i; while (j < steps && !arr[j]) j++; rest((j - i) * 0.25); i = j; continue; } let nx = i + 1; while (nx < steps && !arr[nx]) nx++; const gap = nx - i, len = Math.min(e.len, gap); out.push({ note: e.n, durationBeats: len * 0.25 }); if (gap > len) rest((gap - len) * 0.25); i = nx; }
    return out;
  };
  const drum = (inst: Instrument, key: string, vol: number, pan: number): Track => ({ waveform: "square", instrument: inst, volume: vol, pan, notes: toNotes(T[key]).map((n) => (n.note === REST ? n : { ...n, note: "C2" })) });
  const mel = (inst: Instrument, key: string, vol: number, pan: number, wave: Track["waveform"] = "sawtooth"): Track => ({ waveform: wave, instrument: inst, volume: vol, pan, notes: toNotes(T[key]) });
  const tracks: Track[] = [
    drum("kick", "kick", 0.34, 0), drum("snare", "snare", 0.22, 0.05), drum("clap", "clap", 0.22, 0.1), drum("hihat", "hihat", 0.11, 0.25), drum("openhat", "openhat", 0.13, -0.25), drum("crash", "crash", 0.17, -0.2), drum("tom", "tom", 0.2, -0.15),
    mel(g.bass.inst, "bass", g.bass.vol, 0), mel(g.chord.inst, "chord", g.chord.vol, g.chord.pan),
    ...(g.arp ? [mel(g.arp.inst, "arp", g.arp.vol, g.arp.pan)] : []), mel(g.lead.inst, "lead", g.lead.vol, 0.1),
    ...(g.pad ? [mel(g.pad.inst, "pad", g.pad.vol, 0)] : []), ...(g.strings ? [mel("strings", "strings", 0.12, -0.3)] : []),
    ...(g.chops ? [mel("choir", "chop", 0.15, 0.35)] : []), ...(g.riser ? [mel("riser", "riser", 0.2, 0)] : []),
    ...(g.extra ? [drum(g.extra.inst, "extra", g.extra.vol, g.extra.pan)] : []),
  ].filter((t) => t.notes.some((n) => n.note !== REST));
  return { tempoBpm: bpm, loop: true, drumKit: g.drumKit, tone: "rock", tracks, ...(g.pump ? { pump: true } : {}), ...(g.pump === "all" ? { pumpAll: true } : {}), ...(g.synth ? { synth: true } : {}), ...(g.fx ? { fx: g.fx } : {}) };
}
