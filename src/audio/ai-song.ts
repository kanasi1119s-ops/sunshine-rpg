import { noteNameToMidi } from "./note";
import { buildNewSong } from "./newsong";
import { REST, type AmpSetting, type Instrument, type NoteEvent, type Score, type Track } from "./score";

/**
 * AIが書く「曲の設計図」（AIソング形式）と、それを曲（Score）に組み立てる道具。
 * 作曲ソフトの「AIに作曲してもらう」（APIキーで Claude を呼ぶ）と、Claude Code から使う
 * `node tools/composer/song.mjs`（`.claude/skills/compose-song/`）の両方が、この形式を使う。
 */
export interface AiPart {
  /** 楽器（AI_INSTRUMENTS のキー）。 */
  instrument: Instrument;
  /** パートの名前（メロディ・ハモリ・ベースなど。表示用）。 */
  role: string;
  /** 音量 0〜0.4 くらい。 */
  volume: number;
  /** 左右の位置 -1（左）〜1（右）。 */
  pan: number;
  /** アンプ（ギター・ベース向け）。"auto" なら曲の音色から自動。 */
  amp: "auto" | "clean" | "overdrive" | "distortion" | "metal" | "prs" | "jazz" | "blues" | "funk" | "crunch" | "hardrock" | "punk" | "fuzz" | "shoegaze" | "lofi" | "retro8bit" | "radio";
  /**
   * 音の並び。「音名:拍」を空白でくぎる（例 "E5:1 D5:0.5 R:0.5 C5:2"）。R は休み。
   * ドラム（kick/snare/hihat/crash/tom）は音名のかわりに x（打つ）か R（休み）。
   * 曲の長さより短いときは、くり返して埋める（ドラムの型やリフを短く書ける）。長いときは切る。
   */
  notes: string;
}

export interface AiSong {
  title: string;
  /** どんな曲か（1〜2文。日本語）。 */
  description: string;
  bpm: number;
  /** 1小節の拍の数。 */
  beats: 3 | 4 | 6 | 7;
  /** コード進行（例 "Am F C G"）。伴奏とくり返しの長さの基準になる。 */
  chords: string;
  barsPerChord: 1 | 2;
  /** 進行をくり返す回数（曲の長さ = コードの数 × barsPerChord × repeats 小節）。 */
  repeats: number;
  /** true なら、コード進行から自動の伴奏（ドラム・ベース・ギター・ピアノ・弦）を足す。 */
  autoAccompaniment: boolean;
  /** 自動の伴奏の雰囲気。 */
  feel: "rock" | "pop" | "ballad";
  /** ギターの音色の方向。 */
  tone: "rock" | "metal" | "prs";
  /** サイドチェーン（キックに合わせた音量の凹み）。true＝パッド・弦・合唱、"all"＝リード・キーボード・ブラス・鐘・ピアノ・クリーンギターにも。DJ・EDM向け。 */
  pump?: boolean | "all";
  /** true＝リードとパッドを電子的なシンセの音色にする（DJ・EDM向け）。 */
  synth?: boolean;
  /** ドラムセット（0=標準、16=パワー、24=電子、25=TR-808、32=ジャズ）。DJ・EDMは 24 か 25。 */
  drumKit?: number;
  /** AIが書くパート（メロディ・対旋律・ベースライン・ドラムなど）。 */
  parts: AiPart[];
}

/** AIが使える楽器（キー → 説明）。 */
export const AI_INSTRUMENTS: Record<string, string> = {
  kick: "バスドラム（ドラム）", snare: "スネア（ドラム）", hihat: "ハイハット（ドラム）", crash: "クラッシュシンバル（ドラム）", tom: "タム（ドラム）",
  clap: "ハンドクラップ（ドラム。DJ・クラブ向け）", openhat: "オープンハイハット（ドラム。裏拍に）", scratch: "レコードのスクラッチ（ドラム。プッシュとプルが交互に鳴る）", riser: "ライザー（盛り上げの逆再生シンバル。長い音で書く。音名はC4など）",
  bass: "エレキベース（E1〜G3）", slap: "スラップベース（E1〜G3）", sub808: "808の重低音（C1〜C3）",
  guitar: "クリーンギター（E2〜E5）", crunch: "クランチギター（E2〜E5）", distGuitar: "ディストーションギター・刻み（E2〜E4）", leadGuitar: "リードギター・ソロ（E3〜E6）", echoGuitar: "エコーギター（E3〜E6）",
  piano: "ピアノ（A0〜C8）", keys: "エレピ（C2〜C6）", harpsichord: "チェンバロ（C2〜C6）", strings: "弦楽（C2〜C7）", pad: "パッド（C2〜C6）", choir: "合唱（C3〜C6）", brass: "ブラス（E2〜C6）", lead: "シンセリード（C3〜C7）", bell: "鐘（C4〜C7）",
};
const DRUMS = new Set(["kick", "snare", "hihat", "crash", "tom", "clap", "openhat", "scratch"]);
/** AIソング形式で使えるアンプの名前（`AI_SONG_SCHEMA` の amp と同じ）。 */
const AI_AMPS = new Set(["auto", "clean", "overdrive", "distortion", "metal", "prs", "jazz", "blues", "funk", "crunch", "hardrock", "punk", "fuzz", "shoegaze", "lofi", "retro8bit", "radio"]);

