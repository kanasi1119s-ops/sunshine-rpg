/**
 * パート別ミックスの設計（音量の目標・EQ・圧縮・残響の量）。
 * 作曲ソフトの曲を、パート（ドラム・ベース・ギター・鍵盤・弦…）ごとに別々に音にして、パートごとに音をととのえてから合わせるための表。
 * ここは計算とデータだけ（音を出す処理は tools/composer/render-node.mjs）。
 */

export type Group = "drums" | "drumKick" | "drumSnare" | "drumToms" | "drumCym" | "bass" | "gtrRhythm" | "gtrLead" | "gtrClean" | "keys" | "orch" | "pad" | "lead" | "ethnic" | "perc" | "ambience";
export const GROUPS: readonly Group[] = ["drums", "drumKick", "drumSnare", "drumToms", "drumCym", "bass", "gtrRhythm", "gtrLead", "gtrClean", "keys", "orch", "pad", "lead", "ethnic", "perc", "ambience"];

/** 楽器の音色（Instrument）→ パートの種類。 */
export function groupOf(instrument: string | undefined): Group {
  switch (instrument) {
    case "kick": case "snare": case "hihat": case "crash": case "tom":
      return "drums";
    case "bass": case "slap": case "sub808":
      return "bass";
    case "crunch": case "distGuitar":
      return "gtrRhythm";
    case "leadGuitar":
      return "gtrLead";
    case "guitar": case "echoGuitar":
      return "gtrClean";
    case "keys": case "piano": case "harpsichord": case "bell": case "chime":
      return "keys";
    case "strings": case "brass":
      return "orch";
    case "pad": case "choir":
      return "pad";
    case "lead":
      return "lead";
    case "sitar": case "koto": case "shamisen": case "banjo": case "harp": case "kalimba": case "panflute": case "shakuhachi": case "ocarina": case "fiddle": case "bagpipe":
      return "ethnic";
    case "cowbell":
      return "perc";
    case "wind": case "rain": case "stream": case "bird": case "crickets": case "sfxDown": case "sfxUp": case "impact": case "swoosh": case "pierce":
      return "ambience";
    default:
      return "lead";
  }
}

export interface Eq {
  /** 中心周波数（Hz）。 */
  f: number;
  /** 増減（dB）。 */
  g: number;
  /** 幅（Q）。 */
  q: number;
}
export interface Comp {
  /** しきい値（dBFS）。 */
  threshold: number;
  ratio: number;
  /** ミリ秒。 */
  attack: number;
  release: number;
}
export interface GroupMix {
  /** 音量の目標（dBFS。パートを鳴っている間だけ測ったRMS）。 */
  target: number;
  /** 低域をカットする周波数（Hz）。 */
  hp: number;
  /** 高域をカットする周波数（Hz）。 */
  lp: number;
  eq: Eq[];
  comp: Comp | null;
  /** 残響への送りの量（0〜1）。 */
  reverb: number;
  /** やまびこ（ディレイ）への送りの量（0〜1）と、間隔（拍に合わせるため、呼び出し側で決める）。 */
  delay: number;
  /** 飽和（歪み）を少し足す量（0〜1）。 */
  warmth: number;
  /** 左右の広がり（1が元のまま、1.3で広く、0で中央に寄せる）。 */
  width: number;
  /** ギターのアンプとキャビネット（クリーンのギターに、FFmpeg で歪みと箱鳴りをつける）。なければ null。 */
  amp?: AmpFx | null;
  /** 2回弾いて左右に置いたように聞かせる（片方を少し遅らせ、音色を少し変える）。 */
  double?: boolean;
  /**
   * 2つに分けて重ねる（ベースの定番）: きれいなまま低い音だけ（splitHz 以下）＋ 歪ませた中音（splitHz 以上）。
   * 歪ませる量（driveDb）、歪ませた音の高域の上限（lp）、重ねる大きさ（mixDb）。
   */
  parallel?: { splitHz: number; driveDb: number; lp: number; mixDb: number } | null;
}

/**
 * アンプとキャビネットの設定（FFmpeg のフィルターで作る。実在の機材のまねではない）。
 * 流れ: 低域を締める → 中域を押し出す（歪みの前） → 増幅して2段で丸く歪ませる（折り返しノイズを減らすため4倍で処理）
 *   → トーン（低・中・高） → スピーカーの箱（4発の箱のような低域の山・中低域のくぼみ・5kHzから上を急に落とす）
 */
