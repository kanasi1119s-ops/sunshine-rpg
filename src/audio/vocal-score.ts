import { noteNameToMidi } from "./note";

/**
 * 歌声合成（VOICEVOX の歌唱）用の楽譜づくり。
 *  - 歌詞（ひらがな・カタカナ）を、1音ずつ（モーラ）に分ける
 *  - 作曲ソフトが作った歌のメロディ（音名:拍 の並び）に、歌詞をのせる
 *  - VOICEVOX の楽譜（notes: key / frame_length / lyric）の形にする
 * 外部サービスは使わない（ここはただの計算）。実際に声にするのは tools/music（PC側の vocal_tool.py）。
 */

/** VOICEVOX の歌唱が受け付ける1音（エンジンの mora_mapping と同じ一覧）。 */
export const VALID_MORAS: ReadonlySet<string> = new Set(
  "ァ ア ィ イ イェ ゥ ウ ウィ ウゥ ウェ ウォ ェ エ ォ オ カ ガ キ キィ キェ キャ キュ キョ ギ ギィ ギェ ギャ ギュ ギョ ク クァ クィ クゥ クェ クォ クヮ グ グァ グィ グゥ グェ グォ グヮ ケ ゲ コ ゴ サ ザ シ シェ シャ シュ ショ ジ ジェ ジャ ジュ ジョ ス スィ ズ ズィ セ ゼ ソ ゾ タ ダ チ チェ チャ チュ チョ ヂ ヂェ ヂャ ヂュ ヂョ ッ ツ ツァ ツィ ツェ ツォ ヅ テ ティ テェ テャ テュ テョ デ ディ デェ デャ デュ デョ ト トゥ ド ドゥ ナ ニ ニィ ニェ ニャ ニュ ニョ ヌ ネ ノ ハ バ パ ヒ ヒィ ヒェ ヒャ ヒュ ヒョ ビ ビィ ビェ ビャ ビュ ビョ ピ ピィ ピェ ピャ ピュ ピョ フ ファ フィ フェ フォ ブ プ ヘ ベ ペ ホ ボ ポ マ ミ ミィ ミェ ミャ ミュ ミョ ム メ モ ャ ヤ ュ ユ ョ ヨ ラ リ リィ リェ リャ リュ リョ ル レ ロ ヮ ワ ヰ ヱ ヲ ン ヴ ヴァ ヴィ ヴェ ヴォ ヴャ ヴュ ヴョ ヶ".split(" "),
);

/** 歌のフレームレート（VOICEVOX は 93.75 フレーム/秒）。 */
export const FRAMERATE = 93.75;
/** 1つの音の最短（フレーム）。これより短くなる分割はしない（約0.12秒）。 */
export const MIN_NOTE_FRAMES = 11;
/** 「っ」を、直前の音の末尾に置くときの長さ（フレーム）。 */
const TSU_FRAMES = 9;
/** 歌詞の行の終わりに入れる息つぎ（フレーム。最後の音を、これだけ短くして休符にする）。 */
const BREATH_FRAMES = 12;

// ── 歌詞を1音ずつに分ける ──

export interface Mora {
  /** カタカナ1音（"カ"・"キャ"・"ン"・"ッ" など）。 */
  kana: string;
  /** 「っ」。前の音の末尾に短くつける。 */
  tail?: boolean;
}

const SMALL_VOWEL: Record<string, string> = { ァ: "ア", ィ: "イ", ゥ: "ウ", ェ: "エ", ォ: "オ", ャ: "ア", ュ: "ウ", ョ: "オ", ヮ: "ア" };
const ROWS: [string, string][] = [
  ["ア", "アカガサザタダナハバパマヤラワァャヮ"],
  ["イ", "イキギシジチヂニヒビピミリィ"],
  ["ウ", "ウクグスズツヅヌフブプムユルゥュヴ"],
  ["エ", "エケゲセゼテデネヘベペメレェ"],
  ["オ", "オコゴソゾトドノホボポモヨロヲォョ"],
];
const VOWEL_KANA: Record<string, string> = {};
for (const [v, chars] of ROWS) for (const c of chars) VOWEL_KANA[c] = v;

/** 音の母音（"キャ"→"ア"）。のばす音（メリスマ）に使う。母音がない音（ン）は null。 */
export function vowelOf(kana: string): string | null {
  const last = kana[kana.length - 1];
  if (last === "ン" || last === "ッ") return null;
  return SMALL_VOWEL[last] ?? VOWEL_KANA[last] ?? null;
}

