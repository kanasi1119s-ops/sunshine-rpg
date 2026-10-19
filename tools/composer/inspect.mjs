// 楽器ごとの点検（2026-10-17、人間の指示「数値ってシステムチェックでさらに細かくできたりする？波形を種類別にするとか」）。
//
//   node tools/composer/song.mjs inspect <曲.json> [--out <フォルダ>] [--aes] [--keep-wav]
//        [--bass finger --drums muldjord --guitar shiny-acoustic --piano salamander --orchestra vsco --edition real]
//
// やること:
//   1. 1 回の描き出しで、楽器の種類ごと（同じ楽器・同じ音色のパートは 1 つにまとめる。ドラムは全部で 1 つ）に音を分けて取り出す
//      （全体の大きさ合わせと同じ倍率なので、楽器どうしの大きさを比べられる）
//   2. 楽器ごとに、大きさ・帯域（低〜空気）・重心・出だしの硬さ・プチッ（波形の飛び）を測る（tools/audio-check/part-inspect.py）
//      --aes を付けると、楽器ごとの音質の点数（Audiobox の PQ）も出す（1 楽器 30 秒〜1 分）
//   3. 2 つの楽器が同じ帯域・同じ時間に重なる「ぶつかり」を、大きい組み合わせから出す
// 自動ミックス（automix）はパートの音量の調整案まで出す道具。こちらは「どの楽器が、どんな音か」を細かく見る道具。
import fs from "fs";
import os from "os";
import path from "path";
import { execFileSync } from "child_process";
import { openSongKit, ROOT } from "./song-lib.mjs";
import { ensureComposerHtml, openStemSession } from "./stem-lib.mjs";

const DRUMS = new Set(["kick", "snare", "hihat", "crash", "tom", "cowbell", "rotoTom", "cajon"]);

