// サウンドセット: 「この音で作る」を1つ選ぶだけで、アンプ・パートごとの音量の目安・ミックス・ドラムの設定・使う音源（ベース・ドラム・ギター）をまとめて切りかえる。
// 作り方: 参考にした録音や、人間が「いい」と言った曲を、tools/audio-check/analyze.py・analyze-rhythm.py で測り、その数値（帯域・音量比・左右）から決める。
// 録音の音そのものは取り込まない（数値だけ）。名前はバンド名ではなく、音の特徴にする（CLAUDE.md 1-1）。
import type { AmpSetting, Instrument, Score, Track } from "./score";

export interface PartMix {
  /** このパートの音量（0〜1）。曲の全パートの合計が 0.9 をこえないように、書き出しの前にそろえる（内部のリミッターでつぶれて割れるのを避ける）。 */
  volume?: number;
  amp?: AmpSetting;
  bright?: number;
  reverb?: number;
  chorus?: number;
  duck?: number;
  /** 左右の位置。同じ楽器が複数あるときは、元の左右の向きを保って、この大きさ（0〜1）に合わせる。 */
  panWidth?: number;
}
export interface SoundSet {
  id: string;
  label: string;
  /** どんな音か（人間向けの説明）。 */
  description: string;
  /** 元にした録音・曲のメモ（数値の出どころ）。音そのものは入っていない。 */
  source: string;
  /** 使う追加の音源（作曲ソフトの「ベース音源」「ドラム音源」「ギター音源」の id）。 */
  overlays: { bass: string; drums: string; guitar: string };
  tone?: Score["tone"];
  human?: number;
  /** 楽器ごとの設定。書いていない楽器の音量は 0.06 を上限にする。 */
  parts: Partial<Record<Instrument, PartMix>>;
  drumMix?: Score["drumMix"];
  /** 目安のテンポ（BPM）。自動では変えない。 */
  tempoHint?: [number, number];
  /** 打ち込みの型の例（16分の格子。ドラムのパートに書く）。 */
  drumPatterns?: Record<string, string>;
}

export const SOUND_SETS: Record<string, SoundSet> = {
  "punk-run": {
    id: "punk-run",
    label: "疾走パンク（2ビート・ギター前）",
    description: "歪みギターを左右に振って前に出し、ベースとキックは控えめ。ドラムは2ビート（キックが表・スネアが裏）。メロディは生ギターのクリーン。",
    source: "参考録音（人間から受け取った録音・画面収録）との帯域比べ＋見本曲 melodic-punk-run の調整（2026-10-11）。音は取り込んでいない",
    overlays: { bass: "pick", drums: "rock", guitar: "gretsch" },
    tone: "rock",
    human: 0.4,
    parts: {
      kick: { volume: 0.03 }, snare: { volume: 0.054 }, hihat: { volume: 0.034 }, crash: { volume: 0.04 }, tom: { volume: 0.033 },
      bass: { volume: 0.026, bright: 0.5, duck: 0.15 },
      distGuitar: { volume: 0.12, amp: { type: "punk" }, panWidth: 0.55 },
      crunch: { volume: 0.12, amp: { type: "punk" }, panWidth: 0.55 },
      leadGuitar: { volume: 0.09, amp: { type: "clean" }, reverb: 0.2 },
      echoGuitar: { volume: 0.06, amp: { type: "clean" }, reverb: 0.2, chorus: 0 },
    },
    drumMix: { hat: { level: 1.05, pan: -0.3, reverb: 0.05 }, snare: { level: 1.15, reverb: 0.15 }, tom: { spread: 0.6, reverb: 0.12, tune: -3 }, crash: { level: 1.0, pan: 0.3, reverb: 0.25 } },
    tempoHint: [160, 210],
    drumPatterns: {
      "2beat-kick": "x...x...x...x...", "2beat-kick-b": "x...x...x..xx...", "2beat-snare": "..x...x...x...x.", "2beat-hat": "x.X.x.X.x.X.x.X.",
      "halftime-kick": "x.......x.......", "halftime-snare": "........x.......",
    },
  },
  "clear-guitar-rock": {
    id: "clear-guitar-rock",
    label: "透明感ギターロック（生ギター・自然な余韻）",
    description: "生ギターの自然な減り方を聴かせる。ビブラートや sustain で無理に鳴りを作らない。アコースティックはナイロン弦。タムは低め、クラッシュは余韻長め。",
    source: "人間が「いい」と言った通し（band-pedal-arpeggio）の設定（2026-10-11）。音は取り込んでいない",
    overlays: { bass: "finger", drums: "supra", guitar: "gretsch" },
    tone: "rock",
    human: 0.45,
    parts: {
      kick: { volume: 0.09 }, snare: { volume: 0.065 }, hihat: { volume: 0.03 }, crash: { volume: 0.032 }, tom: { volume: 0.05 },
      bass: { volume: 0.095, bright: 0.2, duck: 0.2 },
      guitar: { volume: 0.2, amp: { type: "clean" }, chorus: 0, reverb: 0.15, panWidth: 0.5 },
      echoGuitar: { volume: 0.095, amp: { type: "clean" }, reverb: 0.2, chorus: 0, panWidth: 0.55 },
      leadGuitar: { volume: 0.09, amp: { type: "clean" }, reverb: 0.25 },
      bell: { volume: 0.05, reverb: 0.4 }, harp: { volume: 0.055, reverb: 0.4 }, strings: { volume: 0.06, reverb: 0.5 },
    },
    drumMix: { hat: { level: 0.62, pan: -0.35, reverb: 0.08 }, snare: { reverb: 0.2 }, tom: { spread: 0.7, reverb: 0.15, level: 0.9, tune: -4.5 }, crash: { level: 0.85, pan: 0.35, reverb: 0.25 } },
    tempoHint: [120, 160],
  },
};

export const SOUND_SET_IDS = Object.keys(SOUND_SETS);

/**
 * 曲にサウンドセットを当てはめる（元の曲は変えず、新しい曲を返す）。何度当てても同じ結果になる（音量は目標の値に置きかえる）。
 * 音量: セットに書かれた楽器は目標の音量に、書かれていない楽器は 0.06 を上限に。最後に、合計が 0.9 をこえたら全体を同じ比率で下げる。
 */
export function applySoundSet(score: Score, set: SoundSet): Score {
  const tracks: Track[] = score.tracks.map((t) => {
    const inst = t.instrument;
    const mix = inst ? set.parts[inst] : undefined;
    if (!mix) return { ...t, volume: Math.min(t.volume, 0.06) };
    const next: Track = { ...t, volume: mix.volume ?? t.volume };
    if (mix.amp) next.amp = { ...mix.amp };
    if (mix.bright !== undefined) next.bright = mix.bright;
    if (mix.reverb !== undefined) next.reverb = mix.reverb;
    if (mix.chorus !== undefined) next.chorus = mix.chorus;
    if (mix.duck !== undefined) next.duck = mix.duck;
    if (mix.panWidth !== undefined && t.pan !== undefined && t.pan !== 0) next.pan = Math.sign(t.pan) * mix.panWidth;
    return next;
  });
  const sum = tracks.reduce((a, t) => a + t.volume, 0);
  if (sum > 0.9) for (const t of tracks) t.volume = Math.round((t.volume * 0.9) / sum * 10000) / 10000;
  const out: Score = { ...score, tracks };
  if (set.tone) out.tone = set.tone;
  if (set.human !== undefined) out.human = set.human;
  if (set.drumMix) out.drumMix = { ...(score.drumMix ?? {}), ...set.drumMix };
  return out;
}
