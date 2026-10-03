// ドラムとベースを、本物の録音（SFZ の録音集）で鳴らす。render-node.mjs が使う。
// 録音集はリポジトリに入れない。置き場所は、環境変数 SUNSHINE_SAMPLE_LIBS、なければ「ユーザーのフォルダ/Music/sample-libraries」。
// どれも CC0（自由に使える・クレジット不要）。見つからなければ、そのパートは従来の音源で鳴らす。
//   ドラム: Virtuosity Drums（Versilian Studios・Karoryfer）、Unruly Drums（Karoryfer）
//   ベース: Growlybass（ピック弾き）・Fashionbass（指弾き）・Meatbass（ウッドベースのピチカート）（いずれも Karoryfer）
import fs from "fs";
import os from "os";
import path from "path";
import { openSfz } from "./sfz-player.mjs";

export function sampleLibDir() {
  const cands = [process.env.SUNSHINE_SAMPLE_LIBS, path.join(os.homedir(), "Music", "sample-libraries")].filter(Boolean);
  return cands.find((d) => fs.existsSync(d)) ?? null;
}

// 電子音楽の曲（打ち込みのドラム・シンセベースが合う曲）は、従来の音源のまま
const ELECTRONIC = new Set(["electro", "phonk", "cleandance", "space", "nature", "mystery", "discord"]);
const HEAVY = new Set(["metal", "deathmetal", "hardcore", "progmetal", "rock", "dancerock", "epic", "finale"]);
const SOFT = new Set(["jazz", "cafe"]);

/** 曲調に合うドラムの録音集と、GM の打楽器の番号 → その録音集の番号の対応。 */
function drumKitFor(style, lib) {
  if (!style || ELECTRONIC.has(style)) return null;
  if (HEAVY.has(style)) {
    return {
      name: "Virtuosity Drums",
      file: path.join(lib, "virtuosity_drums", "virtuosity_drums-master", "Programs", "02-full-kit.sfz"),
      // 割り当て表を「42=閉じたハイハット・46=開いたハイハット」の版に差しかえる（もとの表は 42 だけで、CC4 で開き具合を変える）
      opts: { replace: { "keymaps/keymap.sfz": "keymaps/default/keymap.sfz" } },
      // タムは2つ（41〜47=低いタム、48・50=高いタム）。サイドスティックは 88。チャイナはないのでクラッシュ
      map: { 35: 36, 37: 88, 41: 41, 43: 41, 45: 48, 47: 48, 48: 48, 50: 48, 52: 49, 55: 49 },
    };
  }
  return {
    name: SOFT.has(style) ? "Unruly Drums（ブラシ）" : "Unruly Drums",
    file: path.join(lib, "karoryfer.unruly-drums", "karoryfer.unruly-drums-main", "Programs", SOFT.has(style) ? "02-kit-brushes.sfz" : "01-kit-sticks.sfz"),
    // 46 のハイハットは CC4 で開き具合が決まる（127=開く）。41・43 は「22インチのスネアをタムとして」なので、ふつうのタムへ。52 は止める音なのでクラッシュへ
    opts: { cc: { 4: 127 } },
    map: { 35: 36, 41: 45, 43: 45, 48: 47, 50: 47, 52: 49 },
  };
}

function bassFor(style, lib) {
  if (!style || ELECTRONIC.has(style)) return null;
  if (SOFT.has(style)) return { name: "Meatbass（ウッドベース）", file: path.join(lib, "karoryfer.meatbass", "karoryfer.meatbass-master", "Programs", "04_pizz.sfz") };
  if (HEAVY.has(style)) return { name: "Growlybass（ピック弾き）", file: path.join(lib, "karoryfer.growlybass", "karoryfer.growlybass-master", "growlybass_dirty.sfz") };
  return { name: "Fashionbass（指弾き）", file: path.join(lib, "karoryfer.fashionbass", "karoryfer.fashionbass-master", "fashionbass.sfz") };
}

