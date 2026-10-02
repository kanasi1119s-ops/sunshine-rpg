// Suno式の「文章から曲を作る」コマンド。スタイル指定の文章（と、あれば歌詞・テンポ・調）から、4〜5分の曲を自動で組み立てる。
// APIキーはいらない。有料サービスも使わない。同じ文章・同じ種からは、いつも同じ曲ができる。
//
//   node tools/composer/make.mjs one --title "曲名" --prompt "melodic metal, twin guitars, 150 BPM, E minor"
//        [--length 270] [--seed 7] [--variations 3] [--lyrics 歌詞.txt] [--out <フォルダ>] [--edition real|ps2|modern] [--wav [--engine node|browser]]
//       1曲を作る。--variations N: 種を変えた別バージョンを N 個作る（Sunoの「2曲出る」と同じ。聴いて選ぶ）。
//
//   node tools/composer/make.mjs batch songs.json [--only 1 3 5] [--length 270] [--variations 1] [--out <フォルダ>] [--wav]
//       songs.json（マスタープロンプトが出す形式）の全曲をまとめて作る。
//       songs.json: [{"title","prompt","lyrics","bpm","key_scale","time_signature","audio_duration"}, ...]
//
//   歌入りにするには、songs.json の曲に "lyrics_kana"（ひらがな・カタカナの歌詞。[verse] [bridge] [chorus] の見出しで区切る）を書く。
//   任意: "voice"（歌い手。既定 波音リツ）、"transpose"（移調。半音の数）、"vocal_gain_db"（声の大きさの微調整。dB）、"vocal": false（歌なしにする）。
//   すると曲ごとに <名前>.vocal.json（歌声用の楽譜）も書き出す。声にするのはPC側の vocal_tool.py（VOICEVOX）。
//
//   出力（--out、既定は dist-songs/<日付>/）: 曲ごとに プロジェクト(.sunshine-song.json)・MIDI(.mid)・歌詞(.lyrics.txt)・
//   報告(.report.json)、全体の一覧(index.md)。--wav を付けると WAV も作る。既定（--engine node）はブラウザ不要の高品質レンダラー（パート別ミックス。FFmpeg が必要）。--engine browser は従来の Playwright + Chromium。失敗したら警告を出して続ける。
import fs from "fs";
import path from "path";
import { openSongKit } from "./song-lib.mjs";
import { analyzeWav } from "./audio-report.mjs";

const args = process.argv.slice(2);
const flag = (name) => args.includes(name);
const opt = (name, fallback) => {
  const i = args.indexOf(name);
  return i >= 0 && i + 1 < args.length ? args[i + 1] : fallback;
};
const optList = (name) => {
  const i = args.indexOf(name);
  if (i < 0) return null;
  const out = [];
  for (let j = i + 1; j < args.length && !args[j].startsWith("--"); j++) out.push(Number(args[j]));
  return out;
};

const MIN_SEC = 240;
const MAX_SEC = 300;

/** 文字列から、安定した整数の種を作る（同じ曲名・文章なら同じ種）。 */
function hashSeed(text) {
  let h = 2166136261;
  for (const ch of text) {
    h ^= ch.codePointAt(0);
    h = Math.imul(h, 16777619);
  }
  return (h >>> 0) % 1000000;
}
const mmss = (sec) => `${Math.floor(sec / 60)}:${String(Math.round(sec % 60)).padStart(2, "0")}`;
const today = () => new Date().toISOString().slice(0, 10);

