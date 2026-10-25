// 使い方: node tools/soundfont/build-drums.mjs
// Muldjord Kit（Lars Muldjord / DrumGizmo。CC BY 4.0）の元素材を、GMのドラムセット（0・8・16・32）の音を入れかえる小さなSoundFontにする。
//   assets-src/soundfont/extra/drums-muldjord.sf3（標準）と、ジャンル別の drums-rock / drums-metal / drums-jpop .sf3（同じ録音のまぜ方・音の長さ・イコライザー・コンプレッサーを変えたもの）
// 使い方: node --experimental-strip-types tools/soundfont/build-drums.mjs [std|rock|metal|jpop ...]（省略は全部）
// 元素材: 設定ファイル（Data/）は assets-src/soundfont/extra/src/muldjord/ に置いてある。録音（Samples/、約340MB）は大きいので git には入れない。
//   git clone https://github.com/sfzinstruments/DrumGizmo.MuldjordKit し、環境変数 MULDJORD_SAMPLES に DrumGizmo/MuldjordKit/Samples のパスを渡す。
// 元はマイク16本ぶんの録音。ここでは各ドラムを「近くのマイク＋オーバーヘッド＋部屋の音」をまぜたステレオ1組にし、
// 強さ（ベロシティ）の層ごとに1つずつ（ラウンドロビンは使わない）、必要な長さだけ切り出す。
//
// 2026-10-22 CrocellKit（DrumGizmo。録音 JBOSound／サンプリング Lars Muldjord。CC BY 4.0）にも対応（--kit crocell）:
//   node tools/soundfont/build-drums.mjs --kit crocell [crocell crocell-aux]
//   前処理 tools/soundfont/dg-extract.py が、DrumGizmo 本家の形式（楽器の XML と多チャンネル WAV）から、必要な打音の頭だけを取り出して
//   Muldjord と同じ並び（Data/region/*.txt・Data/macro.txt と Samples/<楽器>/<番号>-<楽器>-<マイク>.flac）に直す。
//   Data/ は assets-src/soundfont/extra/src/crocell/ に置く。録音は環境変数 CROCELL_SAMPLES（git には入れない）。
//   crocell-aux は、補助打楽器（タンバリン・カウベルなどの録音）を drums-muldjord-aux.sf3 から引きつぐ。
//
// 2026-10-22 Naked Drums（Wilkinson Audio。SFZ 化 kinwie。CC BY 4.0）＋Frankensnare（Karoryfer。CC0）のスネアにも対応（--kit naked）:
//   前処理 tools/soundfont/naked-extract.py が、git の中の flac から必要な打音と強さの層だけを取り出す（Data/ は assets-src/soundfont/extra/src/naked/）。
//   NAKED_SAMPLES=<取り出した録音> node tools/soundfont/build-drums.mjs --kit naked [naked naked-punch ...]（鍵盤は docs/sound/drum-keys-naked.md）
//   パスは path.join と import.meta.url から作るので、Windows でもリポジトリの外から動かせる。
import fs from "fs";
import os from "os";
import path from "path";
import { fileURLToPath } from "url";
import { decodeMono, filterStereo, loadBank, stereoPair, timecents, compressBank, SR, BasicSoundBank, GeneratorTypes } from "./lib.mjs";

const KIT_ID = process.argv.includes("--kit") ? process.argv[process.argv.indexOf("--kit") + 1] : "muldjord";
const ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const SRC = path.join(ROOT, "assets-src", "soundfont", "extra", "src", KIT_ID);
const OUT = path.join(ROOT, "assets-src", "soundfont", "extra");
const SAMPLES = KIT_ID === "crocell"
  ? process.env.CROCELL_SAMPLES ?? path.join(os.tmpdir(), "crocell", "Samples")
  : KIT_ID === "naked"
    ? process.env.NAKED_SAMPLES ?? path.join(os.tmpdir(), "naked", "Samples")
    : process.env.MULDJORD_SAMPLES ?? "/home/claude/sfzinstruments/drumgizmo.muldjordkit/DrumGizmo/MuldjordKit/Samples";
// 環境変数: DRUM_RR＝強さの層ごとに使う録音の数（1＝これまでどおり）、DRUM_Q＝Vorbis の品質（0〜10、既定 4）
const RR = Number(process.env.DRUM_RR ?? (KIT_ID === "crocell" || KIT_ID === "naked" ? 2 : 1));
const Q = Number(process.env.DRUM_Q ?? 4);
const gameBank = loadBank(path.join(ROOT, "src", "audio", "soundfont", "game.sf3"));
// 元の SFZ の音量の補正（dB。楽器→マイク）。naked-extract.py が Data/trim.json に書く
const TRIM = fs.existsSync(path.join(SRC, "Data", "trim.json")) ? JSON.parse(fs.readFileSync(path.join(SRC, "Data", "trim.json"), "utf8")) : {};

