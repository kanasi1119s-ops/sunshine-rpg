// song.mjs から呼ばれる、旋律・対位法の道具のコマンド（motif・pattern・counter・canon・pedal）。
// vite を起動しない軽い処理なので、song.mjs の本体（openSongKit）より先に処理する。扱ったら true を返す。
//   node tools/composer/song.mjs motif <shift|semitone|invert|retro|augment|diminish|fragment|thin|ornament> "<動機>" [...]   … 動機の変形（motif-ops.mjs）
//   node tools/composer/song.mjs pattern --scene 町 --key D [--beats 4] [--record <曲ID>]                               … 旋律の型の下書き（melody-patterns.mjs）
//   node tools/composer/song.mjs counter <曲.json> [--part 番号] [--above] [--enter 小節] [--instrument strings]          … 対旋律を1本つくる（counterpoint.mjs）
//   node tools/composer/song.mjs canon "<notes>" --delay 4 [--transpose 7] [--invert] [--factor 2]                       … カノン（遅れて入る模倣）のパート
//   node tools/composer/song.mjs pedal "C Am F G" [--degree root|fifth] [--beats 4] [--octave 2]                          … 保持音（ペダル）の列
import fs from "fs";
import { runMotifCommand } from "./motif-ops.mjs";
import { runPatternCommand } from "./melody-patterns.mjs";
import { generateCounter, counterEntering, canonOf } from "./counterpoint.mjs";
import { prepareForCheck, barChords, melodyParts, expand } from "../audio-check/score-lib.mjs";
import { pedalLine } from "../audio-check/voice-lint.mjs";

export const CRAFT_COMMANDS = ["motif", "pattern", "counter", "canon", "pedal"];

export async function runCraftCommand(args) {
  const cmd = args[0];
  if (!CRAFT_COMMANDS.includes(cmd)) return false;
  const opt = (n, d) => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : d; };
  try {
    if (cmd === "motif") console.log(runMotifCommand(args.slice(1)));
    else if (cmd === "pattern") console.log(runPatternCommand(args));
    else if (cmd === "canon") {
      if (!args[1]) throw new Error("使い方: song.mjs canon \"<notes>\" --delay 4 [--transpose 7] [--invert] [--factor 2] [--total 拍]");
      console.log(canonOf(args[1], { delay: Number(opt("--delay", 0)), transpose: Number(opt("--transpose", 0)), invert: args.includes("--invert"), factor: Number(opt("--factor", 1)), total: opt("--total") === undefined ? undefined : Number(opt("--total")) }));
    } else if (cmd === "pedal") {
      if (!args[1]) throw new Error("使い方: song.mjs pedal \"C Am F G\" [--degree root|fifth] [--beats 4] [--octave 2]");
      const r = pedalLine(args[1].split(/[\s|]+/).filter(Boolean), { degree: opt("--degree", "root"), beats: Number(opt("--beats", 4)), octave: Number(opt("--octave", 2)) });
      console.log(r.notes);
      for (const w of r.warnings) console.log(`注意: ${w}`);
    } else if (cmd === "counter") {
      if (!args[1]) throw new Error("使い方: song.mjs counter <曲.json> [--part 番号] [--above] [--enter 小節] [--instrument strings]");
      const song = await prepareForCheck(JSON.parse(fs.readFileSync(args[1], "utf8")));
      const beats = Number(song.beats) || 4;
      const chords = barChords(song);
      const total = chords.length * beats;
      const idx = opt("--part");
      const part = idx !== undefined ? song.parts[Number(idx)] : melodyParts(song, (p) => expand(p, total))[0];
      if (!part) throw new Error("旋律のパートが見つかりません（--part 番号 で指定）");
      const place = args.includes("--above") ? "above" : "below";
      const instrument = opt("--instrument", "strings");
      const res = opt("--enter") !== undefined
        ? counterEntering(part.notes, chords, { beats, enterBar: Number(opt("--enter")) - 1, instrument, place })
        : { instrument, role: "対旋律", notes: generateCounter(part.notes, chords, { beats, place }).notes, volume: 0.5, pan: 0.4 };
      console.log(JSON.stringify(res, null, 1));
    }
  } catch (e) {
    console.error("× " + e.message);
    process.exitCode = 1;
  }
  return true;
}
