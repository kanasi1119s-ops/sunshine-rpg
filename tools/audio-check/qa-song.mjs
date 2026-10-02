// 使い方: node tools/audio-check/qa-song.mjs assets-src/ai-songs/<曲ID>.json [--no-build]
// 曲の設計図（AIソング形式のJSON）を、聴かなくてもできる検査にまとめてかける（聴取係・ミキサーの自動検査）。
//   1. 楽理の点検（score-check.mjs）  2. 書き出し（song.mjs build --wav。--no-build なら既存のWAVを使う）
//   3. 音の測定（analyze.py）と目安との比較  4. ループの継ぎ目（両端の無音・端の値）
// 結果は dist-songs/<曲ID>.qa.md に、「自動検査レポート」と「人間への聴取依頼（そのまま送れる文）」として書き出す。
// 数値で言えることと、耳でないと分からないことを分けて書く。聴いた感想の代わりにはならない。
import { execFileSync } from "child_process";
import fs from "fs";
import path from "path";

const ROOT = path.resolve(new URL("../../", import.meta.url).pathname);
const [songFile, ...flags] = process.argv.slice(2);
if (!songFile) {
  console.error("使い方: node tools/audio-check/qa-song.mjs assets-src/ai-songs/<曲ID>.json [--no-build]");
  process.exit(1);
}
const id = path.basename(songFile).replace(/\.json$/i, "").toLowerCase().replace(/[^a-z0-9-]+/g, "-");
const out = path.join(ROOT, "dist-songs");
const wav = path.join(out, `${id}.wav`);
const run = (cmd, args, opt = {}) => execFileSync(cmd, args, { cwd: ROOT, encoding: "utf8", maxBuffer: 1 << 26, ...opt });
const song = JSON.parse(fs.readFileSync(songFile, "utf8"));

// 1. 楽理の点検
const score = run("node", ["tools/audio-check/score-check.mjs", songFile]);
const scoreWarn = score.split("\n").filter((l) => l.startsWith("△"));

// 2. 書き出し
if (!flags.includes("--no-build")) {
  // 書き出しは dist-composer を使う。エンジンのコードを変えたときは先に node tools/composer/build.mjs
  run("node", ["tools/composer/song.mjs", "build", songFile, "--out", out, "--wav"], { stdio: ["ignore", "pipe", "pipe"] });
}
if (!fs.existsSync(wav)) throw new Error(`WAVがありません: ${wav}`);

// 3. 測定
const measured = JSON.parse(run("python3", ["tools/audio-check/analyze.py", wav], { stdio: ["ignore", "pipe", "ignore"] }));
const m = Object.values(measured)[0];
const tmp = path.join(out, `${id}.measure.json`);
fs.writeFileSync(tmp, JSON.stringify(measured));
const compare = run("python3", ["tools/audio-check/analyze.py", "--compare", tmp]).trim();
fs.rmSync(tmp);