export interface AmpFx {
  /** 歪ませる前に、低い音を切る（Hz。大きいほど締まった歪み）。 */
  tightHz: number;
  /** 歪ませる前に押し出す中域（Hz）と量（dB）。 */
  pushHz: number;
  pushDb: number;
  /** 増幅の量（dB。大きいほど強く歪む）。 */
  driveDb: number;
  /** 歪みの段数（1〜2）。 */
  stages: number;
  bassDb: number;
  midHz: number;
  midDb: number;
  /** 張り（2.5〜3.5kHz）の増減（dB）。 */
  presenceDb: number;
  /** 箱の高域の落ち始め（Hz）。 */
  cabHz: number;
  /** 弾いていない間の雑音を消す（激しく歪ませるときだけ）。 */
  gate?: boolean;
}

/** 曲調ごとのアンプ（リズムギター）。 */
const AMP_BY_STYLE: Record<string, AmpFx> = {
  metal:      { tightHz: 130, pushHz: 800, pushDb: 6, driveDb: 20, stages: 2, bassDb: 3, midHz: 650, midDb: -5, presenceDb: 3, cabHz: 5200, gate: true },
  deathmetal: { tightHz: 140, pushHz: 850, pushDb: 7, driveDb: 23, stages: 2, bassDb: 3, midHz: 600, midDb: -6, presenceDb: 3, cabHz: 5000, gate: true },
  hardcore:   { tightHz: 130, pushHz: 900, pushDb: 6, driveDb: 20, stages: 2, bassDb: 2, midHz: 700, midDb: -4, presenceDb: 3, cabHz: 5200, gate: true },
  progmetal:  { tightHz: 125, pushHz: 800, pushDb: 5, driveDb: 18, stages: 2, bassDb: 2, midHz: 700, midDb: -3, presenceDb: 2, cabHz: 5500, gate: true },
  rock:       { tightHz: 100, pushHz: 1000, pushDb: 4, driveDb: 15, stages: 2, bassDb: 1, midHz: 1000, midDb: 2, presenceDb: 2, cabHz: 5800 },
  dancerock:  { tightHz: 110, pushHz: 1200, pushDb: 3, driveDb: 10, stages: 1, bassDb: -1, midHz: 1200, midDb: 2, presenceDb: 2, cabHz: 6500 },
  jpop:       { tightHz: 110, pushHz: 1100, pushDb: 3, driveDb: 11, stages: 1, bassDb: 0, midHz: 1100, midDb: 2, presenceDb: 2, cabHz: 6200 },
};
/** ソロ・主旋律のギター（よくのびるように、中域を押し出して強めに歪ませる）。 */
const AMP_LEAD: AmpFx = { tightHz: 150, pushHz: 900, pushDb: 7, driveDb: 19, stages: 2, bassDb: -1, midHz: 1100, midDb: 3, presenceDb: 2, cabHz: 5600 };

