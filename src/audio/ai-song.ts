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
  /** 音の伸び（鳴らす長さの倍率 0.2〜3。省略は1。小さいと歯切れよく、大きいと次の音まで余韻が重なる）。ドラムでは使わない。 */
  sustain?: number;
  /** タイミングのずれ（拍。-0.1〜0.1）。+＝あと乗り（スネア・バックビート）、-＝前のめり（ハイハット・刻み）。省略は0。 */
  push?: number;
  /** フレーズの山（拍。2〜32）。この長さごとに、出だしをやや弱く→山で強く→終わりを引く強弱をつける（歌うような表情）。ドラムでは使わない。 */
  phrase?: number;
  /** アンプ（ギター・ベース向け）。"auto" なら曲の音色から自動。 */
  amp: "auto" | "clean" | "overdrive" | "distortion" | "metal" | "prs" | "jazz" | "blues" | "funk" | "crunch" | "hardrock" | "punk" | "fuzz" | "shoegaze" | "lofi" | "retro8bit" | "radio" | "loudmetal" | "loudrock" | "delicate";
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
  feel: "rock" | "pop" | "ballad" | "dance";
  /** ギターの音色の方向。 */
  tone: "rock" | "metal" | "prs";
  /** 裏拍を遅らせる量（0〜1。省略は0）。ジャズ・ブルース・ヒップホップ・ファンクのノリに。 */
  swing?: number;
  /** true なら、lead をシンセリード、pad をシンセパッドの音色にする（省略は false＝lead はフルート、pad は合唱に近い生楽器寄りの音色）。ダンス・電子音楽向け。 */
  synth?: boolean;
  /** true なら、曲の最初の1/8（最大4小節）を小さく始めて上げ、真ん中あたりで一度引いて戻す（曲の起伏。省略は false）。 */
  dynamics?: boolean;
  /** AIが書くパート（メロディ・対旋律・ベースライン・ドラムなど）。 */
  parts: AiPart[];
}