/** ドラムの部品ごとのパート（mix-plan.ts の drumKick など）。 */
function drumPart(gm) {
  if (gm === 35 || gm === 36) return "drumKick";
  if ([37, 38, 39, 40].includes(gm)) return "drumSnare";
  if ([41, 43, 45, 47, 48, 50].includes(gm)) return "drumToms";
  return "drumCym";
}

/** MIDI のあるチャンネルの音符を、秒で取り出す。 */
export function notesOf(midi, ch) {
  const notes = [];
  const open = new Map();
  for (const tr of midi.tracks) {
    for (const ev of tr.events) {
      const type = ev.statusByte & 0xf0;
      if ((ev.statusByte & 0x0f) !== ch || (type !== 0x90 && type !== 0x80)) continue;
      const key = ev.data[0], vel = ev.data[1];
      const t = midi.midiTicksToSeconds(ev.ticks);
      if (type === 0x90 && vel > 0) {
        if (!open.has(key)) open.set(key, []);
        open.get(key).push({ start: t, key, vel });
      } else {
        const n = open.get(key)?.shift();
        if (n) notes.push({ ...n, end: t });
      }
    }
  }
  return notes.sort((a, b) => a.start - b.start);
}

/**
 * ドラムとベースを本物の録音で鳴らす。
 * 戻り値: { parts: { パート名: { L, R } }, muted: Set<チャンネル>, used: [使った録音集の名前] }
 */
export function renderRealRhythm({ midi, instruments, style, total }) {
  const lib = sampleLibDir();
  const parts = {};
  const muted = new Set();
  const used = [];
  if (!lib) return { parts, muted, used };
  const add = (g, buf) => {
    if (!parts[g]) parts[g] = { L: new Float32Array(total), R: new Float32Array(total) };
    for (let i = 0; i < total; i++) (parts[g].L[i] += buf.L[i]), (parts[g].R[i] += buf.R[i]);
  };

  // ドラム（チャンネル10＝番号9）
  const kit = drumKitFor(style, lib);
  const kitSfz = kit && openSfz(kit.file, kit.opts);
  if (kitSfz) {
    const raw = notesOf(midi, 9);
    // 楽譜の書き出しで厚みのために重ねた音（キックの 35、スネアの手拍子 39・40）は、本物の録音では二重になるので外す
    const snareAt = new Set(raw.filter((n) => n.key === 38).map((n) => Math.round(n.start * 500)));
    const notes = raw.filter((n) => n.key !== 35 && !((n.key === 39 || n.key === 40) && snareAt.has(Math.round(n.start * 500))));
    const byPart = {};
    // 打楽器は叩きっぱなし（余韻は録音のまま）。止めるのはハイハットの開閉など off_by だけ
    for (const n of notes) (byPart[drumPart(n.key)] ??= []).push({ ...n, key: kit.map[n.key] ?? n.key, end: n.start + 6 });
    for (const [g, ns] of Object.entries(byPart)) add(g, kitSfz.render(ns, total, { maxSec: g === "drumCym" ? 6 : 3 }));
    muted.add(9);
    used.push(kit.name);
  }

  // ベース（いちばん音の多いベースのチャンネルを本物の録音で。重ねるために作った他のベースのチャンネルは止める）
  const bass = bassFor(style, lib);
  const bassSfz = bass && openSfz(bass.file);
  if (bassSfz) {
    const chs = Object.keys(instruments).map(Number).filter((c) => c !== 9 && instruments[c] === "bass");
    let best = null, bestNotes = [];
    for (const c of chs) {
      const ns = notesOf(midi, c);
      if (ns.length > bestNotes.length) (best = c), (bestNotes = ns);
    }
    if (best !== null && bestNotes.length) {
      // 重低音のために1オクターブ下に重ねた音は外す（同じ時に、12半音上の音がある音）
      const at = new Map();
      for (const n of bestNotes) at.set(`${Math.round(n.start * 500)}:${n.key}`, true);
      const notes = bestNotes.filter((n) => !at.has(`${Math.round(n.start * 500)}:${n.key + 12}`));
      add("bass", bassSfz.render(notes, total, { maxSec: 6, pitched: true }));
      for (const c of chs) muted.add(c);
      used.push(bass.name);
    }
  }
  return { parts, muted, used };
}
