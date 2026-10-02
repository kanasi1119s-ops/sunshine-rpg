// 作曲ソフトの「曲を組み立てる・書き出す」部分。コマンド（song.mjs）とコネクタ（tools/mcp/server.mjs）の両方が使う。
// ゲームと同じ TypeScript のコードを、vite で読み込んで使う。標準出力には何も書かない（コネクタの通信をこわさないため）。
import { createServer } from "vite";
import fs from "fs";
import path from "path";
import { execSync } from "child_process";
import { fileURLToPath, pathToFileURL } from "url";

// Windows でも動くよう、URL.pathname ではなく fileURLToPath を使う（"/C:/..." → "C:\\..."）
export const ROOT = path.resolve(fileURLToPath(new URL("../../", import.meta.url)));
const EDITIONS = ["real", "ps2", "modern"];

export async function openSongKit() {
  let self;
  const server = await createServer({ root: ROOT, configFile: false, logLevel: "silent", server: { middlewareMode: true, hmr: false }, appType: "custom" });
  const load = (p) => server.ssrLoadModule(p);

  async function guide() {
    const { AI_SONG_GUIDE } = await load("/src/audio/ai-song.ts");
    return AI_SONG_GUIDE;
  }

  /** 曲（AIソング形式のオブジェクト）を確かめて、プロジェクト・MIDI（・WAV）を書き出す。 */
  async function build(songData, { name, edition = "real", outDir, wav = false } = {}) {
    const { aiSongToScore } = await load("/src/audio/ai-song.ts");
    const { score, song, warnings } = aiSongToScore(songData);
    const r = await buildFromScore(score, { name, title: song.title, description: song.description, edition, outDir, wav });
    return { ...r, warnings };
  }

  /** 譜面（Score）から、プロジェクト・MIDI（・WAV）を書き出す。自動作曲（composeSong）の曲もこれで書き出す。 */
  async function buildFromScore(score, { name, title, description = "", edition = "real", outDir, wav = false, wavEngine = "node", flavors = [] } = {}) {
    if (!EDITIONS.includes(edition)) throw new Error("edition は real・ps2・modern のどれか");
    if (!/^[a-z0-9][a-z0-9-]*$/.test(name ?? "")) throw new Error(`name は英小文字・数字・「-」だけ（${name}）`);
    const { scoreToMidi } = await load("/src/audio/midi-export.ts");
    const { realEdition } = await load("/src/audio/real-edition.ts");
    const { ps2Edition } = await load("/src/audio/ps2-edition.ts");
    const { getScoreDurationSec } = await load("/src/audio/score.ts");
    const out = path.resolve(outDir ?? path.join(ROOT, "dist-songs"));
    fs.mkdirSync(out, { recursive: true });
    let mixInfo = null;
    const files = { project: path.join(out, `${name}.sunshine-song.json`), midi: path.join(out, `${name}.mid`) };
    fs.writeFileSync(files.project, JSON.stringify({ format: "sunshine-song", version: 1, name: title, edition, score }));
    const edited = edition === "ps2" ? ps2Edition(score) : edition === "real" ? realEdition(score) : score;
    fs.writeFileSync(files.midi, scoreToMidi(edited));
    if (wav) {
      files.wav = path.join(out, `${name}.wav`);
      if (wavEngine === "browser") await renderWav(score, edition, files.wav);
      else {
        // ブラウザなしの高品質レンダラー（パート別ミックス）。既定。
        const { renderMix } = await import("./render-node.mjs");
        const r = await renderMix(self, score, { edition, outWav: files.wav, flavors });
        mixInfo = { groups: r.groups, timing: r.timing };
      }
    }
    const sec = getScoreDurationSec(score);
    return { title, description, tracks: score.tracks.length, seconds: Math.round(sec * 10) / 10, bpm: score.tempoBpm, warnings: [], files, score, mixInfo };
  }

  /** パート別ミックス用の部品（MIDI・チャンネルごとの楽器・ミックス設計）。ブラウザなしで音にする render-node.mjs が使う。 */
  async function mixKit(score, edition = "real") {
    const { scoreToMidiInfo } = await load("/src/audio/midi-export.ts");
    const { realEdition } = await load("/src/audio/real-edition.ts");
    const { ps2Edition } = await load("/src/audio/ps2-edition.ts");
    const { getScoreDurationSec } = await load("/src/audio/score.ts");
    const mix = await load("/src/audio/mix-plan.ts");
    const edited = edition === "ps2" ? ps2Edition(score) : edition === "real" ? realEdition(score) : score;
    const info = scoreToMidiInfo(edited);
    return { ...info, seconds: getScoreDurationSec(edited), tempoBpm: edited.tempoBpm, mix };
  }

  /** 自動作曲・スタイル指定の読み取りなど、曲を作る側の部品を読み込む。 */
  async function maker() {
    const { composeSong, planKinds } = await load("/src/audio/songwriter.ts");
    const { parseStylePrompt } = await load("/src/audio/style-prompt.ts");
    const { getScoreDurationSec } = await load("/src/audio/score.ts");
    const { buildVocalPlan } = await load("/src/audio/vocal-score.ts");
    return { composeSong, planKinds, parseStylePrompt, getScoreDurationSec, buildVocalPlan };
  }

  /** 作った曲を、ゲームの曲として登録する（src/audio/songs/<id>.sunshine-song.json）。 */
  async function register(score, { id, title, scene = "" }) {
    const { allEntries } = await load("/src/audio/catalog.ts");
    const { songFileToEntry } = await load("/src/audio/user-songs.ts");
    const target = path.join(ROOT, "src/audio/songs", `${id}.sunshine-song.json`);
    const taken = new Set(allEntries().map((e) => e.id).filter((x) => !(x === id && fs.existsSync(target))));
    const data = { format: "sunshine-game-song", version: 1, id, title, scene, score };
    songFileToEntry(data, taken);
    fs.writeFileSync(target, JSON.stringify(data));
    return target;
  }

  /** ゲームの曲の一覧（ID・曲名・場面・曲調）。 */
  async function listGameSongs() {
    const { allEntries } = await load("/src/audio/catalog.ts");
    await load("/src/audio/user-songs.ts");
    return allEntries().map((e) => ({ id: e.id, title: e.title, scene: e.scene, style: e.styleLabel, group: e.group }));
  }

  /** ジャンル別アンプの一覧。 */
  async function ampPresets() {
    const { AMP_PRESETS } = await load("/src/audio/amp.ts");
    return Object.entries(AMP_PRESETS).map(([id, p]) => ({ id, label: p.label, genre: p.genre }));
  }

  self = { guide, build, buildFromScore, maker, mixKit, register, listGameSongs, ampPresets, close: () => server.close() };
  return self;
}