/** 構造化出力（JSONスキーマ）。 */
export const AI_SONG_SCHEMA = {
  type: "object",
  additionalProperties: false,
  required: ["title", "description", "bpm", "beats", "chords", "barsPerChord", "repeats", "autoAccompaniment", "feel", "tone", "parts"],
  properties: {
    title: { type: "string" },
    description: { type: "string" },
    bpm: { type: "integer" },
    beats: { type: "integer", enum: [3, 4, 6, 7] },
    chords: { type: "string" },
    barsPerChord: { type: "integer", enum: [1, 2] },
    repeats: { type: "integer" },
    autoAccompaniment: { type: "boolean" },
    feel: { type: "string", enum: ["rock", "pop", "ballad"] },
    tone: { type: "string", enum: ["rock", "metal", "prs"] },
    pump: { anyOf: [{ type: "boolean" }, { type: "string", enum: ["all"] }] },
    synth: { type: "boolean" },
    drumKit: { type: "integer", enum: [0, 16, 24, 25, 32] },
    parts: {
      type: "array",
      items: {
        type: "object",
        additionalProperties: false,
        required: ["instrument", "role", "volume", "pan", "amp", "ampPreset", "notes"],
        properties: {
          instrument: { type: "string", enum: Object.keys(AI_INSTRUMENTS) },
          role: { type: "string" },
          volume: { type: "number" },
          pan: { type: "number" },
          amp: { type: "string", enum: ["auto", "clean", "overdrive", "distortion", "metal", "prs", "jazz", "blues", "funk", "crunch", "hardrock", "punk", "fuzz", "shoegaze", "lofi", "retro8bit", "radio"] },
          notes: { type: "string" },
        },
      },
    },
  },
} as const;