async function makeOne(kit, m, item, { index, length, seedBase, variations, outDir, edition, wav, wavEngine }) {
  const lines = [];
  const results = [];
  const choice = m.parseStylePrompt(item.prompt ?? "", { bpm: item.bpm, keyScale: item.key_scale, timeSignature: item.time_signature });
  const targetSec = Number(length ?? item.audio_duration ?? 270);
  const drive = ["hardcore", "deathmetal", "metal"].includes(choice.style) && choice.beats === 4;
  const kanaText = item.lyrics_kana ?? (item.vocal === true ? item.lyrics : undefined);
  const wantVocal = item.vocal !== false && typeof kanaText === "string" && kanaText.trim() !== "";
  for (let v = 0; v < variations; v++) {
    const seed = (seedBase ?? hashSeed(`${item.title}|${item.prompt}`)) + v;
    const spec = {
      id: `song-${String(index).padStart(2, "0")}`,
      title: item.title,
      scene: "",
      style: choice.style,
      tonic: choice.tonic,
      minor: choice.minor,
      bpm: choice.bpm,
      seed,
      beats: choice.beats,
      targetSec,
      ...(choice.flavors.length ? { flavor: choice.flavors } : {}),
      ...(drive ? { drive: true } : {}),
      ...(wantVocal ? { vocal: true } : {}),
    };
    const extra = {};
    const score = m.composeSong(spec, extra);
    const sec = m.getScoreDurationSec(score);
    const warnings = [...choice.warnings];
    if (sec < MIN_SEC || sec > MAX_SEC) warnings.push(`長さが4:00〜5:00から外れています（${mmss(sec)}）。テンポか目標の長さを調整してください。`);
    const base = `${String(index).padStart(2, "0")}${variations > 1 ? `-v${v + 1}` : ""}`;
    const name = `song-${base}`;
    let built;
    try {
      built = await kit.buildFromScore(score, { name, title: item.title, description: item.prompt ?? "", edition, outDir, wav, wavEngine, flavors: choice.flavors });
    } catch (e) {
      // WAV だけ失敗したら、プロジェクトとMIDIだけで続ける
      warnings.push(`WAVを作れませんでした: ${e.message.split("\n")[0]}`);
      built = await kit.buildFromScore(score, { name, title: item.title, description: item.prompt ?? "", edition, outDir, wav: false });
    }
    let audio = null;
    if (built.files.wav && fs.existsSync(built.files.wav)) {
      audio = analyzeWav(built.files.wav);
      for (const w of audio.warnings) warnings.push(`音: ${w}`);
    }
    let vocal = null;
    if (wantVocal) {
      const transpose = Number(item.transpose ?? 0);
      const plan = m.buildVocalPlan(extra.vocal ?? [], kanaText, choice.bpm, transpose);
      const voice = item.voice ?? "波音リツ";
      fs.writeFileSync(
        path.join(outDir, `${name}.vocal.json`),
        JSON.stringify({ title: item.title, bpm: choice.bpm, framerate: 93.75, voice, credit: `VOICEVOX:${voice}`, ...(item.vocal_gain_db !== undefined ? { gain_db: Number(item.vocal_gain_db) } : {}), chunks: plan.chunks }, null, 1) + "\n",
        "utf8",
      );
      vocal = { voice, chunks: plan.chunks.length, moras: plan.chunks.reduce((n, c) => n + c.moraCount, 0), notes: plan.chunks.reduce((n, c) => n + c.noteCount, 0) };
      warnings.push(...plan.warnings);
      if (!plan.chunks.length) warnings.push("歌う区間がありません（歌詞の見出しと曲の構成が合っているか確認してください）");
    }
    if (item.lyrics) fs.writeFileSync(path.join(outDir, `${name}.lyrics.txt`), item.lyrics.endsWith("\n") ? item.lyrics : item.lyrics + "\n", "utf8");
    const report = {
      title: item.title,
      prompt: item.prompt ?? "",
      decided: { style: choice.style, flavors: choice.flavors, bpm: choice.bpm, beats: choice.beats, key: `${choice.tonic} ${choice.minor ? "minor" : "major"}`, seed },
      matched: choice.matched,
      structure: m.planKinds(choice.bpm, choice.beats, targetSec),
      duration: mmss(sec),
      seconds: built.seconds,
      tracks: built.tracks,
      files: Object.fromEntries(Object.entries(built.files).map(([k, f]) => [k, path.basename(f)])),
      vocal,
      audio: audio && audio.ok ? { lufs: audio.lufs, lra: audio.lra, truePeak: audio.truePeak, bands: audio.bands } : undefined,
      mix: built.mixInfo ? Object.fromEntries(Object.entries(built.mixInfo.groups).map(([g, v]) => [g, v.gain === null ? null : Math.round(v.gain * 10) / 10])) : undefined,
      warnings,
    };
    fs.writeFileSync(path.join(outDir, `${name}.report.json`), JSON.stringify(report, null, 2) + "\n", "utf8");
    results.push(report);
    lines.push(`  ${name}: ${choice.style}${choice.flavors.length ? "+" + choice.flavors.join("+") : ""} ${choice.bpm}BPM ${report.decided.key} ${report.duration} ${built.tracks}トラック${vocal ? ` 歌:${vocal.voice}(${vocal.chunks}区間)` : ""}${warnings.length ? " ⚠ " + warnings.join(" / ") : ""}`);
  }
  console.log(`[${index}] ${item.title}\n${lines.join("\n")}`);
  return results;
}