async function loadPlaywright() {
  const tries = ["playwright", "@playwright/test"];
  try {
    tries.push(path.join(execSync("npm root -g", { encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] }).trim(), "playwright/index.mjs"));
  } catch {
    // npm が見つからなければ、ほかの場所だけ試す
  }
  for (const t of tries) {
    try {
      return await import(t);
    } catch {
      // 次を試す
    }
  }
  throw new Error("WAVを作るには Playwright が必要です（npm i -D playwright && npx playwright install chromium）。作曲ソフトでプロジェクトを開いて「WAVで書き出す」でも作れます。");
}

/** 作曲ソフト（1ファイルのHTML）をヘッドレスのブラウザで開き、作曲ソフトと同じ音でWAVを作る。 */
export async function renderWav(score, edition, file) {
  const html = path.join(ROOT, "dist-composer/index.html");
  const newest = Math.max(...["tools/composer/entry.ts", "tools/composer/template.html"].map((f) => fs.statSync(path.join(ROOT, f)).mtimeMs));
  if (!fs.existsSync(html) || fs.statSync(html).mtimeMs < newest) {
    execSync(`node ${JSON.stringify(path.join(ROOT, "tools/composer/build.mjs"))}`, { stdio: "ignore" });
  }
  const { chromium } = await loadPlaywright();
  const browser = await chromium.launch({ args: ["--autoplay-policy=no-user-gesture-required"] });
  try {
    const page = await browser.newPage();
    await page.goto(pathToFileURL(html).href);
    await page.waitForFunction(() => "__composer" in window);
    const b64 = await page.evaluate(([s, e]) => window.__composer.renderWav(s, e), [score, edition]);
    fs.writeFileSync(file, Buffer.from(b64, "base64"));
  } finally {
    await browser.close();
  }
}
