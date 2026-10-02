import { noteNameToMidi } from "./note";
import { REST } from "./score";
import { parseNotes, type AiSong } from "./ai-song";

/**
 * AIソング形式の曲の、書いた直後の点検（学んだこと: `docs/sound/mixing-guide.md`・`music-knowledge.md`）。
 * 聴かなくても分かる「つぶれ・濁り・楽器の割り当て・ループ」の注意を、日本語の一覧で返す。警告は目安で、わざとなら直さなくてよい。
 * 楽理の詳しい点検は `tools/audio-check/score-check.mjs`、書き出しての測定は `qa-song.mjs`。
 */

/** 楽器ごとの音域（MIDI番号。作曲ソフトの手引きの音域）。 */
const RANGE: Record<string, [string, string]> = {
  bass: ["E1", "G3"], slap: ["E1", "G3"], sub808: ["C1", "C3"], guitar: ["E2", "E5"], crunch: ["E2", "E5"], distGuitar: ["E2", "E4"],
  leadGuitar: ["E3", "E6"], echoGuitar: ["E3", "E6"], keys: ["C2", "C6"], harpsichord: ["C2", "C6"], strings: ["C2", "C7"], pad: ["C2", "C6"],
  choir: ["C3", "C6"], brass: ["E2", "C6"], lead: ["C3", "C7"], bell: ["C4", "C7"], sitar: ["C3", "C6"], koto: ["C3", "C6"], shamisen: ["C3", "C6"],
  banjo: ["C3", "C6"], harp: ["C2", "C7"], kalimba: ["C4", "C7"], panflute: ["C4", "C7"], shakuhachi: ["C4", "C6"], ocarina: ["C4", "C7"],
  fiddle: ["G3", "E6"], bagpipe: ["A3", "A5"], piano: ["A0", "C8"],
};
const DRUMS = new Set(["kick", "snare", "hihat", "crash", "tom"]);
const DIST_GUITARS = new Set(["distGuitar"]);

export function lintAiSong(song: AiSong): string[] {
  const out: string[] = [];
  const parts = Array.isArray(song.parts) ? song.parts : [];

  // 1. 音域外
  for (const p of parts) {
    const r = RANGE[p.instrument];
    if (!r || DRUMS.has(p.instrument)) continue;
    const errors: string[] = [];
    const events = parseNotes(String(p.notes ?? ""), false, errors, "");
    const lo = noteNameToMidi(r[0]);
    const hi = noteNameToMidi(r[1]);
    const outside = events.filter((e) => e.note !== REST && (noteNameToMidi(e.note) < lo || noteNameToMidi(e.note) > hi)).length;
    if (outside) out.push(`音域外: ${p.instrument}（${p.role}）に ${outside}音（${r[0]}〜${r[1]}の外）。楽器の音域を確かめてください`);
  }

  // 2. 歪みギターの音量（つぶれの主因。実験: 2本を0.075→×0.3で PLR 7.4→9.7）
  const dist = parts.filter((p) => DIST_GUITARS.has(p.instrument));
  if (dist.some((p) => Number(p.volume) > 0.06)) {
    out.push("つぶれ注意: 歪みギター（distGuitar）の volume が 0.06 を超えています。つぶれ（PLR）と音量の主因になりやすいので、0.03〜0.05 まで下げて測ってください（qa-song.mjs / layer-report.mjs）");
  }

  // 3. 音量の合計
  const total = parts.reduce((s, p) => s + (Number(p.volume) || 0), 0);
  if (total > 1.6) out.push(`音量の合計が ${total.toFixed(2)} と大きめです（パート数が多い曲は目安 1.6 まで）。持続音の層（弦・パッド・合唱・歪みギター）を小さくするとつぶれにくくなります`);

  // 4. lead の音色（実楽器版では曲調で変わる）
  if (parts.some((p) => p.instrument === "lead") && song.synth !== true && (song.style === undefined || song.style === "rock" || song.style === "metal")) {
    out.push("音色の注意: lead は、実楽器版（書き出し・ゲーム）ではオーバードライブのギターで鳴ります（style が rock／省略のとき）。シンセにしたいなら synth: true、フルートなどの生楽器なら style（folk・jazz・classic など）を選んでください");
  }
  if (parts.some((p) => p.instrument === "bass") && song.synth !== true && (song.style === undefined || song.style === "rock")) {
    out.push("音色の注意: bass は、style が rock／省略のとき、ピック弾きのベースで鳴ります。フォーク・ジャズなどウッドベースにしたいなら style を選んでください");
  }

  // 5. ループ: 最初と最後のコードが違う
  const chords = String(song.chords ?? "").trim().split(/\s+/).filter(Boolean);
  if (chords.length >= 2 && chords[0] !== chords[chords.length - 1]) {
    out.push(`ループ: 最初のコード（${chords[0]}）と最後のコード（${chords[chords.length - 1]}）が違います。同じにすると、ループのつなぎ目の違和感が大きく減ります（意図的ならそのままで）`);
  }

  // 6. 起伏: 全パートが最初から鳴る
  const startsLoud = parts.length >= 4 && parts.every((p) => {
    const first = String(p.notes ?? "").trim().split(/\s+/)[0] ?? "";
    return !/^R:/i.test(first);
  });
  if (startsLoud) out.push("起伏: 全パートが1拍目から鳴ります。前奏は楽器を2〜3に減らし、小さく始めると起伏が出ます（R:拍数 で休ませる）");

  return out;
}
