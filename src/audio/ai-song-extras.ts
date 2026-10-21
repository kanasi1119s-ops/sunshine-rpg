import type { DoubleDetuneSpec, EchoSpec, StrumSpec } from "./part-expand";
import { GUITAR_TECH_GUIDE, GUITAR_TECH_PART_SCHEMA, type GuitarTechPartFields } from "./guitar-tech";

/**
 * AiPart／AiSong に足した項目（2026-10-11）。ai-song.ts を大きく変えないよう、型・スキーマ・説明をここにまとめた。
 * 実装: part-expand.ts（展開）・articulation.ts（奏法）・instrument-range.ts（点検）・scale-check.ts（音階の点検）。
 */
export interface AiPartExtras extends GuitarTechPartFields {
  /** ギターのストローク。コードフォームから 3〜6 本のパートに展開される（8 パートの数には入れない）。notes は使わない（""でよい）。 */
  strum?: StrumSpec;
  /** エコー（やまびこ）。遅れて小さくなるコピーを左右交互に足す。 */
  echo?: EchoSpec;
  /** 自動ダブル。同じ旋律を 2 パートにして左右に振り、±数セントずらす。true か { cents, spread }。 */
  doubleDetune?: DoubleDetuneSpec | true;
  /** ダブルトラック（2026-10-20 ラウドロック）。同じリフを「2回別々に弾いた」ように、左右いっぱいに分けた 2 パートにする。
   * doubleDetune と違い、音程はほとんどずらさず（±2セント）、1音ごとのタイミング・強さを左右で別々にばらつかせ、右だけ別のキャビネットIR・少し違う音色にする。
   * true か { spread（0〜1、既定1）, irR（右のIR）, timing（タイミングのずれの倍率、既定1.8） }。 */
  double?: boolean | { spread?: number; irR?: string; timing?: number; diR?: "emily" | "fsbs" | "shiny" | "gretsch" | "hofner" };
  /** このパートのギターの録音（2026-10-21）。emily＝ハムバッカーの太い音／fsbs＝シングルコイルの明るい音／shiny＝アーチトップ／gretsch＝明るいホロウ／hofner＝丸いホロウ。歪ませる前の録音なので、アンプ（amp）で音を作る。曲の diGuitar より優先。 */
  di?: "emily" | "fsbs" | "shiny" | "gretsch" | "hofner";
  /** 和音（strum）を歪みのアンプに通すときの、入力の倍率（既定 0.4＝人間が聞き比べて選んだ値。1 で下げない）。和音を歪ませすぎると割れて聞こえるため。 */
  chordGain?: number;
  /** true で、弦の雑音（音を止める音・指がすべる音）を、本物のギターで出る所にだけ小さく足す（Emilyguitar の録音。同じアンプを通す）。 */
  stringNoise?: boolean;
  /** アンプの前のノイズゲートの深さ（dB。0〜60。刻みの合間を静かにする。24＝自然、40＝ラウド）。 */
  ampGate?: number;
  /** アンプの前の、低音を締めるブースト（0〜1）。歪みの前で低音を削り中域を上げる（実機のチューブスクリーマーの使い方）。 */
  ampTight?: number;
  /** ゲートの検出の周波数（Hz）。低いチューニング（7・8弦）は 500 前後。 */
  ampGateHz?: number;
  /** ブーストが低音を削る周波数（Hz、120〜250）。低いチューニングほど高く。 */
  ampTightHz?: number;
  /** false にすると、歪みギター（distGuitar・crunch）に5度とオクターブを自動で重ねない（8弦の単音の刻み・旋律のリフ。2026-10-20） */
  powerChord?: boolean;
  /** ドローン。曲の主音（tonic）の長い音を自動で作る。"root5" は主音と 5 度の 2 パート。notes は使わない。 */
  drone?: "root" | "root5";
  /** リズムの型の名前（son32・rumba32・tresillo・bembe・soleaCompas・taikoJi・taikoOmote・taiko2）。notes のかわりに展開される。 */
  pattern?: string;
  /** pattern を音程のある楽器に使うときの音（省略は C5）。 */
  patternNote?: string;
  /** true にすると、notes の音を曲の scale（と tonic）の音にそろえる。"down"／"up" で向きを指定。 */
  snap?: boolean | "nearest" | "down" | "up";
  /** 音の並びを後ろへずらす拍数（エコーが使う内部の項目）。 */
  shift?: number;
  /** 音程のずれ（セント。-50〜50）。 */
  detune?: number;
  /** 音の立ち上がりの遅さ（0〜1。録音音源のコントローラ CC73。効くかは音源しだい）。 */
  attack?: number;
  /** 余韻の長さ（0〜1。CC72。効くかは音源しだい）。 */
  release?: number;
  /** ピアノ・エレピのペダル。chord＝コードの変わり目で踏み替え、bar＝1 小節ごと、none＝踏まない。省略は 4 拍ごと。 */
  pedal?: "chord" | "bar" | "none";
  /** true（または秒数）で、息の楽器（lead・brass・choir・shakuhachi・ocarina・panflute）が休まず鳴る長さを区切り、息継ぎの隙間（0.25拍）を自動で作る。 */
  breath?: boolean | number;
  /** false にすると、曲の autoArticulation をこのパートだけ止める。true なら、このパートだけ付ける。 */
  autoArticulation?: boolean;
}

