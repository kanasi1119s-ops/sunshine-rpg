import { resolveLayers, type ArrangeOptions, type Layer, type Section } from "./arrangement";
import { noteNameToMidi } from "./note";
import { REST, velocityScale, type Score } from "./score";
import { resampleEnergy, type EnergyCurve } from "./scene";
import { expandBars } from "./song-plan";

/**
 * ループ検査（docs/sound/form-structure-guide.md §12 の提案3、game-music-guide.md §10 の提案6）。
 * - checkLoop … 曲のJSONに "loop": true（または "seamless"、{startBar,endBar}）と書いたときだけ働く静的チェック。小節番号と直し方つき。
 * - checkScoreSeam … できあがった曲（Score）の継ぎ目の検査。最後の和音と頭の関係・末尾の山・静かな曲の頭の一撃・つながらない長い音。
 * どれも注意の文を返すだけで、曲は作れなくなりません。
 */

/** 場面ごとの、1周の長さの目安（秒）。form-structure-guide.md §8.1 の表に、少し余裕を持たせたもの。 */
export const LOOP_SECONDS: Record<string, [number, number]> = {
  battle: [18, 55], boss: [55, 120], finalBoss: [40, 150], town: [60, 125], village: [70, 130], field: [80, 140],
  dungeon: [90, 180], castle: [60, 150], shrine: [70, 160], mystery: [60, 150], sad: [40, 150], inn: [25, 60],
  title: [120, 210], ending: [120, 290],
};

