// Claude Code から作曲ソフトを使うための道具（APIキーはいらない。曲は Claude Code 自身が書く）。
// 同じことは、コネクタ（MCPサーバー、tools/mcp/server.mjs）からもできる。
//
//   node tools/composer/song.mjs guide
//       AIソング形式の説明（楽器の一覧・書き方・よい曲にするコツ）を表示する。曲を書く前に読む。
//   node tools/composer/song.mjs build <曲.json> [--out <フォルダ>] [--edition real|ps2|modern] [--wav] [--register <曲ID> --scene "<場面>"]
//       AIソング形式のJSONを確かめて、作曲ソフトで開けるプロジェクト（.sunshine-song.json）とMIDIを書き出す。
//       --bass finger|pick|rock|metal|jazz|jpop: ベースを FreePats のエレキベースの音源に。--sound punk-run|clear-guitar-rock: サウンドセット（アンプ・音量・ミックス・ドラム・使う音源をまとめて当てはめる。--bass/--drums/--guitar を別に書けばそちらが優先）。--master-preset <名前>: 書き出しの仕上げ（大きさ・広がり・圧縮・EQ・天井）をまとめて決める。従来の 4 つ game=-14LUFS・rock=-10・loud=-8・calm=-16 のほか、ジャンル別の metal・punk・rock-clean・pop・jazz・orch・edm・hiphop・lofi・ambient・wafu・solo と、ゲーム用の game-field・game-battle・game-boss・game-dungeon・retro（`node tools/composer/song.mjs presets` で一覧）。--space hall|room|plate: 書き出しのWAVに畳み込みリバーブ（自作のIR）を足す。--space-wet 0〜1（既定0.25）が残響の量。--widen 1.8: 書き出しのWAVの左右の広がりを広げる（1=そのまま。master と一緒に使う。おすすめ 1.5〜2）。--master -9: 書き出しのWAVの大きさ（LUFS）をそろえる（サウンドセットに master があれば自動。ピークは約 -1.5dB 以下）。--guitar gretsch|hofner: ジャズギター(26)・クリーンギター(27)を Karoryfer の生ギター（CC0）に。--drums muldjord|rock|metal|jazz|jpop|supra: ドラムを生ドラム（Muldjord Kit）に（省略は標準）。
//       仕上げの細かい指定（プリセットの値を上書き。--master 系と一緒に使う）: --tp -1.5: 真のピークの天井(dBTP)。--lowmono 140: この周波数(Hz)より下をモノに（0=切る）。--side-hpf 150: サイドだけをこの周波数より上に（M/S ワイド。--widen がサイドの倍率 slev になる）。--clip 1.5: ソフトクリップに使うゲイン(dB、0=なし)。--hpf 25・--lpf 19000: 掃除(Hz)。--match-eq rock|punk|edm|hiphop|jazz|lofi|ambient|game-battle: 帯域の量を家族別の目標の傾き（docs/sound/data/mix-targets.json。数字だけ）に寄せるマッチング EQ（--match-amount 0.4: 強さ。0.5 が上限、各帯域 ±3dB で切る）。--loop-tail: 曲の長さより後ろの残響の尾を先頭に重ねる（ループの継ぎ目をなじませる。仕上げの前）。
//       書き出した WAV は、最後に 1 行の合否表（○／要直し: I・TP・LRA・PLR・PSR・左右の相関・100Hz 以下の相関・継ぎ目）を表示する。サウンドセット（--sound）の master に preset・space・spaceWet があれば、同じ引数を書いたことになる（引数が優先）。
//   node tools/composer/song.mjs report <WAV> [--lufs -14] [--tp -1.5] [--no-loop]
//       すでにある WAV の合否表だけを表示する（ループの継ぎ目も見る。ループしない曲は --no-loop）。
//   node tools/composer/song.mjs presets
//       書き出しの仕上げのプリセット一覧（大きさ・天井・広がり・圧縮・EQ）を表示する。
//   node tools/composer/song.mjs delays <BPM>
//       BPM に同期した 1/4・付点1/8・1/8・3連・1/16 の長さ（秒）と、残響の長さの目安、duck の戻りの時間を表示する。
//       --soundfont gu: WAVを GeneralUser GS の音源で作る（省略はゲームと同じ FluidR3）。
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

const num = (name) => (opt(name) === undefined ? null : Number(opt(name)));

