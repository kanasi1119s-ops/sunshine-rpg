import type { Section } from "./arrangement";
import { isLoopSpec } from "./loop-check";
import type { BossPhase, Score, SongMeta } from "./score";

/**
 * 曲の付随情報（ループ点・導入と終わりの型・ボスの段階・主題ID）。音そのものは変えず、Score.meta と書き出しの管理ファイルに残す。
 * docs/sound/form-structure-guide.md §12 の提案4・5、game-music-guide.md の「ボス戦の段階」。
 */
export const INTRO_TYPES: Record<string, string> = {
  I1: "いきなり全員", I2: "1パートだけ", I3: "サビ先出し", I4: "無音と一撃", I5: "ドローン",
  I6: "リズムだけ", I7: "途中から", I8: "問いかけの動機", I9: "少しずつ層が増える", I10: "前の曲の最後を受ける",
};
export const OUTRO_TYPES: Record<string, string> = {
  E1: "頭へつなぐ", E2: "偽終止で続ける", E3: "ぴたりと止める", E4: "層をはがして消える", E5: "長い余韻",
  E6: "最後の主題の回帰", E7: "半音上げて止める", E8: "解決しないで宙づり", E9: "偽の終わり", E10: "ゆっくりした減速",
};

export function parseIntroType(v: unknown, warnings: string[]): string | undefined {
  if (v === undefined || v === null || v === "") return undefined;
  const s = String(v).toUpperCase();
  if (s in INTRO_TYPES) return s;
  warnings.push(`introType「${String(v)}」は使えません（${Object.keys(INTRO_TYPES).join("・")}）。無視しました`);
  return undefined;
}
export function parseOutroType(v: unknown, warnings: string[]): string | undefined {
  if (v === undefined || v === null || v === "") return undefined;
  const s = String(v).toUpperCase();
  if (s in OUTRO_TYPES) return s;
  warnings.push(`outroType「${String(v)}」は使えません（${Object.keys(OUTRO_TYPES).join("・")}）。無視しました`);
  return undefined;
}

/** ループ点。true／"seamless" は曲全体。{startBar,endBar} は導入を1回だけ鳴らして、その範囲をくり返す。 */
export function buildLoopMeta(loop: unknown, totalBars: number, beatsPerBar: number, bpm: number, warnings: string[]): SongMeta["loop"] | undefined {
  if (!isLoopSpec(loop)) return undefined;
  let startBar = 1, endBar = totalBars;
  if (typeof loop === "object") {
    startBar = Math.round(Number(loop.startBar));
    endBar = Math.round(Number(loop.endBar));
    if (!(startBar >= 1 && endBar > startBar && endBar <= totalBars)) {
      warnings.push(`loop: startBar（${loop.startBar}）と endBar（${loop.endBar}）は、1 ≤ startBar < endBar ≤ ${totalBars}（曲の小節数）にしてください。曲全体のループにしました`);
      startBar = 1; endBar = totalBars;
    }
  }
  const sec = (bar: number): number => Math.round(((bar * beatsPerBar * 60) / bpm) * 1000) / 1000;
  return { startBar, endBar, startSec: sec(startBar - 1), endSec: sec(endBar) };
}

/**
 * ボス戦の段階表。[{ "id": "p1", "startBar": 1, "endBar": 16, "hpBelow": 1 }, { "id": "p2", "startBar": 17, "endBar": 32, "hpBelow": 0.6 }, ...]
 * HPが hpBelow を下回ったら、その段階のループ（startBar〜endBar）に入る。段階はテンポ・調・拍子を変えない（同じ曲の中の別の塊）。
 */