const f2a = (n: number): string => (Math.round(n * 100) / 100).toString();
/** アンプとキャビネットの FFmpeg フィルター。id はフィルターの中の名前（パートごとに別にする）。 */
export function ampChain(a: AmpFx, id = "g"): string {
  const f: string[] = [];
  f.push(`highpass=f=${f2a(a.tightHz)}:p=2`);
  f.push(`equalizer=f=${f2a(a.pushHz)}:t=o:w=1.2:g=${f2a(a.pushDb)}`);
  const per = a.driveDb / a.stages;
  for (let i = 0; i < a.stages; i++) f.push(`volume=${f2a(per)}dB`, "asoftclip=type=tanh:oversample=4");
  // 弾いていない間の、歪みで持ち上がった雑音を消す（刻みの切れをよくする）
  if (a.gate) f.push("agate=threshold=0.012:ratio=4:attack=0.5:release=70:range=0.05");
  f.push(`volume=${f2a(-11)}dB`); // 歪ませると音が詰まって大きく聞こえるので、ほかのパートとの釣り合いに戻す
  f.push(`equalizer=f=110:t=o:w=1:g=${f2a(a.bassDb)}`);
  f.push(`equalizer=f=${f2a(a.midHz)}:t=o:w=1.4:g=${f2a(a.midDb)}`);
  f.push(`equalizer=f=3000:t=o:w=1:g=${f2a(a.presenceDb)}`);
  // スピーカーの箱: 低域の山（約110Hz）・中低域のくぼみ（約400Hz）・高域を急に落とす（4次）・耳ざわりな 7kHz 付近をさらに下げる
  f.push("highpass=f=75:p=2", "equalizer=f=110:t=q:w=1.4:g=2.5", "equalizer=f=400:t=q:w=1.2:g=-3");
  // 高域は落としすぎるとこもる。5〜6kHz の少し上から2段で落とし、ざらつきの出る 7kHz 付近は軽く下げるだけ
  f.push(`lowpass=f=${f2a(a.cabHz * 1.2)}:p=2`, `lowpass=f=${f2a(a.cabHz * 1.6)}:p=2`, "equalizer=f=7200:t=q:w=2:g=-3");
  // スピーカーのコーンの細かいクセ（山と谷）。平らなフィルターだけだと、電子的に聞こえるため
  f.push("equalizer=f=1600:t=q:w=2:g=1.5", "equalizer=f=2800:t=q:w=2:g=2", "equalizer=f=3400:t=q:w=3:g=-2", "equalizer=f=4300:t=q:w=2:g=1.5", "equalizer=f=6000:t=q:w=2:g=-3");
  // マイク2本を混ぜる: スピーカーの中心に向けた明るいマイク（7割）＋ 外側に向けた暗く太いマイク（4割）
  f.push(`asplit[${id}on][${id}off];[${id}on]equalizer=f=4000:t=o:w=1:g=2,volume=0.7[${id}on2];[${id}off]lowpass=f=3000:p=2,equalizer=f=250:t=o:w=1:g=1.5,volume=0.4[${id}off2];[${id}on2][${id}off2]amix=inputs=2:normalize=0`);
  return f.join(",");
}

