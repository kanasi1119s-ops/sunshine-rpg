/**
 * 自動ミックスの「決める」部分（2026-10-14）。パートの役割を決め、測った数字と目標（auto-mix-targets.ts）を比べて、
 * volume／gainDb／pan／duck／EQ（既存の fx の filter・eq）の調整案を出し、曲の JSON に反映する。
 * 耳では確かめていない。数字の根拠は docs/sound/band-ensemble/auto-mix.md。
 */
import type { Analysis, MaskingReport } from "./auto-mix";
import { BAND_IDS, isDrumRole } from "./auto-mix";
import { recommendDuck, type DuckGenre } from "./mix-tools";
import { GROUP_LABEL, GROUP_TARGETS, MIX_RULES, ROLE_SPECS, type MixGroup, type MixRole } from "./auto-mix-targets";

/** AIソング形式のパート（調整に関係する項目だけ）。 */
export interface AiPartLike {
  instrument: string;
  role?: string;
  volume?: number;
  gainDb?: number;
  pan?: number;
  amp?: string;
  bright?: number;
  duck?: number;
  reverb?: number;
  fx?: Record<string, unknown>[];
  notes?: string;
  /** 自動ミックス用の役割の指定（作曲ソフトは無視する）。MixRole のどれか。 */
  mixRole?: string;
  [k: string]: unknown;
}

const DRUM_INSTRUMENTS = new Set(["kick", "snare", "hihat", "crash", "tom", "rotoTom", "cowbell"]);
const BASS_INSTRUMENTS = new Set(["bass", "slap", "sub808"]);
const GUITAR_INSTRUMENTS = new Set(["guitar", "echoGuitar", "crunch", "distGuitar", "leadGuitar"]);
const KEYS_INSTRUMENTS = new Set(["piano", "keys", "harpsichord", "fmEpiano", "organ", "bell", "fmBell", "harp", "kalimba", "marimba", "vibraphone"]);
const STRINGS_INSTRUMENTS = new Set(["strings", "pad", "choir", "fiddle", "violin", "cello"]);
const BRASS_INSTRUMENTS = new Set(["brass", "trumpet", "horn", "sax"]);
const CLEAN_AMPS = new Set(["clean", "crystal", "sparkleClean", "jpopClean", "delicate", "jazz", "blues"]);
const LEAD_WORDS = /メロディ|主旋律|リード|lead|melody|歌|ボーカル|vocal/i;
const COUNTER_WORDS = /合いの手|対旋律|カウンター|オブリ|ハモ|counter|obbligato|response/i;
const CLEAN_WORDS = /クリーン|きらめき|アルペジオ|arp|sparkle/i;
const SOLO_WORDS = /ソロ|solo/i;

const isDrumPart = (p: AiPartLike): boolean => DRUM_INSTRUMENTS.has(p.instrument);
const normNotes = (p: AiPartLike): string => String(p.notes ?? "").replace(/\s+/g, " ").trim();

export interface RoleAssignment {
  roles: MixRole[];
  /** リード（基準）のパート番号。見つからなければ -1 */
  leadIndex: number;
  /** どう決めたかの説明（パートごと） */
  why: string[];
}

/**
 * パートの役割を決める。手がかりは楽器・role の文章・アンプ・音量・音符。外れたら mixRole（JSON）か overrides（CLI）で指定する。
 * リードは、「メロディ」「リード」などの語を role に持つ旋律パート（複数なら最初のもの）、なければリードギター、なければ旋律パートでいちばん大きいもの。
 */
