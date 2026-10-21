import type { FxSpec } from "./fx-chain";
import type { AmpPresetName } from "./amp";
import type { KeysAmpType } from "./amp-keys";
import type { AmpPluginDef } from "./amp-plugins";
import type { AudioTrack } from "./audio-clips";
import { noteNameToFrequency } from "./note";
import { pushBeatsOf, swingOf } from "./groove-feel";
import { makeTempoClock, type TempoPoint } from "./tempo-map";

/** 音を鳴らさない拍（休符）。 */
export const REST = "R";

/** NoteEvent.velocity を「1が標準」の尺度に直す。自動伴奏のドラムなどが MIDI の数字（40〜127）で入れた値は 100 で割る（dynamics: "natural" と同じ決まり）。 */
export function velocityScale(v: number | undefined): number {
  return v === undefined ? 1 : v > 2 ? v / 100 : v;
}

export interface NoteEvent {
  /** "C4" のような音名、または休符（REST）。 */
  note: string;
  /** 何拍分の長さか（4分音符=1、8分音符=0.5など）。 */
  durationBeats: number;
  /** 強さ（1が標準。ゴーストノートなど弱い音は0.5など）。省略時は1。 */
  velocity?: number;
  /** 音の伸び（鳴らす長さの倍率。1が標準、0.3は短く切る、2は次の音まで余韻を重ねる）。次の音の始まりは変わらない。省略時は1。 */
  gate?: number;
  /** ベンド（チョーキング）: 音が出てから、この半音数だけ音程を持ち上げる（1＝半音、2＝全音）。録音音源で鳴らすときに働く。 */
  bend?: number;
  /** しゃくり（スライドで入る）: この半音数だけ下から入って、本来の音程へすべり上がる（負の値なら上から下がる）。 */
  scoop?: number;
  /** フォール（落とす）: 音の終わりに向けて、この半音数だけ音程を下げていく。 */
  fall?: number;
  /** ビブラート（音の揺れ）の深さ。0.4＝弱（~.）・0.7＝ふつう（~）・1＝深い（~~）。1より大きい値（~~~＝1.5）は、モジュレーションに加えてピッチベンドの揺れ（幅±数セント）も自前で作る。音が出て少したってから揺れ始める。 */
  vibrato?: number;
  /** デッドノート（x。音程のない「チッ」。ミュートした弦を弾く音）。低めの音程・弱い・短い音で鳴らす（guitar-tech.ts）。 */
  dead?: boolean;
  /** ボリューム奏法（< ＝音量が立ち上がる、> ＝音量が減っていく）。1＝クレッシェンド、-1＝デクレッシェンド。MIDIの CC11 で動かす。 */
  swell?: 1 | -1;
  /** スライド（レガート）: 同じ音の長さの中で、この半音数だけ音程をなめらかに動かす（A4:1>D5 → +5）。範囲は±12。 */
  slide?: number;
  /** ベンドの上昇にかける拍数（^^@0.25）。省略は min(音の長さの35%, 0.5拍)。 */
  bendT?: number;
  /** しゃくりで本来の音程に着くまでの拍数（/@0.1）。省略は min(音の長さの40%, 0.3拍)。 */
  scoopT?: number;
  /** フォールやベンドのリリースを始める位置（音の長さに対する割合 0.05〜0.95。\\@0.5）。省略は 0.7。 */
  fallAt?: number;
  /** オープンハイハット（ハイハットだけ。開いて長く鳴らす）。録音音源（MIDI経由）で鳴らすときに働く。 */
  open?: boolean;
}

export type Waveform = "square" | "triangle" | "sawtooth" | "sine";

/**
 * 楽器の音色。指定がなければ、`waveform`の波形をそのまま鳴らす（従来の音）。
 * 打楽器（kick・snare・hihat・crash）は音の高さを使わない（音名は何でもよい）。
 */