const BASE: Record<Group, GroupMix> = {
  drums:     { target: -21, hp: 30,  lp: 17000, eq: [{ f: 320, g: -2.5, q: 1 }, { f: 5000, g: 2, q: 0.8 }], comp: { threshold: -22, ratio: 3, attack: 12, release: 120 }, reverb: 0.1, delay: 0, warmth: 0.1, width: 1 },
  bass:      { target: -22, hp: 35,  lp: 4500,  eq: [{ f: 90, g: 2, q: 1 }, { f: 300, g: -2, q: 1 }, { f: 1500, g: 1.5, q: 1 }], comp: { threshold: -24, ratio: 4, attack: 20, release: 160 }, reverb: 0, delay: 0, warmth: 0.25, width: 0.1 },
  gtrRhythm: { target: -24, hp: 85,  lp: 9000,  eq: [{ f: 250, g: -3, q: 1 }, { f: 2800, g: 2, q: 1 }], comp: { threshold: -22, ratio: 2.5, attack: 25, release: 140 }, reverb: 0.05, delay: 0, warmth: 0.2, width: 1.15 },
  gtrLead:   { target: -23, hp: 150, lp: 11000, eq: [{ f: 400, g: -2, q: 1 }, { f: 3200, g: 2, q: 1 }], comp: { threshold: -24, ratio: 3, attack: 15, release: 130 }, reverb: 0.2, delay: 0.14, warmth: 0.1, width: 1 },
  gtrClean:  { target: -26, hp: 110, lp: 11000, eq: [{ f: 300, g: -2, q: 1 }, { f: 4000, g: 1.5, q: 1 }], comp: { threshold: -26, ratio: 2, attack: 20, release: 140 }, reverb: 0.2, delay: 0.1, warmth: 0, width: 1.2 },
  keys:      { target: -26, hp: 100, lp: 12000, eq: [{ f: 350, g: -2, q: 1 }], comp: { threshold: -26, ratio: 2, attack: 25, release: 160 }, reverb: 0.2, delay: 0, warmth: 0, width: 1.1 },
  orch:      { target: -26, hp: 120, lp: 11000, eq: [{ f: 300, g: -2, q: 1 }, { f: 5500, g: 1, q: 0.8 }], comp: { threshold: -26, ratio: 2, attack: 30, release: 200 }, reverb: 0.4, delay: 0, warmth: 0, width: 1.3 },
  pad:       { target: -29, hp: 150, lp: 9000,  eq: [{ f: 300, g: -3, q: 1 }, { f: 5000, g: 1.5, q: 0.8 }], comp: null, reverb: 0.45, delay: 0, warmth: 0, width: 1.3 },
  lead:      { target: -23, hp: 200, lp: 12000, eq: [{ f: 400, g: -2, q: 1 }, { f: 3000, g: 1.5, q: 1 }], comp: { threshold: -25, ratio: 2.5, attack: 15, release: 120 }, reverb: 0.25, delay: 0.1, warmth: 0, width: 1 },
  ethnic:    { target: -26, hp: 150, lp: 12000, eq: [{ f: 350, g: -2, q: 1 }], comp: { threshold: -26, ratio: 2, attack: 15, release: 140 }, reverb: 0.25, delay: 0, warmth: 0, width: 1.1 },
  perc:      { target: -30, hp: 300, lp: 12000, eq: [], comp: null, reverb: 0.1, delay: 0, warmth: 0, width: 1 },
  ambience:  { target: -34, hp: 100, lp: 10000, eq: [], comp: null, reverb: 0.3, delay: 0, warmth: 0, width: 1.4 },
  // 本物のドラムの録音（sfz-player.mjs）を使うときは、キック・スネア・タム・シンバル（ハイハット含む）を別々にととのえる。
  // キック: 低い押し出し（60Hz）を足し、こもり（350Hz）を削り、ビーターの当たり（4kHz）を足す。速めに強く圧縮して粒をそろえる
  drumKick:  { target: -24, hp: 28,  lp: 12000, eq: [{ f: 60, g: 3, q: 1 }, { f: 350, g: -4, q: 1.2 }, { f: 4000, g: 3, q: 1 }], comp: { threshold: -20, ratio: 3, attack: 15, release: 120 }, reverb: 0.04, delay: 0, warmth: 0.1, width: 0 },
  // スネア: 胴鳴り（200Hz）を少し、箱っぽさ（500Hz）を削り、響き線の張り（5kHz）を足す。少し部屋の響きを
  drumSnare: { target: -25, hp: 80,  lp: 16000, eq: [{ f: 200, g: 2, q: 1 }, { f: 500, g: -2.5, q: 1.2 }, { f: 5000, g: 3, q: 0.9 }], comp: { threshold: -22, ratio: 2.5, attack: 20, release: 150 }, reverb: 0.18, delay: 0, warmth: 0.1, width: 0.6 },
  // タム: こもり（400Hz）を削り、当たり（4kHz）を少し
  drumToms:  { target: -28, hp: 60,  lp: 14000, eq: [{ f: 400, g: -3, q: 1 }, { f: 4000, g: 2, q: 1 }], comp: { threshold: -22, ratio: 2, attack: 25, release: 200 }, reverb: 0.15, delay: 0, warmth: 0, width: 1 },
  // シンバル・ハイハット: 低い音は切り（300Hz）、耳に刺さる 2.5kHz を少し削り、空気感（10kHz）を足す。圧縮はしない（余韻をつぶさない）
  drumCym:   { target: -30, hp: 300, lp: 18000, eq: [{ f: 2500, g: -2, q: 1 }, { f: 10000, g: 2, q: 0.7 }], comp: null, reverb: 0.1, delay: 0, warmth: 0, width: 1.1 },
};
const DRUM_PARTS: readonly Group[] = ["drumKick", "drumSnare", "drumToms", "drumCym"];

/** 曲調ごとの、パートの音量の補正（dB）。重い曲調ではギターとドラムを前に、静かな曲調ではやわらかく。 */
const STYLE_OFFSET: Partial<Record<string, Partial<Record<Group, number>>>> = {
  metal: { drums: 1, gtrRhythm: 2, bass: 0.5, keys: -2, pad: -2 },
  deathmetal: { drums: 1.5, gtrRhythm: 2.5, bass: 0.5, keys: -3, pad: -3 },
  hardcore: { drums: 1, gtrRhythm: 2, bass: 1, keys: -3, pad: -3 },
  progmetal: { drums: 0.5, gtrRhythm: 1.5, keys: 0.5 },
  rock: { gtrRhythm: 1, drums: 0.5 },
  dancerock: { drums: 1, bass: 1, gtrRhythm: 0.5 },
  electro: { drums: 1.5, bass: 1.5, pad: 1, gtrRhythm: -2 },
  phonk: { drums: 1, bass: 3, perc: 3, pad: -2 },
  cleandance: { drums: 1, bass: 1.5 },
  classic: { orch: 3, keys: 2, drums: -4, bass: -2 },
  baroque: { keys: 3, orch: 2 },
  jazz: { drums: -2, bass: 1, keys: 1 },
  epic: { orch: 3, drums: 1, pad: 1 },
  space: { pad: 4, ambience: 3 },
  nature: { ambience: 6 },
  cafe: { keys: 2, drums: -2 },
};