/** AIが使える楽器（キー → 説明）。 */
export const AI_INSTRUMENTS: Record<string, string> = {
  kick: "バスドラム（ドラム）", snare: "スネア（ドラム）", hihat: "ハイハット（ドラム）", crash: "クラッシュシンバル（ドラム）", tom: "タム（ドラム）",
  bass: "エレキベース（E1〜G3）", slap: "スラップベース（E1〜G3）", sub808: "808の重低音（C1〜C3）",
  guitar: "クリーンギター（E2〜E5）", crunch: "クランチギター（E2〜E5）", distGuitar: "ディストーションギター・刻み（E2〜E4）", leadGuitar: "リードギター・ソロ（E3〜E6）", echoGuitar: "エコーギター（E3〜E6）",
  piano: "ピアノ（A0〜C8）", keys: "エレピ（C2〜C6）", harpsichord: "チェンバロ（C2〜C6）", strings: "弦楽（C2〜C7）", pad: "パッド（C2〜C6）", choir: "合唱（C3〜C6）", brass: "ブラス（E2〜C6）", lead: "シンセリード（C3〜C7）", bell: "鐘（C4〜C7）",
  sitar: "シタール（C3〜C6。インド風の撥弦。ドローンと旋律に）", koto: "琴（C3〜C6。和風の撥弦）", shamisen: "三味線（C3〜C6。歯切れのよい和の撥弦）", banjo: "バンジョー（C3〜C6）", harp: "ハープ（C2〜C7。分散和音に）", kalimba: "カリンバ（C4〜C7。やさしい指ピアノ）",
  panflute: "パンフルート（C4〜C7。息の音の入った民族風の笛）", shakuhachi: "尺八（C4〜C6。和風の息の笛）", ocarina: "オカリナ（C4〜C7。素朴な笛）", fiddle: "フィドル（G3〜E6。民謡風の擦弦）", bagpipe: "バグパイプ（A3〜A5。ドローン向きのリード）",
};
const DRUMS = new Set(["kick", "snare", "hihat", "crash", "tom"]);
/** AIソング形式で使えるアンプの名前（`AI_SONG_SCHEMA` の amp と同じ）。 */
const AI_AMPS = new Set(["auto", "clean", "overdrive", "distortion", "metal", "prs", "jazz", "blues", "funk", "crunch", "hardrock", "punk", "fuzz", "shoegaze", "lofi", "retro8bit", "radio", "loudmetal", "loudrock", "delicate"]);

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
    feel: { type: "string", enum: ["rock", "pop", "ballad", "dance"] },
    tone: { type: "string", enum: ["rock", "metal", "prs"] },
    swing: { type: "number" },
    synth: { type: "boolean" },
    dynamics: { type: "boolean" },
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
          sustain: { type: "number" },
          push: { type: "number" },
          phrase: { type: "number" },
          amp: { type: "string", enum: ["auto", "clean", "overdrive", "distortion", "metal", "prs", "jazz", "blues", "funk", "crunch", "hardrock", "punk", "fuzz", "shoegaze", "lofi", "retro8bit", "radio", "loudmetal", "loudrock", "delicate"] },
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
- autoAccompaniment: true なら、コード進行から伴奏（ドラム・ベース・ギター・ピアノ・弦）を自動で足す。自分でドラムやベースを書くときは false にしてよい。feel: 自動の伴奏の雰囲気（rock / pop / ballad / dance＝4つ打ち・メロディのように動くベース・ピアノの分散和音・エコーギターの、きれいで現代的な伴奏）。
- tone: ギターの音色の方向（rock / metal / prs＝なめらかなリード）。
- synth: true にすると、lead（シンセリード）と pad が電子的なシンセの音色になる。省略（false）だと lead はフルート、pad は合唱に近い生楽器寄りの音色で鳴る（tone が metal / prs の lead はオーバードライブのギター）。ダンス・電子音楽のアルペジオやリードには true にする。
- dynamics: true にすると、曲の出だし（最初の1/8、最大4小節）を小さく始めて上げ、中盤で一度引いてから戻す（曲の起伏）。同じ音量で続く曲を避けたいときに使う。
- parts: 自分で書くパート。1曲に1〜8パート。
  - instrument: 楽器（下の一覧）。role: 「メロディ」「ハモリ」「ベースライン」など。
  - sustain: 音の伸び（0.2〜3、省略は1）。0.3〜0.6＝スタッカート（歯切れよく。ピアノ・ギターの刻み・シンセの刻み）、1＝ふつう、1.5〜3＝余韻を残す（ハープ・鐘・パッド・琴・アルペジオ）。長くした音は次の音に重なる。
  - phrase: フレーズの長さ（拍。2〜32。メロディは4か8がおすすめ）。その長さごとに、出だしを少し弱く→山で強く→終わりを引く強弱がつく（機械的に平らな演奏をさけ、歌うような表情になる）。ドラムでは使わない。
  - volume: 0.1〜0.35 くらい（メロディ 0.22〜0.3、伴奏 0.1〜0.2）。pan: -1〜1。amp: ギター・ベースのアンプ（auto / clean / overdrive / distortion / metal / prs、ジャンル別: jazz / blues / funk / crunch / hardrock / punk / fuzz / shoegaze / lofi / retro8bit / radio / loudmetal＝ラウドメタル / loudrock＝ラウドロック / delicate＝繊細な弱い音）。ほかの楽器は auto。
  - notes: 「音名:拍」を空白でくぎる。例 "E5:1 D5:0.5 R:0.5 C5:2"。R は休み。音名は C4（ド）〜B4 のように、シャープは #、フラットは b（例 F#4, Bb3）。拍のあとに奏法の記号を付けられる: ! アクセント（強く）・,（弱く）・\'（スタッカート）・_（レガート。次の音につなげる）。例 "E5:1! D5:0.5\' C5:2_"。拍は 0.25（16分音符）・0.5・0.75・1・1.5・2・3・4 など。
  - ドラムのパートは、音名のかわりに x（打つ）、X（強く）、o（弱く＝ゴーストノート）、R（休み）。1文字＝16分音符のグリッド記法も使える: "g:x...x...x...x..."（x 打つ・X 強く・o 弱く・. 休み）。例 kick "x:1 R:1 x:0.5 x:0.5 R:1"。
  - notes の合計の拍が曲の長さより短いときは、くり返して埋める（ドラムの1〜2小節の型やリフを短く書ける）。メロディは曲全体ぶん書くのがよい（Aメロ・Bメロ・サビのように変化をつける）。