/** AIへの説明（システムプロンプト）。Claude Code から使うときも、この文を読む（`song.mjs guide`）。 */
export const AI_SONG_GUIDE = `あなたは、ブラウザのRPG用のBGMを作る作曲家です。依頼に合わせて、次の「AIソング形式」のJSONで1曲を書きます。

## 大切な決まり
- 完全なオリジナル曲にする。既存の曲（ゲーム・アニメ・映画・J-POP・クラシックの有名曲など）のメロディやコード進行の特徴的な部分を写さない。「〜風」「〜のような」と頼まれたら、ジャンル・雰囲気・楽器の使い方だけを参考にする。
- 1つのパートは同時に1音だけ鳴る（和音はパートを分けて重ねる）。
- 長さは、特に指定がなければ60〜90秒。曲の長さ = コードの数 × barsPerChord × repeats 小節 × beats 拍 ÷ bpm × 60 秒。

## 形式
- title / description: 曲名と、どんな曲か（日本語）。
- bpm: テンポ（50〜220）。beats: 1小節の拍（3・4・6・7）。
- chords: コード進行（空白でくぎる。C・Am・F#m7・Bbmaj7・Csus4・Gdim・Eaug・D7 など）。
- barsPerChord: 1コードの小節数（1か2）。repeats: 進行のくり返し回数。
- autoAccompaniment: true なら、コード進行から伴奏（ドラム・ベース・ギター・ピアノ・弦）を自動で足す。自分でドラムやベースを書くときは false にしてよい。feel: 自動の伴奏の雰囲気（rock / pop / ballad）。
- tone: ギターの音色の方向（rock / metal / prs＝なめらかなリード）。
- （DJ・クラブ・EDM向けの任意の設定）pump: true でパッド・弦・合唱を、"all" でリード・エレピ・ブラス・鐘・ピアノ・クリーンギターも、キックに合わせて凹ませる（サイドチェーン）。synth: true でリードとパッドを電子的なシンセの音色に。drumKit: 24（電子）か 25（TR-808）。DJらしい音は、clap（2・4拍）・openhat（裏拍）・scratch（つなぎや合いの手）・riser（ドロップ前の8〜16拍の長い音で盛り上げ）・kick の4つ打ち・snare のロールで作る。
- parts: 自分で書くパート。1曲に1〜8パート。
  - instrument: 楽器（下の一覧）。role: 「メロディ」「ハモリ」「ベースライン」など。
  - volume: 0.1〜0.35 くらい（メロディ 0.22〜0.3、伴奏 0.1〜0.2）。pan: -1〜1。amp: ギター・ベースのアンプ（auto / clean / overdrive / distortion / metal / prs、ジャンル別: jazz / blues / funk / crunch / hardrock / punk / fuzz / shoegaze / lofi / retro8bit / radio）。ほかの楽器は auto。
  - notes: 「音名:拍」を空白でくぎる。ギター（leadGuitar など）は、音名のあとに +半音数（0.5〜2）でチョーキング（例 E5+2:1＝音を出してから2半音持ち上げる）、@ でタッピング（例 E5@:0.25＝ハンマリング・プリングのなめらかな音）を書ける。例 "E5:1 D5:0.5 R:0.5 C5:2"。R は休み。音名は C4（ド）〜B4 のように、シャープは #、フラットは b（例 F#4, Bb3）。拍は 0.25（16分音符）・0.5・0.75・1・1.5・2・3・4 など。
  - ドラムのパートは、音名のかわりに x（打つ）か R（休み）。例 kick "x:1 R:1 x:0.5 x:0.5 R:1"。
  - notes の合計の拍が曲の長さより短いときは、くり返して埋める（ドラムの1〜2小節の型やリフを短く書ける）。メロディは曲全体ぶん書くのがよい（Aメロ・Bメロ・サビのように変化をつける）。

## 楽器
${Object.entries(AI_INSTRUMENTS).map(([k, v]) => `- ${k}: ${v}`).join("\n")}

## よい曲にするコツ
- メロディは、コードの音（根音・3度・5度）を拍の頭に置き、間を音階の音でつなぐ。跳躍のあとは反対向きに戻る。
- 動機（2〜4音の短い形）をくり返し、少しずつ変える。サビは音域を上げ、長い音を使う。
- ベースは根音を中心に、コードの変わり目の前に経過音を入れる。ドラムは、キック・スネア・ハイハットの基本の型に、4小節や8小節ごとのフィル（タムやスネアの連打）とクラッシュを入れる。
- RPGの場面（町・フィールド・ダンジョン・戦闘・ボス・悲しい場面など）に合った速さと調（明るい=長調、暗い=短調）を選ぶ。`;

const DUR_RULE = /^\d+(\.\d+)?$/;

