// Claude Code から作曲ソフトを使うための道具（APIキーはいらない。曲は Claude Code 自身が書く）。
// 同じことは、コネクタ（MCPサーバー、tools/mcp/server.mjs）からもできる。
//
//   node tools/composer/song.mjs guide
//       AIソング形式の説明（楽器の一覧・書き方・よい曲にするコツ）を表示する。曲を書く前に読む。
//   node tools/composer/song.mjs noise <WAV> [--vocal] [--notes 歌.py] [--bpm N]  … 雑音の検知（音割れ・直流・超低域・プチッ、歌はボッ・サー・ジリッ・ザッも）
//   node tools/composer/song.mjs build <曲.json> [--stems] [--out <フォルダ>] [--edition real|ps2|modern] [--wav] [--register <曲ID> --scene "<場面>"]
//       AIソング形式のJSONを確かめて、作曲ソフトで開けるプロジェクト（.sunshine-song.json）とMIDIを書き出す。
//       --bass finger|pick|rock|metal|jazz|jpop: ベースを FreePats のエレキベースの音源に。--sound punk-run|clear-guitar-rock|rock-4|pop-lead|jpop-bright|ballad-piano-strings|jazz-trio|funk-bass|house-duck|ambient-wide|orchestra-depth|game-battle|game-boss|game-town|game-dungeon（`sounds` で一覧）: サウンドセット（アンプ・音量・ミックス・ドラム・使う音源をまとめて当てはめる。--bass/--drums/--guitar を別に書けばそちらが優先）。--master-preset <名前>: 書き出しの仕上げ（大きさ・広がり・圧縮・EQ・天井）をまとめて決める。従来の 4 つ game=-14LUFS・rock=-10・loud=-8・calm=-16 のほか、ジャンル別の metal・punk・rock-clean・pop・jazz・orch・edm・hiphop・lofi・ambient・wafu・solo と、ゲーム用の game-field・game-battle・game-boss・game-dungeon・retro（`node tools/composer/song.mjs presets` で一覧）。--space hall|room|plate: 書き出しのWAVに畳み込みリバーブ（自作のIR）を足す。--space-wet 0〜1（既定0.25）が残響の量。--widen 1.8: 書き出しのWAVの左右の広がりを広げる（1=そのまま。master と一緒に使う。おすすめ 1.5〜2）。--master -9: 書き出しのWAVの大きさ（LUFS）をそろえる（サウンドセットに master があれば自動。ピークは約 -1.5dB 以下）。--orchestra vsco: 弦・金管・木管・ティンパニ・ハープ・マリンバ・オルガンを VSCO 2 CE（CC0）の録音に。--piano salamander: ピアノを Salamander Grand Piano（CC BY 3.0）に。--guitar gretsch|hofner: ジャズギター(26)・クリーンギター(27)を Karoryfer の生ギター（CC0）に。--drums muldjord|rock|metal|jazz|jpop|supra: ドラムを生ドラム（Muldjord Kit）に（省略は標準）。
//       仕上げの細かい指定（プリセットの値を上書き。--master 系と一緒に使う）: --tp -1.5: 真のピークの天井(dBTP)。--lowmono 140: この周波数(Hz)より下をモノに（0=切る）。--side-hpf 150: サイドだけをこの周波数より上に（M/S ワイド。--widen がサイドの倍率 slev になる）。--clip 1.5: ソフトクリップに使うゲイン(dB、0=なし)。--hpf 25・--lpf 19000: 掃除(Hz)。--match-eq rock|punk|edm|hiphop|jazz|lofi|ambient|game-battle: 帯域の量を家族別の目標の傾き（docs/sound/data/mix-targets.json。数字だけ）に寄せるマッチング EQ（--match-amount 0.4: 強さ。0.5 が上限、各帯域 ±3dB で切る）。--loop-tail: 曲の長さより後ろの残響の尾を先頭に重ねる（ループの継ぎ目をなじませる。仕上げの前）。
//       書き出した WAV は、最後に 1 行の合否表（○／要直し: I・TP・LRA・PLR・PSR・左右の相関・100Hz 以下の相関・継ぎ目）を表示する。サウンドセット（--sound）の master に preset・space・spaceWet があれば、同じ引数を書いたことになる（引数が優先）。
//   node tools/composer/song.mjs report <WAV> [--lufs -14] [--tp -1.5] [--no-loop] [--genre <ジャンル名> --bpm N]（flat・空気も出す。--genre でジャンル目安からの外れも添える）
//       すでにある WAV の合否表だけを表示する（ループの継ぎ目も見る。ループしない曲は --no-loop）。
//   node tools/composer/song.mjs presets
//       書き出しの仕上げのプリセット一覧（大きさ・天井・広がり・圧縮・EQ）を表示する。
//   node tools/composer/song.mjs delays <BPM>
//       BPM に同期した 1/4・付点1/8・1/8・3連・1/16 の長さ（秒）と、残響の長さの目安、duck の戻りの時間を表示する。
//       --genre rock|metal|jazz|funk|trap|house|dnb|reggae|bossa|…（drum-genres.ts のジャンル名）: そのジャンルの drumMix・swing・human の推奨値と、ドラム音源（--drums）・ベース音源（--bass）をまとめて決める（--drums/--bass を別に書けばそちらが優先）。
//       --soundfont gu: WAVを GeneralUser GS の音源で作る（省略はゲームと同じ FluidR3）。
//       --wav: 作曲ソフトと同じ音（録音音源・アンプ・仕上げ）でWAVも作る（Playwright と Chromium が必要）。
//       --register: ゲームの曲として src/audio/songs/<曲ID>.sunshine-song.json に登録する。
//   node tools/composer/song.mjs sfx [<id>] [--wav] [--out <フォルダ>] [--key 2:aeolian]
//       合成の効果音（src/audio/sfx-recipes.ts の 58 種）を描いて、山・RMS・長さ・立ち上がり・重心・検査を表示する。id を省くと一覧と全件の検査。
//       --wav で WAV を書く（既定は tmp/sfx/）。--key は「主音(0〜11):音階名」で ※調 の層をその音階へ寄せる。画面で聞き比べるなら dist-composer/sfx-lab.html。
//   曲作りの流れの道具（docs/sound/ai-composition-workflow.md）:
//   node tools/composer/song.mjs plan-template                       … 曲の設計図（属性カードとセクション表）の雛形を表示
//   node tools/composer/song.mjs plan-check <plan.json> [曲.json]     … 設計図の検査（強さカーブ・音域表・曲との食い違い）
//   旋律・対位法の道具: motif（動機の変形）・pattern（旋律の型の下書き）・counter（対旋律）・canon（カノン）・pedal（保持音）。詳しくは craft-cli.mjs の先頭
//   node tools/composer/song.mjs novelty <曲.json> [--n 3] [--vs 曲名,曲名]  … 直前の曲と調・進行・入り方・終わり方・旋律の輪郭が同じでないか
//   node tools/composer/song.mjs inspect <曲.json> [--aes] [--bass ... --drums ... --guitar ...]  … 楽器の種類ごとに音を分けて、大きさ・帯域・重心・出だしの硬さ・プチッ・ぶつかり（・--aes で楽器ごとの点数）を測る
//   node tools/composer/song.mjs automix <曲.json> [--loop [N]] [--apply [出力.json]] ...  … パートごとに数字で測って、volume／gainDb・pan・duck・EQ を調整（元の曲は変えない）。最後に全体を測って preset を提案。使い方は引数なしで表示、詳しくは docs/sound/band-ensemble/auto-mix.md
//   node tools/composer/song.mjs gate <曲.wav> [--genre <ジャンル名>|--song <曲.json>] [--bpm N] ...  … ジャンル別の目標（genre-targets.mjs）で判定。 genre-target <ジャンル名> [--bpm N] … 目標の幅を出す
//   node tools/composer/song.mjs gate <曲.wav> [--target -14] [--save 曲ID] [--json]  … LUFS・真のピーク・LRA・PLR・相関・頭の大きさ・無音の合否表（○／要直し）
//   node tools/composer/song.mjs gate-compare <曲.wav> <基準.wav>    … 音量をそろえてから帯域ごとの差を出す
//   node tools/composer/song.mjs log <曲ID> --before .. --change .. --after .. --ear ..  … 直しの記録を1行残す（docs/sound/revisions.md）
//   node tools/audio-check/score-check.mjs <曲.json> --facts [--json]  … 楽譜の点検を、小節番号つきの事実の一覧で出す（アヴォイドノートなど）
//   node tools/composer/chord-pick.mjs --scene battle --avoid-last 3  … 場面に合って直近の曲と違う進行の候補を出す
import fs from "fs";
import path from "path";
import { openSongKit, ROOT } from "./song-lib.mjs";
import { runWorkflowCommand } from "./workflow-cli.mjs";
import { runCraftCommand } from "./craft-cli.mjs";
import { revisionReminder } from "./revision-log.mjs";
import { runR2Command } from "./r2-cli.mjs";

