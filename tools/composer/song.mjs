// Claude Code から作曲ソフトを使うための道具（APIキーはいらない。曲は Claude Code 自身が書く）。
// 同じことは、コネクタ（MCPサーバー、tools/mcp/server.mjs）からもできる。
//
//   node tools/composer/song.mjs guide
//       AIソング形式の説明（楽器の一覧・書き方・よい曲にするコツ）を表示する。曲を書く前に読む。
//   node tools/composer/song.mjs genre <曲調> [--key F] [--major] [--bpm 140] [--seed 1] [--name <英小文字>] [--out <フォルダ>] [--edition real|ps2|modern] [--wav] [--register <曲ID> --scene "<場面>"]
//       最新ジャンル（trap・drill・lofi・futurebass・hyperpop・synthwave・citypop・house・techno・trance・dnb・dubstep・ukgarage・amapiano・reggaeton・vaporwave・hardstyle・jerseyclub・poppunk・bedroompop・nudisco・trailer）の曲を、型から組み立てて書き出す。
//   node tools/composer/song.mjs build <曲.json> [--out <フォルダ>] [--edition real|ps2|modern] [--wav] [--register <曲ID> --scene "<場面>"]
//       AIソング形式のJSONを確かめて、作曲ソフトで開けるプロジェクト（.sunshine-song.json）とMIDIを書き出す。
//       --wav: 作曲ソフトと同じ音（録音音源・アンプ・仕上げ）でWAVも作る（Playwright と Chromium が必要）。
//       --register: ゲームの曲として src/audio/songs/<曲ID>.sunshine-song.json に登録する。
import fs from "fs";
import path from "path";
import { openSongKit } from "./song-lib.mjs";

const args = process.argv.slice(2);
const opt = (name) => {
  const i = args.indexOf(name);
  return i >= 0 ? args[i + 1] : undefined;
};

const kit = await openSongKit();
try {
  if (args[0] === "guide") {
    console.log(await kit.guide());
    console.log("\n## 見本\nassets-src/ai-songs/ にある .json を見てください。");
  } else if (args[0] === "genre" && args[1]) {
    try {
      const style = args[1];
      const name = (opt("--name") ?? `${style}-${opt("--seed") ?? 1}`).toLowerCase().replace(/[^a-z0-9-]+/g, "-");
      const r = await kit.buildGenre({ style, tonic: opt("--key") ?? "C", minor: !args.includes("--major"), bpm: Number(opt("--bpm") ?? 0), seed: Number(opt("--seed") ?? 1), title: opt("--title") }, { name, edition: opt("--edition") ?? "real", outDir: opt("--out"), wav: args.includes("--wav") });
      console.log(`○ 「${r.title}」 ${r.tracks}トラック・${Math.floor(r.seconds / 60)}分${Math.round(r.seconds % 60)}秒・テンポ${r.bpm}`);
      console.log("  プロジェクト:", r.files.project);
      console.log("  MIDI:", r.files.midi);
      if (r.files.wav) console.log("  WAV:", r.files.wav);
      const id = opt("--register");
      if (id) console.log("  ゲームに登録:", await kit.register(r.score, { id, title: r.title, scene: opt("--scene") ?? "" }));
    } catch (e) {
      console.error("× " + e.message);
      process.exitCode = 1;
    }
  } else if (args[0] === "build" && args[1]) {
    try {
      const name = path.basename(args[1]).replace(/\.json$/i, "").toLowerCase().replace(/[^a-z0-9-]+/g, "-");
      const r = await kit.build(JSON.parse(fs.readFileSync(args[1], "utf8")), { name, edition: opt("--edition") ?? "real", outDir: opt("--out"), wav: args.includes("--wav") });
      for (const w of r.warnings) console.warn("注意:", w);
      console.log(`○ 「${r.title}」 ${r.tracks}トラック・${Math.floor(r.seconds / 60)}分${Math.round(r.seconds % 60)}秒・テンポ${r.bpm}`);
      console.log("  プロジェクト:", r.files.project, "（作曲ソフトの「プロジェクトを読み込む」で開ける）");
      console.log("  MIDI:", r.files.midi);
      if (r.files.wav) console.log("  WAV:", r.files.wav);
      const id = opt("--register");
      if (id) console.log("  ゲームに登録:", await kit.register(r.score, { id, title: r.title, scene: opt("--scene") ?? "" }));
    } catch (e) {
      console.error("× 曲を組み立てられませんでした。直してから、もう一度 build してください:\n" + e.message);
      process.exitCode = 1;
    }
  } else {
    console.log(fs.readFileSync(new URL(import.meta.url), "utf8").split("\n").filter((l) => l.startsWith("//")).map((l) => l.slice(3)).join("\n"));
    process.exitCode = 1;
  }
} finally {
  await kit.close();
}