function writeIndex(outDir, all) {
  const rows = all.map((r, i) => `| ${i + 1} | ${r.title.replace(/\|/g, "/")} | ${r.decided.style}${r.decided.flavors.length ? "+" + r.decided.flavors.join("+") : ""} | ${r.decided.bpm} | ${r.decided.key} | ${r.duration} | ${r.vocal ? r.vocal.voice : "—"} | ${r.files.wav ?? r.files.midi} | ${r.warnings.join(" / ")} |`);
  const md = ["# 今日の曲の一覧", "", "| # | 曲名 | 曲調 | BPM | 調 | 長さ | 歌 | ファイル | 注意 |", "|---|---|---|---|---|---|---|---|---|", ...rows, ""].join("\n");
  fs.writeFileSync(path.join(outDir, "index.md"), md, "utf8");
}

const kit = await openSongKit();
try {
  const m = await kit.maker();
  const mode = args[0];
  const outDir = path.resolve(opt("--out", path.join("dist-songs", today())));
  fs.mkdirSync(outDir, { recursive: true });
  const common = { length: opt("--length"), variations: Math.max(1, Number(opt("--variations", 1))), outDir, edition: opt("--edition", "real"), wav: flag("--wav"), wavEngine: opt("--engine", "node") };
  if (mode === "one") {
    const title = opt("--title");
    const prompt = opt("--prompt");
    if (!title || !prompt) throw new Error("--title と --prompt が必要です");
    const lyricsArg = opt("--lyrics");
    const lyrics = lyricsArg ? (fs.existsSync(lyricsArg) ? fs.readFileSync(lyricsArg, "utf8") : lyricsArg) : undefined;
    const seed = opt("--seed") !== undefined ? Number(opt("--seed")) : undefined;
    const r = await makeOne(kit, m, { title, prompt, lyrics }, { ...common, index: 1, seedBase: seed });
    writeIndex(outDir, r);
    console.log("出力先:", outDir);
  } else if (mode === "batch" && args[1]) {
    const songs = JSON.parse(fs.readFileSync(args[1], "utf8"));
    if (!Array.isArray(songs) || !songs.length) throw new Error("songs.json は曲の配列にしてください");
    const only = optList("--only");
    const all = [];
    for (const [i, item] of songs.entries()) {
      if (only && !only.includes(i + 1)) continue;
      if (!item.title || !item.prompt) {
        console.warn(`[${i + 1}] title と prompt がないためスキップしました`);
        continue;
      }
      all.push(...(await makeOne(kit, m, item, { ...common, index: i + 1 })));
    }
    writeIndex(outDir, all);
    const bad = all.filter((r) => r.warnings.length).length;
    console.log(`\n完了: ${all.length}件（注意あり ${bad}件）。出力先: ${outDir}`);
  } else {
    console.log(fs.readFileSync(new URL(import.meta.url), "utf8").split("\n").filter((l) => l.startsWith("//")).map((l) => l.slice(3)).join("\n"));
    process.exitCode = 1;
  }
} catch (e) {
  console.error("× " + e.message);
  process.exitCode = 1;
} finally {
  await kit.close();
}