const PC: Record<string, number> = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };
/** コード名の根音（0〜11）。読めなければ null。 */
export function chordRootPc(name: string): number | null {
  const m = /^([A-G])([#b]?)/.exec(name.split("/")[0]);
  return m ? (PC[m[1]] + (m[2] === "#" ? 1 : m[2] === "b" ? -1 : 0) + 12) % 12 : null;
}

/** 継ぎ目として自然な関係か（同じ・V・IV・♭VII）。last→first。 */
export function seamRelation(lastPc: number, firstPc: number): "same" | "V" | "IV" | "bVII" | null {
  const d = (((lastPc - firstPc) % 12) + 12) % 12;
  return d === 0 ? "same" : d === 7 ? "V" : d === 5 ? "IV" : d === 10 ? "bVII" : null;
}

export type LoopSpec = true | "seamless" | { startBar: number; endBar: number };
export function isLoopSpec(v: unknown): v is LoopSpec {
  return v === true || v === "seamless" || (!!v && typeof v === "object" && Number.isFinite(Number((v as { startBar?: unknown }).startBar)) && Number.isFinite(Number((v as { endBar?: unknown }).endBar)));
}

export interface LoopCheckInput {
  loop: unknown;
  bpm: number;
  beatsPerBar: number;
  totalBars: number;
  /** 1小節ごとのコード名（なければ空）。 */
  barChords: string[];
  sections?: Section[];
  arrange?: ArrangeOptions;
  energy?: unknown;
  scene?: string;
  /** パートの音の並び（同じ8小節のブロックを見つけるために使う）。 */
  parts?: { notes: string; instrument?: string }[];
  /** loopTail を使っているか。 */
  loopTail?: string;
}

const levelOf = (l: Layer, end: boolean): number => Math.max(1, Math.min(10, Math.round(10 * (Math.min(l.groups.length, 7) / 7) * Math.min(1, end ? l.to : l.from))));

function energyLevels(energy: unknown, n: number): number[] | null {
  if (Array.isArray(energy) && energy.length && energy.every((x) => Number.isFinite(Number(x)))) return resampleEnergy(energy.map(Number), n);
  if (typeof energy === "string") { try { const r = resampleEnergy(energy as EnergyCurve, n); return r.length ? r : null; } catch { return null; } }
  return null;
}

/** 「音名:拍」の並びを、曲の長さまで繰り返したトークン列（開始拍つき）にする。 */
function expandTokens(notes: string, total: number): { t: number; tok: string }[] {
  const toks = notes.trim().split(/\s+/).filter(Boolean);
  const dur = (s: string): number => { const m = /:(\d+(?:\.\d+)?)/.exec(s); return m ? Number(m[1]) : 0; };
  const out: { t: number; tok: string }[] = [];
  if (!toks.some((t) => dur(t) > 0)) return out;
  let pos = 0;
  for (let i = 0; pos < total - 1e-9 && i < 100000; i++) {
    const tok = toks[i % toks.length];
    const d = dur(tok);
    if (!(d > 0)) continue;
    out.push({ t: pos, tok });
    pos += d;
  }
  return out;
}

export function checkLoop(inp: LoopCheckInput): string[] {
  if (!isLoopSpec(inp.loop)) return [];
  const w: string[] = [];
  const { totalBars, beatsPerBar, barChords } = inp;
  const spec = inp.loop;
  let loopStart = 1, loopEnd = totalBars;
  if (typeof spec === "object") {
    loopStart = Math.round(Number(spec.startBar));
    loopEnd = Math.round(Number(spec.endBar));
    if (!(loopStart >= 1 && loopEnd > loopStart && loopEnd <= totalBars)) {
      w.push(`loop: startBar は1以上、endBar は startBar より大きく曲の長さ（${totalBars}小節）以下にしてください（今 ${spec.startBar}〜${spec.endBar}）`);
      loopStart = 1; loopEnd = totalBars;
    }
  }
  const sections = inp.sections;
  const layers = sections?.length ? resolveLayers(sections, inp.arrange) : undefined;
  const starts: number[] = [];
  if (sections) { let b = 0; for (const s of sections) { starts.push(b); b += s.bars; } }

  // ① 最後の強さと最初の強さ（ループの範囲の最初と最後のセクションで比べる）
  if (sections && layers && sections.length >= 2) {
    const iFirst = Math.max(0, starts.findIndex((s, i) => loopStart - 1 < s + sections[i].bars));
    let iLast = sections.length - 1;
    while (iLast > 0 && starts[iLast] >= loopEnd) iLast--;
    const lv = inp.energy !== undefined ? energyLevels(inp.energy, sections.length) : null;
    const first = lv ? lv[iFirst] : levelOf(layers[iFirst], false);
    const last = lv ? lv[iLast] : levelOf(layers[iLast], true);
    if (Math.abs(first - last) > 2) {
      w.push(`loop: 最後のセクション（${starts[iLast] + 1}小節目〜）の強さ ${last} が、最初のセクションの強さ ${first} と ${Math.abs(first - last)} 段階ちがいます。継ぎ目で急に強さが変わるので、最後を薄く・最初を濃く（または差を2以内に）。energy の最後の値を最初に近づけてください`);
    }
  }

  // ② 最後のコードが主和音・V・IV ではない
  if (barChords.length >= 2) {
    const firstPc = chordRootPc(barChords[loopStart - 1] ?? barChords[0]);
    const lastName = barChords[Math.min(barChords.length, loopEnd) - 1];
    const lastPc = chordRootPc(lastName);
    if (firstPc !== null && lastPc !== null && seamRelation(lastPc, firstPc) === null && !inp.loopTail) {
      w.push(`loop: ${loopEnd}小節目のコード ${lastName} が、頭（${barChords[loopStart - 1]}）につながりにくい形です（主和音・V・IV・♭VII が自然）。"loopTail": "dominant"（V7 で頭へ）か "deceptive"（偽終止）を試してください`);
    }
  }

  // ③ 長音・全休止で終わる
  if (sections?.length) {
    const lastSec = sections[Math.min(sections.length - 1, Math.max(0, starts.findLastIndex((s) => s < loopEnd)))];
    if (lastSec.kind === "tag" || (layers && layers[sections.indexOf(lastSec)]?.hold)) {
      w.push(`loop: 最後が余韻（tag／長音のみ）の場面です。ループのたびに音が途切れて隙間ができます。最後は outro（薄い編成）にして V か IV で頭へつなぐか、loop を外してください`);
    } else if (lastSec.kind === "break") {
      w.push(`loop: 最後が break（全員が止まる場面）です。継ぎ目が無音になります。最後の場面を変えてください`);
    }
  }

  // ④ 8の倍数でない
  const span = loopEnd - loopStart + 1;
  if (span % 4 !== 0) w.push(`loop: ループの長さ ${span} 小節が4の倍数ではありません。塊の長さは4の倍数（多くは8）にすると、聴き手が継ぎ目を予想できて自然です`);
  else if (span % 8 !== 0 && span >= 16) w.push(`loop: ループの長さ ${span} 小節は8の倍数ではありません（4の倍数なので許容。8の倍数が基本です）`);

  // ⑤ 同じ8小節ブロックが全体の半分以上（ループの中のループ）
  if (span >= 24 && span % 8 === 0) {
    const sigs: string[] = [];
    const total = totalBars * beatsPerBar;
    const tokens = (inp.parts ?? []).map((p) => expandTokens(String(p.notes ?? ""), total));
    for (let b = loopStart - 1; b + 8 <= loopEnd; b += 8) {
      const a = b * beatsPerBar, z = (b + 8) * beatsPerBar;
      const chords = barChords.slice(b, b + 8).join(",");
      const arr = layers && sections ? sections.map((s, i) => (starts[i] < b + 8 && starts[i] + s.bars > b ? `${s.kind}:${layers[i].groups.join("+")}` : "")).filter(Boolean).join("|") : "";
      const parts = tokens.map((tk) => tk.filter((x) => x.t >= a - 1e-9 && x.t < z - 1e-9).map((x) => `${(x.t - a).toFixed(2)}${x.tok}`).join(" ")).join("/");
      sigs.push(`${chords}#${arr}#${parts}`);
    }
    const count = new Map<string, number>();
    sigs.forEach((s) => count.set(s, (count.get(s) ?? 0) + 1));
    const top = Math.max(0, ...count.values());
    if (top >= 2 && top * 8 >= span / 2) {
      w.push(`loop: まったく同じ8小節のブロックが ${top} 回あります（全体 ${span} 小節の半分以上）。「ループの中のループ」で、聞こえる繰り返しの回数が増えます。2回目以降は旋律を変える・楽器を足す（occurrence: true）・別の進行にする、のどれかを`);
    }
  }

  // ⑥ 1周の長さが場面の目安の外
  const range = inp.scene ? LOOP_SECONDS[inp.scene] : undefined;
  if (inp.scene === "fanfare") w.push(`loop: scene "fanfare"（勝利・取得）はループさせない場面です。loop を外してください`);
  else if (range && inp.bpm > 0) {
    const sec = Math.round((span * beatsPerBar * 60) / inp.bpm);
    if (sec < range[0] || sec > range[1]) w.push(`loop: 1周 ${sec} 秒は、scene "${inp.scene}" の目安 ${range[0]}〜${range[1]} 秒の外です（${sec < range[0] ? "短すぎて、すぐ同じ所に戻ります" : "長すぎて、場面の滞在時間に合いません"}）`);
  }
  return w;
}

// ───────── できあがった曲（Score）の継ぎ目の検査 ─────────
const DRUMS = new Set(["kick", "snare", "hihat", "crash", "tom", "cowbell"]);
const BASSES = new Set(["bass", "sub808", "slap"]);

function beatsOf(notes: Score["tracks"][number]["notes"]): number {
  return notes.reduce((s, n) => s + n.durationBeats, 0);
}

/** 1小節ごとの「音の量」（音数×音量×強さ）。ドラム以外・以内で数える。 */
function barLevels(score: Score, beatsPerBar: number, bars: number, onlyPitched = false): number[] {
  const lv = new Array<number>(bars).fill(0);
  for (const t of score.tracks) {
    if (onlyPitched && t.instrument && DRUMS.has(t.instrument)) continue;
    let pos = 0;
    for (const n of t.notes) {
      if (n.note !== REST) {
        const b = Math.min(bars - 1, Math.floor(pos / beatsPerBar + 1e-9));
        lv[b] += t.volume * velocityScale(n.velocity);
      }
      pos += n.durationBeats;
    }
  }
  return lv;
}

function lowestPcInBar(score: Score, beatsPerBar: number, bar: number, bassOnly: boolean): number | null {
  let best: number | null = null;
  for (const t of score.tracks) {
    if (t.instrument && DRUMS.has(t.instrument)) continue;
    if (bassOnly && !(t.instrument && BASSES.has(t.instrument))) continue;
    let pos = 0;
    for (const n of t.notes) {
      if (n.note !== REST && pos >= bar * beatsPerBar - 1e-9 && pos < (bar + 1) * beatsPerBar - 1e-9) {
        try { const m = noteNameToMidi(n.note); if (best === null || m < best) best = m; } catch { /* 読めない音名は飛ばす */ }
      }
      pos += n.durationBeats;
    }
  }
  return best === null ? null : ((best % 12) + 12) % 12;
}

/** できあがった曲の、ループの継ぎ目の検査。score.loop が false の曲は何も返さない。 */
export function checkScoreSeam(score: Score): string[] {
  if (!score.loop) return [];
  const w: string[] = [];
  const beatsPerBar = score.timeSig?.num && score.timeSig.den ? (score.timeSig.num * 4) / score.timeSig.den : 4;
  const total = Math.max(0, ...score.tracks.map((t) => beatsOf(t.notes)));
  const bars = Math.round(total / beatsPerBar);
  if (bars < 2) return w;
  const fromBar = (score.meta?.loop?.startBar ?? 1) - 1;

  // ① 最後の和音（低音の根音）と頭の関係
  const first = lowestPcInBar(score, beatsPerBar, fromBar, true) ?? lowestPcInBar(score, beatsPerBar, fromBar, false);
  const last = lowestPcInBar(score, beatsPerBar, bars - 1, true) ?? lowestPcInBar(score, beatsPerBar, bars - 1, false);
  if (first !== null && last !== null && seamRelation(last, first) === null) {
    w.push(`最後の小節の低音（${["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"][last]}）が、頭の低音（${["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"][first]}）につながりにくい関係です。最後を頭と同じ・V・IV にするとなめらかです`);
  }

  // ② 末尾2小節に音量の山がないか
  const lv = barLevels(score, beatsPerBar, bars);
  const sorted = [...lv].sort((a, b) => a - b);
  const median = sorted[Math.floor(sorted.length / 2)] || 1e-9;
  const tail = Math.max(lv[bars - 1], lv[bars - 2]);
  if (bars >= 8 && tail > median * 1.6) w.push(`最後の1〜2小節の音の量が、曲の中央値の ${(tail / median).toFixed(1)} 倍あります。ループ末尾の山は「また来る」と先読みされて飽きます。山は周回の中ほどに置いてください`);

  // ③ 静かな曲の頭に大きな一撃
  const drumCount = score.tracks.filter((t) => t.instrument && DRUMS.has(t.instrument)).reduce((s, t) => s + t.notes.filter((n) => n.note !== REST).length, 0);
  const quiet = drumCount / bars < 4;
  const head = lv[fromBar] ?? lv[0];
  if (quiet && !score.opening && bars >= 8 && head > median * 1.8) w.push(`静かな曲なのに、頭の小節の音の量が中央値の ${(head / median).toFixed(1)} 倍あります。ループのたびに一撃が来て不自然になります。頭は他の小節と同じ強さに`);

  // ④ 末尾の長い音（1小節以上）が、頭の音と半音・増4度でぶつかる（長音は継ぎ目をまたいで鳴り続けるので、ぶつかると濁る）
  for (const t of score.tracks) {
    if (t.instrument && DRUMS.has(t.instrument)) continue;
    const lastN = t.notes[t.notes.length - 1];
    const firstN = t.notes.find((n) => n.note !== REST);
    if (!lastN || !firstN || lastN.note === REST || lastN.durationBeats * (lastN.gate ?? 1) < beatsPerBar - 1e-9) continue;
    if (t.notes[0].note === REST) continue;
    try {
      const d = Math.abs(noteNameToMidi(lastN.note) - noteNameToMidi(firstN.note)) % 12;
      if (d === 1 || d === 6 || d === 11) w.push(`パート ${t.instrument ?? t.waveform}: 末尾の長い音（${lastN.note}・${lastN.durationBeats}拍）が、頭の音（${firstN.note}）と${d === 6 ? "増4度" : "半音"}でぶつかります。長音は継ぎ目をまたいで鳴るので、最後を頭と同じ音か近い和音の音にするか、短くしてください`);
    } catch { /* 読めない音名は飛ばす */ }
  }
  return w;
}

/** expandBars を使って曲の1小節ごとのコード名を返す（chords と barsPerChord と repeats から）。読めなければ空。 */
export function barChordsOf(chords: string, barsPerChord: number, repeats: number): string[] {
  try {
    const one = expandBars(chords, barsPerChord === 2 ? 2 : 1);
    const out: string[] = [];
    for (let r = 0; r < Math.max(1, Math.round(repeats || 1)); r++) out.push(...one);
    return out;
  } catch { return []; }
}