export function assignRoles(parts: AiPartLike[], overrides: Record<number, string> = {}): RoleAssignment {
  const roles: MixRole[] = parts.map(() => "other");
  const why: string[] = parts.map(() => "");
  const melodic = (p: AiPartLike): boolean => !isDrumPart(p) && !BASS_INSTRUMENTS.has(p.instrument);
  // リードの選定
  let leadIndex = -1;
  const forced = parts.findIndex((_, i) => overrides[i] === "lead" || parts[i].mixRole === "lead");
  if (forced >= 0) leadIndex = forced;
  if (leadIndex < 0) {
    const cands = parts.map((p, i) => ({ p, i })).filter(({ p }) => melodic(p) && (LEAD_WORDS.test(String(p.role ?? "")) && !COUNTER_WORDS.test(String(p.role ?? ""))));
    if (cands.length) leadIndex = cands[0].i;
  }
  if (leadIndex < 0) {
    const lg = parts.findIndex((p) => p.instrument === "leadGuitar" || p.instrument === "lead");
    if (lg >= 0) leadIndex = lg;
  }
  if (leadIndex < 0) {
    let best = -1, bestV = -1;
    parts.forEach((p, i) => { if (melodic(p) && !KEYS_INSTRUMENTS.has(p.instrument) && (p.volume ?? 0) > bestV) { best = i; bestV = p.volume ?? 0; } });
    leadIndex = best;
  }
  const leadNotes = leadIndex >= 0 ? normNotes(parts[leadIndex]) : "";
  parts.forEach((p, i) => {
    const o = overrides[i] ?? p.mixRole;
    if (o && o in ROLE_SPECS) { roles[i] = o as MixRole; why[i] = "指定"; return; }
    const inst = p.instrument, role = String(p.role ?? "");
    if (i === leadIndex) { roles[i] = "lead"; why[i] = "リード（基準）"; return; }
    if (DRUM_INSTRUMENTS.has(inst)) {
      roles[i] = inst === "kick" ? "kick" : inst === "snare" ? "snare" : inst === "hihat" ? "hihat" : inst === "crash" ? "cymbal" : "tom";
      if (inst === "cowbell") roles[i] = "cymbal";
      why[i] = "楽器から"; return;
    }
    if (BASS_INSTRUMENTS.has(inst)) { roles[i] = "bass"; why[i] = "楽器から"; return; }
    if (leadNotes && normNotes(p) === leadNotes) { roles[i] = "leadDouble"; why[i] = "リードと同じ音符"; return; }
    if (COUNTER_WORDS.test(role)) { roles[i] = "counter"; why[i] = "role の語"; return; }
    if (SOLO_WORDS.test(role)) { roles[i] = "leadDouble"; why[i] = "role に「ソロ」"; return; }
    if (inst === "leadGuitar" || inst === "lead") { roles[i] = "counter"; why[i] = "リード以外のリード楽器"; return; }
    if (GUITAR_INSTRUMENTS.has(inst)) {
      const clean = (p.amp && CLEAN_AMPS.has(p.amp)) || CLEAN_WORDS.test(role) || inst === "guitar" && !p.amp;
      roles[i] = clean ? "guitarClean" : "guitarRhythm"; why[i] = clean ? "クリーン系のアンプ／role" : "歪み系のアンプ"; return;
    }
    if (KEYS_INSTRUMENTS.has(inst)) { roles[i] = "keys"; why[i] = "楽器から"; return; }
    if (STRINGS_INSTRUMENTS.has(inst)) { roles[i] = "strings"; why[i] = "楽器から"; return; }
    if (BRASS_INSTRUMENTS.has(inst)) { roles[i] = "brass"; why[i] = "リード以外のブラス"; return; }
    roles[i] = "other"; why[i] = "楽器が一覧にない";
  });
  return { roles, leadIndex, why };
}

// ───────────────────────── 測定の単位（ユニット） ─────────────────────────

/** 測った 1 つの音（パート 1 つ、または分けられなかったドラム全体）。 */
export interface Unit {
  id: string;
  /** 含むパート番号 */
  parts: number[];
  /** ドラム全体を 1 つにまとめた音なら "drums"（太鼓ごとに分けて測れたときは各役割） */
  role: MixRole | "drums";
  label: string;
  analysis: Analysis;
}

export interface LevelRow {
  id: string;
  label: string;
  role: MixRole | "drums";
  group: MixGroup;
  /** 鳴っている間の力（リード = 0 の dB） */
  measuredRelDb: number;
  targetRelDb: number;
  /** 目標 − 測定（プラスなら足りない） */
  diffDb: number;
  tolDb: number;
  status: "ok" | "near" | "off";
  /** 実際に動かす量（dB。0 なら動かさない） */
  stepDb: number;
}

