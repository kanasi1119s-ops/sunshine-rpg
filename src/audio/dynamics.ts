// 曲の「人が弾いたような強弱」を自動でつける（dynamics: "natural"）。
// 曲全体の山と谷 × フレーズごとの息づかい × 拍の強弱 × ベロシティのわずかなばらつき。
// 乱数は固定の種から作るので、同じ曲は何度書き出しても同じ結果になる。
import type { Track } from "./score";

function rng(seed: number): () => number {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/** 曲全体の大きな起伏（0.5〜1）。出だしは小さく、7割あたりが頂点、終わりは静かに。 */
export function bigArc(pos: number, total: number): number {
  const x = total > 0 ? pos / total : 0;
  if (x < 0.7) return 0.62 + 0.38 * Math.sin((x / 0.7) * (Math.PI / 2));
  return 1 - 0.3 * Math.pow((x - 0.7) / 0.3, 2);
}

/** 4小節のフレーズごとの息づかい。始まりはやわらかく、3小節目で張って、終わりで少し引く（0.84〜1）。 */
export function phraseBreath(barInPhrase: number, barsPerPhrase = 4): number {
  const p = (barInPhrase + 0.5) / barsPerPhrase;
  return p < 0.7 ? 0.86 + 0.14 * (p / 0.7) : 1 - 0.16 * ((p - 0.7) / 0.3);
}

/** 拍の強弱。1拍目は強く、裏拍は少し弱く。 */
export function beatAccent(beatInBar: number, beats: number): number {
  const frac = beatInBar - Math.floor(beatInBar);
  if (frac > 1e-6) return 0.94;
  const b = Math.floor(beatInBar);
  if (b === 0) return 1.0;
  if (beats === 4 && b === 2) return 0.97;
  return 0.93;
}

export function applyNaturalDynamics(tracks: Track[], total: number, beats: number): Track[] {
  const barsPerPhrase = 4;
  return tracks.map((t, ti) => {
    const drum = t.instrument ? ["kick", "snare", "hihat", "hat", "tom", "crash", "ride", "clap", "perc"].some((d) => String(t.instrument).startsWith(d)) : false;
    const depth = drum ? 0.5 : 1;
    const rand = rng(1234 + ti * 97);
    let pos = 0;
    const notes = t.notes.map((n) => {
      const bar = Math.floor(pos / beats + 1e-9);
      const beatInBar = pos - bar * beats;
      let g = bigArc(pos, total) * phraseBreath(bar % barsPerPhrase, barsPerPhrase) * beatAccent(beatInBar, beats);
      g = 1 - (1 - g) * depth;
      if (!drum) g *= 1 + (rand() - 0.5) * 0.12;
      pos += n.durationBeats;
      // 自動の伴奏の音は、強さが MIDI の数字（70〜112）で入っている。0〜1の比（0.7〜1.12）に直してから強弱をかける
      const base = (n.velocity ?? 1) > 1.5 ? (n.velocity as number) / 100 : (n.velocity ?? 1);
      return { ...n, velocity: Math.max(0.05, base * g) };
    });
    return { ...t, notes };
  });
}