export type Instrument =
  | "kick" | "snare" | "hihat" | "crash" | "tom"
  | "bass" | "guitar" | "echoGuitar" | "crunch" | "distGuitar" | "leadGuitar"
  | "keys" | "piano" | "harpsichord" | "strings" | "pad" | "choir" | "brass" | "bell" | "lead"
  // 効果音向け: 音程が滑る（sfxDown＝下がる／sfxUp＝上がる）、ノイズの衝撃音（impact）、風を切る音（swoosh）、金属的な鈴（chime）
  | "sfxDown" | "sfxUp" | "impact" | "swoosh" | "chime"
  // 自然音（風・雨・せせらぎ・鳥・虫）。音の高さは、風の吹く高さ・鳥の声の高さなど音色の目安として使う
  | "pierce" | "slap" | "wind" | "rain" | "stream" | "bird" | "crickets"
  // フォンク向け: 重く歪んだ低音（808）とカウベル
  | "sub808" | "cowbell"
  // 民族楽器（2026-10-02）: 撥弦（sitar・koto・shamisen・banjo・harp・kalimba）、息の楽器（panflute・shakuhachi・ocarina）、擦弦・リード（fiddle・bagpipe）
  | "sitar" | "koto" | "shamisen" | "banjo" | "harp" | "kalimba" | "panflute" | "shakuhachi" | "ocarina" | "fiddle" | "bagpipe"
  // 追加の音源（2026-10-11）: FMのベル／エレピ、ドローバーオルガン、ユニゾンのノコギリ波
  | "fmBell" | "fmEpiano" | "drawbarOrgan" | "unisonSaw"
  // 打楽器の音程つきタム（2026-10-13）: ロートタム・キャノンタム・インチ違いのタム。鍵盤の高さ＝太鼓の基本の高さ（C2〜C6）
  | "rotoTom" | "cannonTom" | "inchTom"
  // カホン（2026-10-19、人間「作曲ソフトの音源にカホンを追加して」）: 録音（VCSL Cajon, CC0）。鍵盤で打ち方を選ぶ（C3 付近＝低音・D3＝トーン・E3〜＝スラップ）
  | "cajon"
  // バスドラのトリガー（打撃音の層）と、映画のインパクト（2026-10-13）
  | "kickTrigger" | "impactHit"
  // 木琴・鉄琴・アコーディオン（2026-10-16、人間の指示「木琴、鉄琴、アコーディオンも音源追加して」）。録音音源は VCSL（CC0）と FreePats の Hohner（CC0）
  | "xylophone" | "glockenspiel" | "accordion";

/**
 * ジャンル別のアンプ（2026-09-30 追加）。ジャズ・ブルース・ファンク・クランチ・ハードロック・パンク・ファズ・
 * シューゲイザー・ローファイ・レトロ8bit・ラジオ。作り方は `amp-rack.ts`、向いている場面は `docs/sound/composition-notes.md`。
 */
export type GenreAmpType = "jazz" | "blues" | "funk" | "crunch" | "hardrock" | "punk" | "fuzz" | "shoegaze" | "lofi" | "retro8bit" | "radio" | "loudmetal" | "loudrock" | "delicate" | "crystal" | "lead" | "modernHigh" | "sparkleClean" | "jpopClean" | "bassSplit" | "bassGrind";

