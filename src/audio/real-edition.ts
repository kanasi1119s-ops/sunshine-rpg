import type { Instrument, Score, Track } from "./score";

/**
 * 実楽器版（別編成）: 電子的な音色を、実際のバンド・オーケストラ・楽器の音に近い音色に置き換える。
 * - リード: ロック・メタル=オーバードライブのギター、ジャズ・カフェ・R&B=サックス、クラシック・バロック=オーボエ、
 *   フォーク・サンバ・自然=フルート、オーケストラ風=トランペット、ミステリー=ビブラフォン、空間系=合唱、J-POP=エレキギター
 * - ベース: ロック・メタル系はピック弾き、ジャズ・クラシックなどはウッドベース、そのほかは指弾き
 * - パッド: 弦楽合奏または合唱
 * - クラシック・バロック・オーケストラ風・特別曲は、主旋律をバイオリン（または弦）が、ベースをチェロが重ねる
 * - 演奏のゆらぎを大きめに（`midi-export.ts`）、残響は自然なホール（`audio-engine.ts`）
 * 電子音楽（エレクトリック・フォンク）は、電子楽器が実際の音なので、電子的な音色のままにする。
 * 元の曲は変えず、新しい曲データとして返す。
 */
const LEAD: Record<string, number> = {
  rock: 29, metal: 29, hardcore: 29, deathmetal: 29, progmetal: 29, finale: 29, jpop: 27, cafe: 65, rnb: 65, jazz: 65,
  samba: 73, folk: 73, nature: 73, classic: 68, baroque: 68, epic: 56, mystery: 11, space: 52, discord: 9,
};
const BASS_PICK = ["rock", "metal", "hardcore", "deathmetal", "progmetal", "finale", "jpop", "epic"];
const BASS_WOOD = ["jazz", "cafe", "classic", "baroque", "folk", "nature"];
const PAD_CHOIR = ["space", "nature", "mystery", "metal", "hardcore", "deathmetal", "progmetal", "finale"];
const ORCHESTRAL = ["classic", "baroque", "epic", "finale"];
const ELECTRONIC = ["electro", "phonk"];

export function realEdition(score: Score): Score {
  const style = score.style ?? "rock";
  const electronic = ELECTRONIC.includes(style);
  const tracks: Track[] = score.tracks.map((t) => {
    const inst: Instrument | undefined = t.instrument;
    const next: Track = { ...t, notes: t.notes.map((n) => ({ ...n })) };
    if (electronic || !inst) {
      return next;
    }
    if (inst === "lead" && LEAD[style] !== undefined) next.program = LEAD[style];
    if (inst === "bass") next.program = BASS_PICK.includes(style) ? 34 : BASS_WOOD.includes(style) ? 32 : 33;
    if (inst === "pad") next.program = PAD_CHOIR.includes(style) ? 52 : 48;
    if (inst === "guitar" && style === "folk") next.program = 24;
    return next;
  });
  if (ORCHESTRAL.includes(style)) {
    for (const t of score.tracks) {
      const inst = t.instrument;
      if (!inst || t.notes.every((n) => n.note === "R")) continue;
      const melodic = inst === "lead" || inst === "leadGuitar" || inst === "brass" || inst === "harpsichord";
      if (melodic) {
        tracks.push({ ...t, instrument: "strings", waveform: "sawtooth", volume: t.volume * 0.5, pan: 0, program: style === "classic" || style === "baroque" ? 40 : 48, gm: undefined, gmDrum: undefined, notes: t.notes.map((n) => ({ ...n })) });
      } else if (inst === "bass") {
        tracks.push({ ...t, instrument: "strings", waveform: "sawtooth", volume: t.volume * 0.4, pan: 0, program: 42, gm: undefined, gmDrum: undefined, notes: t.notes.map((n) => ({ ...n })) });
      }
    }
  }
  return { ...score, tracks, edition: "real" };
}