/** 曲調・味つけから、パートごとのミックス設計を作る。 */
export function mixPlan(style: string | undefined, flavors: readonly string[] = []): Record<Group, GroupMix> {
  const plan = {} as Record<Group, GroupMix>;
  for (const g of GROUPS) plan[g] = { ...BASE[g], eq: BASE[g].eq.map((e) => ({ ...e })), comp: BASE[g].comp ? { ...BASE[g].comp! } : null };
  const off = (style && STYLE_OFFSET[style]) || {};
  for (const g of GROUPS) plan[g].target += off[g] ?? (DRUM_PARTS.includes(g) ? off.drums ?? 0 : 0);
  // メタル系: キックはビーターの当たりをさらに、スネアは張りをさらに（速い刻みの中でも1打ずつ聞こえるように）
  if (style && ["metal", "deathmetal", "hardcore", "progmetal"].includes(style)) {
    plan.drumKick.eq = [{ f: 60, g: 2, q: 1 }, { f: 350, g: -5, q: 1.2 }, { f: 4500, g: 5, q: 1 }];
    plan.drumSnare.eq = [{ f: 220, g: 2, q: 1 }, { f: 500, g: -3, q: 1.2 }, { f: 5500, g: 4, q: 0.9 }];
  }
  // ジャズ・カフェ: 圧縮は軽く、響きを多めに（生の強弱を残す）
  if (style && ["jazz", "cafe"].includes(style)) {
    for (const g of DRUM_PARTS) if (plan[g].comp) plan[g].comp = { ...plan[g].comp!, ratio: 2 };
    plan.drumSnare.reverb = 0.25;
    plan.drumCym.reverb = 0.15;
  }
  // 味つけ: ラウド＝ギターを太く前に、オーケストラ＝弦とブラスを前に、和楽器＝和楽器を前に
  if (flavors.includes("loud")) {
    plan.gtrRhythm.target += 1.5;
    plan.gtrRhythm.warmth = Math.min(1, plan.gtrRhythm.warmth + 0.2);
    plan.drums.target += 1;
  }
  // ベース: 電子音楽以外は、本物のベースの録音を想定して「きれいな低音＋歪ませた中音」の2つに分けて重ね、少し前に出す（小さなスピーカーでも聞こえるように）
  const ELECTRONIC = ["electro", "phonk", "cleandance", "space", "nature", "mystery", "discord"];
  const HEAVY = ["metal", "deathmetal", "hardcore", "progmetal", "rock", "dancerock", "epic", "finale"];
  if (!style || !ELECTRONIC.includes(style)) {
    const heavy = !!style && HEAVY.includes(style);
    plan.bass.target += heavy ? 2.5 : 2;
    plan.bass.warmth = 0;
    plan.bass.lp = 6000;
    plan.bass.parallel = heavy ? { splitHz: 250, driveDb: 20, lp: 4500, mixDb: -3 } : { splitHz: 300, driveDb: 8, lp: 5000, mixDb: -9 };
    plan.bass.eq = [{ f: 80, g: 2, q: 1 }, { f: 300, g: -3, q: 1 }, { f: 900, g: heavy ? 3 : 2.5, q: 1 }, { f: 2200, g: heavy ? 2 : 1.5, q: 1 }];
  }
  // ギター: クリーンで鳴らした音に、曲調に合うアンプとキャビネットをかける。リズムギターは左右に2本あるように
  const amp = (style && AMP_BY_STYLE[style]) || AMP_BY_STYLE.rock;
  // 歪ませすぎると音がつぶれてにごるので、増幅は控えめ（2026-10-03 に耳で確かめて、メタル 30→20dB など約3分の2に）
  plan.gtrRhythm.amp = flavors.includes("loud") ? { ...amp, driveDb: amp.driveDb + 2 } : amp;
  plan.gtrRhythm.warmth = 0; // 歪みはアンプでかけるので、二重にしない
  plan.gtrRhythm.double = !flavors.includes("loud"); // ラウドは楽譜の段階で左右2本にしてある
  plan.gtrLead.amp = AMP_LEAD;
  // ギターの音の終わりが、ぷつっと切れて聞こえないよう、短い部屋の響きを少し（リズムギター 0.05→0.12）
  plan.gtrRhythm.reverb = Math.max(plan.gtrRhythm.reverb, 0.12);
  plan.gtrLead.warmth = 0;
  if (flavors.includes("orchestra")) {
    plan.orch.target += 3;
    plan.pad.target += 1;
  }
  if (flavors.includes("wagakki")) plan.ethnic.target += 4;
  return plan;
}

