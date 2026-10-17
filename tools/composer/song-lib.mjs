// 作曲ソフトの「曲を組み立てる・書き出す」部分。コマンド（song.mjs）とコネクタ（tools/mcp/server.mjs）の両方が使う。
// ゲームと同じ TypeScript のコードを、vite で読み込んで使う。標準出力には何も書かない（コネクタの通信をこわさないため）。
import { createServer } from "vite";
import fs from "fs";
import path from "path";
import { execSync, execFileSync } from "child_process";
import { masterFile, resolvePreset } from "./master.mjs";
import { masterReport, loopTailWrap, lowShareDb } from "./master-report.mjs";
import { makeIr, writeWav, SPACES } from "./space-ir.mjs";
import { checkChordVariety, loadOtherSongs } from "./chord-variety.mjs";
import { workflowWarnings } from "./workflow-check.mjs";

export const ROOT = path.resolve(new URL("../../", import.meta.url).pathname);
const EDITIONS = ["real", "ps2", "modern"];

export async function openSongKit() {
  const server = await createServer({ root: ROOT, configFile: false, logLevel: "silent", server: { middlewareMode: true, hmr: false, watch: null }, appType: "custom" });
  const load = (p) => server.ssrLoadModule(p);

  async function soundSets() {
    return load("/src/audio/sound-sets.ts");
  }

  async function mixTools() {
    return load("/src/audio/mix-tools.ts");
  }

  async function guide() {
    const { AI_SONG_GUIDE } = await load("/src/audio/ai-song.ts");
    const { AI_SONG_EXTRAS_GUIDE } = await load("/src/audio/ai-song-extras.ts");
    return AI_SONG_GUIDE + AI_SONG_EXTRAS_GUIDE;
  }

  /** 曲（AIソング形式のオブジェクト）を確かめて、プロジェクト・MIDI（・WAV）を書き出す。 */
  async function build(songData, { name, edition = "real", outDir, wav = false, soundfont = "game", bass = "std", drums = "std", guitar = "std", orchestra = "std", piano = "std", sound = "", master = null, widen = null, space = "", spaceWet = null, masterPreset = "", tp = null, lowmono = null, sideHpf = null, clip = null, hpf = null, lpf = null, matchEq = "", matchAmount = null, loopTail = false, genre = "", autoRetune = true } = {}) {
    if (!EDITIONS.includes(edition)) throw new Error("edition は real・ps2・modern のどれか");
    if (!/^[a-z0-9][a-z0-9-]*$/.test(name ?? "")) throw new Error(`name は英小文字・数字・「-」だけ（${name}）`);
    const { aiSongToScore } = await load("/src/audio/ai-song.ts");
    const { scoreToMidi } = await load("/src/audio/midi-export.ts");
    const { realEdition } = await load("/src/audio/real-edition.ts");
    const { ps2Edition } = await load("/src/audio/ps2-edition.ts");
    const { getScoreDurationSec } = await load("/src/audio/score.ts");
    // --genre: ジャンル名から、drumMix・swing・human の推奨値と、ドラム／ベースの音源（--drums／--bass を別に書けばそちらが優先）を決める
    if (genre) {
      const { DRUM_GENRES } = await load("/src/audio/drum-genres.ts");
      const g = DRUM_GENRES[genre];
      if (!g) throw new Error(`--genre「${genre}」は使えません（${Object.keys(DRUM_GENRES).join("・")}）`);
      songData = { drumGenre: genre, ...songData };
      if (drums === "std") drums = g.drums;
      if (bass === "std") bass = g.bass;
    }
    // 書き出しでは、楽器の音域・同時発音・息継ぎの点検を既定で行う（曲に instrumentCheck:false で止める）
    if (songData && typeof songData === "object" && songData.instrumentCheck === undefined) songData = { ...songData, instrumentCheck: true };
    // オーケストラの patch（violin・cello・flute・horn など）を使う曲は、オーケストラ音源を自動で選ぶ
    const { ORCHESTRA_PATCHES } = await load("/src/audio/ai-song.ts");
    if (orchestra === "std" && Array.isArray(songData?.parts) && songData.parts.some((p) => ORCHESTRA_PATCHES.includes(p?.patch))) orchestra = "vsco";
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
      if (orchestra === "std" && set.overlays.orchestra) orchestra = set.overlays.orchestra;
      if (piano === "std" && set.overlays.piano) piano = set.overlays.piano;
      if (master === null && set.master) master = set.master.lufs;
      if (widen === null && set.master?.widen) widen = set.master.widen;
      // サウンドセットの master に preset・space・spaceWet があれば、同じ引数（--master-preset・--space・--space-wet）を書いたのと同じ（引数のほうが優先）
      if (!masterPreset && set.master?.preset) masterPreset = set.master.preset;
      if (!space && set.master?.space) space = set.master.space;
      if (spaceWet === null && set.master?.spaceWet !== undefined) spaceWet = set.master.spaceWet;
    }
    if (spaceWet === null) spaceWet = 0.25;
    // 曲の自動チェック（楽譜）: 低音のにごり・同じ音域のぶつかり・単調さ。入力のまちがいではなく、直すと良くなるヒント
    const { checkScore } = await load("/src/audio/song-check.ts");
    warnings.push(...checkScore(score));
    // キックとベースの整合率（情報。ロック・パンクは kickWithBass が高め、ファンク・レゲエ・ジャズ・ボサノバは低めが正常）
    const { kickBassAlignment } = await load("/src/audio/song-check.ts");
    const align = kickBassAlignment(score);
    if (align) console.log(`  キックとベースの整合率: キック${align.kicks}回のうちベースも鳴る ${Math.round(align.kickWithBass * 100)}%・スネア${align.snares}回のうちベースが休む ${Math.round(align.snareRest * 100)}%`);
    // ミックスの検査（kick・bass・sub808 の左右・残響、低域のパートの数、主役の重複、音量の合計）と、150Hz 以下をモノにできるか
    const { checkMixRoles } = await load("/src/audio/mix-tools.ts");
    warnings.push(...checkMixRoles(score));
    // コード進行の自動チェック: 基本の和音だけ・少ない種類のくり返し・他の曲と同じ形
    warnings.push(...checkChordVariety(song.chords, loadOtherSongs(path.join(ROOT, "assets-src", "ai-songs"), name)));
    // 曲作りの流れの点検: 直前の曲と同じ選択・旋律と和音のぶつかり（アヴォイドノート）・同じ4小節の反復（tools/composer/workflow-check.mjs）
    warnings.push(...workflowWarnings(song, name, ROOT));
    // MIDI のチャンネルあふれの点検（2026-10-16）: 楽器・左右・残響などが違うパートは別のチャンネルになり、15 を超えると
    // 残りのパートが「同じ楽器のチャンネル」か 16番目のチャンネルへ回され、別の楽器の音で鳴ってしまう（ケルトの曲で、弦・チェロなどがアコーディオンの音になった）
    {
      const { scoreToMidiInfo } = await load("/src/audio/midi-export.ts");
      const sc = edition === "real" ? realEdition(score) : edition === "ps2" ? ps2Edition(score) : score;
      const info = scoreToMidiInfo(sc);
      const byCh = new Map();
      sc.tracks.forEach((t, i) => {
        const ch = info.trackChannels[i];
        if (ch === undefined || ch === 9) return;
        const id = `${t.program ?? ""}:${t.instrument ?? t.waveform}`;
        if (!byCh.has(ch)) byCh.set(ch, new Map());
        byCh.get(ch).set(id, [...(byCh.get(ch).get(id) ?? []), t.name ?? t.instrument ?? String(i)]);
      });
      for (const [ch, ids] of byCh) {
        if (ids.size > 1) warnings.push(`MIDI のチャンネルが足りません: チャンネル${ch + 1}に、別の楽器のパートが入っています（${[...ids.values()].map((v) => v.join("・")).join(" ／ ")}）。後ろのパートが前のパートの楽器の音で鳴ります。楽器の種類を減らすか、同じ楽器のパートの pan・reverb・chorus・bright・release などをそろえて、チャンネルを共有させてください（ドラム以外で15まで）`);
      }
    }
    const out = path.resolve(outDir ?? path.join(ROOT, "dist-songs"));
    fs.mkdirSync(out, { recursive: true });
    let reportLine = null;
    const files = { project: path.join(out, `${name}.sunshine-song.json`), midi: path.join(out, `${name}.mid`) };
    fs.writeFileSync(files.project, JSON.stringify({ format: "sunshine-song", version: 1, name: song.title, edition, sources: { bass, drums, guitar, orchestra, piano }, score }));
    const edited = edition === "ps2" ? ps2Edition(score) : edition === "real" ? realEdition(score) : score;
    fs.writeFileSync(files.midi, scoreToMidi(edited));
    // ゲーム内の曲の切り替え（BgmDirector）が読む、ループ点・導入と終わりの型・ボスの段階の表
    try { const { buildManifest } = await load("/src/audio/song-meta.ts"); files.manifest = path.join(out, `${name}.manifest.json`); fs.writeFileSync(files.manifest, JSON.stringify(buildManifest(name, song.title, score, getScoreDurationSec(score)))); } catch { /* 表が作れなくても曲の書き出しは続ける */ }
    if (wav) {
      files.wav = path.join(out, `${name}.wav`);
      await renderWav(score, edition, files.wav, soundfont, bass, drums, guitar, orchestra, piano);
      // プチッ（1〜2サンプルだけ波形が飛ぶ点）を、前後の波形からなめらかに埋める（2026-10-17、人間の指示「雑音とれない？」）。
      //   オーケストラの録音（ホルン・コントラバスなど）の音の切りかわりに出る。残響（space）や仕上げの前の、乾いた音で直す。SUNSHINE_NO_DECLICK=1 で止める
      //   残響や仕上げのあとにも、もう一度かける（乾いた音では目立たなかった点が、仕上げのあとに見つかることがある）
      const declick = () => {
        if (process.env.SUNSHINE_NO_DECLICK) return;
        try { execFileSync("python3", [path.join(ROOT, "tools/audio-check/declick.py"), files.wav], { stdio: "ignore", maxBuffer: 1 << 26 }); } catch { /* 直せなくても書き出しは続ける */ }
      };
      declick();
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
      // 尾の重ね書き（--loop-tail）: 書き出しの末尾（曲の長さより後ろ＝残響の尾）を先頭に重ねて、曲の長さに切る。仕上げの前にやる
      if (loopTail) {
        const t = await loopTailWrap(files.wav, getScoreDurationSec(score));
        if (!t.wrapped) warnings.push("--loop-tail: 曲の長さより後ろに残響の尾がほとんど無いので、重ねませんでした");
      }
      let glue, pr = null;
      if (masterPreset) {
        pr = resolvePreset(masterPreset);
        if (master === null || master === undefined) master = pr.lufs;
        if (widen === null) widen = pr.widen;
        const nat = songData.dynamics === "natural";
        // natural の曲は起伏をつぶさないよう、圧縮を一段やさしくする
        glue = nat ? ({ normal: "gentle", bus3: "bus2", bus2: "light" }[pr.glue] ?? pr.glue) : pr.glue;
      }
      let masterOpts = null, lowCutoff = 100, shareBefore = null, rawFile = null;
      if (master !== null && master !== undefined) {
        // 仕上げ（tools/composer/master.mjs）: 掃除・EQ・低域モノ・左右の広がり・目標の大きさ・ソフトクリップ・トゥルーピーク・ディザ
        const { id: _id, lufs: _l, glue: _g, widen: _w, ...rest } = pr ?? {};
        masterOpts = { ...rest, lufs: master, widen: widen ?? 1, natural: songData.dynamics === "natural", glue };
        if (tp !== null) masterOpts.tp = tp;
        if (lowmono !== null) masterOpts.lowmono = lowmono;
        if (sideHpf !== null) masterOpts.sideHpf = sideHpf;
        if (clip !== null) masterOpts.clip = clip;
        if (hpf !== null) masterOpts.hpf = hpf;
        if (lpf !== null) masterOpts.lpf = lpf;
        if (matchEq) { masterOpts.match = matchEq; if (matchAmount !== null) masterOpts.matchAmount = matchAmount; }
        const lm = masterOpts.lowmono ?? 140;
        lowCutoff = lm > 0 ? Math.min(100, Math.round(lm * 0.5)) : 100;
        if (lm > 0) shareBefore = lowShareDb(files.wav, lm * 0.8);
        // 「つぶれ気味」が出たときの再調整用に、仕上げ前の音を取っておく
        rawFile = files.wav + ".raw.wav";
        fs.copyFileSync(files.wav, rawFile);
        masterFile(files.wav, masterOpts);
        // モノ化で低音が痩せていないか（逆相気味の低音は、モノにすると消える）: 全体に対する低域の割合が 3dB 以上減ったら注意
        if (shareBefore !== null) {
          const loss = shareBefore - lowShareDb(files.wav, lm * 0.8);
          if (loss > 3) warnings.push(`低域モノ化（${lm}Hz 以下）で、全体に対する低音の割合が ${loss.toFixed(1)}dB 減りました。左右が逆相気味の低音（chorus・ダブル・広い残響）があるかもしれません。低音パートの pan を 0 に、chorus を外してください。`);
        }
      }
      declick();
      // 書き出しの合否表（I・TP・LRA・PLR・PSR・左右の相関・100Hz 以下の相関・継ぎ目を 1 行で）
      let rep = masterReport(files.wav, { lufs: masterOpts?.lufs ?? null, tp: masterOpts?.tp ?? -1.5, loop: true, lowCutoff });
      // 再調整のルーティン（人間の指示 2026-10-11）: 「つぶれ気味」（PLR・PSR が小さい）が出たら、仕上げをやさしくして最大2回やり直す
      //   1回目: クリップ 0・圧縮を一段やさしく・目標を 1.5LU 下げる ／ 2回目: さらに 3LU 下げる。それでも出たら、元の音（アンプ・音量の合計）が原因なので見直しを促す
      const crushed = (r) => r.issues.some((t) => t.includes("つぶれ気味"));
      const LIGHTER = { bus3: "bus2", bus2: "light", strong: "normal", normal: "gentle", gentle: "light" };
      if (autoRetune && masterOpts && rawFile && crushed(rep)) {
        const first = rep.line;
        for (let k = 1; k <= 2 && crushed(rep); k++) {
          const next = { ...masterOpts, clip: 0, glue: LIGHTER[masterOpts.glue] ?? masterOpts.glue, lufs: masterOpts.lufs - 1.5 * k };
          fs.copyFileSync(rawFile, files.wav);
          masterFile(files.wav, next);
          declick();
          rep = masterReport(files.wav, { lufs: next.lufs, tp: next.tp ?? -1.5, loop: true, lowCutoff });
          warnings.push(`つぶれ気味が出たので仕上げを再調整しました（${k}回目: クリップ 0・圧縮 ${next.glue}・目標 ${next.lufs}LUFS）→ ${rep.line}`);
        }
        if (crushed(rep)) warnings.push(`再調整しても「つぶれ気味」が残りました。元の音がつぶれています（最初: ${first}）。歪みギターのアンプ（punk は高域の割れが出やすい。loudrock・crunch を試す）、パートの音量の合計（0.7 前後）、同じ音を重ねすぎていないかを見直してください`);
      }
      if (rawFile) fs.rmSync(rawFile, { force: true });
      reportLine = rep.line;
      // 鳴らした音の自動チェック（音割れ・低音の多すぎ・強弱の平らさ・途中の無音）
      const { analyzeMix } = await load("/src/audio/song-check.ts");
      const bytes = fs.readFileSync(files.wav);
      const frames = (bytes.length - 44) >> 2;
      const ch = [new Float32Array(frames), new Float32Array(frames)];
      for (let i = 0; i < frames; i++) { ch[0][i] = bytes.readInt16LE(44 + i * 4) / 32768; ch[1][i] = bytes.readInt16LE(46 + i * 4) / 32768; }
      warnings.push(...analyzeMix(ch, bytes.readUInt32LE(24)));
    }
    const sec = getScoreDurationSec(score);
    return { report: reportLine, title: song.title, description: song.description, tracks: score.tracks.length, seconds: Math.round(sec * 10) / 10, bpm: score.tempoBpm, warnings, files, score };
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

  return { load, guide, soundSets, mixTools, build, register, listGameSongs, ampPresets, close: () => server.close() };
}