/** ギターなどの音づくり（アンプ）の設定。`auto`は、曲の音色（tone）と楽器から自動で選ぶ。 */
export interface AmpSetting {
  /** direct＝何も通さない（歪ませる前の録音そのもの。音の点検・あとでアンプに通す「リアンプ」用。2026-10-20） */
  type: "auto" | "direct" | "clean" | "overdrive" | "distortion" | "metal" | "prs" | "nam" | GenreAmpType | KeysAmpType | "genre" | "plugin";
  /** type=plugin のとき、使うアンプ定義のID（`Score.ampPlugins` のキー）。 */
  plugin?: string;
  /** type=genre のとき、amp.ts のプリセット名（ジャンル別の種類は、なるべく上の直接の種類へ置きかえて鳴らす）。 */
  preset?: AmpPresetName;
  /** 歪みの深さの倍率（0.5〜2、既定1）。 */
  drive?: number;
  /** 高音の明るさ（dB。-6〜+6、既定0）。 */
  tone?: number;
  /** 出力の大きさの倍率（0.5〜1.5、既定1）。 */
  level?: number;
  /** キャビネット近似の箱（closed=締まる／open=開放的／dark=暗い／bright=明るい）。省略は、ロールの既定（なければ足さない＝これまでの音）。 */
  cab?: "closed" | "open" | "dark" | "bright";
  /** マイクの位置（center=明るく直接的／edge=暗く丸い／off=斜めで温かい／far=遠く柔らかい）。cab がなければ closed を足す。 */
  mic?: "center" | "edge" | "off" | "far";
  /** 録音のキャビネットIRの名前（作曲ソフトに登録されたもの）。"none" で使わない。省略すると、歪み系のアンプは標準のIR（dfc-bestplugins）を通す（作曲ソフトだけ。ゲーム本体には IR が無いので通さない）。 */
  cabIr?: string;
  /** タイト（0〜1）。歪みの前に、低音の締め（ハイパス100〜300Hz）＋中域の山＋ごく軽いソフトクリップを足す。省略は無効。 */
  tight?: number;
  /** ノイズゲートの深さ（dB。0=なし、24=自然、60=ほぼ切る）。省略はロールの既定。 */
  gate?: number;
  /** ゲートの検出の周波数（Hz。省略 1500、学習式アンプでは 600）。低いチューニングは 500 前後。2026-10-20 */
  gateHz?: number;
  /** tight の低音を削る周波数（Hz。省略は 100+200×tight）。低いチューニングで 120〜250。傾きはゆるく。2026-10-20 */
  tightHz?: number;
  /** 前段ローパス（Hz。最初の歪みの前に入れる。省略はロールの既定。0で無効）。 */
  preLowpass?: number;
  /** 歪みの波形曲線（省略は tanh）。 */
  curve?: "tanh" | "softsqrt" | "diode" | "deadzone";
  /** type=nam のとき、使うNAMモデルの名前（`Score.namModels`のキー）。 */
  model?: string;
}

