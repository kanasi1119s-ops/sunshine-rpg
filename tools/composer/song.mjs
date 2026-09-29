// Claude Code から作曲ソフトを使うための道具（APIキーはいらない。曲は Claude Code 自身が書く）。
//
//   node tools/composer/song.mjs guide
//       AIソング形式の説明（楽器の一覧・書き方・よい曲にするコツ）を表示する。曲を書く前に読む。
//   node tools/composer/song.mjs build <曲.json> [--out <フォルダ>] [--edition real|ps2|modern] [--wav] [--register <曲ID> --scene "<場面>"]
//       AIソング形式のJSONを確かめて、作曲ソフトで開けるプロジェクト（.sunshine-song.json）とMIDIを書き出す。
//       --wav: 作曲ソフトと同じ音（録音音源・アンプ・仕上げ）でWAVも作る（Playwright と Chromium が必要）。
//       --register: ゲームの曲として src/audio/songs/<曲ID>.sunshine-song.json に登録する。
import { createServer } from "vite";
import fs from "fs";
import path from "path";
import { execSync } from "child_process";

const root = new URL("../../", import.meta.url).pathname;
const args = process.argv.slice(2);
const cmd = args[0];
const opt = (name) => {
  const i = args.indexOf(name);
  return i >= 0 ? args[i + 1] : undefined;
};

const server = await createServer({ root, configFile: false, logLevel: "silent", server: { middlewareMode: true, hmr: false }, appType: "custom" });
const load = (p) => server.ssrLoadModule(p);
try {
  if (cmd === "guide") {
    const { AI_SONG_GUIDE } = await load("/src/audio/ai-song.ts");
    console.log(AI_SONG_GUIDE);
    console.log("\n## 見本\nassets-src/ai-songs/ にある .json を見てください。");
  } else if (cmd === "build" && args[1]) {
    try {
      await buildSong(args[1]);
    } catch (e) {
      console.error("× " + e.message);
      process.exitCode = 1;
    }
  } else {
    console.log(fs.readFileSync(new URL(import.meta.url), "utf8").split("\n").filter((l) => l.startsWith("//")).map((l) => l.slice(3)).join("\n"));
    process.exitCode = 1;
  }
} finally {
  await server.close();
}

async function buildSong(file) {
  const { aiSongToScore } = await load("/src/audio/ai-song.ts");
  const { scoreToMidi } = await load("/src/audio/midi-export.ts");
  const { realEdition } = await load("/src/audio/real-edition.ts");
  const { ps2Edition } = await load("/src/audio/ps2-edition.ts");
  const { getScoreDurationSec } = await load("/src/audio/score.ts");
  const edition = opt("--edition") ?? "real";
  if (!["real", "ps2", "modern"].includes(edition)) throw new Error("--edition は real・ps2・modern のどれか");
  let result;
  try {
    result = aiSongToScore(JSON.parse(fs.readFileSync(file, "utf8")));
  } catch (e) {
    console.error("× 曲を組み立てられませんでした。直してから、もう一度 build してください:\n" + e.message);
    process.exitCode = 1;
    return;
  }
  const { score, song, warnings } = result;
  for (const w of warnings) console.warn("注意:", w);
  const base = path.basename(file).replace(/\.json$/i, "");
  const out = path.resolve(opt("--out") ?? root + "dist-songs");
  fs.mkdirSync(out, { recursive: true });
  const project = path.join(out, `${base}.sunshine-song.json`);
  fs.writeFileSync(project, JSON.stringify({ format: "sunshine-song", version: 1, name: song.title, edition, score }));
  const edited = edition === "ps2" ? ps2Edition(score) : edition === "real" ? realEdition(score) : score;
  fs.writeFileSync(path.join(out, `${base}.mid`), scoreToMidi(edited));
  const sec = getScoreDurationSec(score);
  console.log(`○ 「${song.title}」 ${score.tracks.length}トラック・${Math.floor(sec / 60)}分${Math.round(sec % 60)}秒・テンポ${score.tempoBpm}`);
  console.log("  プロジェクト:", project, "（作曲ソフトの「プロジェクトを読み込む」で開ける）");
  console.log("  MIDI:", path.join(out, `${base}.mid`));

  const id = opt("--register");
  if (id) {
    const { allEntries } = await load("/src/audio/catalog.ts");
    const { songFileToEntry } = await load("/src/audio/user-songs.ts");
    const target = path.join(root, "src/audio/songs", `${id}.sunshine-song.json`);
    const taken = new Set(allEntries().map((e) => e.id).filter((x) => !(x === id && fs.existsSync(target))));
    const data = { format: "sunshine-game-song", version: 1, id, title: song.title, scene: opt("--scene") ?? "", score };
    songFileToEntry(data, taken);
    fs.writeFileSync(target, JSON.stringify(data));
    console.log("  ゲームに登録:", target);
  }
  if (args.includes("--wav")) {
    const wav = path.join(out, `${base}.wav`);
    await renderWav(score, edition, wav);
    console.log("  WAV:", wav);
  }
}

async function loadPlaywright() {
  const tries = ["playwright", "@playwright/test"];
  try {
    tries.push(path.join(execSync("npm root -g", { encoding: "utf8" }).trim(), "playwright/index.mjs"));
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
  throw new Error("WAVを作るには Playwright が必要です（npx playwright install chromium）。作曲ソフトでプロジェクトを開いて「WAVで書き出す」でも作れます。");
}

async function renderWav(score, edition, file) {
  const html = root + "dist-composer/index.html";
  const stale = !fs.existsSync(html) || fs.statSync(html).mtimeMs < fs.statSync(root + "tools/composer/entry.ts").mtimeMs;
  if (stale) {
    console.log("  作曲ソフトをビルドしています…");
    execSync(`node ${JSON.stringify(root + "tools/composer/build.mjs")}`, { stdio: "ignore" });
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