if (args[0] === "report" && args[1]) {
  const { masterReport } = await import("./master-report.mjs");
  console.log(masterReport(args[1], { lufs: num("--lufs"), tp: num("--tp") ?? -1.5, loop: !args.includes("--no-loop") }).line);
  process.exit(0);
}
if (args[0] === "presets") {
  const { MASTER_PRESETS, MASTER_PRESET_ALIASES } = await import("./master.mjs");
  for (const [id, p] of Object.entries(MASTER_PRESETS)) console.log(`${id.padEnd(13)} ${String(p.lufs).padStart(5)}LUFS  天井 ${p.tp ?? -1.5}  広がり ${p.widen}${p.sideHpf ? `(M/S, サイド HPF ${p.sideHpf})` : "(extrastereo)"}  低域モノ ${p.lowmono ?? 140}Hz  圧縮 ${p.glue ?? "normal"}${p.clip ? `  クリップ ${p.clip}dB` : ""}${p.mb ? "  低域マルチバンド" : ""}${p.hpf ? `  HPF ${p.hpf}` : ""}${p.lpf ? `  LPF ${p.lpf}` : ""}${p.tilt ? `  ティルト ${p.tilt}dB/oct` : ""}${p.eq ? `  EQ ${p.eq.map((e) => `${e.type}${e.f}:${e.g > 0 ? "+" : ""}${e.g}`).join(",")}` : ""}`);
  console.log("別名: " + Object.entries(MASTER_PRESET_ALIASES).map(([a, b]) => `${a}→${b}`).join("  "));
  process.exit(0);
}
if (args[0] === "delays" && args[1]) {
  const bpm = Number(args[1]);
  const kitTools = await openSongKit();
  try {
    const mod = await kitTools.mixTools();
    const t = mod.syncDelaySeconds(bpm);
    const ms = (v) => `${(v * 1000).toFixed(1)}ms`;
    console.log(`BPM ${bpm}: 1/4=${ms(t.quarter)}  付点1/8=${ms(t.dottedEighth)}  1/8=${ms(t.eighth)}  1/8の3連=${ms(t.eighthTriplet)}  1/16=${ms(t.sixteenth)}  1小節=${t.bar.toFixed(3)}秒`);
    const rv = mod.reverbDecayHint(bpm);
    console.log(`残響の長さの目安: ${rv.min}〜${rv.max}秒　duck の戻り: 約${mod.duckRecoverMs(bpm)}ms`);
  } finally {
    await kitTools.close();
  }
  process.exit(0);
}

const kit = await openSongKit();
try {
  if (args[0] === "guide") {
    console.log(await kit.guide());
    console.log("\n## 見本\nassets-src/ai-songs/ にある .json を見てください。");
  } else if (args[0] === "sounds") {
    const { SOUND_SETS } = await kit.soundSets();
    for (const s of Object.values(SOUND_SETS)) console.log(`${s.id}\t${s.label}\n  ${s.description}\n  音源: ベース ${s.overlays.bass}・ドラム ${s.overlays.drums}・ギター ${s.overlays.guitar}${s.tempoHint ? `　目安テンポ ${s.tempoHint[0]}〜${s.tempoHint[1]}` : ""}`);
  } else if (args[0] === "build" && args[1]) {
    try {
      const name = path.basename(args[1]).replace(/\.json$/i, "").toLowerCase().replace(/[^a-z0-9-]+/g, "-");
      const r = await kit.build(JSON.parse(fs.readFileSync(args[1], "utf8")), { name, edition: opt("--edition") ?? "real", outDir: opt("--out"), wav: args.includes("--wav"), soundfont: opt("--soundfont") === "gu" ? "gu" : "game", bass: opt("--bass") ?? "std", drums: opt("--drums") ?? "std", guitar: opt("--guitar") ?? "std", sound: opt("--sound") ?? "", master: opt("--master") === undefined ? null : Number(opt("--master")), widen: opt("--widen") === undefined ? null : Number(opt("--widen")), space: opt("--space") ?? "", masterPreset: opt("--master-preset") ?? "", spaceWet: num("--space-wet"), tp: num("--tp"), lowmono: num("--lowmono"), sideHpf: num("--side-hpf"), clip: num("--clip"), hpf: num("--hpf"), lpf: num("--lpf"), matchEq: opt("--match-eq") ?? "", matchAmount: num("--match-amount"), loopTail: args.includes("--loop-tail") });
      for (const w of r.warnings) console.warn("注意:", w);
      console.log(`○ 「${r.title}」 ${r.tracks}トラック・${Math.floor(r.seconds / 60)}分${Math.round(r.seconds % 60)}秒・テンポ${r.bpm}`);
      console.log("  プロジェクト:", r.files.project, "（作曲ソフトの「プロジェクトを読み込む」で開ける）");
      console.log("  MIDI:", r.files.midi);
      if (r.files.wav) console.log("  WAV:", r.files.wav);
      if (r.report) console.log("  仕上がり:", r.report);
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
