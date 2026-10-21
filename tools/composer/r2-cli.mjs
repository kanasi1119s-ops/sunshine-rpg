// 形式・ゲーム内の使い方の道具（docs/sound/form-structure-guide.md §12・game-music-guide.md §10）。
//   node tools/composer/song.mjs phone-check <曲.wav>        … スマホのスピーカーで聞こえ方を確かめる（帯域を絞り、モノにして、低音の倍音を見る）
//   node tools/composer/song.mjs suite-check <組曲.json>     … 組曲のテンポ比・調の関係・つなぎ・強さの曲線を点検
//   node tools/composer/song.mjs type-check <曲.json> [--vs 曲名,曲名]  … 導入・終わりの型が直前の曲と同じでないか
//   node tools/composer/song.mjs motif-ledger [--write]      … 主題の台帳（docs/sound/motif-ledger.md）を出す・書く
//   node tools/composer/song.mjs loop-report <曲.json>       … ループ点の点検
// vite で TypeScript を読み込む。扱ったら true を返す。
import { fileURLToPath } from "url";
import fs from "fs";
import path from "path";
import { createServer } from "vite";

const ROOT = path.resolve(fileURLToPath(new URL("../../", import.meta.url)));
const CMDS = ["phone-check", "suite-check", "type-check", "motif-ledger", "loop-report"];

export async function runR2Command(args) {
  const cmd = args[0];
  if (!CMDS.includes(cmd)) return false;
  const opt = (n) => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : undefined; };
  const server = await createServer({ root: ROOT, configFile: false, logLevel: "silent", server: { middlewareMode: true, hmr: false, watch: null }, appType: "custom" });
  const load = (p) => server.ssrLoadModule(p);
  const songDir = path.join(ROOT, "assets-src/ai-songs");
  const readSongJson = (name) => {
    const f = fs.existsSync(name) ? name : path.join(songDir, name.replace(/\.json$/, "") + ".json");
    return fs.existsSync(f) ? JSON.parse(fs.readFileSync(f, "utf8")) : null;
  };
  try {
    if (cmd === "phone-check") {
      const m = await load("/src/audio/phone-check.ts");
      const { channels, sampleRate } = m.readWavPcm16(new Uint8Array(fs.readFileSync(args[1])));
      console.log(m.formatPhoneReport(m.phoneCheck(channels, sampleRate), path.basename(args[1])));
    } else if (cmd === "suite-check") {
      const m = await load("/src/audio/suite-check.ts");
      const def = JSON.parse(fs.readFileSync(args[1], "utf8"));
      console.log(m.formatSuiteReport(def.name ?? path.basename(args[1]), m.checkSuite(def, readSongJson)));
    } else if (cmd === "type-check") {
      const m = await load("/src/audio/type-check.ts");
      const name = path.basename(args[1]).replace(/\.json$/, "");
      const cur = readSongJson(args[1]);
      const fromTable = m.readTrackTypes(fs.readFileSync(path.join(ROOT, "docs/sound/tracks.md"), "utf8"));
      const vs = (opt("--vs") ?? "").split(",").filter(Boolean);
      const recent = fromTable.filter((t) => vs.length === 0 || vs.includes(t.name)).slice(-3);
      const w = m.typeWarnings({ name, introType: cur.introType, outroType: cur.outroType, song: cur }, recent);
      console.log(w.length ? w.map((x) => "注意: " + x).join("\n") : "○ 導入・終わりの型は直前の曲と重なっていません");
    } else if (cmd === "motif-ledger") {
      const m = await load("/src/audio/motif.ts");
      const songs = fs.existsSync(songDir) ? fs.readdirSync(songDir).filter((f) => f.endsWith(".json")).map((f) => ({ name: f.replace(/\.json$/, ""), uses: m.motifUses(JSON.parse(fs.readFileSync(path.join(songDir, f), "utf8"))) })) : [];
      const md = m.ledgerMarkdown(songs);
      if (args.includes("--write")) { fs.writeFileSync(path.join(ROOT, "docs/sound/motif-ledger.md"), md); console.log("書きました: docs/sound/motif-ledger.md"); }
      else console.log(md);
      for (const w of m.checkLedger(songs)) console.warn("注意:", w);
    } else if (cmd === "loop-report") {
      const kit = await load("/src/audio/ai-song.ts");
      const song = readSongJson(args[1]);
      const score = kit.aiSongToScore(song);
      const seam = (await load("/src/audio/loop-check.ts")).checkScoreSeam(score);
      console.log(JSON.stringify(score.meta?.loop ?? null));
      console.log(seam.length ? seam.map((x) => "注意: " + x).join("\n") : "○ ループの継ぎ目に問題は見つかりませんでした");
    }
  } finally { await server.close(); }
  return true;
}
