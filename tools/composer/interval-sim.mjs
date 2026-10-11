// 旋律の音程列の類似点検（docs/sound/melody-craft-guide.md §8 の提案 P10。CLAUDE.md 1-1「既存作品のまねをしない」の補強）。
// novelty.mjs の輪郭（Parsons code：上がる・同じ・下がるだけ）は大まかなので、半音数の列（6音の窓）で細かく比べる。
// 窓が一致した割合が 20% を超えたら注意。リズム（隣の音との長さの比）も同じ位置で一致した窓が多ければ強い警告。
import { expand, barChords, melodyParts } from "../audio-check/score-lib.mjs";

/** 旋律の音の並び（{pitch, dur}）。旋律のパートがなければ空。 */
export function melodySeq(song) {
  const total = barChords(song).length * Number(song.beats);
  const mel = melodyParts(song, (p) => expand(p, total))[0];
  return mel ? mel.seq : [];
}

/** n 音の窓ごとの { iv: 半音数の列, rh: 長さの比の列 }。同じ音が並ぶだけ（変化なし）の窓は除く。 */
export function windows(seq, n = 6) {
  const out = [];
  for (let i = 0; i + n <= seq.length; i++) {
    const w = seq.slice(i, i + n);
    const iv = [], rh = [];
    for (let k = 1; k < n; k++) { iv.push(w[k].pitch - w[k - 1].pitch); rh.push(+(w[k].dur / w[k - 1].dur).toFixed(2)); }
    if (iv.every((x) => x === 0)) continue;
    out.push({ iv: iv.join(","), rh: rh.join(",") });
  }
  return out;
}

/**
 * 旋律 a が b と似ている度合い。
 *   rate … a の窓のうち b にも同じ音程列がある割合（0〜1）
 *   rhythmRate … そのうち、長さの比も同じだった割合（a の窓全体に対して）
 */
export function intervalSimilarity(a, b, n = 6) {
  const wa = windows(a, n), wb = windows(b, n);
  if (!wa.length || !wb.length) return { rate: 0, rhythmRate: 0, windows: wa.length };
  const setIv = new Set(wb.map((w) => w.iv));
  const setBoth = new Set(wb.map((w) => `${w.iv}|${w.rh}`));
  let hit = 0, both = 0;
  for (const w of wa) {
    if (setIv.has(w.iv)) hit++;
    if (setBoth.has(`${w.iv}|${w.rh}`)) both++;
  }
  return { rate: hit / wa.length, rhythmRate: both / wa.length, windows: wa.length };
}

/** 自分の曲と、直近の曲（loadRecentFull の結果 [{name, song}]）を比べて、注意の文を返す。 */
export function checkIntervalSimilarity(song, others, { threshold = 0.2, n = 6 } = {}) {
  const me = melodySeq(song);
  const warnings = [];
  const rows = [];
  for (const o of others) {
    const r = intervalSimilarity(me, melodySeq(o.song), n);
    rows.push({ name: o.name, ...r });
    if (r.rate > threshold) {
      const strong = r.rhythmRate > threshold;
      warnings.push(`${strong ? "【強い警告】" : ""}旋律の音程列（${n}音の窓）が「${o.name}」と${Math.round(r.rate * 100)}%一致${strong ? `し、リズムも同じ位置で${Math.round(r.rhythmRate * 100)}%一致` : ""}しています。使い回しや、既存曲に似ていないか確かめ、出だしの音程とリズムを変えてください。`);
    }
  }
  return { warnings, rows };
}