export async function runInspect(argv) {
  const pos = []; const val = {}; const flag = new Set();
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (!a.startsWith("--")) { pos.push(a); continue; }
    if (["--aes", "--keep-wav"].includes(a)) { flag.add(a); continue; }
    val[a] = argv[++i];
  }
  if (!pos[0]) {
    console.log(fs.readFileSync(new URL(import.meta.url), "utf8").split("\n").filter((l) => l.startsWith("//")).map((l) => l.slice(3)).join("\n"));
    process.exitCode = 1; return;
  }
  const songPath = path.resolve(pos[0]);
  const song = JSON.parse(fs.readFileSync(songPath, "utf8"));
  const name = path.basename(songPath).replace(/\.json$/i, "").toLowerCase().replace(/[^a-z0-9-]+/g, "-");
  const out = path.resolve(val["--out"] ?? path.join(ROOT, "dist-songs", "inspect", name));
  fs.mkdirSync(out, { recursive: true });
  const overlays = { bass: val["--bass"] ?? "std", drums: val["--drums"] ?? "std", guitar: val["--guitar"] ?? "std", orchestra: val["--orchestra"] ?? "std", piano: val["--piano"] ?? "std" };
  const edition = val["--edition"] ?? "real";
  const kit = await openSongKit();
  let session = null;
  try {
    const aiSong = await kit.load("/src/audio/ai-song.ts");
    const { score } = aiSong.aiSongToScore(song);
    // パート → トラックの数（ストロークの弦などで増える）
    const counts = song.parts.map((p) => aiSong.aiSongToScore({ ...song, autoAccompaniment: false, parts: [p] }).score.tracks.length);
    const auto = score.tracks.length - counts.reduce((a, b) => a + b, 0);
    if (auto < 0) throw new Error("パートとトラックの対応が取れません");
    const partOfTrack = []; for (let t = 0; t < auto; t++) partOfTrack.push(-1);
    counts.forEach((c, i) => { for (let k = 0; k < c; k++) partOfTrack.push(i); });
    // 楽器の種類 → まとまり
    // 楽器の種類ごと。種類が多い曲（フィドルの2本重ねなどでチャンネルが足りない）は、音色（patch）の違いをまとめて楽器名だけで分ける
    let fine = true;
    const keyOf = (p) => (DRUMS.has(p.instrument) ? "drums" : fine ? `${p.instrument}${p.patch ? "-" + p.patch : ""}` : p.instrument);
    const extraCh = song.parts.filter((p) => p.doubleDetune).length;
    if (new Set(song.parts.map(keyOf)).size + extraCh > 14) fine = false;
    const groupKey = keyOf;
    const groups = new Map();
    song.parts.forEach((p, i) => {
      const k = groupKey(p);
      if (!groups.has(k)) groups.set(k, { key: k, parts: [], roles: [] });
      groups.get(k).parts.push(i); groups.get(k).roles.push(String(p.role ?? p.instrument));
    });
    const labelOf = (g) => {
      if (g.key === "drums") return "ドラム";
      const bases = [...new Set(g.roles.map((r) => r.replace(/（[^）]*本目）|（和音[^）]*）|（[上下][^）]*）/g, "")))];
      return bases.length === 1 ? bases[0] : g.roles[0].replace(/（.*$/, "");
    };
    const gid = [...groups.keys()];
    if (gid.length > 15) throw new Error(`楽器の種類が ${gid.length} あり、15 を超えています`);
    const keyed = { ...score, tracks: score.tracks.map((t, ti) => ({ ...t, stemKey: partOfTrack[ti] >= 0 ? `g${gid.indexOf(groupKey(song.parts[partOfTrack[ti]]))}` : "auto" })) };
    console.error("作曲ソフトの用意中…");
    const html = ensureComposerHtml(path.join(os.tmpdir(), "sunshine-inspect", "composer.html"));
    session = await openStemSession(html, overlays);
    console.error("描き出し中…（曲の長さによって 2〜5 分）");
    const mix = path.join(out, `${name}-mix.wav`);
    // 取り出せるチャンネルは全部で 15 まで（音の入れ物の上限）。16 になる曲は、ドラムを別の描き出しで取る
    const midi = await kit.load("/src/audio/midi-export.ts");
    const tapsOf = (sc) => new Set(Object.values(midi.scoreToMidiInfo({ ...sc, loop: false }).stemChannels).flat()).size;
    const drumIdx = gid.indexOf("drums");
    const split = tapsOf(keyed) > 15 && drumIdx >= 0;
    const first = split ? { ...keyed, tracks: keyed.tracks.map((t) => (t.stemKey === `g${drumIdx}` ? { ...t, stemKey: undefined } : t)) } : keyed;
    const main = await session.render(first, edition, { busFile: mix, keepStems: true, timeoutMs: 1200000 });
    const man = { song: songPath, mix, groups: [] };
    for (const [i, k] of gid.entries()) {
      if (split && i === drumIdx) continue;
      const file = path.join(out, `${name}-${k}.wav`);
      if (await session.writeStem(`g${i}`, file)) man.groups.push({ key: k, label: labelOf(groups.get(k)), parts: groups.get(k).parts.map((x) => x + 1), wav: file });
    }
    if (split) {
      console.error("ドラムだけを描き出し中…");
      const only = { ...keyed, tracks: keyed.tracks.filter((t) => t.stemKey === `g${drumIdx}`) };
      await session.render(only, edition, { keepStems: true, fixedGainDb: main.gainDb, timeoutMs: 1200000 });
      const file = path.join(out, `${name}-drums.wav`);
      if (await session.writeStem(`g${drumIdx}`, file)) man.groups.push({ key: "drums", label: "ドラム", parts: groups.get("drums").parts.map((x) => x + 1), wav: file });
    }
    await session.close(); session = null;
    const manFile = path.join(out, `${name}.inspect.json`);
    fs.writeFileSync(manFile, JSON.stringify(man, null, 1));
    console.error("測定中…");
    const args = [path.join(ROOT, "tools/audio-check/part-inspect.py"), manFile].concat(flag.has("--aes") ? ["--aes"] : []);
    const txt = execFileSync("python3", args, { encoding: "utf8", env: { ...process.env, HF_HUB_OFFLINE: "1", HF_HOME: process.env.HF_HOME ?? "/root/.cache/huggingface" }, maxBuffer: 1 << 26, cwd: os.tmpdir() });
    console.log(`○ 「${song.title}」の楽器ごとの点検（${man.groups.length} 種類）`);
    console.log(txt.trimEnd());
    console.log(`  結果: ${manFile.replace(/\.json$/, ".result.json")}`);
    if (!flag.has("--keep-wav")) { for (const g of man.groups) fs.rmSync(g.wav, { force: true }); fs.rmSync(mix, { force: true }); }
  } finally {
    if (session) await session.close();
    await kit.close();
  }
}