const db10 = (p: number): number => 10 * Math.log10(p);

/** 各ユニットの目標（リード = 0 の dB）。グループ全体の目標を、グループ内の役割の差で分け合う。 */
export function levelTargets(units: Unit[], leadId: string): LevelRow[] {
  const lead = units.find((u) => u.id === leadId);
  if (!lead) return [];
  const groupOf = (u: Unit): MixGroup => (u.role === "drums" ? "drums" : ROLE_SPECS[u.role].group);
  const within = (u: Unit): number => (u.role === "drums" ? 0 : ROLE_SPECS[u.role].withinDb);
  const sums = new Map<MixGroup, number>();
  for (const u of units) sums.set(groupOf(u), (sums.get(groupOf(u)) ?? 0) + Math.pow(10, within(u) / 10));
  return units.map((u) => {
    const g = groupOf(u);
    const target = GROUP_TARGETS[g].relDb + within(u) - db10(sums.get(g) ?? 1);
    const measured = u.analysis.activeRmsDb - lead.analysis.activeRmsDb;
    const diff = target - measured;
    const tol = g === "lead" ? 0 : GROUP_TARGETS[g].tolDb;
    const r = (v: number): number => Math.round(v * 10) / 10;
    const status: LevelRow["status"] = g === "lead" ? "ok" : Math.abs(diff) <= tol ? "ok" : Math.abs(diff) <= tol * 2 ? "near" : "off";
    let step = 0;
    if (g !== "lead" && Math.abs(diff) > MIX_RULES.deadbandDb) step = Math.max(-MIX_RULES.maxStepDb, Math.min(MIX_RULES.maxStepDb, diff * MIX_RULES.damping));
    return { id: u.id, label: u.label, role: u.role, group: g, measuredRelDb: r(measured), targetRelDb: r(target), diffDb: r(diff), tolDb: tol, status, stepDb: r(step) };
  });
}

// ───────────────────────── 調整案 ─────────────────────────

export interface PartChange {
  index: number;
  label: string;
  set: { gainDb?: number; volume?: number; pan?: number; duck?: number };
  /** automix の印を付けて fx に足す（同じ印の既存分は置きかえる） */
  fx: Record<string, unknown>[];
  reasons: string[];
}
export interface Advisory { target: string; text: string }
export interface MixPlan {
  rows: LevelRow[];
  changes: PartChange[];
  advisories: Advisory[];
  /** 動かす案がある（収束していない） */
  changed: boolean;
}

export interface PlanInput {
  parts: AiPartLike[];
  roles: MixRole[];
  leadIndex: number;
  units: Unit[];
  masking: MaskingReport | null;
  /** そのパートが、本番の書き出しで他のパートと同じ MIDI チャンネルを共有しているか（gainDb・fx・duck が一緒に効いてしまう） */
  sharedChannel: boolean[];
  bpm: number;
  genre: DuckGenre;
}

const clamp = (v: number, lo: number, hi: number): number => Math.max(lo, Math.min(hi, v));
const r2 = (v: number): number => Math.round(v * 100) / 100;
const r3 = (v: number): number => Math.round(v * 1000) / 1000;
const lowShare = (a: Analysis): number => db10(Math.pow(10, a.bandShareDb.sub / 10) + Math.pow(10, a.bandShareDb.bass / 10));

/** 既存の automix の fx（印 key）の量を読む */
function existingAutomix(part: AiPartLike, key: string): Record<string, unknown> | undefined {
  return (part.fx ?? []).find((f) => f && (f as Record<string, unknown>).automix === key);
}