// 4. 継ぎ目と自動判定
const checks = [];
const check = (ok, okMsg, ngMsg) => checks.push(`${ok ? "○" : "△"} ${ok ? okMsg : ngMsg}`);
check(m.TP <= -0.8, `True Peak ${m.TP}dBTP（-1dBTP付近）`, `True Peak ${m.TP}dBTP が高い（-1dBTP以下に）`);
check(m.PLR >= 9, `PLR ${m.PLR}（9以上）`, `PLR ${m.PLR}（9未満＝つぶれ気味。編曲の密度を見直す）`);
check(m.corr >= 0.4 && m.corr <= 0.88, `左右の相関 ${m.corr}（0.4〜0.88）`, `左右の相関 ${m.corr}（0.4〜0.88の外。${m.corr > 0.88 ? "真ん中寄り" : "広すぎ・モノで消える恐れ"}）`);
check(m.LRA >= 2.3 && m.LRA <= 9, `LRA ${m.LRA}（起伏あり）`, `LRA ${m.LRA}（${m.LRA < 2.3 ? "起伏が少ない" : "起伏が大きい。静かな部分が小さすぎないか"}）`);
check(m.intro_vs_max_dB <= -2, `曲の頭は最大より ${m.intro_vs_max_dB}dB（小さく始まる）`, `曲の頭が最大に近い（${m.intro_vs_max_dB}dB）`);
check(m.centroid_Hz >= 300 && m.centroid_Hz <= 1100, `音の重心 ${m.centroid_Hz}Hz`, `音の重心 ${m.centroid_Hz}Hz（目安 300〜700Hz前後。ラウド系は高めになりやすい）`);
check(m.head_silence_ms <= 100 && m.tail_silence_ms <= 400, `両端の無音 先頭${m.head_silence_ms}ms／末尾${m.tail_silence_ms}ms`, `両端の無音が長い（先頭${m.head_silence_ms}ms／末尾${m.tail_silence_ms}ms）`);
check(m.edge_level_start <= 0.01 && m.edge_level_end <= 0.01, `端の値 先頭${m.edge_level_start}／末尾${m.edge_level_end}（クリックが出にくい）`, `端の値が大きい（先頭${m.edge_level_start}／末尾${m.edge_level_end}）。ループでぷつっと鳴る恐れ`);
check(m.dur_s >= 60, `長さ ${m.dur_s}秒（60秒以上）`, `長さ ${m.dur_s}秒（60〜120秒以上が目安。短いと飽きやすい）`);

const md = `# 自動検査レポート: ${song.title}（${id}）
作成: ${new Date().toISOString().slice(0, 16).replace("T", " ")}（UTC）。**聴いた感想ではなく、計測値です。** 耳での確認は下の聴取依頼で。

## 数値で確かめたこと
${checks.join("\n")}

### 楽理の点検（score-check.mjs。警告 ${scoreWarn.length}件）
${scoreWarn.length ? scoreWarn.join("\n") : "（警告なし）"}

### 目安との比較（analyze.py --compare）
\`\`\`
${compare}
\`\`\`
- I（統合ラウドネス）: ${m.I} LUFS ／ crest ${m.crest_dB}dB ／ 曲の長さ ${m.dur_s}秒

## 耳でないと分からないこと（人間に聴いてもらう）
場面に合うか／旋律を口ずさめるか／リードが聞こえるか／低音が濁っていないか／うるさい・耳に痛い所／ループの継ぎ目が気にならないか／飽きるのは何回目か／効果音と重なって困らないか。

## 聴取依頼（そのまま送れる文）
【お願い】曲「${song.title}」${song.description ? "（" + song.description.replace(/^（[^）]*）/, "").slice(0, 60) + "…）" : ""}を聴いて感想をください。上手・下手の評価ではなく、感じたままで大丈夫です。
聴き方: 機器は【イヤホン/スピーカー/スマホ内蔵】、音量は【普段聴く大きさ】。曲は最後まで（または2周）聴く。
- Q1 聴いて最初に思い浮かんだ場面や気持ちを、一言で。
- Q2 この曲は【使う場面】に合っていますか。5(ぴったり)〜1(合わない)
- Q3 聴きやすさ 5(心地よい)〜1(つらい)。1〜2なら、どのあたり(何秒ごろ・どの楽器)か。
- Q4 耳に痛い、うるさい、こもる、遠い、と感じた所はありますか。あれば時間と言葉で。
- Q5 メロディを口ずさめますか。
- Q6 2周目で「また同じだ」と感じ始めた時間は。気にならなかったなら「なし」。
- Q7 つなぎ目（曲の終わり→始まり）で、ぶつっと途切れる・間が空く・音が跳ぶことはありましたか。
- Q8 ほかの音（効果音・声）とのバランスは。曲が大きすぎ・小さすぎ・ちょうどいい。
- Q10 自由記述。直すなら1つだけ何を変えたいか。
`;
const report = path.join(out, `${id}.qa.md`);
fs.writeFileSync(report, md);
console.log(md);
console.log(`\n→ ${report} に書きました（△ ${checks.filter((c) => c.startsWith("△")).length}件）`);