export interface Track {
  /** true なら、歪みギター・クランチに5度とオクターブを自動で重ねない（単音の刻み）。2026-10-20 */
  noPower?: boolean;
  /** 自動ミックスの解析用（auto-mix.ts）: 同じ値のトラックは同じ MIDI チャンネルに、違う値は別のチャンネルに分ける。普通の曲には付けない。 */
  stemKey?: string;
  waveform: Waveform;
  /** 楽器の音色（省略時は`waveform`のまま）。 */
  instrument?: Instrument;
  /** 左右の位置（-1=左、0=中央、1=右）。省略時は中央。 */
  pan?: number;
  /** 音づくり（アンプ）の設定。省略時は自動。 */
  amp?: AmpSetting;
  /** エフェクター（アンプのあとに、書いた順につながる。`fx-chain.ts`）。 */
  fx?: FxSpec[];
  /** パートの音量の上乗せ（dB。-12〜+18）。`volume` は音の強さ（ベロシティ）に変わり 0.22 あたりで頭打ちになるので、それ以上に大きくするときはこちら。エフェクターの最後に素直な増幅（boost）として入る。 */
  gainDb?: number;
  /** 録音音源で鳴らすときの、GMの楽器番号の指定（省略時は`instrument`から決める）。実楽器版で使う。 */
  program?: number;
  /** 効果音用: 録音音源（GMの楽器番号）で鳴らす。準備ができていないときは、`instrument`・`waveform`の合成音で鳴らす。 */
  gm?: number;
  /** 効果音用: trueなら、音名は「GMドラムのキー番号」を表す（例: 36=C2=バスドラム）。 */
  gmDrum?: boolean;
  /** 0〜1。 */
  volume: number;
  /** 残響の送り量（0〜1）。省略時は楽器ごとの標準。録音音源（MIDIのCC91）で効く。 */
  reverb?: number;
  /** コーラス（広がりの揺らぎ）の量（0〜1）。省略時は楽器ごとの標準。録音音源（CC93）で効く。 */
  chorus?: number;
  /** true なら、主旋律のエコー（同じ音を0.75拍後・1.5拍後に小さく鳴らし直す）をしない。音を伸ばしたいリード・ギターに。 */
  noRestrike?: boolean;
  /** 音の明るさ（-1〜0.5）。マイナスで高域を丸く（ローパス）。0が標準。録音音源（CC74）で効く。高域を足す方向は音源の元の明るさまで。 */
  bright?: number;
  /** キックに合わせて音量を凹ませる深さ（0〜1。サイドチェイン風。ベース・ギター・パッドの隙間をキックに空ける）。録音音源で効く。 */
  duck?: number;
  /** タイミングのずれ（拍。-0.1〜0.1）。プラス＝あと乗り（少し遅らせる。スネアやバックビートに）、マイナス＝前のめり（少し早める。ハイハットに）。省略時は0。 */
  push?: number;
  /** タイミングのずれ（ミリ秒。-50〜50）。bpm で拍に直して push に足す（rhythm-groove-guide §10 提案2）。 */
  pushMs?: number;
  /** このパートの human の倍率（0〜2。省略は曲の humanRoles か 1）。0 ならこのパートは機械的に正確なまま。 */
  human?: number;
  /** human のうち、タイミングのずれだけの倍率（省略は1）。 */
  humanTiming?: number;
  /** human のうち、強さのゆらぎだけの倍率（省略は1）。 */
  humanVelocity?: number;
  /** human のうち、音程のごくわずかなずれ（±8セント×human）だけの倍率（省略は1、0でずれなし）。ギターの音が「ゆらいで」聞こえるときに 0 にする。 */
  humanPitch?: number;
  /** このパートの swing（8分の裏）。曲の swing を上書き（0 でまっすぐ）。16分の裏も同じ量（swing16 で別にもできる）。 */
  swing?: number;
  /** このパートの 16分の裏の swing（省略は swing と同じ）。 */
  swing16?: number;
  /** true なら、キックと同じ拍の音（16分以内）は、キックと同じだけずれる（human を上げても、キックとそろったまま）。ベース・ギター向け。 */
  lockToKick?: boolean;
  /** 音程のずれ（セント。-50〜50）。同じ旋律を2パートにして±数セントずらすと、スーパーソー風の厚みが出る。録音音源（MIDIのRPN 1）で効く。 */
  detune?: number;
  /** 音の立ち上がりの遅さ（0〜1。0.5が標準＝音源のまま）。大きいほどゆっくり立ち上がる。録音音源（MIDIのCC73）で効くかは音源しだい。 */
  attack?: number;
  /** 余韻の長さ（0〜1。0.5が標準）。大きいほど長く残る。録音音源（MIDIのCC72）で効くかは音源しだい。 */
  release?: number;
  /** false にすると、このパートだけギターの自動しゃくりを止める。true なら、曲が autoScoop:false でもこのパートだけ付ける。省略は曲の設定に従う。 */
  autoScoop?: boolean;
  /** ビブラートを自前で作る（ピッチベンドの正弦波）。rate＝速さ(Hz。3〜8、既定5.5)、depth＝幅(セント。8〜60、既定30)、delay＝揺れ始めるまでの拍(既定0.4)。~ を付けた音（0.4拍以上）に効く。 */
  vibratoSpec?: { rate?: number; depth?: number; delay?: number };
  /** グライド（アームの揺れ）: 1 拍以上の音の間じゅう、ゆっくり不規則に音程が揺れる（シューゲイザーのグライドギター）。depth＝幅(セント。20〜150、既定100)、rate＝速さ(Hz。0.05〜1、既定0.2)。 */
  glide?: { depth?: number; rate?: number };
  /** ピアノ・エレピのペダル。mode＝chord（コードの変わり目で踏み替え）・bar（1小節ごと）・none（踏まない）。changes＝踏み替える拍。省略は4拍ごと。 */
  pedal?: { mode: "chord" | "bar" | "none"; changes: number[] };
  notes: NoteEvent[];
}