/**
 * 測定結果から調整案を作る。動かすのは、次の 5 つ。
 *  1. 大きさ: 鳴っている間の力を、役割ごとの目標（リード = 0 の dB）に寄せる（gainDb。ドラムと同じチャンネルを共有するパートは volume）
 *  2. 左右: 低域・リードは中央、同じ役割が 2 つ以上のリズムギターは左右に
 *  3. 低域の掃除: 低域が要らない役割で Sub+Bass の力が多ければハイパス（fx の filter）
 *  4. 濁り: 200-500Hz が多いとき、寄与の大きい（削ってよい）パートを fx の eq で −2〜−3dB
 *  5. キックとベースの重なり: 重なりが多ければベースの duck。リードが埋もれるときは、同じ帯域の最大の競合を fx の eq で削る
 * ドラムは 1 つのチャンネルを共有するので、太鼓ごとの EQ は書けない（提案だけ出す）。
 */
export function planMix(inp: PlanInput): MixPlan {
  const { parts, roles, units, masking } = inp;
  const leadUnit = units.find((u) => u.role === "lead") ?? units[inp.leadIndex >= 0 ? units.findIndex((u) => u.parts.includes(inp.leadIndex)) : 0];
  const rows = leadUnit ? levelTargets(units, leadUnit.id) : [];
  const byIndex = new Map<number, PartChange>();
  const change = (i: number): PartChange => {
    let c = byIndex.get(i);
    if (!c) { c = { index: i, label: String(parts[i].role ?? parts[i].instrument), set: {}, fx: [], reasons: [] }; byIndex.set(i, c); }
    return c;
  };
  const advisories: Advisory[] = [];

  // 1. 大きさ
  for (const row of rows) {
    if (!row.stepDb) continue;
    const u = units.find((x) => x.id === row.id)!;
    for (const i of u.parts) {
      const c = change(i);
      const spec = row.role === "drums" ? ROLE_SPECS.kick : ROLE_SPECS[row.role];
      const useVolume = isDrumPart(parts[i]) || spec.levelBy === "volume" || inp.sharedChannel[i];
      if (useVolume) {
        const cur = parts[i].volume ?? 0.2;
        const next = clamp(cur * Math.pow(10, row.stepDb / MIX_RULES.volumeDbPerDecade), MIX_RULES.volumeRange[0], MIX_RULES.volumeRange[1]);
        c.set.volume = r3(next);
        c.reasons.push(`大きさ ${row.stepDb >= 0 ? "+" : ""}${row.stepDb}dB（${row.label}: 測定 ${row.measuredRelDb}／目標 ${row.targetRelDb}）→ volume ${cur} → ${r3(next)}${inp.sharedChannel[i] && !isDrumPart(parts[i]) ? "（他のパートと同じチャンネルを共有しているので gainDb ではなく volume）" : ""}`);
      } else {
        const cur = parts[i].gainDb ?? 0;
        const next = clamp(cur + row.stepDb, MIX_RULES.gainDbRange[0], MIX_RULES.gainDbRange[1]);
        c.set.gainDb = r2(next);
        c.reasons.push(`大きさ ${row.stepDb >= 0 ? "+" : ""}${row.stepDb}dB（${row.label}: 測定 ${row.measuredRelDb}／目標 ${row.targetRelDb}）→ gainDb ${cur} → ${r2(next)}`);
      }
    }
  }

  // 2. 左右
  const spreadGroups = new Map<MixRole, number[]>();
  parts.forEach((p, i) => {
    const role = roles[i], spec = ROLE_SPECS[role];
    if (isDrumPart(p)) return;
    const pan = p.pan ?? 0;
    if (spec.pan === "center" && Math.abs(pan) > 0.1) {
      change(i).set.pan = 0;
      change(i).reasons.push(`左右: ${spec.label}は中央に（pan ${pan} → 0）。低域・リードは中央がよい（rock-metal.md §3.2）`);
    }
    if (spec.pan === "spread") spreadGroups.set(role, [...(spreadGroups.get(role) ?? []), i]);
  });
  for (const [role, idxs] of spreadGroups) {
    if (idxs.length < 2) continue;
    const weak = idxs.filter((i) => Math.abs(parts[i].pan ?? 0) < 0.6);
    if (weak.length === 0) continue;
    idxs.forEach((i, k) => {
      const want = k % 2 === 0 ? -0.75 : 0.75;
      if (Math.abs((parts[i].pan ?? 0) - want) < 0.05) return;
      change(i).set.pan = want;
      change(i).reasons.push(`左右: ${ROLE_SPECS[role].label}が ${idxs.length} 本あるので左右に（pan ${parts[i].pan ?? 0} → ${want}）。ギターは 75〜100% 左右（rock-metal.md §3.2）`);
    });
  }

  // 3. 低域の掃除（ハイパス）
  for (const u of units) {
    if (u.role === "drums") continue;
    const spec = ROLE_SPECS[u.role];
    if (!spec.lowCut) continue;
    const ls = lowShare(u.analysis);
    if (ls <= spec.lowCut.maxLowShareDb) continue;
    for (const i of u.parts) {
      if (isDrumPart(parts[i])) {
        advisories.push({ target: u.label, text: `Sub+Bass が自分の ${ls.toFixed(1)}dB（目安 ${spec.lowCut.maxLowShareDb}dB 以下）。${spec.lowCut.hpfHz}Hz 以下を切りたいが、ドラムは 1 チャンネルを共有するので fx では書けない（drumMix の tune／level で調整）。${spec.lowCut.source}` });
        continue;
      }
      const prev = existingAutomix(parts[i], "hpf");
      if (prev && Number(prev.freq) >= spec.lowCut.hpfHz) { advisories.push({ target: u.label, text: `ハイパス ${prev.freq}Hz を既に入れたが、Sub+Bass がまだ ${ls.toFixed(1)}dB。音源か amp 側の低域が強いので、音域（オクターブ）を見直す` }); continue; }
      change(i).fx.push({ type: "filter", kind: "highpass", freq: spec.lowCut.hpfHz, q: 0.7, automix: "hpf" });
      change(i).reasons.push(`低域の掃除: Sub+Bass が自分の ${ls.toFixed(1)}dB（目安 ${spec.lowCut.maxLowShareDb}dB 以下）→ ${spec.lowCut.hpfHz}Hz ハイパス。${spec.lowCut.source}`);
    }
  }

  // 4. 濁り（200-500Hz）
  if (masking && masking.mud.excessDb >= MIX_RULES.mudExcessActDb) {
    const cands = masking.mud.top
      .map((t) => ({ t, u: units.find((u) => u.id === t.id) }))
      .filter((x): x is { t: { id: string; pct: number }; u: Unit } => !!x.u && x.u.role !== "drums" && ROLE_SPECS[x.u.role].mudCutPriority > 0)
      .sort((a, b) => b.t.pct * ROLE_SPECS[(b.u.role as MixRole)].mudCutPriority - a.t.pct * ROLE_SPECS[(a.u.role as MixRole)].mudCutPriority)
      .slice(0, 2);
    const cut = masking.mud.excessDb >= 4 ? -3 : -2;
    for (const { t, u } of cands) {
      const spec = ROLE_SPECS[u.role as MixRole];
      for (const i of u.parts) {
        const prev = existingAutomix(parts[i], "mud");
        const total = clamp(Number(prev?.mid ?? 0) + cut, -MIX_RULES.eqCutLimitDb, 0);
        if (total === Number(prev?.mid ?? 0)) { advisories.push({ target: u.label, text: `200-500Hz の寄与 ${t.pct}% で削りたいが、EQ の削りが上限 ${MIX_RULES.eqCutLimitDb}dB に達している。音域をずらす（オクターブ上げる）か、パートを減らす` }); continue; }
        change(i).fx.push({ type: "eq", mid: total, midHz: spec.mudCutHz ?? 320, automix: "mud" });
        change(i).reasons.push(`濁り: 200-500Hz が全体の ${masking.mud.shareMedianDb}dB（目標 ${MIX_RULES.mudShareTargetDb}dB、超過 ${masking.mud.excessDb}dB）。このパートの寄与 ${t.pct}% → ${spec.mudCutHz ?? 320}Hz を ${total}dB（合計 ${MIX_RULES.eqCutLimitDb}dB まで。mixing-guide.md）`);
      }
    }
    const drumTop = masking.mud.top.find((t) => units.find((u) => u.id === t.id)?.role === "drums");
    if (drumTop && drumTop.pct >= 25) advisories.push({ target: "ドラム", text: `200-500Hz の寄与の ${drumTop.pct}% がドラム。キックの箱鳴り（200〜500Hz）やスネア（400〜800Hz）を削る場合は、ドラムの音源（--drums）を替えるか drumMix の level を下げる` });
  }

  // 5-a. キックとベースの重なり → ベースの duck
  if (masking?.kickBass && masking.kickBass.closePct >= MIX_RULES.kickBassClosePct) {
    parts.forEach((p, i) => {
      if (roles[i] !== "bass" || (p.duck ?? 0) > 0) return;
      const d = recommendDuck("bass", inp.genre, inp.bpm);
      change(i).set.duck = d.duck;
      change(i).reasons.push(`キックとベースの重なり: Sub+Bass で差が 4dB 以内の窓が ${masking.kickBass!.closePct}%（目安 ${MIX_RULES.kickBassClosePct}% 未満）→ duck ${d.duck}（推奨範囲 ${d.range[0]}〜${d.range[1]}）。${d.notes.join(" ")}`);
    });
  }
  // 5-b. リードの埋もれ → 最大の競合を削る
  const leadClarity = masking?.clarity.find((c) => c.role === "lead");
  if (leadClarity && leadUnit) {
    const spec = ROLE_SPECS.lead;
    if (spec.clarity && leadClarity.medianDb < spec.clarity.minMedianDb) {
      const bands = spec.clarity.bands;
      const power = (a: Analysis): number => bands.reduce((s, b) => s + Math.pow(10, a.bandAbsDb[b] / 10), 0);
      const rival = units.filter((u) => u.role !== "lead" && u.role !== "drums" && !isDrumRole(String(u.role))).sort((a, b) => power(b.analysis) - power(a.analysis))[0];
      if (rival) {
        for (const i of rival.parts) {
          const prev = existingAutomix(parts[i], "clarity");
          const total = clamp(Number(prev?.mid ?? 0) - 2, -MIX_RULES.eqCutLimitDb, 0);
          if (total === Number(prev?.mid ?? 0)) { advisories.push({ target: rival.label, text: "リードの帯域を削る上限に達した。リードの音域をずらすか、リードを上げる" }); continue; }
          change(i).fx.push({ type: "eq", mid: total, midHz: 2500, automix: "clarity" });
          change(i).reasons.push(`リードの聞こえやすさ: ${bands.join("+")} で他のパート全体に対し 中央値 ${leadClarity.medianDb}dB（目安 ${spec.clarity.minMedianDb}dB 以上）→ 最大の競合を 2.5kHz で ${total}dB。リードを持ち上げた帯域は伴奏を少し削る（rock-metal.md §3.1）`);
        }
      }
    }
  }
  const changes = [...byIndex.values()].filter((c) => Object.keys(c.set).length || c.fx.length).sort((a, b) => a.index - b.index);
  return { rows, changes, advisories, changed: changes.length > 0 };
}