export async function loadPlaywright() {
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
export async function renderWav(score, edition, file, soundfont = "game", bass = "std", drums = "std", guitar = "std", orchestra = "std", piano = "std") {
  const html = path.join(ROOT, "dist-composer/index.html");
  // 作曲ソフトの元（entry.ts・template.html・tools/composer の .ts・src/audio の .ts/.json・音源の .sf3）のどれかが新しければ作り直す
  // （2026-10-15: 以前は entry.ts と template.html しか見ておらず、src/audio を直しても古い音で書き出されていた）
  const files = ["tools/composer/entry.ts", "tools/composer/template.html"].map((f) => path.join(ROOT, f));
  const walk = (dir, re) => {
    for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
      const p = path.join(dir, e.name);
      if (e.isDirectory()) walk(p, re);
      else if (re.test(e.name) && !e.name.endsWith(".test.ts")) files.push(p);
    }
  };
  walk(path.join(ROOT, "src/audio"), /\.(ts|json)$/);
  for (const e of fs.readdirSync(path.join(ROOT, "tools/composer"))) if (e.endsWith(".ts")) files.push(path.join(ROOT, "tools/composer", e));
  for (const e of fs.readdirSync(path.join(ROOT, "assets-src/soundfont/extra"))) if (e.endsWith(".sf3")) files.push(path.join(ROOT, "assets-src/soundfont/extra", e));
  const newest = Math.max(...files.map((f) => fs.statSync(f).mtimeMs));
  if (!fs.existsSync(html) || fs.statSync(html).mtimeMs < newest) {
    execSync(`node ${JSON.stringify(path.join(ROOT, "tools/composer/build.mjs"))}`, { stdio: "ignore" });
  }
  const { chromium } = await loadPlaywright();
  const browser = await chromium.launch({ args: ["--autoplay-policy=no-user-gesture-required", "--disable-gpu"] });
  try {
    const page = await browser.newPage({ viewport: { width: 320, height: 240 } });
    await page.goto("file://" + html, { timeout: 240000 });
    // 画面の動き（光るアニメーション）が、描き出しのCPUを食うので止める
    await page.addStyleTag({ content: "*,*::before,*::after{animation:none!important;transition:none!important}" });
    await page.waitForFunction(() => "__composer" in window, undefined, { timeout: 240000 });
    await page.evaluate(([b, d, g, o, p]) => window.__composer.setOverlays(b, d, g, o, p), [bass, drums, guitar, orchestra, piano]);
    if (soundfont === "gu") await page.evaluate(() => window.__composer.setSoundfont("gu"));
    const b64 = await page.evaluate(([s, e]) => window.__composer.renderWav(s, e), [score, edition]);
    fs.writeFileSync(file, Buffer.from(b64, "base64"));
  } finally {
    await browser.close();
  }
}
