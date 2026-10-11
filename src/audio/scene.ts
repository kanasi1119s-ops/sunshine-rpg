import { GROUPS, type CrashAt, type Group, type Layer, type LayerSpec, type Modulate, type Section, type SectionKind } from "./arrangement";

/**
 * 場面プリセット（scene）とエネルギー曲線（energy）。docs/sound/arrangement-deep.md §4.3・§6・§11。
 * 曲のJSONに "scene": "battle" と書くと、sections・feel・tone・dynamics・layers・crashAt・modulate などの既定値が入る。
 * 曲に自分で書いた値があれば、そちらが優先される（scene は「書かなかったところ」を埋める）。
 */
export type SceneName =
  | "town" | "village" | "field" | "battle" | "boss" | "finalBoss" | "castle" | "dungeon" | "shrine"
  | "mystery" | "sad" | "inn" | "fanfare" | "title" | "ending";

export interface ScenePreset {
  label: string;
  /** 目安のテンポ（範囲の外だと注意を出す）。 */
  bpm: [number, number];
  feel: "rock" | "pop" | "ballad" | "dance" | "vocaloid";
  tone: "rock" | "metal" | "prs";
  swing?: number;
  dynamics?: boolean | "natural";
  fills?: boolean;
  /** セクションの型。曲の長さにあわせて小節数を伸び縮みさせる（scaleSections）。 */
  sections: Section[];
  layers?: Partial<Record<SectionKind, LayerSpec>>;
  energy?: number[] | EnergyCurve;
  energyOrder?: Group[];
  crashAt?: CrashAt[];
  occurrence?: boolean;
  modulate?: Modulate;
  /** 編成と書き方のおすすめ（AI_SONG_GUIDE と文書用）。 */
  hint: string;
}

/** エネルギー曲線の型（arrangement-deep.md §4.3）。 */
export type EnergyCurve = "mountain" | "twoPeaks" | "valley" | "stairs" | "flat" | "bigValley";
export const ENERGY_CURVES: Record<EnergyCurve, number[]> = {
  mountain: [3, 5, 7, 9, 4],
  twoPeaks: [2, 5, 9, 3, 6, 10, 4],
  valley: [2, 4, 6, 9, 6, 4, 6, 9, 3, 10, 5],
  stairs: [6, 7, 8, 9, 10],
  flat: [4, 5, 4, 5, 4],
  bigValley: [7, 4, 1, 10],
};

const S = (kind: SectionKind, bars: number, extra: Partial<Section> = {}): Section => ({ kind, bars, ...extra });
/** 静かな場面で、ドラムを使わない・ほとんど使わないときの優先順（energy の群の並び）。 */
const SOFT_ORDER: Group[] = ["keys", "strings", "bass", "guitar", "hat", "kick", "snare"];
const flat = (groups: Group[], level: number, to = level): LayerSpec => ({ groups, from: level, to });