## 楽器
${Object.entries(AI_INSTRUMENTS).map(([k, v]) => `- ${k}: ${v}`).join("\n")}

## よい曲にするコツ
- メロディは、コードの音（根音・3度・5度）を拍の頭に置き、間を音階の音でつなぐ。跳躍のあとは反対向きに戻る。
- 動機（2〜4音の短い形）をくり返し、少しずつ変える。サビは音域を上げ、長い音を使う。
- ベースは根音を中心に、コードの変わり目の前に経過音を入れる。ドラムは、キック・スネア・ハイハットの基本の型に、4小節や8小節ごとのフィル（タムやスネアの連打）とクラッシュを入れる。
- RPGの場面（町・フィールド・ダンジョン・戦闘・ボス・悲しい場面など）に合った速さと調（明るい=長調、暗い=短調）を選ぶ。
- きれいで現代的な音にするには（フリーBGM 1000曲を測って分かったこと）: キック・ベース・メロディは真ん中（pan 0前後）、和音の楽器・弦・パッド・ギターは左右に大きく振る（-0.9〜0.9）。歪んだギターは音量を小さめ（0.05〜0.1）にし、低音と響きの楽器（弦・パッド・合唱）で厚みを出す。
- ラウドメタル・ラウドロックにするには: tone を "metal"（ロックなら "rock"）にし、リズムギターは amp を loudmetal（ロックは loudrock）にして左右に振る（-0.9 と 0.9 の2本を同じ刻みで）。キックは速い連打（0.25拍）、ベースは amp を auto にして根音を刻みギターに合わせる。歪みギターの volume は 0.05〜0.12 まで（大きくすると音割れの元）。壁のような厚みは、ギターを重ねるより弦・合唱・ブラスの低い響きで足す。サビ前はドラムとギターを一度止め（R）、サビで全部を戻す。
- ジャンル別の作り方（詳しくは docs/sound/genre-guides.md）:
  - メタル: 短調（E・D・Aマイナー）、bpm 140〜200。リフは根音の16分刻み（0.25 0.25 0.5 のくり返し、記号 ' で短く ! で拍頭を強く）。進行は i ♭VI ♭III ♭VII（Em C G D）、終わりを V で閉じる。ドラムはツーバス（kick 16分）・スネア2、4拍・4〜8小節ごとのフィル。ベースはギターの根音に合わせ、sub808 の低音で重さを足す。出だしを静かに（キックだけなど）、ブリッジで一度止める。
  - ロック: I・IV・V が中心（C G Am F、Am F C G、I IV V I）。根音（と5度）を8分で刻み、サビで大きく。ベースはルート弾き、ときどき5度・オクターブ。ドラムは8ビート。構成は Aメロ・Bメロ・サビ・ギターソロ・サビ。
  - ジャズ: bpm 120〜200、swing 0.5〜0.7。ii-V-I（Dm7 G7 Cmaj7）と 7th・9th・13th。ベースは1拍1音のウォーキング（根音→経過音→5度→次の根音へ半音で近づく）。ドラムはライド風のハイハット、キックはごく弱く、スネアはゴーストノート。構成はテーマ・アドリブ・テーマ。
  - J-POP: bpm 90〜180。王道進行 IV V iii vi（F G Em Am）、IV I V vi、vi IV V I。V の前に副ドミナント（E7 など）で緊張感。Aメロは低く語り、Bメロでせり上げ、サビで音域を一気に上げる。サビ前にブレイク。16ビートの軽いドラム、指弾きのベース。
  - ベース・ドラムの音源は、書き出しの --bass と --drums に rock / metal / jazz / jpop を選べる（ジャンルに合わせる）。