/** 調整案を曲の JSON に反映した新しい曲を返す（元は変えない）。 */
export function applyPlan<T extends { parts?: AiPartLike[] }>(song: T, changes: PartChange[]): T {
  const out = JSON.parse(JSON.stringify(song)) as T;
  for (const c of changes) {
    const p = out.parts?.[c.index];
    if (!p) continue;
    if (c.set.gainDb !== undefined) { if (c.set.gainDb === 0) delete p.gainDb; else p.gainDb = c.set.gainDb; }
    if (c.set.volume !== undefined) p.volume = c.set.volume;
    if (c.set.pan !== undefined) p.pan = c.set.pan;
    if (c.set.duck !== undefined) p.duck = c.set.duck;
    if (c.fx.length) {
      const keys = new Set(c.fx.map((f) => f.automix));
      p.fx = [...(p.fx ?? []).filter((f) => !keys.has((f as Record<string, unknown>).automix)), ...c.fx];
    }
  }
  return out;
}

/** 低域・左右・位相などの全体の警告（パート別の調整では直せないもの）。 */
export function stereoWarnings(a: Analysis): string[] {
  const w: string[] = [];
  if (Math.abs(a.stereo.balanceDb) > MIX_RULES.balanceWarnDb) w.push(`左右のバランスが ${a.stereo.balanceDb > 0 ? "右" : "左"}に ${Math.abs(a.stereo.balanceDb)}dB 寄っています（目安 ${MIX_RULES.balanceWarnDb}dB 以内）。強い側のパートの pan を中央へ寄せる`);
  if (a.stereo.lowCorr < MIX_RULES.lowCorrWarn) w.push(`150Hz 以下の左右の相関が ${a.stereo.lowCorr}（目安 ${MIX_RULES.lowCorrWarn} 以上）。モノで聞くと低音が痩せます。低域のパートの pan を 0 に、chorus・widen を外す`);
  return w;
}

