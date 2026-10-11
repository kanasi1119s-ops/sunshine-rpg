import type { AiSong } from "./ai-song";
import { SECTION_KINDS, type SectionKind } from "./arrangement";
import { midiToName } from "./compose";
import { REST, type NoteEvent, type Score, type Track } from "./score";

/**
 * feel "jpop" の自動伴奏と、曲全体の前処理（2026-10-11、jpop-clean-guitar-guide.md 提案7・9）。
 *   feel "jpop" … 「pop」の伴奏をもとに、ギターを jpopClean の8分アルペジオ（E3〜E5、浅い chorus と残響）に置き換え、ピアノをギターと反対側（右）にする。
 *                 曲に sections も scene もなければ sections:"auto" にし、layers の既定を「イントロ＝ギターと鍵盤だけ（ワンフレーズのフック）、
 *                 Aメロ＝ギターを休む、Bメロ＝ギターが入る、サビ＝全員」にする。drumGenre の既定は "jpop"。書いた値が優先。
 *   bare … 引き算のセクション。曲の bare に書いた種類のセクションで、自動の伴奏のベース・鍵盤・ギター・弦が小節の頭の音だけをのばす。
 *           手書きパートの bare（mute／hold）は part-expand.ts の expandBare が実行する。ここでは、書き方を {mode, kinds} にそろえる。
 */

interface Bar { root: number; intervals: number[] }

/** 8分音符8つのアルペジオ（和音の構成音の番号。n+2 番目までは1オクターブ上の根音・3度）。 */
const ARPEGGIO_ORDER = [0, 1, 2, 1, 2, 3, 2, 1];

/** 和音の構成音（E3=52 から上に1オクターブ以内）。 */
function chordTones(c: Bar): number[] {
  return c.intervals.map((iv) => 52 + ((c.root + iv) % 12));
}

function jpopGuitar(base: Track, bars: Bar[], beats: number): Track {
  const notes: NoteEvent[] = [];
  const steps = Math.max(1, Math.round(beats / 0.5));
  for (const c of bars) {
    const t = chordTones(c);
    const ext = [...t, t[0] + 12, (t[1] ?? t[0]) + 12];
    for (let i = 0; i < steps; i++) {
      const m = ext[ARPEGGIO_ORDER[i % ARPEGGIO_ORDER.length] % ext.length];
      notes.push({ note: midiToName(m), durationBeats: 0.5, velocity: i === 0 ? 100 : i % 2 === 0 ? 92 : 70 });
    }
    const rest = beats - steps * 0.5;
    if (rest > 1e-9) notes.push({ note: REST, durationBeats: rest });
  }
  return { ...base, volume: 0.17, pan: -0.4, amp: { type: "jpopClean" }, reverb: 0.3, chorus: 0.3, notes };
}

/** pop の自動伴奏を、J-POP の質感にする。bars は進行をくり返しまで広げた小節ごとのコード。 */
export function jpopFeelSong(pop: Score, bars: Bar[], beats: number): Score {
  return {
    ...pop,
    tracks: pop.tracks.map((t) => (t.instrument === "guitar" ? jpopGuitar(t, bars, beats) : t.instrument === "piano" ? { ...t, pan: 0.4 } : t)),
  };
}

/** feel "jpop" の layers の既定。 */
export const JPOP_LAYERS = {
  intro: { groups: ["guitar", "keys"], from: 0.8, to: 1 },
  verse: ["kick", "hat", "bass", "keys"],
} as const;
/** 引き算のセクションの layers（ベース・鍵盤・ギター・弦が、小節の頭の音だけをのばす）。 */
export const BARE_LAYER = { groups: ["bass", "keys", "guitar", "strings"], hold: true, from: 0.7, to: 0.75 } as const;

const kindsOf = (v: unknown): SectionKind[] => (Array.isArray(v) ? v.filter((k): k is SectionKind => SECTION_KINDS.includes(k as SectionKind)) : []);

/**
 * 曲のJSONの前処理。feel "jpop"・bare・sectionFx・guitarPair が sections を必要とするとき、sections が無ければ "auto" を補う。
 * どれも書いていない曲は、そのまま返す（今までの曲は変わらない）。
 */
export function applyJpopSong(song: AiSong, warnings: string[]): AiSong {
  if (!song || typeof song !== "object") return song;
  const parts = Array.isArray(song.parts) ? song.parts : [];
  const isJpop = song.feel === "jpop";
  const songBare = song.bare === true ? ["verse" as SectionKind] : kindsOf(song.bare);
  const partNeeds = parts.some((p) => p && (p.sectionFx || p.bare !== undefined || p.guitarPair));
  if (!isJpop && song.bare === undefined && !partNeeds) return song;
  let out: AiSong = { ...song };
  if (!out.sections && !out.scene && (partNeeds || songBare.length || (isJpop && out.autoAccompaniment))) {
    out.sections = "auto";
    if (partNeeds || songBare.length) warnings.push("bare / sectionFx / guitarPair を使うには sections（または scene）が必要です。sections: \"auto\" として扱いました");
  }
  const layers: Record<string, unknown> = { ...(isJpop && out.autoAccompaniment ? JPOP_LAYERS : {}), ...(out.layers ?? {}) };
  for (const k of songBare) if (!(out.layers && k in out.layers)) layers[k] = { ...BARE_LAYER, groups: [...BARE_LAYER.groups] };
  if (Object.keys(layers).length) out.layers = layers as AiSong["layers"];
  if (isJpop && !out.drumGenre) out.drumGenre = "jpop";
  // 手書きパートの bare を { mode, kinds } にそろえる（kinds は、パートに書いたもの → 曲の bare → Aメロ の順）
  if (parts.some((p) => p && p.bare !== undefined)) {
    out = {
      ...out,
      parts: parts.map((p) => {
        if (!p || p.bare === undefined) return p;
        const b = p.bare;
        const mode = typeof b === "string" ? b : b && typeof b === "object" ? b.mode : undefined;
        const own = b && typeof b === "object" ? kindsOf(b.kinds) : [];
        const kinds = own.length ? own : songBare.length ? songBare : ["verse" as SectionKind];
        return { ...p, bare: { mode: mode ?? "mute", kinds } };
      }),
    };
  }
  return out;
}