- 民族音楽にするには: 国・地域の「音階」で notes を書く（例: 琉球風＝C・E・F・G・B、日本の陰旋法＝C・D・Eb・G・Ab、インド風＝C・Db・E・F・G・Ab・B で、ドローンの低い持続音を1パート足す、中東風＝C・Db・E・F・G・Ab・B の増2度、アイルランド風＝Dドリアン、ケルト・北欧風＝ペンタトニック）。和音は少なく、ドローン（根音と5度の長い音）にすると雰囲気が出る。楽器は sitar・koto・shamisen・kalimba・panflute・shakuhachi・ocarina・fiddle・bagpipe・harp・banjo。打楽器は tom と hihat を、小さな音量で不規則なリズムに。**実在する民謡・曲のメロディは使わない**（CLAUDE.md 1-1）。
- ダンスミュージックにするには: bpm 120〜132、feel は dance（自動伴奏で4つ打ちキック・オフビートのハイハット・動くベースが付く）。自分で書くなら、kick は毎拍 "x:1"、hihat は裏拍 "R:0.5 x:0.5"、snare（クラップ）は2・4拍、ベースは sub808 か bass で8分音符の刻み（根音とオクターブ）、リードは lead、アルペジオは keys や bell。8小節ごとに、ドラムを抜く「ブレイク」を作り、直前に snare の16分の連打（0.25拍）でせり上げ、次の小節でキックを全部戻す。音量は kick 0.2・ベース 0.17・リード 0.1 前後。
- ヒップホップにするには: bpm 78〜95（ハーフタイムなら140〜160）、kick は1拍目と「3拍目の手前（2.5拍）」などで間を作り、snare は2・4拍、hihat は8分か16分で、ところどころ 0.25 拍の連打（トラップ風）。ベースは sub808 の長い音（C1〜C2）を、キックに合わせて置く。メロディは keys・piano・bell・pad の短い反復（2小節のループ）で、コードは 7th を使うと雰囲気が出る。サンプリングは使わず、音は自分で書く。
- ジャンルは自由に選んでよい（レトロな音に限らない）: ジャズ（swing・7thコード・ウォーキングベース・amp: jazz）、オーケストラ（strings・brass・harp・choir・tom、amp は auto）、アンビエント（pad・choir・bell・wind を長い音で。ドラムなし）、フォーク・カントリー（guitar・banjo・fiddle）、ボサノバ（guitar・ゆるいハイハット）、R&B・ソウル（keys・slap・amp: funk）、EDM・ハウス・トランス（上のダンス）、ロック・パンク・メタル（amp: hardrock / punk / loudmetal / loudrock）。曲の場面と合うジャンルを先に決めてから、テンポ・音階・楽器・アンプをそろえる。
- 旋律の育て方: 4小節のまとまりで、1小節目の形（リズムと音の上下）を、2小節目で音階の2〜3度ずらして繰り返す（反復進行）と、旋律が育つ。3〜4小節目で変化をつけ、4小節目の終わりは安定した音（主音やコードの根音・3度）に落ち着かせる。大きく（5度以上）跳んだら、次は逆向きに順次進行で戻る。サビは Aメロより音域を高く、音数と強弱を増やす。
- 対旋律とハモリ: メロディが長い音のときに、別のパートが動く（逆に、メロディが動いているときは伴奏は動きを抑える）。ハモリはメロディの3度か6度下に付け、メロディと同じ音域・同じ楽器に重ねすぎない。メロディとベースは、離れる向き（反行）に動かすとすっきりする。
- 伴奏の和音（弦・パッド・ピアノ）は、コードが変わるたびに全部の音が跳ばないように、共通の音は動かさず、ほかの音は近い高さへ動かす（ボイスリーディング）。
- グルーブ（ノリ）: 音符を機械的に並べるだけだとノリが出ない。曲の swing（0〜1）で裏拍を遅らせ（ジャズ・ブルース・ファンク 0.5〜0.7、ヒップホップ・ローファイ 0.2〜0.4、ロック・ダンス 0）、パートの push（-0.1〜0.1拍）でタイミングをずらす（スネア +0.02〜0.04＝あと乗りで重く、ハイハット -0.01〜-0.02＝前のめりで軽く、ベースはキックに合わせて 0）。ドラムは強弱が命: グリッド記法（g:x...）で X＝強、x＝ふつう、o＝弱い（ゴーストノート）を書き分け、ハイハットは表拍を強く裏拍を弱く、スネアの間に o を入れる。ビートの型は docs/sound/drum-patterns.md。
- 繊細な音にするには: amp は delicate か clean、volume は 0.04〜0.12、ピアノ・ハープ・鐘・オルゴール系で細かい音符（0.25〜0.5拍）を、拍の強弱をつけず低めの音域でゆっくり。ドラムは入れないか、ハイハットだけ小さく。パッドと合唱を薄く敷く。
- 音割れを避ける: 全パートの volume を足した値が大きすぎないようにする（歪みギター2本＋ドラム＋ベースで合計 0.7 前後まで）。出口に安全装置（リミッターと最後のソフトクリップ）はあるが、頼りすぎず、書き出した WAV のピークが -1dBFS 以下であることを確かめる。
- 曲は小さく始め（前奏は楽器を減らす）、途中で一度ドラムを抜いて静かにしてから、最後のサビで全部を戻す。ベースは根音だけでなく、5度・オクターブ・10度を行き来し、小節の最後で次のコードへ向かう音を入れると、メロディのように動く。`;

const DUR_RULE = /^\d+(\.\d+)?$/;

/** 「音名:拍」の並びを、音の列にする。まちがいは errors に足す。 */
export function parseNotes(text: string, drum: boolean, errors: string[], where: string): NoteEvent[] {
  const out: NoteEvent[] = [];
  for (const token of text.trim().split(/\s+/).filter(Boolean)) {
    // ドラムのグリッド記法: g:x...x...  1文字が16分音符（0.25拍）。x＝打つ、X＝強く、o＝弱く（ゴーストノート）、. か - ＝休み
    if (drum && /^g:/i.test(token)) {
      const cells = token.slice(2);
      if (!/^[xXo.\-]+$/.test(cells)) {
        errors.push(`${where}: グリッドは x X o . - だけで書きます「${token}」`);
        continue;
      }
      for (const c of cells) {
        out.push(c === "." || c === "-" ? { note: REST, durationBeats: 0.25 } : { note: "C2", durationBeats: 0.25, ...(c === "X" ? { velocity: 1.3 } : c === "o" ? { velocity: 0.5 } : {}) });
      }
      continue;
    }
    const [name, rawDur = ""] = token.split(":");
    // 長さのあとに付けられる奏法の記号: ! アクセント（強く）, 「,」 弱く, ' スタッカート（短く）, _ レガート（次の音につなげる）
    const m = /^(\d+(?:\.\d+)?)([!,'_]*)$/.exec(rawDur);
    const dur = m ? m[1] : rawDur;
    const marks = m ? m[2] : "";
    const art: Partial<NoteEvent> = {
      ...(marks.includes("!") ? { velocity: 1.3 } : marks.includes(",") ? { velocity: 0.7 } : {}),
      ...(marks.includes("'") ? { gate: 0.4 } : marks.includes("_") ? { gate: 1.15 } : {}),
    };
    const beats = Number(dur);
    if (!dur || !DUR_RULE.test(dur) || !(beats > 0) || beats > 64) {
      errors.push(`${where}: 拍が読めません「${token}」`);
      continue;
    }
    if (name === "R" || name === "r") {
      out.push({ note: REST, durationBeats: beats });
    } else if (drum) {
      if (name !== "x" && name !== "X" && name !== "o") {
        errors.push(`${where}: ドラムは x か R で書きます「${token}」`);
        continue;
      }
      out.push({ note: "C2", durationBeats: beats, ...(name === "X" ? { velocity: 1.3 } : name === "o" ? { velocity: 0.5 } : {}), ...(art.velocity ? { velocity: art.velocity } : {}) });
    } else {
      try {
        const midi = noteNameToMidi(name);
        if (midi < 12 || midi > 108) throw new Error("range");
        out.push({ note: name, durationBeats: beats, ...art });
      } catch {
        errors.push(`${where}: 音名が読めません「${token}」（例 C4, F#3, Bb5）`);
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

