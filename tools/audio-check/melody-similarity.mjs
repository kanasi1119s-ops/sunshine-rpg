// 使い方: node tools/audio-check/melody-similarity.mjs <曲.json> [比べる曲.json ...] [--min 7] [--parsons-file 旋律集.txt]
// 旋律の類似を「音程列」で調べる（法務役の自動チェック。docs/sound/roles/legal.md）。
//   ・曲の旋律パート（role に「メロディ」「旋律」を含むもの）を、音程（半音）の並びに直す（移調しても同じになる）
//   ・曲どうしで、共通する音程列の最長の連続（音数）と、6音の組（n-gram）の一致数を出す
//   ・--parsons-file: 1行1旋律の Parsons code（U＝上がる・R＝同じ・D＝下がる）の旋律集と、Parsons code の最長一致を比べる
// 見つかっても「似ている」と決めるものではなく、見直す目安（--min 音以上の連続で警告）。見つからなくても「似ていない」を保証しない。
// 外部の既存曲との照合は、旋律を Parsons code にして Musipedia・Themefinder などで検索する（PARSONS=1 で score-check.mjs が出す）。
import fs from "fs";

const NAMES = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };
const midi = (n) => {
  const m = /^([A-G])([#b]?)(-?\d)$/.exec(n);
  return m ? 12 * (Number(m[3]) + 1) + NAMES[m[1]] + (m[2] === "#" ? 1 : m[2] === "b" ? -1 : 0) : null;
};

/** 旋律パートの音（休みを除く）を、順番どおりに [{pitch, dur}] にする。 */
export function melodyNotes(notesStr) {
  const out = [];
  for (const tok of notesStr.trim().split(/\s+/)) {
    const [n, d] = tok.split(":");
    const p = midi(n);
    if (p !== null && Number.isFinite(Number(d))) out.push({ pitch: p, dur: Number(d) });
  }
  return out;
}
export const intervals = (notes) => notes.slice(1).map((n, i) => n.pitch - notes[i].pitch);
export const parsons = (notes) => notes.slice(1).map((n, i) => (n.pitch > notes[i].pitch ? "U" : n.pitch < notes[i].pitch ? "D" : "R")).join("");

/** 2つの列の、共通する最長の連続（長さと、それぞれの開始位置）。 */
export function longestCommonRun(a, b) {
  let best = { len: 0, ia: 0, ib: 0 };
  const prev = new Array(b.length + 1).fill(0);
  for (let i = 1; i <= a.length; i++) {
    let diag = 0;
    for (let j = 1; j <= b.length; j++) {
      const tmp = prev[j];
      prev[j] = a[i - 1] === b[j - 1] ? diag + 1 : 0;
      if (prev[j] > best.len) best = { len: prev[j], ia: i - prev[j], ib: j - prev[j] };
      diag = tmp;
    }
  }
  return best;
}
export function ngrams(seq, n) {
  const s = new Set();
  for (let i = 0; i + n <= seq.length; i++) s.add(seq.slice(i, i + n).join(","));
  return s;
}

function loadMelodies(file) {
  const song = JSON.parse(fs.readFileSync(file, "utf8"));
  return (song.parts ?? [])
    .filter((p) => /メロディ|旋律/.test(p.role ?? "") && !/重ね|下で/.test(p.role ?? ""))
    .map((p) => ({ song: file, title: song.title, role: p.role, notes: melodyNotes(p.notes) }))
    .filter((m) => m.notes.length >= 4);
}

// コマンドとして実行されたときだけ動く（テストから関数だけ読めるように）
if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  const opt = (name, def) => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : def; };
  const minRun = Number(opt("--min", 7));
  const parsonsFile = opt("--parsons-file");
  const files = args.filter((a, i) => a.endsWith(".json") && args[i - 1] !== "--parsons-file");
  if (!files.length) {
    console.error("使い方: node tools/audio-check/melody-similarity.mjs <曲.json> [比べる曲.json ...] [--min 7] [--parsons-file 旋律集.txt]");
    process.exit(1);
  }
  const all = files.flatMap(loadMelodies);
  let flagged = 0;
  console.log(`旋律パート ${all.length}本（${files.length}曲）。音程列の最長の共通連続が ${minRun} 音程（${minRun + 1}音）以上なら警告。`);
  for (let i = 0; i < all.length; i++) {
    for (let j = i + 1; j < all.length; j++) {
      const a = all[i], b = all[j];
      if (a.song === b.song) continue; // 同じ曲の中の反復は、類似ではなく動機の再利用
      const ia = intervals(a.notes), ib = intervals(b.notes);
      const run = longestCommonRun(ia, ib);
      const shared = [...ngrams(ia, 6)].filter((g) => ngrams(ib, 6).has(g)).length;
      if (run.len >= minRun) {
        flagged++;
        console.log(`△ 「${a.title}」${a.role} と 「${b.title}」${b.role}: 共通する音程列が ${run.len} 音程（${run.len + 1}音）続く（${run.ia + 1}音目〜／${run.ib + 1}音目〜）。6音組の一致 ${shared}`);
      }
    }
  }
  if (parsonsFile) {
    const corpus = fs.readFileSync(parsonsFile, "utf8").split("\n").map((l) => l.trim()).filter((l) => /^[*URD]+$/.test(l));
    for (const m of all) {
      const code = parsons(m.notes);
      for (const [k, ref] of corpus.entries()) {
        const run = longestCommonRun([...code], [...ref]);
        if (run.len >= 12) {
          flagged++;
          console.log(`△ 「${m.title}」${m.role}: 旋律集の ${k + 1}行目と Parsons code が ${run.len} 続けて一致`);
        }
      }
    }
  }
  console.log(flagged ? `\n警告 ${flagged}件。該当箇所の旋律かリズムを作り直すか、意図した再利用なら理由を記録する。` : "\n警告なし（見つからなかったことは「似ていない」の保証ではない）。");
}