export function parseBossPhases(raw: unknown, totalBars: number, sections: Section[] | undefined, warnings: string[]): BossPhase[] | undefined {
  if (raw === undefined || raw === null) return undefined;
  if (!Array.isArray(raw) || raw.length === 0) { warnings.push("bossPhases は { startBar, endBar, hpBelow } の並びで書いてください。無視しました"); return undefined; }
  const items = raw.map((x, i) => ({ x: x as Record<string, unknown>, i })).filter(({ x, i }) => {
    const ok = x && typeof x === "object" && Number.isFinite(Number(x.startBar));
    if (!ok) warnings.push(`bossPhases[${i}]: startBar が読めません。飛ばしました`);
    return ok;
  });
  if (!items.length) return undefined;
  items.sort((a, b) => Number(a.x.startBar) - Number(b.x.startBar));
  const n = items.length;
  const out: BossPhase[] = items.map(({ x, i }, k) => {
    const startBar = Math.round(Number(x.startBar));
    const nextStart = items[k + 1] ? Math.round(Number(items[k + 1].x.startBar)) : totalBars + 1;
    const endBar = Number.isFinite(Number(x.endBar)) && x.endBar !== undefined ? Math.round(Number(x.endBar)) : nextStart - 1;
    const hp = Number.isFinite(Number(x.hpBelow)) && x.hpBelow !== undefined ? Math.max(0, Math.min(1, Number(x.hpBelow))) : k === 0 ? 1 : Math.round((1 - k / n) * 100) / 100;
    return { id: typeof x.id === "string" && x.id ? x.id : `p${i + 1}`, startBar, endBar, hpBelow: hp };
  });
  const starts: number[] = [];
  if (sections) { let b = 1; for (const s of sections) { starts.push(b); b += s.bars; } }
  out.forEach((p, k) => {
    const where = `bossPhases[${k}]（${p.id}）`;
    if (!(p.startBar >= 1 && p.endBar >= p.startBar && p.endBar <= totalBars)) warnings.push(`${where}: startBar〜endBar（${p.startBar}〜${p.endBar}）が曲の範囲（1〜${totalBars}小節）に入っていません`);
    else {
      const len = p.endBar - p.startBar + 1;
      if (len < 4) warnings.push(`${where}: ループが ${len} 小節と短すぎます（4小節以上、できれば8の倍数）`);
      else if (len % 4 !== 0) warnings.push(`${where}: ループの長さ ${len} 小節が4の倍数ではありません`);
      if (starts.length && !starts.includes(p.startBar)) warnings.push(`${where}: startBar ${p.startBar} がセクションの変わり目ではありません（変わり目: ${starts.join("・")}）。段階の切り替えはセクションの頭に合わせてください`);
    }
    if (k > 0) {
      const prev = out[k - 1];
      if (p.hpBelow >= prev.hpBelow) warnings.push(`${where}: hpBelow ${p.hpBelow} が前の段階（${prev.hpBelow}）以上です。HPが減るほど後の段階に入るよう、小さくしてください`);
      if (p.startBar <= prev.endBar) warnings.push(`${where}: 前の段階（${prev.id}: ${prev.startBar}〜${prev.endBar}）と小節が重なっています`);
    }
  });
  if (out[0].hpBelow < 1) warnings.push("bossPhases[0]: 最初の段階の hpBelow は 1（HP満タンから）にしてください");
  return out;
}

export interface MetaInput {
  form?: unknown;
  loop?: unknown;
  introType?: unknown;
  outroType?: unknown;
  bossPhases?: unknown;
  motifs?: string[];
  laps?: number;
}

/** 曲の付随情報を作る。何も書かれていなければ undefined。 */
export function buildSongMeta(inp: MetaInput, ctx: { totalBars: number; beatsPerBar: number; bpm: number; sections?: Section[] }, warnings: string[]): SongMeta | undefined {
  const meta: SongMeta = {};
  const form = typeof inp.form === "string" ? inp.form : inp.form && typeof inp.form === "object" ? String((inp.form as { pattern?: unknown }).pattern ?? "") : "";
  if (form) meta.form = form;
  meta.bars = ctx.totalBars;
  meta.beatsPerBar = ctx.beatsPerBar;
  const loop = buildLoopMeta(inp.loop, ctx.totalBars, ctx.beatsPerBar, ctx.bpm, warnings);
  if (loop) meta.loop = loop;
  const it = parseIntroType(inp.introType, warnings);
  if (it) meta.introType = it;
  const ot = parseOutroType(inp.outroType, warnings);
  if (ot) meta.outroType = ot;
  const bp = parseBossPhases(inp.bossPhases, ctx.totalBars, ctx.sections, warnings);
  if (bp) meta.bossPhases = bp;
  if (inp.motifs?.length) meta.motifs = [...new Set(inp.motifs)];
  if (inp.laps && inp.laps > 1) meta.laps = inp.laps;
  // 何も特別なことが書かれていなければ、meta は付けない（今までの曲のファイルを変えない）
  return Object.keys(meta).filter((k) => k !== "bars" && k !== "beatsPerBar").length ? meta : undefined;
}

/** 書き出しの管理ファイル（<曲>.manifest.json）の中身。 */
export function buildManifest(name: string, title: string, score: Score, seconds: number): Record<string, unknown> {
  return {
    format: "sunshine-song-manifest", version: 1, name, title, bpm: score.tempoBpm, seconds,
    loop: score.loop, ...(score.meta ?? {}),
  };
}
