// 使い方: node tools/audio-check/check-drums.mjs <曲.json|文書.md> [...]
// ドラムの打ち込み（16分の格子 g:）の点検（docs/sound/drum-genre-guide.md §7 の 8）。
//   エラー（終了コード1）: 格子の文字数が4の倍数でない（1拍＝4文字。15文字などは、そのあとの音が16分ずれる）／パートの格子の合計が小節の長さ（beats×4。4拍子は16）の倍数でない。
//   4・8・12文字の短い格子（フィルなど）は、合計が小節にそろうならよい。
//   注意: スネアがバックビート（2・4拍）以外にふつうの強さで出ている／ハイハットやキックが全部同じ強さのベタ打ち／同じ小節が8回以上続く。
// .md を渡すと、文書に書かれた g: の文字数だけを調べる（ワルツ・フィル・12文字などと書いた行は、わざとなので飛ばす）。
import fs from "fs";

const DRUM = new Set(["kick", "snare", "hihat", "crash", "tom"]);
let errors = 0;
const say = (file, level, msg) => { console.log(`${level === "error" ? "×" : "△"} ${file}: ${msg}`); if (level === "error") errors++; };

function checkMarkdown(file, text) {
  text.split("\n").forEach((line, i) => {
    if (/ワルツ|フィル|12文字|拍分|略記|断片/.test(line)) return;
    for (const m of line.matchAll(/g:([xXoO.\-]+)/g)) {
      if (m[1].length % 4 !== 0) say(file, "error", `${i + 1}行目: g:${m[1]} は ${m[1].length} 文字です（1拍＝4文字の倍数にしてください。1小節は16文字）`);
      else if (m[1].length % 16 !== 0) say(file, "warn", `${i + 1}行目: g:${m[1]} は ${m[1].length} 文字です（1小節ぶんの型なら16文字。フィルなどの断片ならそのままでよい）`);
    }
  });
}

function checkSong(file, song) {
  const cells = Math.round((Number(song.beats) || 4) * 4);
  for (const [pi, p] of (song.parts ?? []).entries()) {
    if (!DRUM.has(p.instrument)) continue;
    const label = `parts[${pi}]（${p.role ?? p.instrument}）`;
    const tokens = String(p.notes ?? "").trim().split(/\s+/).filter((t) => /^g:/i.test(t));
    const bars = [];
    let total = 0;
    for (const t of String(p.notes ?? "").trim().split(/\s+/).filter(Boolean)) {
      // 三連グリッド t:（1文字＝三連の1つ、3文字で1拍＝4マス）
      if (/^t:/i.test(t)) {
        const n = t.length - 2;
        if (n % 3 !== 0) say(file, "error", `${label}: ${t} は ${n} 文字です（三連は3文字で1拍。4/4の1小節は12文字）`);
        total += (n / 3) * 4;
        continue;
      }
      if (!/^g:/i.test(t)) { total += (Number(/:([\d.]+)/.exec(t)?.[1] ?? 1)) * 4; continue; }
      const g = t.slice(2);
      total += g.length;
      if (g.length % 4 !== 0) say(file, "error", `${label}: ${t} は ${g.length} 文字です（1拍＝4文字の倍数にしてください。1小節＝${cells}文字）`);
      else if (g.length % cells === 0) for (let i = 0; i < g.length; i += cells) bars.push(g.slice(i, i + cells));
    }
    if (tokens.length && Math.abs(total % cells) > 1e-6 && Math.abs((total % cells) - cells) > 1e-6) say(file, "error", `${label}: 格子と音符の合計が ${total} マスで、小節（${cells}マス）の倍数になりません。そのあとの小節がずれます`);
    if (!bars.length) continue;
    if (p.instrument === "snare" && cells === 16) {
      const off = bars.filter((b) => [...b].some((c, i) => /[xX]/.test(c) && i !== 4 && i !== 12));
      if (off.length) say(file, "warn", `${label}: スネアがバックビート（2・4拍）以外にふつうの強さで鳴る小節が ${off.length} 小節あります（ゴーストは o で弱く。わざとなら無視）`);
    }
    if (p.instrument === "hihat" || p.instrument === "kick") {
      const flat = bars.filter((b) => /^x+$/.test(b));
      if (flat.length === bars.length && bars.length > 0 && cells === 16 && (p.instrument === "hihat" || bars.every((b) => b.length === 16)))
        say(file, "warn", `${label}: 全部 x のベタ打ちです。X（強く）と o（弱く）で強弱をつけると機械的に聞こえにくくなります`);
    }
    let run = 1, maxRun = 1;
    for (let i = 1; i < bars.length; i++) { run = bars[i] === bars[i - 1] ? run + 1 : 1; maxRun = Math.max(maxRun, run); }
    if (maxRun >= 8) say(file, "warn", `${label}: 同じ小節が ${maxRun} 回続きます。2〜4小節ごとに型を変えてください`);
  }
}

const files = process.argv.slice(2);
if (!files.length) { console.log("使い方: node tools/audio-check/check-drums.mjs <曲.json|文書.md> [...]"); process.exit(2); }
for (const f of files) {
  const text = fs.readFileSync(f, "utf8");
  if (/\.md$/i.test(f)) checkMarkdown(f, text);
  else { try { checkSong(f, JSON.parse(text)); } catch (e) { say(f, "error", `読めません: ${e.message}`); } }
}
if (!errors) console.log("○ 格子の文字数に問題はありません");
process.exitCode = errors ? 1 : 0;
