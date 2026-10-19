// 自動ミックス（パート別に数字で測って調整 → 最後にまとめて調整）。docs/sound/band-ensemble/auto-mix.md
//
//   node tools/composer/song.mjs automix <曲.json> [--out <フォルダ>] [--loop [N]] [--apply [<出力.json>]] [--apply-in-place]
//        [--bass pick --drums rock --guitar gretsch --piano salamander --orchestra vsco --soundfont gu --edition real --sound <セット>]
//        [--master-preset rock-clean] [--master -10] [--widen 1.25] [--space hall --space-wet 0.2]
//        [--family rock|punk|jazz|game] [--lead <パート番号>] [--roles "6=cymbal,12=counter"] [--window 0.25] [--no-split-drums] [--json] [--html <作曲ソフトHTMLの置き場>]
//
// やること（耳では確かめない。数字だけで判断する）:
//   1. 1 回の描き出しで、全体の音とパートごとの音を取り出し、パートごとに LUFS・ピーク・クレスト・7 帯域・重心・ステレオを測る
//      （ドラムは太鼓ごとに分けるため、ドラムだけの描き出しを太鼓の種類の数だけ追加する。--no-split-drums で省く）
//   2. 役割（キック・ベース・リズムギター…）ごとの目標（src/audio/auto-mix-targets.ts）と比べる
//   3. パート間のマスキング（濁り・混み・キックとベースの重なり・リードの埋もれ）を時間窓ごとに測り、ぐじゃぐじゃ指数にする
//   4. 調整案（gainDb／volume・pan・duck・fx の filter／eq）を出す。元の曲は変えず、<out>/<曲名>.automix.json に提案版を書く。
//      --apply は <元の曲と同じ場所>/<曲名>.automix.json（または指定したパス）に反映版を書く。--apply-in-place は元を <曲名>.json.bak-automix に残して上書き
//   5. 全体（master-preset 適用後）の LUFS・トゥルーピーク・帯域・傾き・ステレオ・クレストを測り、preset と EQ の案を出す
//   --loop N: 調整 → 再描き出し → 再測定を、収束するまで最大 N 回（既定 3）。描き出しは 1 回約 2〜3 分
import fs from "fs";
import os from "os";
import path from "path";
import { execSync } from "child_process";
import { openSongKit, ROOT } from "./song-lib.mjs";
import { masterFile, resolvePreset, measureLufs } from "./master.mjs";
import { masterReport } from "./master-report.mjs";
import { makeIr, writeWav, SPACES } from "./space-ir.mjs";
import { ensureComposerHtml, openStemSession } from "./stem-lib.mjs";

const log = (...a) => console.error(...a);

function parseArgs(args) {
  const flags = new Set(["--json", "--no-split-drums", "--apply-in-place", "--keep-wav", "--keep-work"]);
  const o = { _: [], flag: new Set(), val: {} };
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (!a.startsWith("--")) { o._.push(a); continue; }
    if (flags.has(a)) { o.flag.add(a); continue; }
    const next = args[i + 1];
    if (next === undefined || next.startsWith("--")) { o.flag.add(a); continue; } // 値が省略できるもの（--loop・--apply）
    o.val[a] = next; i++;
  }
  return o;
}

/** 書き出しの仕上げの引数（song-lib.mjs の build と同じ決め方） */
function masterOptionsFor(songData, presetName, { master = null, widen = null } = {}) {
  const pr = resolvePreset(presetName);
  const nat = songData.dynamics === "natural";
  const glue = nat ? ({ normal: "gentle", bus3: "bus2", bus2: "light" }[pr.glue] ?? pr.glue) : pr.glue;
  const { id: _id, lufs, glue: _g, widen: w, ...rest } = pr;
  return { ...rest, lufs: master ?? lufs, widen: widen ?? w, natural: nat, glue };
}

/** WAV を左右の Float32Array で読む（ffmpeg 経由） */
function readStereo(file, sr = 48000) {
  const buf = execSync(`ffmpeg -v error -i "${file}" -f f32le -ac 2 -ar ${sr} -`, { maxBuffer: 1 << 30 });
  const a = new Float32Array(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength - (buf.byteLength % 4)));
  const n = a.length >> 1;
  const L = new Float32Array(n), R = new Float32Array(n);
  for (let i = 0; i < n; i++) { L[i] = a[2 * i]; R[i] = a[2 * i + 1]; }
  return { L, R, sr };
}