export interface AiSongExtras {
  /** 音階（名前・別名・"miyako@D" のように主音つきでも）。書くと、旋律の音階外の音・小節頭の外れ・特性音を点検して注意を出す。 */
  scale?: string;
  /** 主音（D・Bb・F# など）。scale に @ で書かなければ、ここ（省略は C）。 */
  tonic?: string;
  /** true にすると、すべての手書きパートに、楽器ごとの奏法（ビブラート・レガート・ハンマリング風・スラップの強弱）を自動で付ける。 */
  autoArticulation?: boolean;
  /** true で、音域・同時発音・息継ぎ・和楽器の音階の点検をする（`song.mjs build` は省略時 true。false で止める。ライブラリ単体の既定は点検なし）。 */
  instrumentCheck?: boolean;
}

const rec = { type: "object" } as const;
export const AI_PART_EXTRA_SCHEMA = {
  strum: rec, echo: rec, doubleDetune: { anyOf: [{ type: "boolean" }, rec] }, double: { anyOf: [{ type: "boolean" }, rec] }, di: { type: "string", enum: ["emily", "fsbs", "shiny", "gretsch", "hofner"] }, stringNoise: { type: "boolean" }, chordGain: { type: "number" }, ampGate: { type: "number" }, ampTight: { type: "number" }, ampGateHz: { type: "number" }, ampTightHz: { type: "number" }, powerChord: { type: "boolean" }, drone: { type: "string", enum: ["root", "root5"] },
  pattern: { type: "string" }, patternNote: { type: "string" }, snap: { anyOf: [{ type: "boolean" }, { type: "string", enum: ["nearest", "down", "up"] }] },
  detune: { type: "number" }, attack: { type: "number" }, release: { type: "number" },
  pedal: { type: "string", enum: ["chord", "bar", "none"] }, breath: { anyOf: [{ type: "boolean" }, { type: "number" }] }, autoArticulation: { type: "boolean" },
  ...GUITAR_TECH_PART_SCHEMA,
} as const;
export const AI_SONG_EXTRA_SCHEMA = {
  scale: { type: "string" }, tonic: { type: "string" }, autoArticulation: { type: "boolean" }, instrumentCheck: { type: "boolean" },
} as const;