// ───────────────────────── 全体（マスター）の助言 ─────────────────────────

/** docs/sound/data/mix-targets.json と同じ形（家族別の帯域の目標）。 */
export interface MixTargetsFile {
  tolerance_dB: { bass: number; lowmid: number; mid: number; presence: number };
  families: Record<string, { label: string; bass: number; lowmid: number; mid: number; presence: number; tilt_dB_oct: number }>;
}
export interface MasterMeasure {
  lufs: number;
  tpDb: number;
  /** 真のピーク − 統合 LUFS */
  plr: number;
  crestDb: number;
  family: { bass: number; lowmid: number; mid: number; presence: number };
  /** 1/3 オクターブ幅の帯域での傾き（dB/oct） */
  tilt13: number;
  corr: number;
  widthDb: number;
  lowCorr: number;
  balanceDb: number;
}
export interface MasterRow { name: string; value: string; target: string; status: "ok" | "off" | "info" }
export interface MasterAdvice {
  familyKey: string;
  preset: string;
  rows: MasterRow[];
  notes: string[];
  /** いまの master-preset の EQ に「追加で」足すとよい EQ（build の引数には無いので、自分で preset を作るときの目安） */
  eq: { type: "peak" | "hs"; f: number; g: number; o?: number }[];
}

/**
 * 全体を測った数字から、master-preset の選択と調整の案を出す。数字の目標は mix-targets.json（家族別）と MASTER_FAMILIES。
 * 測るのは「いまの master-preset をかけたあとの音」。EQ の案は、その上に足す量。
 */