export const SCENES: Record<SceneName, ScenePreset> = {
  town: {
    label: "町", bpm: [80, 120], feel: "pop", tone: "rock", dynamics: false,
    sections: [S("verse", 8), S("interlude", 8), S("verse", 8), S("bridge", 8)],
    layers: { verse: flat(["hat", "bass", "keys", "guitar", "strings"], 0.85), interlude: flat(["bass", "keys", "guitar", "strings"], 0.85), bridge: flat(["bass", "keys", "strings"], 0.85) },
    crashAt: [], occurrence: true,
    hint: "ABAC・32小節。ハープ／ギター／笛（lead）／パッド＋軽い打楽器。強さは一定で、途中の急な盛り上げや尖った音は入れない。最後の小節は V か IV で終えて頭に戻す。",
  },
  village: {
    label: "村・のどかな場所", bpm: [62, 95], feel: "ballad", tone: "rock", dynamics: "natural",
    sections: [S("intro", 4), S("verse", 8), S("interlude", 8), S("verse", 8), S("outro", 4)],
    layers: { intro: flat(["keys", "guitar"], 0.8), verse: flat(["hat", "bass", "keys", "guitar", "strings"], 0.8), interlude: flat(["keys", "guitar", "strings"], 0.8), outro: flat(["keys", "guitar"], 0.8, 0.6) },
    crashAt: [], occurrence: true,
    hint: "guitar のアルペジオ・harp・笛・パッド・シェイカー。長調で、旋律→弦へ・対旋律→少し盛る。主音で解決してループ。",
  },
  field: {
    label: "フィールド・旅", bpm: [100, 140], feel: "pop", tone: "rock", dynamics: "natural",
    sections: [S("intro", 4), S("verse", 8), S("pre", 4), S("chorus", 8), S("interlude", 4), S("verse", 8), S("pre", 4), S("chorus", 8)],
    crashAt: ["chorus"], occurrence: true,
    hint: "strings・brass（遠く）・bass・軽いドラム。長調かミクソリディアン。サビで開けた旋律（音域を上げる）。ループ。",
  },
  battle: {
    label: "通常戦闘", bpm: [150, 190], feel: "rock", tone: "metal",
    sections: [S("verse", 8, { crash: true }), S("chorus", 8)],
    layers: { verse: { groups: ["kick", "hat", "snare", "bass", "keys", "guitar", "strings"], from: 0.92, to: 0.95 } },
    crashAt: ["chorus"], occurrence: true,
    hint: "前奏なし・16小節ループ。1拍目から全員。ドラム・distGuitar・strings のスタッカート・brass。短調で、最後の小節は頭へつなぐ。",
  },
  boss: {
    label: "ボス戦", bpm: [130, 170], feel: "rock", tone: "metal",
    sections: [S("intro", 2), S("chorus", 8), S("interlude", 4), S("chorus", 8), S("bridge", 4), S("pre", 4), S("chorus", 8, { from: "stopBeat" }), S("chorus", 8)],
    crashAt: ["chorus", "last"], occurrence: true, modulate: { at: "lastChorus", semitones: 2 },
    hint: "戦闘＋choir・低い strings・tom。3段（山を3回作る）。ブリッジのあと1拍止めてから最後のサビで全員、全音上げ。通常戦闘の動機を引用する。",
  },
  finalBoss: {
    label: "最終決戦", bpm: [150, 190], feel: "rock", tone: "metal",
    sections: [S("intro", 2), S("chorus", 8), S("chorus", 8), S("interlude", 4), S("chorus", 8), S("pre", 4, { from: "riser" }), S("drop", 8), S("drop", 8)],
    energy: [6, 7, 8, 6, 9, 7, 9, 10], crashAt: ["chorus", "drop", "last"], modulate: { at: "lastChorus", semitones: 1 },
    hint: "階段（6→10）。全部＋choir。戦闘とエンディングの主題を混ぜる。最後は半音上げで全員。",
  },
  castle: {
    label: "城・荘厳", bpm: [70, 100], feel: "ballad", tone: "rock", dynamics: "natural",
    sections: [S("intro", 4), S("verse", 8), S("pre", 4), S("chorus", 8), S("interlude", 4), S("verse", 8), S("chorus", 8), S("outro", 4)],
    energy: [4, 5, 6, 8, 5, 6, 8, 4], energyOrder: ["strings", "bass", "keys", "kick", "hat", "guitar", "snare"], crashAt: ["chorus"],
    hint: "strings・brass・choir・harpsichord・tom（ティンパニ）。行進風でゆっくり盛り上げる。荘厳に締める。",
  },
  dungeon: {
    label: "ダンジョン・洞窟", bpm: [50, 80], feel: "ballad", tone: "rock", dynamics: "natural", fills: false,
    sections: [S("intro", 4), S("verse", 8), S("interlude", 8), S("verse", 8), S("bridge", 8), S("outro", 4)],
    layers: { intro: flat(["strings"], 0.7), verse: flat(["bass", "keys", "strings"], 0.65, 0.75), interlude: flat(["keys", "strings"], 0.7), bridge: flat(["strings"], 0.65), outro: flat(["strings", "bass"], 0.7, 0.45) },
    crashAt: [],
    hint: "ドローン（pad・bass の長音）＋bell の点描。余白が主役で、長く聴いても形が変わらない。ドラムなし。始まりと同じ質感で終わる。",
  },
  shrine: {
    label: "神殿・塔・神秘", bpm: [55, 80], feel: "ballad", tone: "rock", dynamics: "natural", fills: false,
    sections: [S("intro", 4), S("verse", 8), S("interlude", 8), S("verse", 8), S("outro", 8)],
    layers: { intro: flat(["strings", "keys"], 0.7), verse: flat(["keys", "strings", "bass"], 0.75, 0.85), interlude: flat(["keys", "strings"], 0.8), outro: flat(["strings", "keys"], 0.8, 0.4) },
    crashAt: [],
    hint: "choir・harp・pad・bell・chime。リディアン。上昇・持続・きらめき。余韻で終わる。",
  },
  mystery: {
    label: "謎・陰謀", bpm: [70, 100], feel: "ballad", tone: "rock", dynamics: "natural", fills: false,
    sections: [S("intro", 4), S("verse", 8), S("bridge", 8), S("verse", 8), S("outro", 4)],
    layers: { intro: flat(["keys"], 0.7), verse: flat(["keys", "bass"], 0.7, 0.8), bridge: flat(["keys", "strings", "bass"], 0.75), outro: flat(["keys"], 0.7, 0.4) },
    crashAt: [],
    hint: "少ない音数・piano・pad。解決しない進行で戻る。控えめな緊張。",
  },
  sad: {
    label: "悲しい場面", bpm: [56, 76], feel: "ballad", tone: "rock", dynamics: "natural", fills: false,
    sections: [S("intro", 4), S("verse", 8), S("bridge", 8), S("verse", 8), S("outro", 4)],
    layers: { intro: flat(["keys"], 0.75), verse: flat(["keys", "bass", "strings"], 0.8, 0.9), bridge: flat(["keys", "strings"], 0.85, 0.95), outro: flat(["keys"], 0.8, 0.45) },
    crashAt: [],
    hint: "piano・strings・ソロ楽器。遅く、旋律と和声を前に。休符を多く。リズム楽器は抜く。長い音でほどく。",
  },
  inn: {
    label: "宿屋・店", bpm: [80, 110], feel: "pop", tone: "rock", dynamics: false,
    sections: [S("verse", 8), S("interlude", 8)],
    layers: { verse: flat(["bass", "keys", "guitar"], 0.8), interlude: flat(["keys", "guitar"], 0.8) },
    crashAt: [],
    hint: "piano・guitar・軽い鍵盤。8〜16小節の短いループで、強さは平ら。",
  },
  fanfare: {
    label: "勝利・ファンファーレ", bpm: [120, 160], feel: "pop", tone: "rock", fills: false,
    sections: [S("intro", 1), S("chorus", 4), S("outro", 2)],
    layers: { intro: { groups: ["bass", "keys", "strings"], from: 1, to: 1 }, outro: { groups: ["bass", "keys", "strings"], from: 0.9, to: 0.7 } },
    crashAt: ["chorus"],
    hint: "brass・strings・tom・bell。短く（4〜8小節）、いきなり山。最後は主音で止まる（ゲーム側でループさせない）。",
  },
  title: {
    label: "タイトル", bpm: [70, 110], feel: "pop", tone: "rock", dynamics: "natural",
    sections: [S("intro", 8), S("verse", 8), S("pre", 8), S("chorus", 16), S("interlude", 4), S("chorus", 16), S("outro", 4)],
    energy: [3, 4, 6, 9, 5, 9, 3], energyOrder: SOFT_ORDER, crashAt: ["chorus"],
    hint: "主題の全合奏、または strings＋piano。導入が長めで、ゆっくり盛り上がる（3→8）。余韻で終わる。",
  },
  ending: {
    label: "エンディング", bpm: [60, 90], feel: "ballad", tone: "rock", dynamics: "natural",
    sections: [S("intro", 8), S("verse", 8), S("pre", 8), S("chorus", 16), S("bridge", 8), S("chorus", 16), S("outro", 8)],
    energy: [2, 4, 7, 9, 2, 10, 2], energyOrder: SOFT_ORDER, crashAt: ["last"], modulate: { at: "lastChorus", semitones: 1 },
    hint: "回想→全合奏→静かに終わる（3→9→2）。piano・strings・harp・choir。主題が帰ってくる。最後はピアノ単独で終止。",
  },
};
export const SCENE_NAMES = Object.keys(SCENES) as SceneName[];