/**
 * グルーブ（ノリ）による、音の始まりのずれ（拍）。`swing`＝裏拍を遅らせる量（0〜1。0.5くらいで三連寄りのはね）、`push`＝パートごとのずれ。
 * 8分の裏拍（0.5拍目）は swing/6 拍、16分の裏（0.25・0.75拍目）は swing/12 拍遅れる。
 */
export function grooveOffsetBeats(swing: number | undefined, push: number | undefined, startBeat: number, swing16?: number): number {
  let off = push ?? 0;
  if (swing || swing16) {
    const frac = Math.round((startBeat - Math.floor(startBeat)) * 1000) / 1000;
    if (frac === 0.5) off += (swing ?? 0) / 6;
    else if (frac === 0.25 || frac === 0.75) off += (swing16 ?? swing ?? 0) / 12;
  }
  return off;
}

/** ボス戦の段階（HPの割合で曲の位置を切り替える。docs/sound/game-music-guide.md、bgm-director.ts）。小節は1から数える。 */
export interface BossPhase {
  id: string;
  /** この段階のループの始まりの小節（1から）。 */
  startBar: number;
  /** この段階のループの終わりの小節（1から数えて、この小節の終わりまで）。 */
  endBar: number;
  /** HPがこの割合（0〜1）を下回ったらこの段階に入る。最初の段階は1。 */
  hpBelow: number;
}

/** 曲の付随情報（ゲームの再生側が使う。音そのものは変えない）。song-meta.ts が作る。 */
export interface SongMeta {
  form?: string;
  bars?: number;
  beatsPerBar?: number;
  /** ループ点。導入を1回だけ鳴らし、そのあと startBar〜endBar をくり返す。 */
  loop?: { startBar: number; endBar: number; startSec: number; endSec: number };
  introType?: string;
  outroType?: string;
  bossPhases?: BossPhase[];
  motifs?: string[];
  laps?: number;
}

