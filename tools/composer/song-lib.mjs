// 作曲ソフトの「曲を組み立てる・書き出す」部分。コマンド（song.mjs）とコネクタ（tools/mcp/server.mjs）の両方が使う。
// ゲームと同じ TypeScript のコードを、vite で読み込んで使う。標準出力には何も書かない（コネクタの通信をこわさないため）。
import { createServer } from "vite";
import fs from "fs";
import path from "path";
import { execSync } from "child_process";

export const ROOT = path.resolve(new URL("../../", import.meta.url).pathname);
const EDITIONS = ["real", "ps2", "modern"];

export async function openSongKit() {
  const server = await createServer({ root: ROOT, configFile: false, logLevel: "silent", server: { middlewareMode: true, hmr: false }, appType: "custom" });
  const load = (p) => server.ssrLoadModule(p);

  async function guide() {
    const { AI_SONG_GUIDE } = await load("/src/audio/ai-song.ts");
    return AI_SONG_GUIDE;
  }

  /** 曲（AIソング形式のオブジェクト）を確かめて、プロジェクト・MIDI（・WAV）を書き出す。 */
  async function build(songData, { name, edition = "real", outDir, wav = false } = {}) {
    if (!EDITIONS.includes(edition)) throw new Error("edition は real・ps2・modern のどれか");
    if (!/^[a-z0-9][a-z0-9-]*$/.test(name ?? "")) throw new Error(`name は英小文字・数字・「-」だけ（${name}）`);
    const { aiSongToScore } = await load("/src/audio/ai-song.ts");
    const { scoreToMidi } = await load("/src/audio/midi-export.ts");
    const { realEdition } = await load("/src/audio/real-edition.ts");
    const { ps2Edition } = await load("/src/audio/ps2-edition.ts");
    const { getScoreDurationSec } = await load("/src/audio/score.ts");
    const { score, song, warnings } = aiSongToScore(songData);
    // 曲の自動チェック（楽譜）: 低音のにごり・同じ音域のぶつかり・単調さ。入力のまちがいではなく、直すと良くなるヒント
    const { checkScore } = await load("/src/audio/song-check.ts");
    warnings.push(...checkScore(score));
    const out = path.resolve(outDir ?? path.join(ROOT, "dist-songs"));
    fs.mkdirSync(out, { recursive: true });
    const files = { project: path.join(out, `${name}.sunshine-song.json`), midi: path.join(out, `${name}.mid`) };
    fs.writeFileSync(files.project, JSON.stringify({ format: "sunshine-song", version: 1, name: song.title, edition, score }));
    const edited = edition === "ps2" ? ps2Edition(score) : edition === "real" ? realEdition(score) : score;
    fs.writeFileSync(files.midi, scoreToMidi(edited));
    if (wav) {
      files.wav = path.join(out, `${name}.wav`);
      await renderWav(score, edition, files.wav);
      // 鳴らした音の自動チェック（音割れ・低音の多すぎ・強弱の平らさ・途中の無音）
      const { analyzeMix } = await load("/src/audio/song-check.ts");
      const bytes = fs.readFileSync(files.wav);
      const frames = (bytes.length - 44) >> 2;
      const ch = [new Float32Array(frames), new Float32Array(frames)];
      for (let i = 0; i < frames; i++) { ch[0][i] = bytes.readInt16LE(44 + i * 4) / 32768; ch[1][i] = bytes.readInt16LE(46 + i * 4) / 32768; }
      warnings.push(...analyzeMix(ch, bytes.readUInt32LE(24)));
    }
    const sec = getScoreDurationSec(score);
    return { title: song.title, description: song.description, tracks: score.tracks.length, seconds: Math.round(sec * 10) / 10, bpm: score.tempoBpm, warnings, files, score };
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

  return { guide, build, register, listGameSongs, ampPresets, close: () => server.close() };
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
    await page.goto("file://" + html);
    await page.waitForFunction(() => "__composer" in window);
    const b64 = await page.evaluate(([s, e]) => window.__composer.renderWav(s, e), [score, edition]);
    fs.writeFileSync(file, Buffer.from(b64, "base64"));
  } finally {
    await browser.close();
  }
}