const args = process.argv.slice(2);
const opt = (name) => {
  const i = args.indexOf(name);
  return i >= 0 ? args[i + 1] : undefined;
};

const num = (name) => (opt(name) === undefined ? null : Number(opt(name)));

if (args[0] === "report" && args[1]) {
  const { masterReport } = await import("./master-report.mjs");
  console.log(masterReport(args[1], { lufs: num("--lufs"), tp: num("--tp") ?? -1.5, loop: !args.includes("--no-loop"), genre: opt("--genre") ?? null, bpm: num("--bpm") ?? NaN }).line);
  process.exit(0);
}
if (args[0] === "noise" && args[1]) {
  // 雑音の検知（tools/audio-check/noise-check.py）。歌だけの WAV は --vocal（と --notes 歌.py --bpm N）
  const { execFileSync } = await import("child_process");
  const py = new URL("../audio-check/noise-check.py", import.meta.url).pathname;
  const rest = args.slice(2);
  process.stdout.write(execFileSync("python3", [py, args[1], ...rest], { encoding: "utf8", maxBuffer: 1 << 26 }));
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
// 楽器ごとの点検（楽器の種類ごとに音を分けて、帯域・重心・硬さ・プチッ・ぶつかり・点数を測る。tools/composer/inspect.mjs）
if (args[0] === "inspect") {
  const { runInspect } = await import("./inspect.mjs");
  await runInspect(args.slice(1));
  process.exit(process.exitCode ?? 0);
}
// 自動ミックス（パート別に数字で測って調整。tools/composer/automix.mjs）
if (args[0] === "automix") {
  const { runAutomix } = await import("./automix.mjs");
  await runAutomix(args.slice(1));
  process.exit(process.exitCode ?? 0);
}
// 曲作りの流れの道具（gate・plan-check・novelty など）は、vite を起動せずに先に処理する
if (await runWorkflowCommand(args)) process.exit(process.exitCode ?? 0);
// 旋律・対位法の道具（motif・pattern・counter・canon・pedal。craft-cli.mjs）
if (await runCraftCommand(args)) process.exit(process.exitCode ?? 0);
if (await runR2Command(args)) process.exit(process.exitCode ?? 0);

const kit = await openSongKit();
try {
  if (args[0] === "guide") {
    console.log(await kit.guide());
    console.log("\n## 見本\nassets-src/ai-songs/ にある .json を見てください。");
  } else if (args[0] === "sfx") {
    const { SFX_RECIPES, SFX_BY_ID } = await kit.load("/src/audio/sfx-recipes.ts");
    const { inspectSe, tuneSe, SE_MAX_SEC } = await kit.load("/src/audio/sfx-synth.ts");
    const { toWav16 } = await kit.load("/src/audio/synth-dsp.ts");
    const key = opt("--key");
    const fix = (r) => (key ? tuneSe(r, Number(key.split(":")[0]), key.split(":")[1] ?? "ionian") : r);
    const one = (r, wav) => {
      const { analysis: a, warnings, samples } = inspectSe(fix(r), 44100);
      console.log(`${r.id}\t${r.name}\t${r.kind}\t山 ${a.peakDb.toFixed(1)}dBFS\tRMS ${a.rmsDb.toFixed(1)}dB\t長さ ${a.lengthSec.toFixed(2)}秒（上限 ${SE_MAX_SEC[r.kind]}）\t立ち上がり ${a.attackMs.toFixed(0)}ms\t重心 ${a.centroidHz.toFixed(0)}Hz`);
      for (const w of warnings) console.log("  要直し: " + w);
      if (wav) {
        const dir = path.resolve(opt("--out") ?? ROOT + "tmp/sfx");
        fs.mkdirSync(dir, { recursive: true });
        fs.writeFileSync(path.join(dir, r.id + ".wav"), toWav16(samples, 44100));
        console.log("  書き出し: " + path.join(dir, r.id + ".wav"));
      }
      return warnings.length;
    };
    if (args[1] && !args[1].startsWith("--")) {
      const r = SFX_BY_ID[args[1]];
      if (!r) { console.error("そのidはありません。node tools/composer/song.mjs sfx で一覧を見てください。"); process.exitCode = 1; }
      else one(r, args.includes("--wav"));
    } else {
      let bad = 0;
      for (const r of SFX_RECIPES) bad += one(r, args.includes("--wav"));
      console.log(bad ? `要直し ${bad} 件` : `${SFX_RECIPES.length} 種すべて問題なし`);
    }
  } else if (args[0] === "sounds") {
    const { SOUND_SETS } = await kit.soundSets();
    for (const s of Object.values(SOUND_SETS)) console.log(`${s.id}\t${s.label}\n  ${s.description}\n  音源: ベース ${s.overlays.bass}・ドラム ${s.overlays.drums}・ギター ${s.overlays.guitar}${s.overlays.orchestra ? `・オーケストラ ${s.overlays.orchestra}` : ""}${s.overlays.piano ? `・ピアノ ${s.overlays.piano}` : ""}${s.tempoHint ? `　目安テンポ ${s.tempoHint[0]}〜${s.tempoHint[1]}` : ""}`);
  } else if (args[0] === "build" && args[1]) {
    try {
      const name = path.basename(args[1]).replace(/\.json$/i, "").toLowerCase().replace(/[^a-z0-9-]+/g, "-");
      if (args.includes("--stems")) {
        // 楽器ごとの音（ステム）を別々の WAV に書き出す: ドラム・ベース・ギター・その他。仕上げ（--master 系）は付けず、音量の比率はそのまま
        const STEM_GROUPS = { drums: ["kick", "snare", "hihat", "crash", "tom"], bass: ["bass", "slap", "sub808"], guitar: ["guitar", "distGuitar", "leadGuitar", "crunch", "echoGuitar"] };
        const base = JSON.parse(fs.readFileSync(args[1], "utf8"));
        if (base.autoAccompaniment) console.warn("注意: autoAccompaniment: true の曲は、自動の伴奏を楽器ごとに分けられません。手書きのパートだけが分かれます（伴奏も分けたいときは false にして、パートを書く）");
        const groupOf = (inst) => Object.entries(STEM_GROUPS).find(([, l]) => l.includes(inst))?.[0] ?? "other";
        const names = [...new Set((base.parts ?? []).map((p) => groupOf(p.instrument)))];
        for (const g of names) {
          const sub = { ...base, autoAccompaniment: false, parts: base.parts.filter((p) => groupOf(p.instrument) === g) };
          const stemName = `${name}-stem-${g}`;
          const rr = await kit.build(sub, { name: stemName, edition: opt("--edition") ?? "real", outDir: opt("--out"), wav: true, soundfont: opt("--soundfont") === "gu" ? "gu" : "game", bass: opt("--bass") ?? "std", drums: opt("--drums") ?? "std", guitar: opt("--guitar") ?? "std", orchestra: opt("--orchestra") ?? "std", piano: opt("--piano") ?? "std", autoRetune: false });
          console.log(`  ステム ${g}: ${rr.files.wav}`);
        }
      }
      const r = await kit.build(JSON.parse(fs.readFileSync(args[1], "utf8")), { name, edition: opt("--edition") ?? "real", outDir: opt("--out"), wav: args.includes("--wav"), soundfont: opt("--soundfont") === "gu" ? "gu" : "game", bass: opt("--bass") ?? "std", drums: opt("--drums") ?? "std", guitar: opt("--guitar") ?? "std", orchestra: opt("--orchestra") ?? "std", piano: opt("--piano") ?? "std", sound: opt("--sound") ?? "", master: Number.isFinite(Number(opt("--master"))) && opt("--master") !== undefined ? Number(opt("--master")) : null, widen: opt("--widen") === undefined ? null : Number(opt("--widen")), space: opt("--space") ?? "", masterPreset: opt("--master-preset") ?? "", spaceWet: num("--space-wet"), tp: num("--tp"), lowmono: num("--lowmono"), sideHpf: num("--side-hpf"), clip: num("--clip"), hpf: num("--hpf"), lpf: num("--lpf"), matchEq: opt("--match-eq") ?? "", matchAmount: num("--match-amount"), loopTail: args.includes("--loop-tail"), genre: opt("--genre") ?? "", autoRetune: !args.includes("--no-retune") });
      for (const w of r.warnings) console.warn("注意:", w);
      console.log(`○ 「${r.title}」 ${r.tracks}トラック・${Math.floor(r.seconds / 60)}分${Math.round(r.seconds % 60)}秒・テンポ${r.bpm}`);
      console.log("  プロジェクト:", r.files.project, "（作曲ソフトの「プロジェクトを読み込む」で開ける）");
      console.log("  MIDI:", r.files.midi);
      if (r.files.wav) console.log("  WAV:", r.files.wav);
      if (r.report) console.log("  仕上がり:", r.report);
      const reminder = revisionReminder(ROOT, name);
      if (reminder) console.log("  " + reminder);
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