/** 音の伸び（gate）を、休符以外の音に付ける。1・未指定なら何もしない。 */
export function applySustain(events: NoteEvent[], sustain: number): NoteEvent[] {
  if (!Number.isFinite(sustain) || sustain === 1) return events;
  const gate = Math.max(0.2, Math.min(3, sustain));
  return events.map((e) => (e.note === REST || e.gate !== undefined ? e : { ...e, gate }));
}

/** AIソングを確かめて、曲（Score）に組み立てる。おかしなところがあれば、全部まとめてエラーにする。 */
/** フレーズごとの強弱（出だし 0.88 → 山 1.1 → 終わり 0.8）を、休符以外の音の強さに掛ける。 */
export function applyPhrase(events: NoteEvent[], phraseBeats: number): NoteEvent[] {
  if (!Number.isFinite(phraseBeats) || phraseBeats < 2) return events;
  const len = Math.min(32, phraseBeats);
  let pos = 0;
  return events.map((e) => {
    const x = (pos % len) / len;
    pos += e.durationBeats;
    if (e.note === REST) return e;
    const g = x < 0.7 ? 0.88 + 0.22 * (x / 0.7) : 1.1 - 0.3 * ((x - 0.7) / 0.3);
    return { ...e, velocity: Math.round((e.velocity ?? 1) * g * 1000) / 1000 };
  });
}

