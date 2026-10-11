// 作曲ソフトの「曲を組み立てる・書き出す」部分。コマンド（song.mjs）とコネクタ（tools/mcp/server.mjs）の両方が使う。
// ゲームと同じ TypeScript のコードを、vite で読み込んで使う。標準出力には何も書かない（コネクタの通信をこわさないため）。
import { createServer } from "vite";
import fs from "fs";
import path from "path";
import { execSync } from "child_process";
import { masterFile, MASTER_PRESETS } from "./master.mjs";
import { makeIr, writeWav, SPACES } from "./space-ir.mjs";
import { checkChordVariety, loadOtherSongs } from "./chord-variety.mjs";
import { workflowWarnings } from "./workflow-check.mjs";

export const ROOT = path.resolve(new URL("../../", import.meta.url).pathname);
const EDITIONS = ["real", "ps2", "modern"];

export async function openSongKit() {
  const server = await createServer({ root: ROOT, configFile: false, logLevel: "silent", server: { middlewareMode: true, hmr: false }, appType: "custom" });
  const load = (p) => server.ssrLoadModule(p);

  async function soundSets() {
    return load("/src/audio/sound-sets.ts");
  }

  async function guide() {
    const { AI_SONG_GUIDE } = await load("/src/audio/ai-song.ts");
    return AI_SONG_GUIDE;
  }

  /** 曲（AIソング形式のオブジェクト）を確かめて、プロジェクト・MIDI（・WAV）を書き出す。 */
  async function build(songData, { name, edition = "real", outDir, wav = false, soundfont = "game", bass = "std", drums = "std", guitar = "std", sound = "", master = null, widen = null, space = "", spaceWet = 0.25, masterPreset = "" } = {}) {
    if (!EDITIONS.includes(edition)) throw new Error("edition は real・ps2・modern のどれか");
    if (!/^[a-z0-9][a-z0-9-]*$/.test(name ?? "")) throw new Error(`name は英小文字・数字・「-」だけ（${name}）`);
    const { aiSongToScore } = await load("/src/audio/ai-song.ts");
    const { scoreToMidi } = await load("/src/audio/midi-export.ts");
    const { realEdition } = await load("/src/audio/real-edition.ts");
    const { ps2Edition } = await load("/src/audio/ps2-edition.ts");
    const { getScoreDurationSec } = await load("/src/audio/score.ts");
    let { score, song, warnings } = aiSongToScore(songData);
    // サウンドセット: アンプ・音量・ミックス・ドラムの設定と、使う音源（ベース・ドラム・ギター）をまとめて当てはめる
    if (sound) {
      const { SOUND_SETS, applySoundSet } = await load("/src/audio/sound-sets.ts");
      const set = SOUND_SETS[sound];
      if (!set) throw new Error(`サウンドセットがありません: ${sound}（${Object.keys(SOUND_SETS).join("・")}）`);
      score = applySoundSet(score, set);
      if (bass === "std") bass = set.overlays.bass;
      if (drums === "std") drums = set.overlays.drums;
      if (guitar === "std") guitar = set.overlays.guitar;
      if (master === null && set.master) master = set.master.lufs;
      if (widen === null && set.master?.widen) widen = set.master.widen;
    }
    // 曲の自動チェック（楽譜）: 低音のにごり・同じ音域のぶつかり・単調さ。入力のまちがいではなく、直すと良くなるヒント
    const { checkScore } = await load("/src/audio/song-check.ts");
    warnings.push(...checkScore(score));
    // コード進行の自動チェック: 基本の和音だけ・少ない種類のくり返し・他の曲と同じ形
    warnings.push(...checkChordVariety(song.chords, loadOtherSongs(path.join(ROOT, "assets-src", "ai-songs"), name)));
    // 曲作りの流れの点検: 直前の曲と同じ選択・旋律と和音のぶつかり（アヴォイドノート）・同じ4小節の反復（tools/composer/workflow-check.mjs）
    warnings.push(...workflowWarnings(song, name, ROOT));
    const out = path.resolve(outDir ?? path.join(ROOT, "dist-songs"));
    fs.mkdirSync(out, { recursive: true });
    const files = { project: path.join(out, `${name}.sunshine-song.json`), midi: path.join(out, `${name}.mid`) };
    fs.writeFileSync(files.project, JSON.stringify({ format: "sunshine-song", version: 1, name: song.title, edition, score }));
    const edited = edition === "ps2" ? ps2Edition(score) : edition === "real" ? realEdition(score) : score;
    fs.writeFileSync(files.midi, scoreToMidi(edited));
    if (wav) {
      files.wav = path.join(out, `${name}.wav`);
      await renderWav(score, edition, files.wav, soundfont, bass, drums, guitar);
      // 仕上げの音量: 書き出しのときだけ、全体の大きさをそろえる（ゲーム中の再生やアプリの音は変わらない）。ピークは -1dB 以下に抑える
      // 空間（畳み込みリバーブ）: 自作のIRで、書き出しのときだけ残響を足す（hall / room / plate）
      if (space) {
        if (!SPACES[space]) throw new Error(`space は ${Object.keys(SPACES).join("・")} のどれか（${space}）`);
        const irFile = files.wav + `.ir-${space}.wav`;
        writeWav(irFile, makeIr(space));
        const tmpv = files.wav + ".space.wav";
        const w = Math.max(0, Math.min(1, Number(spaceWet)));
        execSync(`ffmpeg -y -loglevel error -i "${files.wav}" -i "${irFile}" -filter_complex "[0]asplit[d][w];[w][1]afir=dry=1:wet=10,volume=${(5 * w).toFixed(3)}[r];[d][r]amix=inputs=2:normalize=0:duration=first" -ar 48000 -ac 2 -c:a pcm_s16le "${tmpv}"`);
        fs.renameSync(tmpv, files.wav);
        fs.rmSync(irFile, { force: true });
      }
      let glue;
      if (masterPreset) {
        const pr = MASTER_PRESETS[masterPreset];
        if (!pr) throw new Error(`master-preset は ${Object.keys(MASTER_PRESETS).join("・")} のどれか（${masterPreset}）`);
        if (master === null || master === undefined) master = pr.lufs;
        if (widen === null) widen = pr.widen;
        glue = songData.dynamics === "natural" && pr.glue === "normal" ? "gentle" : pr.glue; // natural の曲は起伏をつぶさない
      }
      if (master !== null && master !== undefined) {
        // 仕上げ（tools/composer/master.mjs）: 低域モノ・左右の広がり・目標の大きさ・トゥルーピーク・ディザ
        masterFile(files.wav, { lufs: master, widen: widen ?? 1, natural: songData.dynamics === "natural", glue });
      }
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

  return { guide, soundSets, build, register, listGameSongs, ampPresets, close: () => server.close() };
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
export async function renderWav(score, edition, file, soundfont = "game", bass = "std", drums = "std", guitar = "std") {
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
    await page.evaluate(([b, d, g]) => window.__composer.setOverlays(b, d, g), [bass, drums, guitar]);
    if (soundfont === "gu") await page.evaluate(() => window.__composer.setSoundfont("gu"));
    const b64 = await page.evaluate(([s, e]) => window.__composer.renderWav(s, e), [score, edition]);
    fs.writeFileSync(file, Buffer.from(b64, "base64"));
  } finally {
    await browser.close();
  }
}