const toKatakana = (s: string): string => s.replace(/[ぁ-ゖ]/g, (c) => String.fromCharCode(c.charCodeAt(0) + 0x60));
const IGNORED = /[\s、。，．,.!?！？「」『』（）()…・~〜\-"'“”‘’♪]/;

export interface MoraResult {
  moras: Mora[];
  /** 読めなかった文字（漢字・英数字など）。ひらがな・カタカナに直してもらう。 */
  invalid: string[];
}

/** ひらがな・カタカナの歌詞を、1音ずつに分ける。「ー」は直前の音の母音にする。 */
export function splitMoras(text: string): MoraResult {
  const s = toKatakana(text.normalize("NFKC"));
  const moras: Mora[] = [];
  const invalid: string[] = [];
  for (const ch of s) {
    if (IGNORED.test(ch)) continue;
    const prev = moras[moras.length - 1];
    if (ch === "ー") {
      const v = prev && !prev.tail ? vowelOf(prev.kana) : null;
      if (v) moras.push({ kana: v });
      continue;
    }
    if (ch === "ッ") {
      if (prev && !prev.tail) moras.push({ kana: "ッ", tail: true });
      continue;
    }
    if (ch in SMALL_VOWEL) {
      const combined = prev && !prev.tail ? prev.kana + ch : "";
      if (combined && VALID_MORAS.has(combined)) {
        prev.kana = combined;
      } else if (VALID_MORAS.has(ch)) {
        moras.push({ kana: SMALL_VOWEL[ch] });
      }
      continue;
    }
    if (VALID_MORAS.has(ch)) moras.push({ kana: ch });
    else invalid.push(ch);
  }
  return { moras, invalid };
}

// ── 歌詞の区切り（[verse] [chorus] …） ──

export type VocalKind = "verse" | "bridge" | "chorus";

export interface Stanza {
  kind: VocalKind | "skip" | null;
  /** [verse 2] のように番号があるとき。 */
  nth?: number;
  lines: string[];
}

const HEADER = /^\s*[\[［(（]\s*([^\]］)）]+?)\s*[\]］)）]\s*$/;
function headerKind(label: string): { kind: VocalKind | "skip"; nth?: number } | null {
  const t = label.normalize("NFKC").toLowerCase();
  const n = /(\d+)/.exec(t);
  const nth = n ? Number(n[1]) : undefined;
  if (/intro|outro|solo|instrumental|interlude|inst\b|イントロ|アウトロ|間奏|ソロ|終奏|前奏/.test(t)) return { kind: "skip" };
  if (/verse|^v\b|^a\b|^a\s*メロ|aメロ|^verse|^1番|ヴァース/.test(t) && !/chorus/.test(t)) return { kind: "verse", nth };
  if (/bridge|pre|^b\b|bメロ|^b\s*メロ|ブリッジ|プレ/.test(t)) return { kind: "bridge", nth };
  if (/chorus|hook|^c\b|サビ|コーラス/.test(t)) return { kind: "chorus", nth };
  return null;
}

/** 歌詞のテキストを、まとまり（stanza）に分ける。見出し行（[chorus] など）か、空行で区切る。 */
export function parseLyrics(text: string): Stanza[] {
  const stanzas: Stanza[] = [];
  let cur: Stanza | null = null;
  const flush = (): void => {
    if (cur && cur.lines.length) stanzas.push(cur);
    cur = null;
  };
  for (const raw of text.replace(/\r/g, "").split("\n")) {
    const h = HEADER.exec(raw);
    if (h) {
      const k = headerKind(h[1]);
      if (k) {
        flush();
        cur = { kind: k.kind, nth: k.nth, lines: [] };
        continue;
      }
    }
    if (!raw.trim()) {
      flush();
      continue;
    }
    if (!cur) cur = { kind: null, lines: [] };
    cur.lines.push(raw.trim());
  }
  flush();
  // 歌わない区間の見出し（[Intro] など）のまとまりは捨てる
  for (let i = stanzas.length - 1; i >= 0; i--) if (stanzas[i].kind === "skip") stanzas.splice(i, 1);
  // 見出しのないまとまりは、Aメロ→Bメロ→サビ の順にくり返して割りあてる
  const order: VocalKind[] = ["verse", "bridge", "chorus"];
  let u = 0;
  for (const st of stanzas) if (!st.kind) st.kind = order[u++ % 3];
  return stanzas;
}

// ── メロディ（"C4:1 R:0.5 …"）を音にする ──

export interface MelodyNote {
  /** 小節の頭からの拍。 */
  startBeat: number;
  durBeats: number;
  /** MIDIノート番号。休符は null。 */
  midi: number | null;
}

export function parseMelody(melody: string): MelodyNote[] {
  const out: MelodyNote[] = [];
  let pos = 0;
  for (const tok of melody.split(/\s+/).filter(Boolean)) {
    const [name, d] = tok.split(":");
    const dur = Number(d);
    if (!(dur > 0)) throw new Error(`メロディの拍が不正です: ${tok}`);
    out.push({ startBeat: pos, durBeats: dur, midi: name === "R" ? null : noteNameToMidi(name) });
    pos += dur;
  }
  return out;
}