/** 「音名:拍」の並びを、音の列にする。まちがいは errors に足す。 */
export function parseNotes(text: string, drum: boolean, errors: string[], where: string): NoteEvent[] {
  const out: NoteEvent[] = [];
  for (const token of text.trim().split(/\s+/).filter(Boolean)) {
    const [name, dur] = token.split(":");
    const beats = Number(dur);
    if (!dur || !DUR_RULE.test(dur) || !(beats > 0) || beats > 64) {
      errors.push(`${where}: 拍が読めません「${token}」`);
      continue;
    }
    if (name === "R" || name === "r") {
      out.push({ note: REST, durationBeats: beats });
    } else if (drum) {
      if (name !== "x" && name !== "X") {
        errors.push(`${where}: ドラムは x か R で書きます「${token}」`);
        continue;
      }
      out.push({ note: "C2", durationBeats: beats, ...(name === "X" ? { velocity: 120 } : {}) });
    } else {
      try {
        // 奏法の書き方: 音名のあとに +半音数（チョーキング。例 E5+2）、@（タッピング。例 E5@）を付けられる
        const m = /^([A-Ga-g][#b]?-?\d)(?:\+(\d+(?:\.\d+)?))?(@)?$/.exec(name);
        if (!m) throw new Error("name");
        const bend = m[2] === undefined ? undefined : Number(m[2]);
        if (bend !== undefined && !(bend > 0 && bend <= 2)) throw new Error("bend");
        const base = m[1];
        const midi = noteNameToMidi(base);
        if (midi < 12 || midi > 108) throw new Error("range");
        out.push({ note: base, durationBeats: beats, ...(bend !== undefined ? { bend } : {}), ...(m[3] ? { tap: true } : {}) });
      } catch {
        errors.push(`${where}: 音名が読めません「${token}」（例 C4, F#3, Bb5。ギターは E5+2＝2半音のチョーキング、E5@＝タッピング）`);
      }
    }
  }
  return out;
}

/** 音の列を、ちょうど total 拍にする（短ければくり返し、長ければ切る）。 */
export function fitToLength(events: NoteEvent[], total: number): NoteEvent[] {
  const len = events.reduce((s, e) => s + e.durationBeats, 0);
  if (len <= 0) return [{ note: REST, durationBeats: total }];
  const out: NoteEvent[] = [];
  let at = 0;
  let i = 0;
  while (at < total - 1e-6) {
    const e = events[i % events.length];
    const dur = Math.min(e.durationBeats, total - at);
    out.push({ ...e, durationBeats: Math.round(dur * 1e6) / 1e6 });
    at += dur;
    i++;
  }
  return out;
}

/** AIソングを確かめて、曲（Score）に組み立てる。おかしなところがあれば、全部まとめてエラーにする。 */
export function aiSongToScore(input: unknown): { score: Score; song: AiSong; warnings: string[] } {
  const song = input as AiSong;
  const errors: string[] = [];
  const warnings: string[] = [];
  if (!song || typeof song !== "object") throw new Error("AIソングのJSONではありません");
  const bpm = Math.round(Number(song.bpm));
  if (!(bpm >= 40 && bpm <= 260)) errors.push(`bpm は 40〜260 にしてください（${song.bpm}）`);
  if (![3, 4, 6, 7].includes(Number(song.beats))) errors.push(`beats は 3・4・6・7 のどれか（${song.beats}）`);
  const repeats = Math.round(Number(song.repeats));
  if (!(repeats >= 1 && repeats <= 32)) errors.push(`repeats は 1〜32（${song.repeats}）`);
  if (!Array.isArray(song.parts)) errors.push("parts がありません");
  if (errors.length) throw new Error(errors.join("\n"));

  const feel = ["rock", "pop", "ballad"].includes(song.feel) ? song.feel : "pop";
  let base: Score;
  try {
    base = buildNewSong({ bpm, beats: Number(song.beats), chords: song.chords, barsPerChord: song.barsPerChord === 2 ? 2 : 1, repeats, feel, leadInstrument: "lead" });
  } catch (e) {
    throw new Error(`chords: ${(e as Error).message}`);
  }
  const total = base.tracks[0].notes.reduce((s, n) => s + n.durationBeats, 0);
  const accompaniment = song.autoAccompaniment ? base.tracks.slice(0, -1) : [];

  const parts: Track[] = [];
  song.parts.forEach((p, i) => {
    const where = `parts[${i}]（${p?.role ?? p?.instrument ?? "?"}）`;
    if (!p || !(p.instrument in AI_INSTRUMENTS)) {
      errors.push(`${where}: 楽器が一覧にありません（${p?.instrument}）`);
      return;
    }
    const drum = DRUMS.has(p.instrument);
    const events = parseNotes(String(p.notes ?? ""), drum, errors, where);
    const length = events.reduce((s, e) => s + e.durationBeats, 0);
    if (length > total + 1e-6) warnings.push(`${where}: 曲の長さ（${total}拍）より長いので、${length}拍のうち後ろを切りました`);
    if (p.amp && !AI_AMPS.has(p.amp)) warnings.push(`${where}: アンプ「${p.amp}」は使えないので、おまかせ（auto）にしました`);
    const amp: AmpSetting | undefined = p.amp && p.amp !== "auto" && AI_AMPS.has(p.amp) ? { type: p.amp } : undefined;
    parts.push({
      waveform: drum ? "square" : "sawtooth",
      instrument: p.instrument,
      volume: Math.max(0.02, Math.min(0.5, Number(p.volume) || 0.2)),
      pan: Math.max(-1, Math.min(1, Number(p.pan) || 0)),
      ...(amp ? { amp } : {}),
      notes: fitToLength(events, total),
    });
  });
  if (errors.length) throw new Error(errors.join("\n"));
  if (parts.length === 0 && accompaniment.length === 0) throw new Error("パートがありません");
  const tracks = [...accompaniment, ...parts];
  const score: Score = { tempoBpm: bpm, loop: true, drumKit: base.drumKit, tone: ["rock", "metal", "prs"].includes(song.tone) ? song.tone : "rock", tracks, ...(song.pump ? { pump: true } : {}), ...(song.pump === "all" ? { pumpAll: true } : {}), ...(song.synth ? { synth: true } : {}), ...([0, 16, 24, 25, 32].includes(Number(song.drumKit)) ? { drumKit: Number(song.drumKit) } : {}) };
  return { score, song, warnings };
}