/** 型の小節数を、曲の小節数に合わせて伸ばす／縮める（なるべく4の倍数）。ぴったりなら型のまま。 */
export function scaleSections(template: Section[], totalBars: number): Section[] {
  const sum = template.reduce((a, s) => a + s.bars, 0);
  if (sum === totalBars) return template.map((s) => ({ ...s }));
  const unit = totalBars >= 24 ? 4 : totalBars >= 8 ? 2 : 1;
  const out = template.map((s) => ({ ...s, bars: Math.max(1, Math.round((s.bars * totalBars) / sum / unit) * unit) }));
  let diff = totalBars - out.reduce((a, s) => a + s.bars, 0);
  // 差は、いちばん長い場面から増減する（1以上を保つ）
  while (diff !== 0) {
    let k = 0;
    out.forEach((s, i) => { if (s.bars > out[k].bars) k = i; });
    const step = diff > 0 ? Math.min(diff, unit) : -Math.min(-diff, Math.max(0, out[k].bars - 1), unit);
    if (step === 0) {
      // どこも減らせない（曲が短すぎる）ときは、後ろの場面を捨てる
      out.pop();
      diff = totalBars - out.reduce((a, s) => a + s.bars, 0);
      if (!out.length) break;
      continue;
    }
    out[k].bars += step;
    diff -= step;
  }
  return out;
}