// ── VOICEVOX の楽譜 ──

export interface VvNote {
  key: number | null;
  frame_length: number;
  lyric: string;
}

export interface VocalChunk {
  kind: VocalKind;
  /** 曲の頭からの開始位置（フレーム）。 */
  startFrame: number;
  /** 先頭の休符は含まない。最初と最後は、必ず音。 */
  notes: VvNote[];
  /** 歌詞（確認用）。 */
  text: string;
  moraCount: number;
  noteCount: number;
  warnings: string[];
}

interface Slot {
  key: number | null;
  frames: number;
}

/** 1つのまとまりの音（休符もふくむ）に、音（モーラ）をのせる。 */
function fitLine(slots: Slot[], moras: Mora[], warnings: string[]): VvNote[] {
  const mains = moras.filter((m) => !m.tail);
  if (!mains.length) return slots.map((s) => ({ key: null, frame_length: s.frames, lyric: "" }));
  const work: Slot[] = slots.map((s) => ({ ...s }));
  // 音が足りないとき: いちばん長い音を半分に割る（短くなりすぎる前まで）
  let notes = work.filter((s) => s.key !== null);
  let guard = 0;
  while (notes.length < mains.length && guard++ < 400) {
    let best = -1;
    for (let i = 0; i < work.length; i++) if (work[i].key !== null && work[i].frames >= MIN_NOTE_FRAMES * 2 && (best < 0 || work[i].frames > work[best].frames)) best = i;
    if (best < 0) break;
    const a = Math.ceil(work[best].frames / 2);
    const b = work[best].frames - a;
    work.splice(best, 1, { key: work[best].key, frames: a }, { key: work[best].key, frames: b });
    notes = work.filter((s) => s.key !== null);
  }
  const usable = notes.length;
  const used = Math.min(usable, mains.length);
  if (mains.length > usable) warnings.push(`音が足りず、歌詞の末尾${mains.length - usable}音を歌えません（歌詞を短くするか、テンポを下げてください）`);
  if (used > 0 && usable / used > 2.5) warnings.push(`歌詞に対して音が多すぎます（音${usable}・歌詞${used}）。のばす音が増えて不自然です`);
  // 歌詞の音（主）を、音に等間隔でわりあてる。あいだの音は、母音をのばす（メリスマ）
  const lyricAt = new Map<number, string>();
  for (let k = 0; k < used; k++) lyricAt.set(Math.floor((k * usable) / used), mains[k].kana);
  // 「っ」は、直前の主の音のすぐあとに入れる（その音の末尾を短く切る）
  const tailAfter = new Map<number, boolean>();
  {
    let mainIdx = -1;
    for (const m of moras) {
      if (!m.tail) mainIdx++;
      else if (mainIdx >= 0 && mainIdx < used) tailAfter.set(Math.floor((mainIdx * usable) / used), true);
    }
  }
  const out: VvNote[] = [];
  let ni = 0;
  let lastKana = "ア";
  for (const s of work) {
    if (s.key === null) {
      out.push({ key: null, frame_length: s.frames, lyric: "" });
      continue;
    }
    let kana = lyricAt.get(ni);
    if (kana === undefined) kana = vowelOf(lastKana) ?? "ア";
    else lastKana = kana;
    if (tailAfter.get(ni) && s.frames >= MIN_NOTE_FRAMES + TSU_FRAMES) {
      out.push({ key: s.key, frame_length: s.frames - TSU_FRAMES, lyric: kana });
      out.push({ key: s.key, frame_length: TSU_FRAMES, lyric: "ッ" });
    } else {
      out.push({ key: s.key, frame_length: s.frames, lyric: kana });
    }
    ni++;
  }
  return out;
}

export interface VocalSectionInput {
  kind: string;
  /** 曲の頭から、この区間の頭までの拍。 */
  startBeat: number;
  melody: string;
}

export interface VocalPlan {
  chunks: VocalChunk[];
  warnings: string[];
}

const toFrame = (beat: number, bpm: number): number => Math.round((beat * 60 * FRAMERATE) / bpm);

/**
 * 区間ごとのメロディと歌詞から、歌声用の楽譜（区間ごと）を作る。
 * 歌詞の1行を、区間の中で時間を等分した1つの区切りにあてる（8小節・4行なら、2小節に1行）。
 */