export function masterAdvice(m: MasterMeasure, familyKey: string, mix: MixTargetsFile, fam: { preset: string; presetLighter: string; lufs: [number, number]; plr: [number, number]; corr: [number, number]; mixTargetFamily: string }, currentPreset = ""): MasterAdvice {
  const t = mix.families[fam.mixTargetFamily] ?? mix.families.rock;
  const tol = mix.tolerance_dB;
  const rows: MasterRow[] = [];
  const notes: string[] = [];
  const eq: MasterAdvice["eq"] = [];
  const range = (v: number, [lo, hi]: [number, number]): "ok" | "off" => (v >= lo && v <= hi ? "ok" : "off");
  rows.push({ name: "統合ラウドネス (LUFS)", value: m.lufs.toFixed(1), target: `${fam.lufs[0]}〜${fam.lufs[1]}`, status: range(m.lufs, fam.lufs) });
  rows.push({ name: "真のピーク (dBTP)", value: m.tpDb.toFixed(1), target: "-1 以下（ストリーミング・変換での割れを避ける）", status: m.tpDb <= -0.9 ? "ok" : "off" });
  rows.push({ name: "PLR (ピーク − 統合LUFS)", value: m.plr.toFixed(1), target: `${fam.plr[0]}〜${fam.plr[1]}`, status: range(m.plr, fam.plr) });
  rows.push({ name: "クレストファクター (dB)", value: m.crestDb.toFixed(1), target: "10 以上でつぶれ過ぎでない（punk-guide.md §8）", status: m.crestDb >= 10 ? "ok" : "off" });
  const bandRow = (name: string, key: "bass" | "lowmid" | "mid" | "presence", label: string): void => {
    const d = m.family[key] - t[key];
    rows.push({ name, value: `${m.family[key].toFixed(1)}dB`, target: `${t[key]} ±${tol[key]}（${t.label}）`, status: Math.abs(d) <= tol[key] ? "ok" : "off" });
    if (Math.abs(d) > tol[key]) {
      const g = Math.round(clamp(Math.abs(d) * 0.5, 0.5, 2) * 10) / 10 * (d > 0 ? -1 : 1);
      if (key === "bass") eq.push({ type: "peak", f: 100, g, o: 2 });
      if (key === "lowmid") eq.push({ type: "peak", f: 300, g, o: 1.5 });
      if (key === "mid") eq.push({ type: "peak", f: 2800, g, o: 1.5 });
      if (key === "presence") eq.push({ type: "hs", f: 6000, g });
      notes.push(`${label}が目標より ${d > 0 ? "多い" : "少ない"}（${d > 0 ? "+" : ""}${d.toFixed(1)}dB）。全体の EQ で ${g > 0 ? "+" : ""}${g}dB を目安（まずパートの音量・EQ で直し、残りだけマスターで）`);
    }
  };
  bandRow("低 60-250Hz（全体に対する dB）", "bass", "低域 60-250Hz");
  bandRow("中低 250-1kHz", "lowmid", "中低域 250Hz〜1kHz");
  bandRow("中 1-4kHz", "mid", "中域 1〜4kHz");
  bandRow("張り 4-8kHz", "presence", "高め 4〜8kHz");
  const dt = m.tilt13 - t.tilt_dB_oct;
  rows.push({ name: "スペクトルの傾き (dB/oct, 1/3oct幅)", value: m.tilt13.toFixed(2), target: `${t.tilt_dB_oct} ±1（${t.label}）【推】`, status: Math.abs(dt) <= 1 ? "ok" : "off" });
  if (Math.abs(dt) > 1) notes.push(`傾きが目標より ${dt > 0 ? "明るい（高域寄り）" : "暗い（低域寄り）"}（差 ${dt.toFixed(2)}dB/oct）`);
  rows.push({ name: "左右の相関", value: m.corr.toFixed(2), target: `${fam.corr[0]}〜${fam.corr[1]}`, status: range(m.corr, fam.corr) });
  rows.push({ name: "ステレオの幅 (Side−Mid, dB)", value: m.widthDb.toFixed(1), target: "情報（0 に近いほど広い。-10 以下はほぼモノ）", status: "info" });
  rows.push({ name: "150Hz 以下の相関", value: m.lowCorr.toFixed(2), target: `${MIX_RULES.lowCorrWarn} 以上`, status: m.lowCorr >= MIX_RULES.lowCorrWarn ? "ok" : "off" });
  rows.push({ name: "左右のバランス (R−L, dB)", value: m.balanceDb.toFixed(1), target: `±${MIX_RULES.balanceWarnDb} 以内`, status: Math.abs(m.balanceDb) <= MIX_RULES.balanceWarnDb ? "ok" : "off" });
  let preset = fam.preset;
  if (m.plr < fam.plr[0] || m.crestDb < 10) {
    preset = fam.presetLighter;
    notes.push(`つぶれ気味（PLR ${m.plr.toFixed(1)}／クレスト ${m.crestDb.toFixed(1)}dB）。master-preset を ${fam.presetLighter} のように圧縮の軽いものに替える${currentPreset ? `（いま ${currentPreset}）` : ""}`);
  }
  if (m.corr < fam.corr[0]) notes.push("左右の相関が低い（広がり過ぎ）。--widen を下げる、逆相気味のコーラス・ダブルを減らす");
  if (m.corr > fam.corr[1]) notes.push("左右の相関が高い（狭い）。ギターの pan を左右へ、--widen を上げる");
  return { familyKey, preset, rows, notes, eq };
}

export { GROUP_LABEL, BAND_IDS };