/** エネルギー（1〜10）を、セクションの数にあわせて取る。曲線の名前も使える。 */
export function resampleEnergy(energy: number[] | EnergyCurve, n: number): number[] {
  const src = Array.isArray(energy) ? energy : ENERGY_CURVES[energy] ?? ENERGY_CURVES.mountain;
  if (!src.length || n <= 0) return [];
  return Array.from({ length: n }, (_, i) => src[n === 1 ? 0 : Math.round((i * (src.length - 1)) / (n - 1))]);
}

/** エネルギー曲線から、セクションごとの群を決める。強さ1〜3＝2群、4〜6＝4群、7〜8＝6群、9〜10＝全群＋クラッシュ。 */
export function energyLayers(levels: number[], order: Group[] = ["kick", "bass", "hat", "keys", "snare", "guitar", "strings"]): Layer[] {
  const gainOf = (l: number): number => 0.55 + 0.045 * l;
  return levels.map((raw, i) => {
    const l = Math.max(1, Math.min(10, Math.round(raw)));
    const n = l <= 3 ? 2 : l <= 6 ? 4 : l <= 8 ? 6 : order.length;
    const next = levels[i + 1] !== undefined ? Math.max(1, Math.min(10, Math.round(levels[i + 1]))) : l;
    const from = gainOf(l);
    const to = next > l ? (gainOf(l) + gainOf(next)) / 2 : from;
    return { groups: order.slice(0, n), from, to, ...(l >= 9 ? { crash: true } : {}) };
  });
}

/** 曲のJSONのうち、scene が埋める項目。 */
export interface SceneFields {
  scene?: string;
  bpm?: number;
  feel?: string; tone?: string; swing?: number; dynamics?: boolean | "natural"; fills?: boolean;
  layers?: unknown; energy?: unknown; energyOrder?: unknown; crashAt?: unknown; occurrence?: boolean; modulate?: unknown;
}

/** scene の既定値を、曲に書いていない項目に入れる。sections は曲の長さが決まってから sceneSections で入れる。 */
export function applyScene<T extends SceneFields>(song: T, warnings: string[]): T {
  if (song.scene === undefined) return song;
  const preset = SCENES[song.scene as SceneName];
  if (!preset) {
    warnings.push(`scene「${String(song.scene)}」は使えません（${SCENE_NAMES.join("・")}）。無視しました`);
    return song;
  }
  const bpm = Number(song.bpm);
  if (Number.isFinite(bpm) && (bpm < preset.bpm[0] || bpm > preset.bpm[1])) {
    warnings.push(`scene「${song.scene}」（${preset.label}）の bpm は ${preset.bpm[0]}〜${preset.bpm[1]} が目安です（今 ${bpm}）`);
  }
  const fill: Record<string, unknown> = {};
  for (const k of ["feel", "tone", "swing", "dynamics", "fills", "layers", "energy", "energyOrder", "crashAt", "occurrence", "modulate"] as const) {
    if ((song as Record<string, unknown>)[k] === undefined && preset[k] !== undefined) fill[k] = preset[k];
  }
  return { ...song, ...fill };
}

/** scene の型から、曲の長さに合わせたセクションを作る。 */
export function sceneSections(scene: string | undefined, totalBars: number): Section[] | undefined {
  const preset = scene ? SCENES[scene as SceneName] : undefined;
  return preset ? scaleSections(preset.sections, totalBars) : undefined;
}

/** energy の生の値と energyOrder の生の値を確かめる。 */
export function parseEnergy(raw: unknown, rawOrder: unknown, sectionCount: number, warnings: string[]): Layer[] | undefined {
  if (raw === undefined || raw === null || !sectionCount) return undefined;
  let levels: number[] | EnergyCurve;
  if (typeof raw === "string") {
    if (!(raw in ENERGY_CURVES)) { warnings.push(`energy「${raw}」は使えません（${Object.keys(ENERGY_CURVES).join("・")}、または 1〜10 の数字の並び）。無視しました`); return undefined; }
    levels = raw as EnergyCurve;
  } else if (Array.isArray(raw) && raw.length && raw.every((x) => Number.isFinite(Number(x)))) {
    levels = raw.map(Number);
    if (levels.length !== sectionCount) warnings.push(`energy の数（${levels.length}）がセクションの数（${sectionCount}）とちがうので、近い位置にあわせました`);
  } else { warnings.push("energy は曲線の名前か、セクション順の 1〜10 の数字の並びで書いてください。無視しました"); return undefined; }
  let order: Group[] | undefined;
  if (Array.isArray(rawOrder)) {
    const ok = rawOrder.filter((g): g is Group => GROUPS.includes(g as Group));
    if (ok.length) order = ok;
    if (ok.length !== rawOrder.length) warnings.push("energyOrder に使えない群があったので無視しました");
  }
  return energyLayers(resampleEnergy(levels, sectionCount), order);
}