/** AI_SONG_GUIDE のあとに足す説明（`song.mjs guide` が表示する）。 */
export const AI_SONG_EXTRAS_GUIDE = `
## 楽器・音階・効果の追加機能（2026-10-11）
- 点検: 書いたパートは、楽器の音域（hard の外は出ない音、safe の外は無理）・同時発音（ギター6・ハープ8・ピアノ10・ドラムは手2本）・息継ぎ（息の楽器が10秒以上休まない）・和楽器の音階（koto は平調子、shakuhachi は D F G A C）を、小節番号つきで点検する。\`instrumentCheck:false\` で止める。
- ストローク: \`{"instrument":"guitar","role":"ストローク","volume":0.14,"pan":-0.3,"amp":"clean","notes":"","strum":{"pattern":"D.DU.UDU","spreadMs":12,"strings":5}}\`。chords を書かなければ曲のコード進行（1小節1コード）。型の文字: D ダウン・d 弱いダウン・U/u アップ（高い弦だけ・弱く）・x ミュート・. のばす・- 休み。1 文字＝0.5拍（step で変える）。開放弦のフォームがあるコード（C G Am Em D Dm E A F G7 ほか）はその形、ないコードはバレーの形になる。押さえ方を音名で直接書くなら chords に \"[B1.F#2.B2.E3.G#3.C#4]\"（低い弦から・点でくぎる。全弦開放の響きなど）。
- 奏法の自動付与: 曲に \`autoArticulation:true\`（パートごとに true/false で上書き）。長い音の終わりのビブラート、弦の旋律のレガート、ギターのハンマリング/プルオフ風、スラップの拍頭アクセントなど。ピアノ・ハープは同時に始まる音の最高音を強く。
- 息継ぎ: 息の楽器のパートに \`breath:true\`。休まず6秒を超えたら、1拍以上の音の終わりを0.25拍休符にする。
- ペダル: ピアノ・エレピに \`pedal:"chord"\`（コードの変わり目で踏み替え）／\`"bar"\`／\`"none"\`（スタッカートが短くなる）。省略は4拍ごと。
- 音階: 曲に \`scale:"miyako"\`・\`tonic:"D"\`（または \`"scale":"miyako@D"\`）を書くと、旋律の音階外の音・小節頭の外れ・特性音の有無・増2度の多用に注意が出る。音階名は docs/sound/scales-world-guide.md の2章（42種）。パートに \`snap:true\` で、音を音階にそろえる。ベンドの記号に . を付けると半分（\`^.\`＝1/4音、\`/.\`・\`\\.\` も同じ）。
- ドローン: パートに \`drone:"root"\`（\`"root5"\` は主音＋5度）を書くと、曲の主音（tonic、なければ最初のコードの根音）の長い音を曲の長さぶん自動で作る。
- リズムの型: ドラム／tom／音程のある楽器のパートに \`pattern:"son32"\`（rumba32・tresillo・bembe・soleaCompas・taikoJi・taikoOmote・taiko2）。
- ダブルトラック（ラウドロックの壁）: \`"double":true\`（同じリフを2回弾いたように左右いっぱいに分ける。1音ごとのタイミング・強さは左右で別々。右は別のキャビネットIR \`"double":{"irR":"dfc-mixxx"}\`）。歪みギターは \`"amp":"namA","ampGate":40,"ampTight":0.6,"ampCabIr":"dfc-bestplugins+dfc-axhom"\`、曲に \`"diGuitar":"emily"\`（歪ませる前の録音で鳴らす）。ベースは \`"amp":"bassSplit"\`（低音はきれいなまま、上だけ歪ませる）。
- 厚みと空間: \`doubleDetune:true\`（同じ旋律を2パートにして左右±0.5、±8セント）、\`echo:{"repeats":2,"time":"dotted8","decay":0.3}\`（遅れて小さくなるコピー）、\`detune\`（セント）、\`attack\`・\`release\`（0〜1、録音音源のCC73・CC72）。
- コード: \`C5\`（パワーコード）、\`Bm7-5\`・\`Bm7b5\`、\`Cmmaj7\`・\`CmM7\`・\`CM7\` が読める。
` + GUITAR_TECH_GUIDE;