export interface Score {
  /** 曲の付随情報（ループ点・導入／終わりの型・ボスの段階・主題ID）。 */
  meta?: SongMeta;
  /** 裏拍を遅らせる量（0〜1）。省略時は0（ずらさない）。 */
  swing?: number;
  /** 16分の裏（0.25・0.75拍目）の swing（省略は swing と同じ動き）。8分の裏だけ揺らして16分をまっすぐにする、などに。 */
  swing16?: number;
  /** パート別の human の倍率（役割 kick・snare・hihat・cymbal・bass・sub・rhythm・lead → 0〜2）。Track.human があればそちらが優先。 */
  humanRoles?: Partial<Record<"kick" | "snare" | "hihat" | "cymbal" | "bass" | "sub" | "rhythm" | "lead" | "other", number>>;
  /** "triangle" なら、human のタイミング・強さのずれを三角分布（中心に寄りやすい）にする。省略は一様（今までどおり）。 */
  humanDist?: "triangle";
  /** true なら、ベース（slap・sub808 を除く）はキックと同じ拍に重なる音を、キックと同じだけずらす。 */
  lockToKick?: boolean;
  /** テンポマップ。拍の位置ごとのテンポ（途中の速まり・遅まり）。省略は曲全体で tempoBpm 1つ。 */
  tempoMap?: TempoPoint[];
  /** "wide" なら、音の強弱を MIDI の強さにそのまま近く反映する（弱い音をより弱く）。dynamics: "natural" の曲で使う。 */
  dynamicRange?: "wide";
  /**
   * 人間らしさ（0〜1）。省略時は0（今までどおり）。大きいほど、打ち込みらしさ（機械的な正確さ）をくずす。録音音源（MIDI経由）で効く。
   * ・各パートのタイミングのずれを大きく（人の手のばらつき）　・バンド全体が少しだけ走ったり溜めたりする（ゆるやかな揺れ）
   * ・音の強さのばらつきを大きく　・音の長さのばらつき　・長い音（リード・パッド・弦）の音量の山（立ち上がって、少し引く）
   * ・リード・ギター・弦の音程の、ごくわずかなずれ（±8セント）。0.3〜0.6が自然、1は「かなりラフ」。
   */
  human?: number;
  /** スネアの音程の調整（半音。マイナスで低く、プラスで高く。-6〜6、0.5刻み）。ドラムのNRPNで、録音音源（MIDI経由）で効く。 */
  snareTune?: number;
  /** false にすると、ギターの長い音を「半音下から持ち上げて入る」自動のしゃくりをかけない（省略は、かける）。 */
  autoScoop?: boolean;
  /**
   * false なら、ギター類の自動の揺れ（リードギターの自動ビブラート CC1・長い音の音量のふくらみ・ギター類の音ごとのわずかな音程のずれ）を付けない。
   * 省略は付ける（10/15 より前と同じ鳴り方）。2026-10-16、人間の指示「削除すんじゃなくて使わなければいいだけ」: 10/15 に全曲から消していたのを戻し、
   * 「ゴムが伸びたような音」がいやな曲だけ false にする（作曲ソフトの新しい曲は false を書く。docs/sound/banned-sounds.md 17）。
   */
  guitarWobble?: boolean;
  /** 読み込んだNAMモデル（.namファイルの中身）。名前 → JSON文字列。 */
  namModels?: Record<string, string>;
  /** 録音したトラック（オーディオインターフェースから録った、実際の楽器・声）。作曲ソフトで鳴る（ゲーム本体では鳴らさない）。 */
  audioTracks?: AudioTrack[];
  /** 追加したアンプ（アンプ定義ファイルの中身）。ID → 定義。 */
  ampPlugins?: Record<string, AmpPluginDef>;
  /** 録音音源で鳴らすときのドラムセット（GMのドラムキット番号。0=標準、16=パワー、24=電子、25=TR-808、32=ジャズ）。省略時は0。 */
  drumKit?: number;
  /** 歪みギター（GM 30）を歪ませる前の録音（DI）で鳴らす（作曲ソフトのみ。emily＝ハムバッカーの太い音／fsbs＝シングルの明るい音）。アンプで歪ませる前提。 */
  diGuitar?: "emily" | "fsbs";
  /**
   * ドラムの太鼓ごとのミックス（録音音源のドラムNRPN）。level＝音量の倍率（1が標準。0〜1.5）、pan＝左右（-1〜1。叩き手から見た位置でなく聴き手から見た位置）、reverb＝残響の送り（0〜1）。
   * 例: ハイハットは小さく左、スネアは残響を足す。tom の spread（0〜1）は、高いタムを左・低いフロアを右へ振り分ける広がり。tune は音の高さを半音単位でずらす（-6〜6）。
   */
  drumMix?: Partial<Record<"kick" | "snare" | "hat" | "tom" | "crash", { level?: number; pan?: number; reverb?: number; spread?: number; tune?: number }>>;
  /** trueなら、パッド・弦・合唱の音量をキックに合わせて周期的に凹ませる（電子音楽風のポンプ感）。 */
  pump?: boolean;
  /** trueなら、リードとパッドを電子的な音色にする（電子音楽向け）。省略時は生楽器に近い音色。 */
  synth?: boolean;
  /** ゲームで鳴らすときの、曲ごとの音量補正（dB）。曲どうしの音量差をそろえる（`bgm-trim.ts`）。省略は0。 */
  trimDb?: number;
  /** 音の版。modern=現代的な音（既定）、ps2=PS2世代のゲーム音楽（オーケストラの重ね・豊かなホール残響・高音をやや丸めた音）。 */
  edition?: "modern" | "ps2" | "real";
  /** 曲調（rock・classic・jazz など）。実楽器版で、楽器の割り当てを決めるために使う。 */
  style?: string;
  /** 楽器の音色の傾向。rock=オーバードライブ・温かいドラム、metal=メタルゾーンのギター・重低音のベース・締まったドラム、prs=特別曲用。粒立ちがよく歌うような、なめらかで澄んだギター（メタルの重さは保つ）。 */
  tone?: "rock" | "metal" | "prs";
  /** trueなら、曲の頭に強い一撃（全楽器の強いアタック、クラッシュ、バスドラム）を入れる。ループのたびに聴き手をつかむ。 */
  opening?: boolean;
  tempoBpm: number;
  /** 拍子（例: 4/4、3/4、7/8、5/4）。省略時は4/4。音の長さ（拍）は、いつも4分音符=1拍で数える。 */
  timeSig?: { num: number; den: number };
  loop: boolean;
  tracks: Track[];
}