const DRUM_GROUP = { kick: "kick", snare: "snare", hihat: "hihat", crash: "cymbal", cowbell: "cymbal", tom: "tom", rotoTom: "tom", cajon: "tom" };
const DRUM_INSTRUMENTS = new Set(Object.keys(DRUM_GROUP));

export async function runAutomix(argv) {
  const o = parseArgs(argv);
  const file = o._[0];
  if (!file) {
    console.log(fs.readFileSync(new URL(import.meta.url), "utf8").split("\n").filter((l) => l.startsWith("//")).map((l) => l.slice(3)).join("\n"));
    process.exitCode = 1;
    return;
  }
  const v = (name, d) => (o.val[name] !== undefined ? o.val[name] : d);
  const songPath = path.resolve(file);
  const original = JSON.parse(fs.readFileSync(songPath, "utf8"));
  const name = path.basename(songPath).replace(/\.json$/i, "").toLowerCase().replace(/[^a-z0-9-]+/g, "-");
  const out = path.resolve(v("--out", path.join(ROOT, "dist-songs", "automix")));
  fs.mkdirSync(out, { recursive: true });
  const edition = v("--edition", "real");
  const windowSec = Number(v("--window", 0.25));
  const loop = o.flag.has("--loop") || o.val["--loop"] !== undefined;
  const maxIter = loop ? Math.max(1, Math.min(6, Number(o.val["--loop"] ?? 3) || 3)) : 0;
  const splitDrums = !o.flag.has("--no-split-drums");
  const html = path.resolve(v("--html", path.join(os.tmpdir(), "sunshine-automix", "composer.html")));
  const overlays = { soundfont: v("--soundfont", "game") === "gu" ? "gu" : "game", bass: v("--bass", "std"), drums: v("--drums", "std"), guitar: v("--guitar", "std"), orchestra: v("--orchestra", "std"), piano: v("--piano", "std") };

  const kit = await openSongKit();
  let session = null;
  try {
    const m = {
      aiSong: await kit.load("/src/audio/ai-song.ts"),
      midi: await kit.load("/src/audio/midi-export.ts"),
      am: await kit.load("/src/audio/auto-mix.ts"),
      plan: await kit.load("/src/audio/auto-mix-plan.ts"),
      targets: await kit.load("/src/audio/auto-mix-targets.ts"),
      report: await kit.load("/src/audio/auto-mix-report.ts"),
      sounds: await kit.load("/src/audio/sound-sets.ts"),
    };
    const mixTargets = JSON.parse(fs.readFileSync(path.join(ROOT, "docs/sound/data/mix-targets.json"), "utf8"));

    // ── 曲の設定から、ジャンルの家族・master-preset を決める ──
    const familyKey = v("--family", original.tone === "metal" || original.drumGenre === "punk" || original.drumGenre === "metal" ? "punk" : "rock");
    const fam = m.targets.MASTER_FAMILIES[familyKey];
    if (!fam) throw new Error(`--family は ${Object.keys(m.targets.MASTER_FAMILIES).join("・")} のどれか`);
    const presetName = v("--master-preset", fam.preset);
    const duckGenre = { rock: "rock", punk: original.tone === "metal" ? "metal" : "punk", jazz: "jazz", game: "game" }[familyKey] ?? "rock";
    const soundSet = v("--sound", "") ? m.sounds.SOUND_SETS[v("--sound", "")] : null;
    if (v("--sound", "") && !soundSet) throw new Error(`サウンドセットがありません: ${v("--sound", "")}`);
    if (soundSet) {
      if (overlays.bass === "std") overlays.bass = soundSet.overlays.bass;
      if (overlays.drums === "std") overlays.drums = soundSet.overlays.drums;
      if (overlays.guitar === "std") overlays.guitar = soundSet.overlays.guitar;
      if (overlays.orchestra === "std" && soundSet.overlays.orchestra) overlays.orchestra = soundSet.overlays.orchestra;
      if (overlays.piano === "std" && soundSet.overlays.piano) overlays.piano = soundSet.overlays.piano;
    }
    const masterLufs = o.val["--master"] !== undefined ? Number(o.val["--master"]) : null;
    const widen = o.val["--widen"] !== undefined ? Number(o.val["--widen"]) : null;

    // ── 役割 ──
    const parseOverrides = (s) => Object.fromEntries(String(s ?? "").split(",").filter(Boolean).map((kv) => { const [k, val] = kv.split("="); return [Number(k) - 1, val]; }));
    const overrides = parseOverrides(o.val["--roles"]);
    if (o.val["--lead"] !== undefined) overrides[Number(o.val["--lead"]) - 1] = "lead";
    const parts0 = original.parts ?? [];
    const assignment = m.plan.assignRoles(parts0, overrides);
    if (assignment.leadIndex < 0) throw new Error("リード（基準）のパートが見つかりません。--lead <番号> で指定してください");
    const partLabel = (i) => `${i + 1}:${String(parts0[i].role ?? parts0[i].instrument).replace(/[（(].*$/, "").slice(0, 14)}`;

    // 描き出しの準備（自分用の作曲ソフト HTML。古ければ作り直す）
    log("作曲ソフトの用意中…（初回や src を変えた後は 1〜2 分かかります）");
    ensureComposerHtml(html);
    session = await openStemSession(html, overlays);
    let rendersInSession = 0;
    // 描き出しを重ねるとブラウザのメモリが増えて止まることがあるので、一定回数ごとにブラウザを開き直す
    const freshSession = async () => { if (rendersInSession >= 6) { await session.close(); session = await openStemSession(html, overlays); rendersInSession = 0; } rendersInSession++; return session; };

    /** 曲 1 つぶんの測定: 描き出し → パートごとの数字 → マスキング → 調整案 → 全体の仕上げ */
    async function measureOnce(songData, tag) {
      const t0 = Date.now();
      let { score, warnings } = m.aiSong.aiSongToScore(songData);
      if (soundSet) score = m.sounds.applySoundSet(score, soundSet);
      // パートが何本のトラックになるか（ストロークの弦・エコー・自動ダブルで増える）を、パート 1 つずつ組み立てて数える
      const counts = (songData.parts ?? []).map((p) => {
        try { return m.aiSong.aiSongToScore({ ...songData, autoAccompaniment: false, parts: [p] }).score.tracks.length; } catch { return null; }
      });
      if (counts.some((c) => c === null)) throw new Error("パートを 1 つずつ組み立てられませんでした（パート間で参照するもの（mask など）があると測れません）");
      const handTotal = counts.reduce((a, b) => a + b, 0);
      const auto = score.tracks.length - handTotal;
      if (auto < 0) throw new Error(`パートとトラックの対応が取れません（パートの合計 ${handTotal} トラック、曲全体 ${score.tracks.length}）`);
      // 本番と同じチャンネルの割り当てで、同じチャンネルを共有するパートを調べる
      const real = m.midi.scoreToMidiInfo({ ...score, loop: false });
      const partOfTrack = [];
      for (let t = 0; t < auto; t++) partOfTrack.push(-1);
      counts.forEach((c, i) => { for (let k = 0; k < c; k++) partOfTrack.push(i); });
      const chanSets = parts0.map(() => new Set());
      partOfTrack.forEach((pi, t) => { if (pi >= 0 && real.trackChannels[t] >= 0) chanSets[pi].add(real.trackChannels[t]); });
      const sharedChannel = parts0.map((p, i) => !DRUM_INSTRUMENTS.has(p.instrument) && [...chanSets[i]].some((ch) => chanSets.some((s, j) => j !== i && !DRUM_INSTRUMENTS.has(parts0[j].instrument) && s.has(ch))));
      // パートごとに別のチャンネルへ（stemKey）
      const keyed = { ...score, tracks: score.tracks.map((t, ti) => ({ ...t, stemKey: partOfTrack[ti] >= 0 ? `p${partOfTrack[ti]}` : "auto" })) };
      const pre = path.join(out, `${name}-automix-pre.wav`);
      const main = await (await freshSession()).render(keyed, edition, { windowSec, busFile: pre });
      const analyses = { ...main.analyses };
      // ドラムは 1 つのチャンネルを共有するので、太鼓の種類ごとにドラムだけを描き直して分ける
      const drumGroups = new Map();
      parts0.forEach((p, i) => { if (DRUM_INSTRUMENTS.has(p.instrument)) drumGroups.set(DRUM_GROUP[p.instrument], [...(drumGroups.get(DRUM_GROUP[p.instrument]) ?? []), i]); });
      let split = false;
      if (splitDrums && drumGroups.size > 1) {
        for (const [g, idxs] of drumGroups) {
          const keep = new Set(idxs);
          const tracks = keyed.tracks.filter((t, ti) => keep.has(partOfTrack[ti])).map((t) => ({ ...t, stemKey: `d:${g}` }));
          const r = await (await freshSession()).render({ ...keyed, tracks }, edition, { windowSec, fixedGainDb: main.gainDb });
          analyses[`d:${g}`] = r.analyses[`d:${g}`];
        }
        split = true;
      }
      // ユニット（測った 1 つの音）
      const units = [];
      parts0.forEach((p, i) => {
        if (DRUM_INSTRUMENTS.has(p.instrument)) return;
        const a = analyses[`p${i}`];
        if (!a) return; // 音符がない（休みだけ）のパート
        if (!(a.samplePeakDb > -100)) { warnings = [...(warnings ?? []), `パート ${i + 1}（${parts0[i].role ?? parts0[i].instrument}）は描き出しで無音でした（音符が全部休み、または音が出ない設定）。測定・調整から外しています`]; return; }
        units.push({ id: `p${i}`, parts: [i], role: assignment.roles[i], label: partLabel(i), analysis: a });
      });
      if (split) {
        for (const [g, idxs] of drumGroups) units.push({ id: `d:${g}`, parts: idxs, role: g, label: `${m.targets.ROLE_SPECS[g].label}（${idxs.map((i) => i + 1).join("・")}）`, analysis: analyses[`d:${g}`] });
      } else if (drumGroups.size) {
        const idxs = [...drumGroups.values()].flat();
        const first = idxs[0];
        units.push({ id: "drums", parts: idxs, role: "drums", label: `ドラム全体（${idxs.map((i) => i + 1).join("・")}）`, analysis: analyses[`p${first}`] });
      }
      const leadUnit = units.find((u) => u.parts.includes(assignment.leadIndex));
      // マスキング診断
      const maskStems = units.filter((u) => u.analysis.windows).map((u) => ({ id: u.id, role: u.role, windows: u.analysis.windows, windowTotal: u.analysis.windowTotal }));
      const clarityRules = ["lead", "kick", "bass"].map((role) => ({ role, bands: m.targets.ROLE_SPECS[role].clarity.bands }));
      const masking = m.am.diagnoseMasking(maskStems, { mudShareTargetDb: m.targets.MIX_RULES.mudShareTargetDb, leadId: leadUnit?.id ?? null, clarity: clarityRules });
      // 調整案
      const bpm = score.tempoBpm;
      const plan = m.plan.planMix({ parts: songData.parts ?? parts0, roles: assignment.roles, leadIndex: assignment.leadIndex, units, masking, sharedChannel, bpm, genre: duckGenre });
      // 全体: 仕上げ（master-preset）をかけて測る
      const mixFile = path.join(out, `${name}-automix.wav`);
      fs.copyFileSync(pre, mixFile);
      let spaceInfo = "";
      if (v("--space", "")) {
        const space = v("--space", "");
        if (!SPACES[space]) throw new Error(`--space は ${Object.keys(SPACES).join("・")} のどれか`);
        const ir = mixFile + `.ir.wav`;
        writeWav(ir, makeIr(space));
        const tmp = mixFile + ".space.wav";
        const wet = Math.max(0, Math.min(1, Number(v("--space-wet", 0.25))));
        execSync(`ffmpeg -y -loglevel error -i "${mixFile}" -i "${ir}" -filter_complex "[0]asplit[d][w];[w][1]afir=dry=1:wet=10,volume=${(5 * wet).toFixed(3)}[r];[d][r]amix=inputs=2:normalize=0:duration=first" -ar 48000 -ac 2 -c:a pcm_s16le "${tmp}"`);
        fs.renameSync(tmp, mixFile);
        fs.rmSync(ir, { force: true });
        spaceInfo = `${space}(${wet})`;
      }
      const mopts = masterOptionsFor(songData, presetName, { master: masterLufs, widen });
      const mr = masterFile(mixFile, mopts);
      const lowCutoff = Math.min(100, Math.round((mopts.lowmono ?? 140) * 0.5));
      const rep = masterReport(mixFile, { lufs: mopts.lufs, tp: mopts.tp ?? -1.5, loop: true, lowCutoff });
      const meas = measureLufs(mixFile);
      const st = readStereo(mixFile);
      const fa = m.am.analyzeChannels(st.L, st.R, st.sr, { meanSpectrum: true });
      const tilt = m.am.spectralTilt(fa.meanSpec, st.sr);
      const masterMeasure = {
        lufs: meas.lufs, tpDb: meas.peak, plr: Math.round((meas.peak - meas.lufs) * 10) / 10, crestDb: fa.crestDb,
        family: m.am.familyBands(fa.meanSpec, st.sr), tilt13: tilt.third, corr: fa.stereo.corr, widthDb: fa.stereo.widthDb, lowCorr: fa.stereo.lowCorr, balanceDb: fa.stereo.balanceDb,
      };
      const advice = m.plan.masterAdvice(masterMeasure, familyKey, mixTargets, fam, presetName);
      log(`  [${tag}] 測定 ${Math.round((Date.now() - t0) / 1000)} 秒（描き出し ${split ? 1 + drumGroups.size : 1} 回）`);
      return { score, warnings, parts: parts0, units, masking, plan, masterMeasure, advice, rep, mr, sharedChannel, split, bpm, mixFile, spaceInfo, mopts, presetName, gainDb: main.gainDb, seconds: main.seconds };
    }

    // ── 測定 → 調整案 →（ループなら）反映して再測定 ──
    const history = [];
    let current = JSON.parse(JSON.stringify(original));
    let result = null;
    for (let it = 0; ; it++) {
      log(it === 0 ? "測定 1 回目…" : `調整を反映して再測定（${it} 回目）…`);
      result = await measureOnce(current, it === 0 ? "元" : `調整${it}`);
      history.push({ iteration: it, mess: result.masking.mess, rows: result.plan.rows, master: result.masterMeasure, rep: result.rep.line, changes: result.plan.changes, advisories: result.plan.advisories, mud: result.masking.mud, lufsFinal: result.masterMeasure.lufs });
      fs.writeFileSync(path.join(out, `${name}-automix-progress.json`), JSON.stringify({ history, current }, null, 1));
      if (!loop || !result.plan.changed || it >= maxIter) break;
      current = m.plan.applyPlan(current, result.plan.changes);
    }
    // 最終の提案版（ループなら、反映したあとの曲 + 最後の測定でまだ出ている案）
    const proposal = m.plan.applyPlan(current, result.plan.changes);
    const proposalFile = path.join(out, `${name}.automix.json`);
    const finalSong = loop ? current : proposal;
    fs.writeFileSync(proposalFile, JSON.stringify(finalSong, null, 2));
    let appliedTo = null;
    if (o.flag.has("--apply-in-place")) {
      fs.copyFileSync(songPath, songPath + ".bak-automix");
      fs.writeFileSync(songPath, JSON.stringify(finalSong, null, 2));
      appliedTo = songPath;
    } else if (o.flag.has("--apply") || o.val["--apply"] !== undefined) {
      appliedTo = path.resolve(o.val["--apply"] ?? path.join(path.dirname(songPath), `${path.basename(songPath, ".json")}.automix.json`));
      fs.writeFileSync(appliedTo, JSON.stringify(finalSong, null, 2));
    }
    const data = {
      title: result.score.title ?? original.title, name, songPath, edition, bpm: result.bpm, seconds: result.seconds, familyKey, familyLabel: fam.label, presetName, spaceInfo: result.spaceInfo,
      overlays, buildFlags: ["bass", "drums", "guitar", "orchestra", "piano"].filter((k) => overlays[k] !== "std").map((k) => `--${k} ${overlays[k]}`).join(" ") + (overlays.soundfont === "gu" ? " --soundfont gu" : ""), windowSec, loop, history, final: result, assignment, parts: parts0, proposalFile, appliedTo, loopDone: loop ? history.length - 1 : 0,
      originalSong: original, finalSong,
    };
    const text = m.report.formatReport(data);
    const reportFile = path.join(out, `${name}-automix.md`);
    fs.writeFileSync(reportFile, text);
    fs.writeFileSync(path.join(out, `${name}-automix-metrics.json`), JSON.stringify({ history, units: result.units.map((u) => ({ id: u.id, label: u.label, role: u.role, parts: u.parts, analysis: { ...u.analysis, windows: undefined, windowTotal: undefined } })), masking: result.masking, master: result.masterMeasure }, null, 1));
    fs.rmSync(path.join(out, `${name}-automix-pre.wav`), { force: true });
    if (!o.flag.has("--keep-wav")) fs.rmSync(result.mixFile, { force: true });
    if (o.flag.has("--json")) console.log(JSON.stringify({ history }, null, 1));
    else console.log(text);
    console.log(`\nレポート: ${reportFile}\n提案版の曲: ${proposalFile}${appliedTo ? `\n反映した曲: ${appliedTo}` : ""}`);
  } finally {
    if (session) await session.close();
    await kit.close();
  }
}
