import { REST, type NoteEvent, type Score, type Track } from "./score";

/**
 * 区間のつなぎ目の演出（長尺の曲）。
 *  - サビ・間奏の頭にクラッシュシンバル（ラスサビは半分でももう1回）
 *  - Bメロ→サビの直前の1拍は、ドラム以外が一瞬だけ止まる（ストップタイム。サビの頭が際立つ）
 * 全パートの長さ（拍数）は変えない（曲がぴったりループできる）。
 */

const DRUMS = new Set(["kick", "snare", "hihat", "crash", "tom"]);
const EPS = 1e-9;

/** 時間（拍）の [start, start+len) を取り除き、そこに repl を入れる。取り除いた長さと同じだけ repl を入れること（長さは変わらない）。 */
export function overlay(notes: NoteEvent[], start: number, len: number, repl: NoteEvent[]): NoteEvent[] {
  const end = start + len;
  const out: NoteEvent[] = [];
  let pos = 0;
  let inserted = false;
  for (const ev of notes) {
    const a = pos;
    const b = pos + ev.durationBeats;
    pos = b;
    if (b <= start + EPS || a >= end - EPS) {
      if (a >= end - EPS && !inserted) {
        out.push(...repl);
        inserted = true;
      }
      out.push(ev);
      continue;
    }
    if (a < start - EPS) out.push({ ...ev, durationBeats: start - a });
    if (!inserted) {
      out.push(...repl);
      inserted = true;
    }
    if (b > end + EPS) out.push({ ...ev, durationBeats: b - end });
  }
  if (!inserted) out.push(...repl);
  return out;
}

const totalBeats = (t: Track): number => t.notes.reduce((s, n) => s + n.durationBeats, 0);

/** 曲の全体の拍数ぶんの休符だけのトラックを作る。 */
function silentTrack(total: number, template: Pick<Track, "waveform" | "instrument" | "volume">): Track {
  return { ...template, notes: [{ note: REST, durationBeats: total }] };
}

export interface TransitionOptions {
  /** ストップタイムの長さ（拍）。 */
  stopBeats?: number;
}

export function applyTransitions(score: Score, kinds: readonly string[], beats: number, opts: TransitionOptions = {}): { crashes: number[]; stops: number[] } {
  const hasDrums = score.tracks.some((t) => t.instrument === "kick" || t.instrument === "snare");
  const result = { crashes: [] as number[], stops: [] as number[] };
  if (!hasDrums) return result;
  const total = Math.max(...score.tracks.map(totalBeats));
  const stop = opts.stopBeats ?? 1;
  let crash = score.tracks.find((t) => t.instrument === "crash");
  if (!crash) {
    crash = silentTrack(total, { waveform: "sine", instrument: "crash", volume: 0.22 });
    score.tracks.push(crash);
  }
  // 各区間の開始位置（拍）
  const starts: number[] = [];
  let pos = 0;
  for (const k of kinds) {
    starts.push(pos);
    pos += (k === "intro" ? 4 : 8) * beats;
  }
  const lastChorus = kinds.lastIndexOf("chorus");
  const hit = (at: number, velocity: number): void => {
    if (at + beats > total + EPS) return;
    // 1拍ぶんをクラッシュ1発（長く鳴らす）と休符にする
    crash!.notes = overlay(crash!.notes, at, 1, [{ note: "C4", durationBeats: 1, velocity, gate: 3 }]);
    result.crashes.push(at);
  };
  kinds.forEach((kind, i) => {
    const at = starts[i];
    if (kind === "chorus" || kind === "solo") hit(at, i === lastChorus ? 1.25 : 1);
    if (i === lastChorus) hit(at + 4 * beats, 0.9); // ラスサビの半分で、もう一度
    // Bメロ → サビ／間奏: 直前の拍だけ、ドラム以外を止める
    if ((kind === "chorus" || kind === "solo") && kinds[i - 1] === "bridge" && at - stop >= 0) {
      for (const t of score.tracks) {
        if (t.instrument && DRUMS.has(t.instrument)) continue;
        t.notes = overlay(t.notes, at - stop, stop, [{ note: REST, durationBeats: stop }]);
      }
      result.stops.push(at - stop);
    }
  });
  return result;
}