export interface ScheduledNote {
  frequency: number;
  startSec: number;
  durationSec: number;
  waveform: Waveform;
  instrument?: Instrument;
  volume: number;
  pan?: number;
  /** 1拍の長さ（秒）。テンポに合わせたエコーなどに使う。 */
  beatSec: number;
}

function trackDurationBeats(track: Track): number {
  return track.notes.reduce((sum, n) => sum + n.durationBeats, 0);
}

/** 曲1回分の長さ（秒）。パートごとに長さが違う場合は一番長いものに合わせる。 */
export function getScoreDurationSec(score: Score): number {
  const secPerBeat = 60 / score.tempoBpm;
  const longestBeats = Math.max(0, ...score.tracks.map(trackDurationBeats));
  if (score.tempoMap?.length) return makeTempoClock(score.tempoBpm, score.tempoMap).beatToSec(longestBeats);
  return longestBeats * secPerBeat;
}

/** 同じ入力なら同じ結果になる、ごく小さな強さのゆらぎ（機械的な均一さをやわらげる）。 */
export function humanize(startSec: number): number {
  const x = Math.sin(startSec * 12.9898 + 78.233) * 43758.5453;
  return 0.93 + 0.14 * (x - Math.floor(x));
}

function flattenTrack(track: Track, score: Score): ScheduledNote[] {
  const tempoBpm = score.tempoBpm;
  const { swing, swing16 } = swingOf(score, track);
  const push = pushBeatsOf(track, tempoBpm);
  const loop = score.loop;
  const secPerBeat = 60 / tempoBpm;
  const clock = score.tempoMap?.length ? makeTempoClock(tempoBpm, score.tempoMap) : null;
  let t = 0;
  let beat = 0;
  const events: ScheduledNote[] = [];
  for (const noteEvent of track.notes) {
    const durationSec = clock ? clock.beatToSec(beat + noteEvent.durationBeats) - clock.beatToSec(beat) : noteEvent.durationBeats * secPerBeat;
    if (noteEvent.note !== REST) {
      const soundSec = durationSec * (noteEvent.gate ?? 1);
      const startSec = clock ? clock.beatToSec(beat) : t;
      const spb = clock ? 60 / clock.bpmAt(beat) : secPerBeat;
      const off = grooveOffsetBeats(swing, push, clock ? beat : t / secPerBeat, swing16);
      events.push({
        frequency: noteNameToFrequency(noteEvent.note),
        startSec: Math.max(0, clock ? clock.beatToSec(Math.max(0, beat + off)) : startSec + off * secPerBeat),
        durationSec: soundSec,
        waveform: track.waveform,
        instrument: track.instrument,
        volume: track.volume * velocityScale(noteEvent.velocity) * (loop && track.instrument ? humanize(clock ? startSec : t) : 1),
        pan: track.pan,
        beatSec: spb,
      });
    }
    t += durationSec;
    beat += noteEvent.durationBeats;
  }
  return events;
}

/** 曲を「いつ・どの高さ・どれくらいの長さで鳴らすか」の一覧に変換する。 */
export function flattenScore(score: Score): ScheduledNote[] {
  return score.tracks.flatMap((track) => flattenTrack(track, score));
}