const f2 = (n: number): string => (Math.round(n * 100) / 100).toString();
const dbToLin = (db: number): number => Math.pow(10, db / 20);

/** 1パートぶんの FFmpeg フィルター（音をととのえる部分）。入力と出力のラベルは呼び出し側がつける。 */
export function dryChain(m: GroupMix, id = "g"): string {
  const f: string[] = [];
  if (m.amp) f.push(ampChain(m.amp, id));
  if (m.parallel) {
    const p = m.parallel;
    f.push(`asplit[${id}pc][${id}pd];[${id}pc]lowpass=f=${f2(p.splitHz)}:p=2[${id}pc2];[${id}pd]highpass=f=${f2(p.splitHz)}:p=2,volume=${f2(p.driveDb)}dB,asoftclip=type=tanh:oversample=4,volume=${f2(-p.driveDb * 0.8)}dB,lowpass=f=${f2(p.lp)},volume=${f2(p.mixDb)}dB[${id}pd2];[${id}pc2][${id}pd2]amix=inputs=2:normalize=0`);
  }
  if (m.double) {
    // 2回弾いたように: いったん真ん中にまとめ、右だけ 14ms 遅らせ、左右で音色を少し変える
    f.push("pan=stereo|c0=0.5*c0+0.5*c1|c1=0.5*c0+0.5*c1", "adelay=delays=0|14", "anequalizer=c0 f=2400 w=900 g=1.5 t=0|c1 f=1600 w=700 g=1.5 t=0");
  }
  f.push(`highpass=f=${f2(m.hp)}`);
  f.push(`lowpass=f=${f2(m.lp)}`);
  for (const e of m.eq) f.push(`equalizer=f=${f2(e.f)}:t=q:w=${f2(e.q)}:g=${f2(e.g)}`);
  if (m.warmth > 0) {
    // やわらかい飽和（真空管のような倍音）。入力を持ち上げて tanh で丸め、戻す
    const pre = 1 + m.warmth * 2.5;
    f.push(`volume=${f2(pre)}`, "asoftclip=type=tanh", `volume=${f2(1 / pre)}`);
  }
  if (m.comp) f.push(`acompressor=threshold=${f2(dbToLin(m.comp.threshold))}:ratio=${f2(m.comp.ratio)}:attack=${f2(m.comp.attack)}:release=${f2(m.comp.release)}:makeup=1`);
  if (m.width !== 1) f.push(`extrastereo=m=${f2(m.width)}:c=0`);
  return f.join(",");
}

/**
 * 音量の合わせ方: パートを鳴っている間だけ測ったRMS（dBFS）が目標になるような倍率（dB）。
 * 鳴っていない（ほぼ無音の）パートは null。ゲインは ±18dB に収める（極端な増幅でノイズを持ち上げない）。
 */
export function gainForTarget(measuredDb: number | null, targetDb: number): number | null {
  if (measuredDb === null || !Number.isFinite(measuredDb)) return null;
  return Math.max(-18, Math.min(18, targetDb - measuredDb));
}

/** 鳴っている間だけのRMS（dBFS）。無音の窓（-60dBFS未満）は数えない。鳴っていなければ null。 */
export function activeRmsDb(left: Float32Array, right: Float32Array, sampleRate: number, windowSec = 0.4): number | null {
  const win = Math.max(1, Math.floor(sampleRate * windowSec));
  let sum = 0;
  let count = 0;
  for (let i = 0; i + win <= left.length; i += win) {
    let s = 0;
    for (let j = i; j < i + win; j++) s += left[j] * left[j] + right[j] * right[j];
    const rms = Math.sqrt(s / (2 * win));
    if (rms > 0.001) {
      sum += s / (2 * win);
      count++;
    }
  }
  if (count === 0) return null;
  return 10 * Math.log10(sum / count);
}