/** 曲の起伏: 出だしを小さく始め、中盤で一度引いてから戻す。 */
export function applyArc(tracks: Track[], total: number, beats: number): Track[] {
  const intro = Math.min(beats * 4, total / 8);
  const duckFrom = total * 0.5;
  const duckTo = total * 0.625;
  const gain = (pos: number): number => {
    if (pos < intro) return 0.55 + 0.45 * (pos / intro);
    if (pos >= duckFrom && pos < duckTo) return 0.75;
    return 1;
  };
  return tracks.map((t) => {
    let pos = 0;
    return { ...t, notes: t.notes.map((n) => { const out = { ...n, velocity: (n.velocity ?? 1) * gain(pos) }; pos += n.durationBeats; return out; }) };
  });
}

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

  const feel = ["rock", "pop", "ballad", "dance"].includes(song.feel) ? song.feel : "pop";
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
      ...(Number(p.push) ? { push: Math.max(-0.1, Math.min(0.1, Number(p.push))) } : {}),
      notes: applySustain(drum ? fitToLength(events, total) : applyPhrase(fitToLength(events, total), Number(p.phrase)), drum ? 1 : Number(p.sustain)),
    });
  });
  if (errors.length) throw new Error(errors.join("\n"));
  if (parts.length === 0 && accompaniment.length === 0) throw new Error("パートがありません");
  const all = [...accompaniment, ...parts];
  const tracks = song.dynamics === true ? applyArc(all, total, Number(song.beats)) : all;
  const score: Score = {
    tempoBpm: bpm, loop: true, drumKit: base.drumKit, tone: ["rock", "metal", "prs"].includes(song.tone) ? song.tone : "rock",
    ...(Number(song.swing) > 0 ? { swing: Math.min(1, Number(song.swing)) } : {}),
    // synth: lead／pad をシンセ音色にする。style "electro" は、実楽器版（real-edition.ts）が電子音楽の音色を生楽器に置き換えないための印
    ...(song.synth === true ? { synth: true, style: "electro" } : {}),
    tracks,
  };
  return { score, song, warnings };
}
