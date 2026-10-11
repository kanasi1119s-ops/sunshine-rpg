// song.mjs から呼ばれる、曲作りの流れの道具のコマンド（gate・gate-compare・plan-check・plan-template・novelty・log）。
// vite を起動しない軽い処理なので、song.mjs の本体（openSongKit）より先に処理する。扱ったら true を返す。
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { judge, formatGate, measureWav, saveMeasurement, compareBands, formatCompare } from "./gate.mjs";
import { PLAN_TEMPLATE, checkPlan, formatPlanCheck } from "./plan-check.mjs";
import { checkNovelty, loadRecentFull } from "./novelty.mjs";
import { appendRevision } from "./revision-log.mjs";
import { prepareForCheck } from "../audio-check/score-lib.mjs";

const ROOT = path.resolve(fileURLToPath(new URL("../../", import.meta.url)));
export const WORKFLOW_COMMANDS = ["gate", "gate-compare", "plan-check", "plan-template", "novelty", "log"];

export async function runWorkflowCommand(args) {
  const cmd = args[0];
  if (!WORKFLOW_COMMANDS.includes(cmd)) return false;
  const opt = (n, d) => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : d; };
  const positional = args.slice(1).filter((a, i, all) => !a.startsWith("--") && !(i > 0 && all[i - 1].startsWith("--") && !["--json"].includes(all[i - 1])));
  try {
    if (cmd === "plan-template") {
      console.log(JSON.stringify(PLAN_TEMPLATE, null, 1));
    } else if (cmd === "gate") {
      if (!positional[0]) throw new Error("使い方: song.mjs gate <曲.wav> [--target -14] [--save <曲ID>] [--json]");
      const target = Number(opt("--target", -14));
      const m = measureWav(positional[0]);
      const rows = judge(m, { target });
      if (args.includes("--json")) console.log(JSON.stringify({ file: positional[0], target, metrics: m, rows }, null, 1));
      else console.log(formatGate(m, rows, path.basename(positional[0])));
      const id = opt("--save");
      if (id) {
        const s = saveMeasurement(ROOT, id, m, rows, target);
        const p = s.previous;
        console.log(`  保存: ${path.relative(ROOT, s.file)}${p ? `（前回 ${p.date}: LUFS ${p.lufs}・LRA ${p.lra}・PLR ${p.plr} → 今回 ${s.entry.lufs}・${s.entry.lra}・${s.entry.plr}）` : ""}`);
      }
      if (rows.some((r) => !r.ok)) process.exitCode = 2;
    } else if (cmd === "gate-compare") {
      if (positional.length < 2) throw new Error("使い方: song.mjs gate-compare <曲.wav> <基準.wav>");
      console.log(formatCompare(compareBands(positional[0], positional[1]), path.basename(positional[0]), path.basename(positional[1])));
    } else if (cmd === "plan-check") {
      if (!positional[0]) throw new Error("使い方: song.mjs plan-check <plan.json> [曲.json]");
      const plan = JSON.parse(fs.readFileSync(positional[0], "utf8"));
      const song = positional[1] ? await prepareForCheck(JSON.parse(fs.readFileSync(positional[1], "utf8"))) : null;
      const r = checkPlan(plan, song);
      console.log(formatPlanCheck(r));
      if (r.errors.length) process.exitCode = 1;
    } else if (cmd === "novelty") {
      if (!positional[0]) throw new Error("使い方: song.mjs novelty <曲.json> [--n 3] [--vs 曲名,曲名] [--plan <plan.json>]");
      const name = path.basename(positional[0]).replace(/\.json$/i, "");
      const song = await prepareForCheck(JSON.parse(fs.readFileSync(positional[0], "utf8")));
      const plan = opt("--plan") ? JSON.parse(fs.readFileSync(opt("--plan"), "utf8")) : null;
      const others = loadRecentFull(path.join(ROOT, "assets-src", "ai-songs"), Number(opt("--n", 3)), name, opt("--vs")?.split(","));
      const r = checkNovelty(song, name, others, plan);
      console.log(r.lines.join("\n"));
      if (r.warnings.length) console.log("\n" + r.warnings.map((w) => `注意: ${w}`).join("\n"));
      else console.log("\n○ 直前の曲と同じ選択はありません");
    } else if (cmd === "log") {
      if (!positional[0]) throw new Error("使い方: song.mjs log <曲ID> --before \"LRA 0.9\" --change \"直した点（1つ）\" --after \"LRA 4.1\" --ear \"耳の印象\"");
      console.log("追記:", appendRevision(ROOT, { id: positional[0], before: opt("--before"), change: opt("--change"), after: opt("--after"), ear: opt("--ear") }));
    }
  } catch (e) {
    console.error("×", e.message);
    process.exitCode = 1;
  }
  return true;
}