// 元の速度の層（$v51l など）
const VEL = {};
for (const m of fs.readFileSync(path.join(SRC, "Data", "macro.txt"), "utf8").matchAll(/#define \$(v\d+)([lh]) (\d+)/g)) (VEL[m[1]] ??= {})[m[2]] = Number(m[3]);

// 楽器ごとの設定: GMのキー、使う近接マイクと音量、近接マイクの左右の位置(-1〜1)、切り出す長さ(秒)、同じ「ハイハットのグループ」か
//   vel: [最小, 最大]＝この楽器の強さの層を、この範囲に詰める（同じキーで、強い打ちだけ別の録音にするとき）
//   release: 鍵盤を離したあとの減り方（秒。省略 0.3）。シンバルは長くして、すぐ止めない（人間の決まり）
const KITS = {
  muldjord: {
    KdrumL:      { keys: [35], close: { KdrumL: 0.9, KdrumR: 0.9 }, pan: 0, sec: 0.9 },
    KdrumR:      { keys: [36], close: { KdrumL: 0.9, KdrumR: 0.9 }, pan: 0, sec: 0.9 },
    Snare:       { keys: [38, 40], close: { Snare_top: 0.8, Snare_bottom: 0.25 }, pan: 0, sec: 0.9 },
    SnareRest:   { keys: [37], close: { Snare_top: 0.8, Snare_bottom: 0.25 }, pan: 0, sec: 0.6 },
    HihatClosed: { keys: [42, 44], close: { Hihat: 0.55 }, pan: -0.35, sec: 0.45, exclusive: 1 },
    HihatOpen:   { keys: [46], close: { Hihat: 0.55 }, pan: -0.35, sec: 1.8, exclusive: 1 },
    Tom4:        { keys: [41, 43], close: { Tom4: 0.7 }, pan: 0.4, sec: 1.6 },
    Tom3:        { keys: [45], close: { Tom3: 0.7 }, pan: 0.2, sec: 1.6 },
    Tom2:        { keys: [47], close: { Tom2: 0.7 }, pan: -0.1, sec: 1.6 },
    Tom1:        { keys: [48, 50], close: { Tom1: 0.7 }, pan: -0.3, sec: 1.6 },
    CrashL:      { keys: [49], close: {}, pan: 0, sec: 3.0 },
    CrashR:      { keys: [57], close: {}, pan: 0, sec: 3.0 },
    RideR:       { keys: [51], close: { RideR: 0.5 }, pan: 0.4, sec: 2.2 },
    RideL:       { keys: [59], close: { RideL: 0.5 }, pan: -0.3, sec: 2.2 },
    RideRBell:   { keys: [53], close: { RideR: 0.5 }, pan: 0.4, sec: 1.8 },
    RideLBell:   { keys: [55], close: { RideL: 0.5 }, pan: -0.3, sec: 1.8 },
    China:       { keys: [52], close: {}, pan: 0, sec: 2.5 },
  },
  // CrocellKit（2018年のメタルのアルバム録音のキット）。GM の番号に合わせ、GM に無いシンバルは 88 番より上の空きキーに置く（docs/sound/drum-keys-crocell.md）
  //   止め打ち（93・94）は、同じクラッシュ（49・57）の余韻を止める（exclusive）。
//   キックは中のマイク（Beta 91A＝アタック）と外のマイク（E602＝胴の重み）をまぜる。スネアのいちばん強い打ち（118〜127）はリムショットの録音
  crocell: {
    KDrumL:        { keys: [35], close: { KDrumInside: 0.75, KDrumOutside: 1.0 }, pan: 0, sec: 1.0 },
    KDrumR:        { keys: [36], close: { KDrumInside: 0.75, KDrumOutside: 1.0 }, pan: 0, sec: 1.0 },
    Snare:         { keys: [38, 40], close: { SnareTop: 0.85, SnareBottom: 0.3 }, pan: 0, sec: 1.0, vel: [1, 117] },
    SnareRimShot:  { keys: [38, 40], close: { SnareTop: 0.85, SnareBottom: 0.3 }, pan: 0, sec: 1.0, vel: [118, 127] },
    SnareRim:      { keys: [37], close: { SnareTop: 0.8, SnareBottom: 0.2 }, pan: 0, sec: 0.5 },
    HihatClosed:   { keys: [42], close: { Hihat: 0.55 }, pan: -0.35, sec: 0.6, exclusive: 1 },
    HihatPedal:    { keys: [44], close: { Hihat: 0.55 }, pan: -0.35, sec: 0.5, exclusive: 1 },
    // 2026-10-22 人間「半開きでももう少し音伸びていい」: 開き・半開きは鍵盤を離したあとも録音の「シャー」を残す（release は −96dB までの秒数。4 秒で −20dB まで約 0.8 秒）。
    //   止まるのは、同じ exclusive 1 の次のクローズ・ペダルが鳴ったときだけ。閉じは録音どおり強さで音色が変わらない（−20dB まで 45〜90ms）
    HihatOpen:     { keys: [46], close: { Hihat: 0.55 }, pan: -0.35, sec: 2.5, exclusive: 1, release: 6 },
    HihatSemiOpen: { keys: [95], close: { Hihat: 0.55 }, pan: -0.35, sec: 1.5, exclusive: 1, release: 4 },
    FTom2:         { keys: [41], close: { FTom2: 0.75 }, pan: 0.45, sec: 2.0 },
    FTom1:         { keys: [43], close: { FTom1: 0.75 }, pan: 0.3, sec: 2.0 },
    Tom2:          { keys: [45, 47], close: { Tom2: 0.75 }, pan: 0.05, sec: 1.8 },
    Tom1:          { keys: [48, 50], close: { Tom1: 0.75 }, pan: -0.2, sec: 1.8 },
    CrashL:        { keys: [49], close: {}, pan: 0, sec: 5.5, release: 4, exclusive: 2 },
    CrashR:        { keys: [57], close: {}, pan: 0, sec: 5.5, release: 4, exclusive: 3 },
    CrashRXtra:    { keys: [92], close: {}, pan: 0, sec: 5.5, release: 4 },
    CrashLStopped: { keys: [93], close: {}, pan: 0, sec: 1.2, release: 0.2, exclusive: 2 },
    CrashRStopped: { keys: [94], close: {}, pan: 0, sec: 1.2, release: 0.2, exclusive: 3 },
    RideR:         { keys: [51, 59], close: { Ride: 0.45 }, pan: 0.4, sec: 3.5, release: 2 },
    RideRBell:     { keys: [53], close: { Ride: 0.45 }, pan: 0.4, sec: 3.5, release: 2 },
    ChinaR:        { keys: [52], close: {}, pan: 0, sec: 4.5, release: 3 },
    ChinaL:        { keys: [90], close: {}, pan: 0, sec: 4.5, release: 3 },
    SplashR:       { keys: [55], close: {}, pan: 0, sec: 3.0, release: 2.5 },
    SplashL:       { keys: [91], close: {}, pan: 0, sec: 3.0, release: 2.5 },
  },
  // Naked Drums（Yamaha Recording Custom・22" キック・タム5つ・Sabian／Zildjian のシンバル）＋Frankensnare のスネア（Fs で始まる楽器）。
  //   鍵盤は GM に合わせる（docs/sound/drum-keys-naked.md）。GM に無いものは CrocellKit と同じ番号（90 チャイナ2・91 スプラッシュ2・93／94 止め打ち・95 半開き）。
  //   keys: [] の楽器は、ふだんは鳴らさない（設定の keys で鍵盤に割り当てる。スネアの差しかえ用）。tune＝元の SFZ のタムの音程の補正（セント）
  //   キックは Kick In（中のマイク＝アタック）と Kick Sub（外の低音のマイク）。スネアは上のマイク2本と下のマイク
  naked: {
    Kick:        { keys: [35, 36], close: { KickIn: 0.8, KickSub: 0.8 }, pan: 0, sec: 1.2 },
    SideStick:   { keys: [37], close: { SnareTop1: 0.6, SnareTop2: 0.4, SnareBot: 0.2 }, pan: 0, sec: 0.6 },
    Snare:       { keys: [38, 40], close: { SnareTop1: 0.6, SnareTop2: 0.4, SnareBot: 0.3 }, pan: 0, sec: 1.3 },
    Snare2:      { keys: [], close: { SnareTop1: 0.6, SnareTop2: 0.4, SnareBot: 0.3 }, pan: 0, sec: 1.3 },
    FsAlu:       { keys: [], close: { FsTop: 0.85, FsBtm: 0.3 }, pan: 0, sec: 1.3 },
    FsAluRim:    { keys: [], close: { FsTop: 0.85, FsBtm: 0.3 }, pan: 0, sec: 1.3 },
    FsMaple:     { keys: [], close: { FsTop: 0.85, FsBtm: 0.3 }, pan: 0, sec: 1.3 },
    // 2026-10-22 人間「オープンなのかクローズなのかわからない」: 42 は元の「tight」（しっかり閉じたチック。−20dB まで 50〜65ms で、強さで音色が変わらない）。
    //   元の「closed」は強く叩くほど余韻が長く（80→130ms）ゆるい閉じ方になるので、ふだんは鳴らさない。開き・半開き・ペダルと同じ exclusive 1 で、次のクローズ・ペダルで止まる
    HihatClosed: { keys: [], close: { Hats: 0.55 }, pan: -0.35, sec: 0.8, exclusive: 1 },
    HihatTight:  { keys: [42], close: { Hats: 0.55 }, pan: -0.35, sec: 0.6, exclusive: 1 },
    HihatPedal:  { keys: [44], close: { Hats: 0.55 }, pan: -0.35, sec: 0.6, exclusive: 1 },
    // 開き・半開きは、鍵盤を離したあとも録音の「シャー」が自然に消えるまで鳴らす（人間「半開きでももう少し音伸びていい」）。止まるのは次のクローズ・ペダルのときだけ。
    //   release は SoundFont の決まりで「−96dB まで」の秒数（4 秒なら −20dB まで約 0.8 秒）
    HihatOpen:   { keys: [46], close: { Hats: 0.55 }, pan: -0.35, sec: 3.2, exclusive: 1, release: 6 },
    HihatHalf:   { keys: [95], close: { Hats: 0.55 }, pan: -0.35, sec: 1.8, exclusive: 1, release: 4 },
    Tom5:        { keys: [41], close: { Tom: 0.75 }, pan: 0.45, sec: 2.2 },
    Tom4:        { keys: [43], close: { Tom: 0.75 }, pan: 0.3, sec: 2.2, tune: -70 },
    Tom3:        { keys: [45], close: { Tom: 0.75 }, pan: 0.1, sec: 2.2, tune: -200 },
    Tom2:        { keys: [47, 48], close: { Tom: 0.75 }, pan: -0.1, sec: 2.2 },
    Tom1:        { keys: [50], close: { Tom: 0.75 }, pan: -0.25, sec: 2.2 },
    Ride:        { keys: [51, 59], close: { Ride: 0.45 }, pan: 0.4, sec: 4.0, release: 2 },
    RideBell:    { keys: [53], close: { Ride: 0.45 }, pan: 0.4, sec: 4.0, release: 2 },
    Crash1:      { keys: [49], close: {}, pan: 0, sec: 5.0, release: 4, exclusive: 2 },
    Crash2:      { keys: [57], close: {}, pan: 0, sec: 5.0, release: 4, exclusive: 3 },
    Crash1Choke: { keys: [93], close: {}, pan: 0, sec: 1.2, release: 0.2, exclusive: 2 },
    Crash2Choke: { keys: [94], close: {}, pan: 0, sec: 1.2, release: 0.2, exclusive: 3 },
    China1:      { keys: [52], close: {}, pan: 0, sec: 5.0, release: 3 },
    China2:      { keys: [90], close: {}, pan: 0, sec: 5.0, release: 3 },
    Splash1:     { keys: [55], close: {}, pan: 0, sec: 4.0, release: 2.5 },
    Splash2:     { keys: [91], close: {}, pan: 0, sec: 4.0, release: 2.5 },
  },
};
const KIT = KITS[KIT_ID];
if (!KIT) throw new Error(`キットがありません: ${KIT_ID}`);
// ジャンル別のまぜ方。overhead／amb＝オーバーヘッド・部屋のマイクの量、kick／snare／tom／hat＝各ドラムの近接マイクの倍率、cym＝シンバルの長さの倍率、sec＝全体の長さの倍率、eq＝仕上げのフィルター（ffmpeg）
// naked-punch 系の共通の設定（数値は 8ビートを測って合わせる。docs/sound/drum-sound-target.md）
const PUNCH_NAKED = {
  overhead: 0.3, ohKind: { kick: 0.08, snare: 0.25, tom: 0.25, hat: 0.5, cym: 0.85 }, ohc: 0,
  amb: 0.25, ambKind: { hat: 0.05, cym: 0.1 },
  ambFx: "highpass=f=500,highpass=f=500,lowpass=f=5000,lowpass=f=5000,acompressor=threshold=-34dB:ratio=10:attack=1:release=60:makeup=10",
  kick: 1.35, snare: 0.95, tom: 0.85, hat: 0.85, cym: 0.7, sec: 1, fade: 0.6,
  inst: { Kick: { close: { KickIn: 1.0, KickSub: 0.45 } } },
  eq: "highpass=f=28",
  snareEq: "highpass=f=90,equalizer=f=180:t=q:w=1:g=3,equalizer=f=550:t=q:w=1.2:g=-7,equalizer=f=5000:t=q:w=1:g=3,equalizer=f=10000:t=q:w=1:g=3,acompressor=threshold=-22dB:ratio=6:attack=3:release=60:makeup=3",
  kindEq: {
    kick: "highpass=f=55,highpass=f=55,highpass=f=55,equalizer=f=120:t=q:w=1:g=3,equalizer=f=320:t=q:w=1.2:g=-8,equalizer=f=4500:t=q:w=1:g=5,equalizer=f=9000:t=q:w=1:g=6,acompressor=threshold=-22dB:ratio=6:attack=5:release=60:makeup=3",
    tom: "highpass=f=55,equalizer=f=500:t=q:w=1.3:g=-6,equalizer=f=4000:t=q:w=1:g=3,acompressor=threshold=-22dB:ratio=5:attack=5:release=80:makeup=2",
    hat: "highpass=f=300,highshelf=f=6000:g=-4",
    cym: "highpass=f=250,equalizer=f=3500:t=q:w=1:g=-3,highshelf=f=6000:g=-3",
  },
  click: { kick: { db: 3, ms: 15, rise: 2, lo: 3000, hi: 12000 } },
  gain: { snare: 17 },
  bandEq: { kick: [-27, -15, 0, 9, -9, -8, -3, 4, 4, 6], snare: [0, 10, 0, -8, -16, -14, -12, -7, -1, 4] },
  attack: { kick: 6, snare: 4, tom: 4 },
  clip: { kick: 2.5, snare: 2, tom: 2 },
};
const PROFILES = {
  std:   { out: "drums-muldjord", label: "標準", overhead: 1.0, amb: 0.45, kick: 1, snare: 1, tom: 1, hat: 1, cym: 1, sec: 1, eq: "" },
  rock:  { out: "drums-rock", label: "ロック", overhead: 1.0, amb: 0.85, kick: 1.1, snare: 1.1, tom: 1.1, hat: 1, cym: 1.2, sec: 1.2,
    eq: "equalizer=f=90:t=q:w=1:g=2,equalizer=f=5000:t=q:w=1:g=1.5,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=1.5" },
  metal: { out: "drums-metal", label: "メタル", overhead: 0.6, amb: 0.1, kick: 1.7, snare: 1.5, tom: 1.4, hat: 1, cym: 0.6, sec: 0.7,
    eq: "highpass=f=35,equalizer=f=60:t=q:w=1:g=3,equalizer=f=450:t=q:w=1.5:g=-3,equalizer=f=3500:t=q:w=1:g=4,acompressor=threshold=-22dB:ratio=4:attack=2:release=50:makeup=2" },
  jpop:  { out: "drums-jpop", label: "J-POP", overhead: 0.9, amb: 0.25, kick: 1.2, snare: 1.3, tom: 1.0, hat: 1.1, cym: 0.8, sec: 0.85,
    eq: "highpass=f=40,equalizer=f=90:t=q:w=1:g=2,equalizer=f=4500:t=q:w=1:g=3,equalizer=f=9000:t=q:w=1:g=2,acompressor=threshold=-20dB:ratio=3:attack=4:release=80:makeup=1.5" },
  // 「スープラ」: 乾いて硬い金属スネア（アルミ胴の定番スネアのような、パシッと抜ける高めの音）に寄せた設定。部屋の鳴りを減らし、スネアだけ別のイコライザーと短い余韻にする
  supra: { out: "drums-supra", label: "スープラ", overhead: 0.8, amb: 0.12, kick: 1.15, snare: 1.45, tom: 1.0, hat: 1.05, cym: 0.8, sec: 0.85, snareSec: 0.55, crashSec: 2.2, crashTail: 6,
    eq: "highpass=f=40,equalizer=f=90:t=q:w=1:g=2,equalizer=f=4500:t=q:w=1:g=2,equalizer=f=9000:t=q:w=1:g=2,acompressor=threshold=-20dB:ratio=3:attack=4:release=80:makeup=1.5",
    snareEq: "highpass=f=110,equalizer=f=230:t=q:w=1.2:g=1.5,equalizer=f=420:t=q:w=1.5:g=-4,equalizer=f=1800:t=q:w=1.5:g=1.5,equalizer=f=5500:t=q:w=1:g=4.5,equalizer=f=10000:t=q:w=1:g=3,acompressor=threshold=-24dB:ratio=4:attack=1.5:release=45:makeup=2" },
  // CrocellKit: 部屋の鳴りを少し、OH の真ん中のマイクを半分。キックは 55Hz の胴の重みと 4kHz のアタック、400Hz の箱鳴りを少し引く
  crocell: { kit: "crocell", out: "drums-crocell", label: "CrocellKit", overhead: 1.0, ohc: 0.5, amb: 0.4, kick: 1.15, snare: 1.1, tom: 1.0, hat: 1, cym: 1, sec: 1, fade: 0.6,
    eq: "highpass=f=28",
    kindEq: { kick: "highpass=f=28,equalizer=f=55:t=q:w=1:g=3,equalizer=f=400:t=q:w=1.5:g=-3,equalizer=f=4000:t=q:w=1:g=2.5" } },
  // 2026-10-22 CrocellKit の「乾いてパンチのある版」（人間「空間を感じすぎる」「NEW ERA みたいなドラム」）。
  // 部屋マイクは使わない・太鼓の OH は少しだけ。作曲ソフトのドラムは1本の通り道を共有して太鼓ごとに fx を掛けられないので、
  // 太鼓ごとの音作り（EQ・1打ごとの圧縮）をここで録音に焼き込む。目標の数値は docs/sound/drum-sound-target.md
  "crocell-punch": { kit: "crocell", out: "drums-crocell-punch", label: "CrocellKit（乾いてパンチ）", overhead: 0.3, ohKind: { kick: 0.12, snare: 0.3, tom: 0.25, hat: 0.5, cym: 0.85 }, ohc: 0, amb: 0,
    kick: 1.35, snare: 0.95, tom: 0.85, hat: 0.9, cym: 0.75, sec: 1, fade: 0.6,
    eq: "highpass=f=28",
    snareEq: "highpass=f=90,equalizer=f=190:t=q:w=1:g=3,equalizer=f=650:t=q:w=1.3:g=-7,equalizer=f=5500:t=q:w=1:g=4,highshelf=f=8000:g=7,acompressor=threshold=-20dB:ratio=4:attack=3:release=60:makeup=2",
    kindEq: {
      kick: "highpass=f=48,highpass=f=48,highpass=f=42,equalizer=f=65:t=q:w=1:g=1.5,equalizer=f=110:t=q:w=1:g=2.5,equalizer=f=380:t=q:w=1.2:g=-6.5,equalizer=f=3500:t=q:w=1:g=3.0,equalizer=f=7500:t=q:w=0.8:g=4.5,acompressor=threshold=-18dB:ratio=4:attack=5:release=60:makeup=2",
      tom: "highpass=f=60,equalizer=f=500:t=q:w=1.3:g=-7,equalizer=f=4000:t=q:w=1:g=4,acompressor=threshold=-20dB:ratio=3:attack=5:release=80",
      hat: "highpass=f=300,highshelf=f=7000:g=7",
      // シンバルは録音の自然な音のまま（人間の決まり「鳴りを伸ばす」。2026-10-22「これはシンバルの音じゃないな」を受けて、持ち上げ・圧縮・クリップはしない）
      cym: "highpass=f=250",
    },
    // 2026-10-22 追加（人間「もうちょっとだけ頑張って近づけよう」）: キックの中のマイク（ビーター側）を強め、録音に無い「カチッ」を合成のクリックで足す。
    // 帯域の補正・アタックの強調・軽いクリップは naked-punch と同じしくみ（数値は 1打ずつ測って合わせた）
    micMul: { KDrumInside: 1.5 },
    // 2026-10-22 人間「バスドラの音がこれだと高すぎ」: 低音を切る周波数を 85→48Hz に下げて胴の低さを戻し、カチッ（3.5k・7.5k・クリック・ビーター側のマイク）を控えめにした（細かい刻みで調整）
    // クリックを 10dB にすると、キックの 6k〜12kHz は目標に近づくが、全体の高域とクレストが目標から離れた（2026-10-22 の8ビートで比べて 6dB にした）
    click: { kick: { db: 2.5, ms: 15, rise: 2, lo: 3000, hi: 12000 } },
    bandEq: { kick: [0, 0, 0, 4.5, 3.5, 4.5, 3.5, 2.5, 2.5, 3.0], snare: [0, 10, 0, -9, -16, -10, -8, -7, -3, 0] },
    attack: { kick: 4, snare: 3, tom: 3 },
    clip: { kick: 2.5, snare: 2, tom: 2 },
    gain: { snare: 16 } },
  // 2026-10-26 人間「07 08 10、トリガーの音がバスドラの重さを掻き消しちゃってる。トリガー無くさなくていいんだけどね」:
  //   crocell-punch から、キックの「カチッ」（合成のクリック 2.5→0.8dB・ビーター側のマイク 1.5→1.15 倍・3.5k／7.5k の持ち上げ）を控え、胴（58〜100Hz）を足した版
  "crocell-punch-heavy": { kit: "crocell", out: "drums-crocell-punch-heavy", label: "CrocellKit（乾いてパンチ・キックの重さ）", overhead: 0.3, ohKind: { kick: 0.12, snare: 0.3, tom: 0.25, hat: 0.5, cym: 0.85 }, ohc: 0, amb: 0,
    kick: 1.35, snare: 0.95, tom: 0.85, hat: 0.9, cym: 0.75, sec: 1, fade: 0.6,
    eq: "highpass=f=28",
    snareEq: "highpass=f=90,equalizer=f=190:t=q:w=1:g=3,equalizer=f=650:t=q:w=1.3:g=-7,equalizer=f=5500:t=q:w=1:g=4,highshelf=f=8000:g=7,acompressor=threshold=-20dB:ratio=4:attack=3:release=60:makeup=2",
    kindEq: {
      kick: "highpass=f=36,highpass=f=36,equalizer=f=58:t=q:w=1:g=4.0,equalizer=f=100:t=q:w=1:g=3.0,equalizer=f=380:t=q:w=1.2:g=-6.5,equalizer=f=3500:t=q:w=1:g=1.0,equalizer=f=7500:t=q:w=0.8:g=1.5,acompressor=threshold=-18dB:ratio=4:attack=5:release=60:makeup=2",
      tom: "highpass=f=60,equalizer=f=500:t=q:w=1.3:g=-7,equalizer=f=4000:t=q:w=1:g=4,acompressor=threshold=-20dB:ratio=3:attack=5:release=80",
      hat: "highpass=f=300,highshelf=f=7000:g=7",
      // シンバルは録音の自然な音のまま（人間の決まり「鳴りを伸ばす」。2026-10-22「これはシンバルの音じゃないな」を受けて、持ち上げ・圧縮・クリップはしない）
      cym: "highpass=f=250",
    },
    // 2026-10-22 追加（人間「もうちょっとだけ頑張って近づけよう」）: キックの中のマイク（ビーター側）を強め、録音に無い「カチッ」を合成のクリックで足す。
    // 帯域の補正・アタックの強調・軽いクリップは naked-punch と同じしくみ（数値は 1打ずつ測って合わせた）
    micMul: { KDrumInside: 1.15 },
    // 2026-10-22 人間「バスドラの音がこれだと高すぎ」: 低音を切る周波数を 85→48Hz に下げて胴の低さを戻し、カチッ（3.5k・7.5k・クリック・ビーター側のマイク）を控えめにした（細かい刻みで調整）
    // クリックを 10dB にすると、キックの 6k〜12kHz は目標に近づくが、全体の高域とクレストが目標から離れた（2026-10-22 の8ビートで比べて 6dB にした）
    click: { kick: { db: 0.8, ms: 15, rise: 2, lo: 3000, hi: 12000 } },
    bandEq: { kick: [1.5, 3.0, 1.0, 3.0, 3.5, 4.5, 2.0, 0.5, 0.0, 1.0], snare: [0, 10, 0, -9, -16, -10, -8, -7, -3, 0] },
    attack: { kick: 4, snare: 3, tom: 3 },
    clip: { kick: 2.5, snare: 2, tom: 2 },
    gain: { snare: 16 } },
  // 2026-10-22 Naked Drums の素直な混ぜ方: 近接マイク＋OH＋部屋（Close Room）少し。元の SFZ の音量の補正（trim.json）どおり
  naked: { kit: "naked", out: "drums-naked", label: "Naked Drums", overhead: 0.9, amb: 0.35, kick: 1.1, snare: 1.0, tom: 1.0, hat: 1, cym: 1, sec: 1, fade: 0.6,
    eq: "highpass=f=28" },
  // 2026-10-22 Naked Drums の「乾いてパンチのある版」（目標は docs/sound/drum-sound-target.md の NEW ERA のドラムの数値）。
  // キックは Kick In（アタック）と Kick Sub（低音）を目標のキックの形になる割合で混ぜる。部屋（Close Room）は 500Hz より下と 5kHz より上を切って潰し、少しだけ。
  // 太鼓ごとに EQ・圧縮（6:1 前後）・アタックの強調・軽いクリップ（2〜3dB）を録音に焼き込む（作曲ソフトのドラムは1本の通り道を共有するため）
  "naked-punch": { kit: "naked", out: "drums-naked-punch", label: "Naked Drums（乾いてパンチ）", ...PUNCH_NAKED },
  // スネアを Frankensnare の 14x8 アルミに差しかえ（強さ 118〜127 はリムショットの録音。CrocellKit と同じ）
  "naked-punch-fs": { kit: "naked", out: "drums-naked-punch-fs", label: "Naked Drums（乾いてパンチ・アルミのスネア）", ...PUNCH_NAKED,
    inst: { ...PUNCH_NAKED.inst, Snare: { keys: [] }, FsAlu: { keys: [38, 40], vel: [1, 117] }, FsAluRim: { keys: [38, 40], vel: [118, 127] } },
    // アルミの胴は高域が明るいので、Naked のスネアより 3k〜12kHz を控えめに
    bandEq: { ...PUNCH_NAKED.bandEq, FsAlu: [0, 10, 0, -13, -16, -14, -12, -13, -9, 0], FsAluRim: [0, 10, 0, -13, -16, -14, -12, -13, -9, 0] } },
  // Naked のスネアに Frankensnare の 14x8 アルミの近接マイクを重ねる
  "naked-punch-stack": { kit: "naked", out: "drums-naked-punch-stack", label: "Naked Drums（乾いてパンチ・アルミを重ねたスネア）", ...PUNCH_NAKED,
    stack: { Snare: { inst: "FsAlu", gain: 0.45 } } },
  "crocell-aux": { kit: "crocell", base: "drums-muldjord-aux", out: "drums-crocell-aux", label: "CrocellKit＋録音の小物", overhead: 1.0, ohc: 0.5, amb: 0.4, kick: 1.15, snare: 1.1, tom: 1.0, hat: 1, cym: 1, sec: 1, fade: 0.6,
    eq: "highpass=f=28",
    kindEq: { kick: "highpass=f=28,equalizer=f=55:t=q:w=1:g=3,equalizer=f=400:t=q:w=1.5:g=-3,equalizer=f=4000:t=q:w=1:g=2.5" } },
};
const which = [...new Set(process.argv.slice(2).filter((a, i, all) => all[i - 1] !== "--kit"))].filter((a) => a in PROFILES && (PROFILES[a].kit ?? "muldjord") === KIT_ID);
/** 近接マイクの倍率（楽器の種類で選ぶ） */
const kindOf = (inst) => (/^(K[dD]rum|Kick)/.test(inst) ? "kick" : /^(Snare|SideStick|Fs)/.test(inst) ? "snare" : inst.startsWith("Tom") ? "tom" : inst.startsWith("Hihat") ? "hat" : "cym");

/** 元の region ファイルから、強さの層ごとの最初のサンプル番号を取り出す。 */
function layers(name, cfg = KIT[name]) {
  const found = new Map();
  for (const line of fs.readFileSync(path.join(SRC, "Data", "region", name + ".txt"), "utf8").split("\n")) {
    const m = /<region>\s+lovel=\$(v\d+)l hivel=\$(v\d+)h.*sample=\$instr\/(\d+)-/.exec(line);
    if (!m) continue;
    if (!found.has(m[1])) found.set(m[1], { v: m[1], idx: Number(m[3]), idxs: [] });
    found.get(m[1]).idxs.push(Number(m[3]));
  }
  // ラウンドロビンの代わり（2026-10-15）: SoundFont にはラウンドロビンがないので、強さの層をさらに RR 個の細い範囲に分け、
  // それぞれに同じ強さの別の録音を入れる。演奏の強さの揺れで毎回ちがう録音が鳴り、同じ音のくり返し（機関銃のような音）を減らす。
  const out = [];
  // vel の指定があるときは、元の層の範囲（1〜127）を、その範囲に詰める
  const squeeze = (v) => (cfg?.vel ? Math.round(cfg.vel[0] + ((v - 1) * (cfg.vel[1] - cfg.vel[0])) / 126) : v);
  for (const x of found.values()) {
    const lo = squeeze(VEL[x.v].l), hi = Math.max(squeeze(VEL[x.v].l), squeeze(VEL[x.v].h));
    const n = Math.max(1, Math.min(RR, x.idxs.length, hi - lo + 1));
    for (let k = 0; k < n; k++) {
      const a = lo + Math.round(((hi - lo + 1) * k) / n), b = lo + Math.round(((hi - lo + 1) * (k + 1)) / n) - 1;
      out.push({ v: x.v, idx: x.idxs[k], lo: a, hi: b });
    }
  }
  return out;
}

function hit(inst, idx, cfg, prof) {
  const sec = cfg.sec * prof.sec * (kindOf(inst) === "cym" ? prof.cym : 1) * (/^Crash/.test(inst) && prof.crashSec ? prof.crashSec : 1) * (kindOf(inst) === "snare" && prof.snareSec ? prof.snareSec : 1);
  cfg = { ...cfg, sec };
  const file = (mic) => path.join(SAMPLES, inst, `${idx}-${inst}-${mic}.flac`);
  // 録音の無いマイク（Frankensnare の部屋など）は無音。TRIM＝元の SFZ の音量の補正（OHL/OHR は OH、AmbL/AmbR は CR）
  const read = (mic) => {
    if (!fs.existsSync(file(mic))) return new Float32Array(0);
    const buf = decodeMono(file(mic), cfg.sec);
    const db = TRIM[inst]?.[mic.replace(/^OH[LR]$/, "OH").replace(/^Amb[LR]$/, "CR")] ?? 0;
    if (db) { const g = Math.pow(10, db / 20); for (let i = 0; i < buf.length; i++) buf[i] *= g; }
    return buf;
  };
  const len = Math.round(cfg.sec * SR);
  const L = new Float32Array(len), R = new Float32Array(len);
  const add = (buf, gl, gr) => { for (let i = 0; i < Math.min(len, buf.length); i++) { L[i] += buf[i] * gl; R[i] += buf[i] * gr; } };
  // ohKind: 楽器の種類ごとの OH（上のマイク）の量。太鼓は近接マイク中心で乾いた音に、シンバルは OH から鳴らす（crocell-punch）
  const oh = prof.ohKind?.[kindOf(inst)] ?? prof.overhead;
  add(read("OHL"), oh, 0); add(read("OHR"), 0, oh);
  // ambFx: 部屋のマイクだけに掛けるフィルター（500Hz より下と 5kHz より上を切って潰す、など。naked-punch）
  const ambAmt = prof.ambKind?.[kindOf(inst)] ?? prof.amb;
  if (ambAmt) {
    let [al, ar] = [read("AmbL"), read("AmbR")];
    if (prof.ambFx && al.length) {
      const pad = (x) => { const y = new Float32Array(len); y.set(x.subarray(0, len)); return y; };
      [al, ar] = filterStereo(pad(al), pad(ar), prof.ambFx);
    }
    add(al, ambAmt, 0); add(ar, 0, ambAmt);
  }
  if (prof.ohc && fs.existsSync(file("OHC"))) { const c = read("OHC"); add(c, prof.ohc * 0.7071, prof.ohc * 0.7071); }
  const ang = ((cfg.pan + 1) * Math.PI) / 4; // 一定パワーのパン
  const boost = prof[kindOf(inst)];
  // micMul: 設定ごとの近接マイクの倍率（キックの中のマイク＝ビーター側を強めて「カチッ」を出す、など）
  for (const [mic, g0] of Object.entries(cfg.close)) { const g = g0 * (prof.micMul?.[mic] ?? 1); add(read(mic), g * boost * Math.cos(ang) * 1.2, g * boost * Math.sin(ang) * 1.2); }
  // 重ね（stack）: 別の楽器の録音（同じくらいの強さの層）を、EQ の前に足す（Naked のスネア＋Frankensnare のアルミなど）
  if (cfg.stackWith) { const [sl, sr] = cfg.stackWith; for (let i = 0; i < Math.min(len, sl.length); i++) { L[i] += sl[i]; R[i] += sr[i]; } }
  const [fl, fr] = filterStereo(L, R, prof.instEq?.[inst] ?? (kindOf(inst) === "snare" && prof.snareEq ? prof.snareEq : prof.kindEq?.[kindOf(inst)] ?? prof.eq));
  L.set(fl.subarray(0, len)); R.set(fr.subarray(0, len));
  // 帯域ごとの補正（bandEq: { 種類: [10帯域の dB] }）。帯域は docs/sound/drum-sound-target.md の測り方と同じ 30〜20kHz の10個
  const beq = prof.bandEq?.[inst] ?? prof.bandEq?.[kindOf(inst)];
  if (beq) { const [bl, br] = filterStereo(L, R, bandEqFilter(beq)); L.set(bl.subarray(0, len)); R.set(br.subarray(0, len)); }
  // 合成のクリック（click: { 種類: { db, ms, lo, hi } }）: 録音に無い「カチッ」を、打音の頭に足す。
  //   短いノイズ（ms）を lo〜hi Hz に絞り、打音の山に比例した大きさ（山から db）で重ねる。乱数は楽器と番号で決まる種でそろえる（毎回同じ音）。
  //   rise＝立ち上がりの ms。音程は持たない（音程が滑る合成音＝「きゅいん」にはしない）
  const ck = prof.click?.[inst] ?? prof.click?.[kindOf(inst)];
  if (ck) addClick(L, R, ck, `${inst}-${idx}`);
  // アタックの強調（トランジェント・シェイパー）: 速い包絡と遅い包絡の比で、叩いた瞬間だけ持ち上げる（attack＝最大の dB）
  const atk = prof.attack?.[kindOf(inst)];
  if (atk) transient(L, R, atk);
  // クラッシュの余韻をのばす: 録音の減り方（約-18dB/秒）をゆるやかにするため、時間とともに音量を持ち上げる（上限 +36dB）
  if (/^Crash/.test(inst) && prof.crashTail) {
    for (let i = 0; i < len; i++) { const g = Math.pow(10, Math.min(36, (prof.crashTail * i) / SR) / 20); L[i] *= g; R[i] *= g; }
  }
  // 終わりを 0.12秒かけて静かにする
  const fade = Math.round(Math.min(cfg.sec * 0.4, (/^Crash/.test(inst) && prof.crashSec) || (prof.fade && kindOf(inst) === "cym") ? prof.fade ?? 0.6 : 0.12) * SR);
  for (let i = 0; i < fade; i++) { const g = i / fade; L[len - 1 - i] *= g; R[len - 1 - i] *= g; }
  return [L, R];
}

const BAND_CENTERS = [42, 77, 141, 283, 566, 1131, 2263, 4525, 8764, 15492];
/** 10帯域の dB を ffmpeg の equalizer（1オクターブ幅）の並びにする */
function bandEqFilter(db) {
  return db.map((g, i) => (g ? `equalizer=f=${BAND_CENTERS[i]}:t=o:w=1:g=${g}` : "")).filter(Boolean).join(",") || "anull";
}
/** 種でそろえた乱数（mulberry32） */
function rng(seedText) {
  let a = 0;
  for (const ch of seedText) a = (Math.imul(a, 31) + ch.charCodeAt(0)) | 0;
  return () => { a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
}
/** 2次の IIR（RBJ）のハイパス／ローパス */
function biquad(x, kind, f0) {
  const w = (2 * Math.PI * f0) / SR, c = Math.cos(w), al = Math.sin(w) / (2 * Math.SQRT1_2);
  const b = kind === "hp" ? [(1 + c) / 2, -(1 + c), (1 + c) / 2] : [(1 - c) / 2, 1 - c, (1 - c) / 2];
  const a0 = 1 + al, a1 = -2 * c, a2 = 1 - al;
  const y = new Float32Array(x.length);
  let x1 = 0, x2 = 0, y1 = 0, y2 = 0;
  for (let i = 0; i < x.length; i++) { const v = (b[0] * x[i] + b[1] * x1 + b[2] * x2 - a1 * y1 - a2 * y2) / a0; x2 = x1; x1 = x[i]; y2 = y1; y1 = v; y[i] = v; }
  return y;
}
/** 打音の頭（山の 10% を最初に越えた所）に、帯域を絞ったノイズのクリックを足す */
function addClick(L, R, ck, seed) {
  let pk = 0, pi = 0;
  for (let i = 0; i < Math.min(L.length, SR * 0.05); i++) { const v = Math.max(Math.abs(L[i]), Math.abs(R[i])); if (v > pk) { pk = v; pi = i; } }
  let on = 0;
  while (on < pi && Math.max(Math.abs(L[on]), Math.abs(R[on])) < pk * 0.1) on++;
  const n = Math.round(((ck.ms ?? 2.5) / 1000) * SR * 3);
  const r = rng(seed);
  let z = new Float32Array(n + 64);
  const tau = ((ck.ms ?? 2.5) / 1000) * SR / 2.3; // ms で約 -20dB まで減る
  for (let i = 0; i < n; i++) z[i] = (r() * 2 - 1) * Math.min(1, i / (SR * ((ck.rise ?? 0.2) / 1000))) * Math.exp(-i / tau);
  for (let k = 0; k < 2; k++) { z = biquad(z, "hp", ck.lo ?? 3000); z = biquad(z, "lp", ck.hi ?? 10000); }
  let zp = 0;
  for (const v of z) zp = Math.max(zp, Math.abs(v));
  const g = (pk * Math.pow(10, (ck.db ?? 0) / 20)) / (zp || 1);
  for (let i = 0; i < z.length && on + i < L.length; i++) { L[on + i] += z[i] * g; R[on + i] += z[i] * g; }
}
/** アタックの強調: 速い包絡（0.5ms）が遅い包絡（12ms）を上まわる所だけ、最大 maxDb まで持ち上げる */
function transient(L, R, maxDb) {
  const a = (ms) => Math.exp(-1 / ((ms / 1000) * SR));
  const fa = a(0.5), sa = a(12), rel = a(40);
  let f = 0, sl = 0;
  const gmax = Math.pow(10, maxDb / 20);
  for (let i = 0; i < L.length; i++) {
    const x = Math.max(Math.abs(L[i]), Math.abs(R[i]));
    f = x > f ? fa * f + (1 - fa) * x : rel * f + (1 - rel) * x;
    sl = x > sl ? sa * sl + (1 - sa) * x : rel * sl + (1 - rel) * x;
    const g = Math.min(gmax, Math.max(1, f / (sl + 1e-9)));
    L[i] *= g; R[i] *= g;
  }
}
/** 軽いクリップ: 楽器のいちばん大きい山から clipDb 下を境に、それより上を tanh でなめらかに丸める */
function softClip(bufs, peak, clipDb) {
  const t = peak * Math.pow(10, -clipDb / 20), room = peak - t;
  for (const b of bufs) for (let i = 0; i < b.length; i++) {
    const v = Math.abs(b[i]);
    if (v > t) b[i] = Math.sign(b[i]) * (t + room * Math.tanh((v - t) / room));
  }
}

async function build(name, prof) {
  // 設定ごとの楽器の上書き（inst: { 楽器: { keys・close・vel など } }）。keys が空の楽器は作らない
  const cfgOf = (inst) => ({ ...KIT[inst], ...(prof.inst?.[inst] ?? {}) });
  // 1. 全部の音をまぜて作り、全体の大きさ（山）をそろえる
  const made = [];
  let peak = 0;
  for (const inst of Object.keys(KIT)) {
    const cfg = cfgOf(inst);
    if (!cfg.keys.length) continue;
    // 調整用: DRUM_ONLY=Kick,Snare なら、その楽器だけ作る（音源は書き出さず、DRUM_DUMP のフォルダに1打ずつ WAV を置く）
    if (process.env.DRUM_ONLY && !process.env.DRUM_ONLY.split(",").includes(inst)) continue;
    const ls = layers(inst, cfg);
    // 重ね（prof.stack: { 楽器: { inst: 重ねる楽器, gain } }）: 同じ強さの範囲の層を選んで、近接マイクだけの録音を足す
    const st = prof.stack?.[inst];
    const sls = st ? layers(st.inst, cfgOf(st.inst)) : [];
    let ipeak = 0;
    const mine = [];
    for (const [k, l] of ls.entries()) {
      let c = cfg;
      if (st) {
        const mid = (l.lo + l.hi) / 2;
        const cand = sls.filter((x) => x.lo <= mid + 4 && x.hi >= mid - 4);
        const sl = cand[k % Math.max(1, cand.length)] ?? sls.reduce((b, x) => (Math.abs((x.lo + x.hi) / 2 - mid) < Math.abs((b.lo + b.hi) / 2 - mid) ? x : b));
        const scfg = { ...cfgOf(st.inst), sec: cfg.sec, close: Object.fromEntries(Object.entries(cfgOf(st.inst).close).map(([m, g]) => [m, g * st.gain])) };
        const [a, b] = hit(st.inst, sl.idx, scfg, { ...prof, overhead: 0, ohKind: null, amb: 0, ohc: 0, eq: "", kindEq: null, snareEq: "", instEq: null, attack: null });
        c = { ...cfg, stackWith: [a, b] };
      }
      const [L, R] = hit(inst, l.idx, c, prof);
      for (const b of [L, R]) for (const v of b) ipeak = Math.max(ipeak, Math.abs(v));
      mine.push({ inst, cfg, ...l, L, R });
    }
    const clip = prof.clip?.[kindOf(inst)];
    if (clip) { softClip(mine.flatMap((m) => [m.L, m.R]), ipeak, clip); ipeak = 0; for (const m of mine) for (const b of [m.L, m.R]) for (const v of b) ipeak = Math.max(ipeak, Math.abs(v)); }
    // gain: 種類ごとの音量（dB）。音作りで変わった大きさの釣り合い（キックとスネアなど）を、書き出した曲を測って戻す
    const gdb = prof.gain?.[inst] ?? prof.gain?.[kindOf(inst)];
    if (gdb) { const g = Math.pow(10, gdb / 20); for (const m of mine) for (const b of [m.L, m.R]) for (let i = 0; i < b.length; i++) b[i] *= g; ipeak *= g; }
    peak = Math.max(peak, ipeak);
    made.push(...mine);
    console.log(inst, "層:", ls.length, st ? `（${st.inst} を重ねる）` : "");
  }
  const gain = 0.95 / peak;
  for (const m of made) for (const b of [m.L, m.R]) for (let i = 0; i < b.length; i++) b[i] *= gain;
  if (process.env.DRUM_DUMP) {
    const dir = path.join(process.env.DRUM_DUMP, name);
    fs.mkdirSync(dir, { recursive: true });
    for (const m of made) {
      const n = m.L.length, buf = Buffer.alloc(44 + n * 8);
      buf.write("RIFF", 0); buf.writeUInt32LE(36 + n * 8, 4); buf.write("WAVEfmt ", 8); buf.writeUInt32LE(16, 16); buf.writeUInt16LE(3, 20); buf.writeUInt16LE(2, 22);
      buf.writeUInt32LE(SR, 24); buf.writeUInt32LE(SR * 8, 28); buf.writeUInt16LE(8, 32); buf.writeUInt16LE(32, 34); buf.write("data", 36); buf.writeUInt32LE(n * 8, 40);
      for (let i = 0; i < n; i++) { buf.writeFloatLE(m.L[i], 44 + i * 8); buf.writeFloatLE(m.R[i], 48 + i * 8); }
      fs.writeFileSync(path.join(dir, `${m.inst}-${m.lo}-${m.hi}.wav`), buf);
    }
    if (process.env.DRUM_ONLY) return;
  }

  // 2. 音源を組み立てる（GMのドラムセットの入れものを写し、鳴らすキーだけ入れかえる。ほかのキー（カウベルなど）は元のまま）
  const out = new BasicSoundBank();
  const base = prof.base ? loadBank(path.join(OUT, prof.base + ".sf3")) : gameBank;
  out.soundBankInfo = { ...gameBank.soundBankInfo, name: KIT_ID === "crocell" ? `Drums ${prof.label} (DrumGizmo CrocellKit, CC BY 4.0)` : KIT_ID === "naked" ? `Drums ${prof.label} (Wilkinson Audio Naked Drums CC BY 4.0 / Karoryfer Frankensnare CC0)` : `Drums Muldjord Kit ${prof.label} (CC BY 4.0)` };
  const mine = new Set(Object.keys(KIT).flatMap((k) => cfgOf(k).keys));
  const done = new Set();
  // 音のデータは1回だけ作り、4つのドラムセットで共有する
  for (const m of made) {
    [m.l, m.r] = stereoPair(`${m.inst} v${m.lo}`, m.L, m.R, m.cfg.keys[0]);
    out.addSamples(m.l, m.r);
  }
  for (const program of [0, 8, 16, 32]) {
    const src = base.presets.find((p) => p.isGMGSDrum && p.program === program);
    if (!src) continue;
    const preset = out.clonePreset(src);
    for (const pz of preset.zones) {
      const inst = pz.instrument;
      if (done.has(inst)) continue;
      done.add(inst);
      for (let i = inst.zones.length - 1; i >= 0; i--) {
        const r = inst.zones[i].keyRange;
        if ([...mine].some((k) => k >= r.min && k <= r.max)) inst.deleteZone(i, true);
      }
      for (const m of made) {
        const { l, r } = m;
        for (const key of m.cfg.keys) {
          for (const smp of [l, r]) {
            const z = inst.createZone(smp);
            z.keyRange = { min: key, max: key };
            z.velRange = { min: m.lo, max: m.hi };
            z.setGenerator(GeneratorTypes.scaleTuning, 0);
            z.setGenerator(GeneratorTypes.pan, smp === l ? -500 : 500);
            // クラッシュは、叩いた直後に鍵盤を離しても余韻が鳴り続けるよう、離したあとの減り方を長くする（crashSec のある設定だけ）
            z.setGenerator(GeneratorTypes.releaseVolEnv, timecents(/^Crash/.test(m.inst) && prof.crashSec ? 12 : m.cfg.release ?? 0.3));
            if (m.cfg.exclusive) z.setGenerator(GeneratorTypes.exclusiveClass, m.cfg.exclusive);
            // 元の SFZ のタムの音程の補正（セント）
            if (m.cfg.tune) { z.setGenerator(GeneratorTypes.coarseTune, Math.trunc(m.cfg.tune / 100)); z.setGenerator(GeneratorTypes.fineTune, m.cfg.tune % 100); }
          }
        }
      }
    }
  }
  out.flush();
  await compressBank(out, Q);
  const buf = out.writeSF2({});
  const file = path.join(OUT, prof.out + ".sf3");
  fs.writeFileSync(file, Buffer.from(buf));
  console.log("書き出し:", file, (buf.byteLength / 1024 / 1024).toFixed(2) + "MB");

}
for (const name of which.length ? which : Object.keys(PROFILES).filter((n) => (PROFILES[n].kit ?? "muldjord") === KIT_ID)) await build(name, PROFILES[name]);