export function buildVocalPlan(sections: VocalSectionInput[], lyricsText: string, bpm: number, transpose = 0): VocalPlan {
  const warnings: string[] = [];
  const stanzas = parseLyrics(lyricsText);
  const used: Record<VocalKind, number> = { verse: 0, bridge: 0, chorus: 0 };
  const chunks: VocalChunk[] = [];
  for (const sec of sections) {
    if (sec.kind !== "verse" && sec.kind !== "bridge" && sec.kind !== "chorus") continue;
    const kind = sec.kind;
    const pool = stanzas.filter((s) => s.kind === kind);
    if (!pool.length) continue; // その種類の歌詞がなければ、楽器だけで進む
    const nth = used[kind]++;
    // 歌詞の数だけ歌う。Aメロ・Bメロの歌詞が足りない回は楽器だけで進む（サビは、最後の歌詞をくり返す）
    const st = pool.find((s) => s.nth === nth + 1) ?? (kind === "chorus" ? pool[Math.min(nth, pool.length - 1)] : pool[nth]);
    if (!st) continue;
    const label = `${kind}${nth + 1}`;
    const melody = parseMelody(sec.melody);
    if (!melody.some((n) => n.midi !== null)) continue;
    const total = melody.reduce((s, n) => s + n.durBeats, 0);
    const lines = st.lines.map((l) => ({ text: l, ...splitMoras(l) }));
    for (const l of lines) if (l.invalid.length) warnings.push(`${label}: 読めない文字「${[...new Set(l.invalid)].join("")}」（ひらがな・カタカナに直してください）: ${l.text}`);
    // 時間で等分した区切りごとに、音をまとめる
    const groups: MelodyNote[][] = lines.map(() => []);
    for (const n of melody) groups[Math.min(lines.length - 1, Math.floor((n.startBeat / total) * lines.length))].push(n);
    // 音のない区切りの歌詞は、となりの区切りにまとめる
    const moraGroups: Mora[][] = lines.map((l) => l.moras);
    for (let g = 0; g < groups.length; g++) {
      if (groups[g].some((n) => n.midi !== null)) continue;
      const dest = groups.findIndex((x, i) => i > g && x.some((n) => n.midi !== null));
      const to = dest >= 0 ? dest : groups.map((x, i) => ({ x, i })).filter((o) => o.i < g && o.x.some((n) => n.midi !== null)).pop()?.i;
      if (to !== undefined) {
        moraGroups[to] = dest >= 0 ? [...moraGroups[g], ...moraGroups[to]] : [...moraGroups[to], ...moraGroups[g]];
        moraGroups[g] = [];
      }
    }
    const secWarn: string[] = [];
    const notes: VvNote[] = [];
    let moraCount = 0;
    let noteCount = 0;
    groups.forEach((notesInGroup, g) => {
      if (!notesInGroup.length) return;
      const slots: Slot[] = notesInGroup.map((n) => {
        const f0 = toFrame(sec.startBeat + n.startBeat, bpm);
        const f1 = toFrame(sec.startBeat + n.startBeat + n.durBeats, bpm);
        return { key: n.midi === null ? null : n.midi + transpose, frames: Math.max(1, f1 - f0) };
      });
      const fitted = moraGroups[g].length ? fitLine(slots, moraGroups[g], secWarn) : slots.map((s) => ({ key: null, frame_length: s.frames, lyric: "" }));
      // 行の終わりで息つぎ（次の行がつづくときだけ。最後の音を少し短くして休符にする）
      if (g < groups.length - 1 && moraGroups[g].length) {
        for (let i = fitted.length - 1; i >= 0; i--) {
          if (fitted[i].key === null) break;
          if (fitted[i].frame_length >= MIN_NOTE_FRAMES + BREATH_FRAMES) {
            fitted[i].frame_length -= BREATH_FRAMES;
            fitted.splice(i + 1, 0, { key: null, frame_length: BREATH_FRAMES, lyric: "" });
          }
          break;
        }
      }
      moraCount += moraGroups[g].length;
      noteCount += fitted.filter((n) => n.key !== null).length;
      notes.push(...fitted);
    });
    // 先頭と末尾の休符は取りのぞく（開始位置で調整する）
    let lead = 0;
    while (notes.length && notes[0].key === null) lead += notes.shift()!.frame_length;
    while (notes.length && notes[notes.length - 1].key === null) notes.pop();
    if (!notes.length) continue;
    // 音の間の休符は、そのまま残す（息つぎ）。ただし歌詞がない音（key=null のまま）だけが連続するのは問題ない
    chunks.push({
      kind,
      startFrame: toFrame(sec.startBeat, bpm) + lead,
      notes,
      text: st.lines.join(" / "),
      moraCount,
      noteCount,
      warnings: secWarn.map((w) => `${label}: ${w}`),
    });
  }
  for (const c of chunks) warnings.push(...c.warnings);
  return { chunks, warnings };
}
