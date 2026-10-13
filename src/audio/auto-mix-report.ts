/**
 * 自動ミックスのレポート（日本語、Markdown）。測った数字・調整案・直したこと・まだ残る問題をまとめる。
 * 純関数（tools/composer/automix.mjs が材料を渡す）。耳で確認していないことを、冒頭と末尾に必ず書く。
 */
import { BANDS, type Analysis, type MaskingReport } from "./auto-mix";
import { stereoWarnings, type AiPartLike, type LevelRow, type MasterAdvice, type MasterMeasure, type MixPlan, type PartChange, type RoleAssignment, type Unit } from "./auto-mix-plan";
import { MIX_RULES, ROLE_SPECS, GROUP_LABEL, GROUP_TARGETS } from "./auto-mix-targets";

export interface HistoryItem {
  iteration: number;
  mess: MaskingReport["mess"];
  rows: LevelRow[];
  master: MasterMeasure;
  rep: string;
  changes: PartChange[];
  advisories: MixPlan["advisories"];
  mud: MaskingReport["mud"];
  lufsFinal: number;
}
export interface FinalResult {
  units: Unit[];
  masking: MaskingReport;
  plan: MixPlan;
  masterMeasure: MasterMeasure;
  advice: MasterAdvice;
  rep: { line: string };
  split: boolean;
  sharedChannel: boolean[];
  warnings: string[];
  gainDb: number;
}
export interface ReportData {
  title: string;
  name: string;
  songPath: string;
  edition: string;
  bpm: number;
  seconds: number;
  familyKey: string;
  familyLabel: string;
  presetName: string;
  spaceInfo: string;
  windowSec: number;
  loop: boolean;
  loopDone: number;
  history: HistoryItem[];
  final: FinalResult;
  assignment: RoleAssignment;
  parts: AiPartLike[];
  proposalFile: string;
  /** build に付ける音源の引数（例: --bass pick --drums rock） */
  buildFlags: string;
  appliedTo: string | null;
  originalSong: { parts?: AiPartLike[] };
  finalSong: { parts?: AiPartLike[] };
}

const f1 = (v: number): string => (Number.isFinite(v) ? v.toFixed(1) : "−∞");
const sgn = (v: number): string => (v > 0 ? `+${v}` : `${v}`);
const mark = (s: "ok" | "near" | "off" | "info"): string => (s === "ok" ? "○" : s === "near" ? "△" : s === "off" ? "×" : "・");
const table = (head: string[], rows: string[][]): string => [`| ${head.join(" | ")} |`, `|${head.map(() => "---").join("|")}|`, ...rows.map((r) => `| ${r.join(" | ")} |`)].join("\n");
const roleLabel = (r: string): string => (r === "drums" ? "ドラム全体" : ROLE_SPECS[r as keyof typeof ROLE_SPECS]?.label ?? r);
const messLabel = (v: number): string => (v >= MIX_RULES.messBad ? "混んでいる" : v >= MIX_RULES.messWarn ? "やや混む" : "すっきり");

/** 元の曲と最終の曲の違い（volume・gainDb・pan・duck・自動ミックスの fx）を、パートごとの文章にする */
export function describeDiff(before: { parts?: AiPartLike[] }, after: { parts?: AiPartLike[] }, label: (i: number) => string): string[] {
  const out: string[] = [];
  (after.parts ?? []).forEach((p, i) => {
    const b = before.parts?.[i];
    if (!b) return;
    const bits: string[] = [];
    const chg = (k: "volume" | "gainDb" | "pan" | "duck"): void => {
      const x = b[k] ?? (k === "gainDb" || k === "pan" || k === "duck" ? 0 : undefined), y = p[k] ?? (k === "gainDb" || k === "pan" || k === "duck" ? 0 : undefined);
      if (x !== y) bits.push(`${k} ${x} → ${y}`);
    };
    (["gainDb", "volume", "pan", "duck"] as const).forEach(chg);
    const fxOf = (q: AiPartLike): string[] => (q.fx ?? []).filter((f) => (f as Record<string, unknown>).automix).map((f) => JSON.stringify(f));
    const bf = fxOf(b), af = fxOf(p);
    for (const f of af) if (!bf.includes(f)) bits.push(`fx ${f.replace(/,"automix":"[a-z]+"/, "")}`);
    if (bits.length) out.push(`- ${label(i)}: ${bits.join("、")}`);
  });
  return out;
}

export function formatReport(d: ReportData): string {
  const L: string[] = [];
  const fin = d.final;
  const first = d.history[0], last = d.history[d.history.length - 1];
  const label = (i: number): string => `${i + 1}番 ${String(d.parts[i].role ?? d.parts[i].instrument)}`;
  L.push(`# 自動ミックスの結果: ${d.title}`);
  L.push("");
  L.push(`> **耳では確認していません。** ここに書いてある判断はすべて、波形から測った数字（ラウドネス・帯域エネルギー・マスキング・位相・ステレオ）と、docs/sound の調査から決めた目標値の比較です。目標値の多くは【推】（出発点）なので、最後は人間の耳で聴いて決めてください。`);
  L.push("");
  L.push(`曲: \`${d.songPath}\`／${d.bpm} BPM・${Math.round(d.seconds)} 秒／版 ${d.edition}／ジャンル家族 ${d.familyLabel}／master-preset \`${d.presetName}\`${d.spaceInfo ? `／space ${d.spaceInfo}` : ""}／時間窓 ${d.windowSec} 秒`);
  L.push("");
  L.push("## 1. 結果の要約");
  L.push("");
  const sumRows: string[][] = [
    ["ぐじゃぐじゃ指数（0〜100、小さいほどすっきり）", `${first.mess.value}（${messLabel(first.mess.value)}）`, `${last.mess.value}（${messLabel(last.mess.value)}）`],
    ["　濁り度（200-500Hz の超過）", String(first.mess.mud), String(last.mess.mud)],
    ["　中域の混み（500-2k で 3 パート以上が同じ強さの窓 %）", String(first.mess.midCrowd), String(last.mess.midCrowd)],
    ["　キックとベースの重なり（%）", first.mess.lowCollision === null ? "—" : String(first.mess.lowCollision), last.mess.lowCollision === null ? "—" : String(last.mess.lowCollision)],
    ["　リードの埋もれ（0〜100）", first.mess.leadBuried === null ? "—" : String(first.mess.leadBuried), last.mess.leadBuried === null ? "—" : String(last.mess.leadBuried)],
    ["全体の LUFS（仕上げ後）", f1(first.master.lufs), f1(last.master.lufs)],
    ["真のピーク dBTP", f1(first.master.tpDb), f1(last.master.tpDb)],
    ["PLR／クレスト dB", `${f1(first.master.plr)}／${f1(first.master.crestDb)}`, `${f1(last.master.plr)}／${f1(last.master.crestDb)}`],
    ["目標から外れているパート数（大きさ）", String(first.rows.filter((r) => r.status !== "ok").length), String(last.rows.filter((r) => r.status !== "ok").length)],
  ];
  L.push(table(["指標", d.history.length > 1 ? "最初の測定" : "測定", ...(d.history.length > 1 ? ["最後の測定"] : [])], sumRows.map((r) => (d.history.length > 1 ? r : r.slice(0, 2)))));
  L.push("");
  L.push(d.loop ? `ループ: 調整を ${d.loopDone} 回反映して、${d.history.length} 回測りました。${last.rows.every((r) => r.stepDb === 0) && !fin.plan.changed ? "最後の測定では新しい調整案が出ず、収束しました。" : "最後の測定でもまだ調整案が残っています（上限回数に達しました）。"}` : "ループなし（測定 1 回）。調整案は提案版の曲に書きました。--loop で、反映 → 再測定 → 収束まで自動で繰り返せます。");
  L.push("");

  L.push("## 2. パートごとの数値");
  L.push("");
  L.push(`${d.final.split ? "ドラムは太鼓の種類ごとにドラムだけを描き直して分けました。" : "ドラムは 1 つのチャンネルを共有するので、ドラム全体で測りました。"}パートの音は、アンプ・エフェクターのあと、全体の仕上げ段（EQ・圧縮・残響）の前で取り出しています（全体は -16 LUFS にそろえた尺度）。`);
  L.push("");
  L.push("### 2-1. 役割・ラウドネス・ダイナミクス");
  L.push("");
  const units = fin.units;
  L.push(table(["パート", "役割", "統合LUFS", "ショートターム最大", "ピーク dBFS", "クレスト dB", "鳴る割合 %"],
    units.map((u) => [u.label, roleLabel(u.role), f1(u.analysis.lufsIntegrated), f1(u.analysis.lufsShortMax), f1(u.analysis.samplePeakDb), f1(u.analysis.crestDb), String(Math.round(u.analysis.activity * 100))])));
  L.push("");
  L.push("### 2-2. 帯域エネルギー（そのパート自身の全体を 0dB とした dB）とスペクトル重心");
  L.push("");
  L.push(table(["パート", ...BANDS.map((b) => b.label), "重心 Hz"], units.map((u) => [u.label, ...BANDS.map((b) => f1(u.analysis.bandShareDb[b.id])), String(u.analysis.centroidHz)])));
  L.push("");
  L.push("### 2-3. ステレオ・位相");
  L.push("");
  L.push(table(["パート", "左右の相関", "幅 Side−Mid dB", "左右バランス R−L dB", "150Hz以下の相関"], units.map((u) => [u.label, String(u.analysis.stereo.corr), f1(u.analysis.stereo.widthDb), f1(u.analysis.stereo.balanceDb), String(u.analysis.stereo.lowCorr)])));
  L.push("");
  L.push("### 2-4. 役割ごとの目標との比較（鳴っている間の力。リード = 0dB）");
  L.push("");
  const rows = fin.plan.rows;
  L.push(table(["パート", "役割（グループ）", "測定", "目標", "差（目標−測定）", "許す幅", "判定", "動かす量 dB"],
    rows.map((r) => [r.label, `${roleLabel(r.role)}（${GROUP_LABEL[r.group]}）`, sgn(r.measuredRelDb), sgn(r.targetRelDb), sgn(r.diffDb), r.tolDb ? `±${r.tolDb}` : "基準", mark(r.status), r.stepDb ? sgn(r.stepDb) : "—"])));
  L.push("");
  L.push("役割の割り当て（外れていたら `--roles \"6=cymbal\"` や、曲の JSON のパートに `mixRole` を書いて直す）:");
  L.push("");
  L.push(table(["パート", "楽器", "役割", "決めた手がかり", "他のパートとチャンネル共有"], d.parts.map((p, i) => [label(i), p.instrument, roleLabel(d.assignment.roles[i]), d.assignment.why[i], fin.sharedChannel[i] ? "あり（gainDb でなく volume で調整）" : "—"])));
  L.push("");

  L.push("## 3. パート間のマスキング診断（時間窓ごと）");
  L.push("");
  const mk = fin.masking;
  L.push(`時間窓 ${d.windowSec} 秒 × ${mk.windows} 個。「主な担い手」は、その帯域でいちばん強いパートから 6dB 以内のパート。3 つ以上が主な担い手なら「混んでいる」。`);
  L.push("");
  L.push(table(["帯域", "主な担い手の数（平均）", "3 パート以上で混んでいる窓 %"], BANDS.map((b) => [b.label, String(mk.crowd[b.id].meanMajor), String(mk.crowd[b.id].crowdedPct)])));
  L.push("");
  L.push(`- **濁り（200-500Hz）**: 全体に占める割合の中央値 ${f1(mk.mud.shareMedianDb)}dB／上位 10% ${f1(mk.mud.shareP90Db)}dB（目標 ${MIX_RULES.mudShareTargetDb}dB【推】。超過 ${mk.mud.excessDb}dB）。寄与の大きいパート: ${mk.mud.top.map((t) => `${units.find((u) => u.id === t.id)?.label ?? t.id} ${t.pct}%`).join("、")}`);
  if (mk.kickBass) L.push(`- **キックとベースの低域（${mk.kickBass.bandLabel}）**: 両方が鳴っている窓 ${mk.kickBass.bothActivePct}%、そのうち差が 4dB 以内（ぶつかっている）の窓 ${mk.kickBass.closePct}%（目安 ${MIX_RULES.kickBassClosePct}% 未満）`);
  else L.push("- キックとベースの低域: キックかベースが無い（またはドラムを分けられなかった）ので測っていません");
  for (const c of mk.clarity) {
    const need = ROLE_SPECS[c.role as keyof typeof ROLE_SPECS]?.clarity?.minMedianDb;
    L.push(`- **聞こえやすさ ${units.find((u) => u.id === c.id)?.label ?? c.id}（${c.bands.join("+")}）**: 他のパート全部との差 中央値 ${sgn(c.medianDb)}dB／下位 10% ${sgn(c.p10Db)}dB（目安 ${need === undefined ? "—" : `${need}dB 以上`}、プラスなら抜けている）`);
  }
  if (mk.pairs.length) {
    L.push("- **同じ帯域で同時に強い組み合わせ（上位）**:");
    for (const p of mk.pairs.slice(0, 6)) L.push(`  - ${units.find((u) => u.id === p.a)?.label ?? p.a} × ${units.find((u) => u.id === p.b)?.label ?? p.b}: ${BANDS.find((b) => b.id === p.band)?.label} で ${p.pct}%`);
  }
  L.push("");

  L.push("## 4. 最後のまとめ（全体＝master-preset 適用後）");
  L.push("");
  L.push(`書き出しの合否表: ${fin.rep.line}`);
  L.push("");
  L.push(table(["指標", "測定", "目標", "判定"], fin.advice.rows.map((r) => [r.name, r.value, r.target, mark(r.status)])));
  L.push("");
  L.push(`推奨 master-preset: \`${fin.advice.preset}\`（いま \`${d.presetName}\`）`);
  for (const n of fin.advice.notes) L.push(`- ${n}`);
  for (const w of stereoWarnings({ stereo: { corr: fin.masterMeasure.corr, widthDb: fin.masterMeasure.widthDb, balanceDb: fin.masterMeasure.balanceDb, lowCorr: fin.masterMeasure.lowCorr } } as Analysis)) L.push(`- ${w}`);
  if (fin.advice.eq.length) L.push(`- 全体の EQ の追加案（今の preset の上に足す。build の引数には無いので、master.mjs の preset を作るときの目安）: ${fin.advice.eq.map((e) => `${e.type === "hs" ? "高域シェルフ" : "ピーク"} ${e.f}Hz ${sgn(e.g)}dB`).join("、")}`);
  L.push("");
  L.push("書き出しの例:");
  L.push("");
  L.push("```");
  L.push(`node tools/composer/song.mjs build ${d.appliedTo ?? d.proposalFile} --wav ${d.buildFlags} --master-preset ${fin.advice.preset}`.replace(/ +/g, " "));
  L.push("```");
  L.push("");

  L.push("## 5. 調整案" + (d.loop ? "（最後の測定で、まだ出ている案）" : ""));
  L.push("");
  if (!fin.plan.changes.length) L.push("新しい調整案はありません。");
  for (const c of fin.plan.changes) {
    L.push(`- **${label(c.index)}**`);
    for (const r of c.reasons) L.push(`  - ${r}`);
  }
  if (fin.plan.advisories.length) {
    L.push("");
    L.push("書き込めない提案・注意:");
    for (const a of fin.plan.advisories) L.push(`- ${a.target}: ${a.text}`);
  }
  L.push("");

  if (d.history.length > 1) {
    L.push("## 6. 反復の推移");
    L.push("");
    L.push(table(["回", "ぐじゃぐじゃ", "濁り 200-500 超過 dB", "目標外のパート", "LUFS", "TP", "PLR", "この回で出た調整数"], d.history.map((h) => [String(h.iteration), String(h.mess.value), String(h.mud.excessDb), String(h.rows.filter((r) => r.status !== "ok").length), f1(h.master.lufs), f1(h.master.tpDb), f1(h.master.plr), String(h.changes.length)])));
    L.push("");
  }

  L.push("## 7. 直したこと・まだ残る問題");
  L.push("");
  L.push("### 直したこと（元の曲 → " + (d.loop ? "反映後の曲" : "提案版の曲") + "）");
  const diff = describeDiff(d.originalSong, d.finalSong, label);
  if (diff.length) for (const t of diff) L.push(t);
  else L.push("- 変更なし（測った範囲では、動かす必要のある差が見つかりませんでした）");
  L.push("");
  L.push("### まだ残る問題");
  const rest: string[] = [];
  for (const r of fin.plan.rows.filter((x) => x.status !== "ok")) rest.push(`${r.label}: 大きさが目標から ${sgn(r.diffDb)}dB（許す幅 ±${r.tolDb}）${r.stepDb ? "" : "。動かす量が小さいか、上限に達したため動かしていません"}`);
  if (last.mess.value >= MIX_RULES.messWarn) rest.push(`ぐじゃぐじゃ指数 ${last.mess.value}（${messLabel(last.mess.value)}）。内訳: 濁り ${last.mess.mud}／中域の混み ${last.mess.midCrowd}%${last.mess.lowCollision !== null ? `／キック×ベース ${last.mess.lowCollision}%` : ""}${last.mess.leadBuried !== null ? `／リードの埋もれ ${last.mess.leadBuried}` : ""}。EQ・gainDb では足りない分は、音域をずらす（オクターブ）・同じ音域のパートを減らす・休符を入れる、という編曲の直しが必要`);
  if (mk.crowd.mid.crowdedPct >= MIX_RULES.midCrowdWarnPct) rest.push(`Mid（500-2k）で 3 パート以上が同時に強い窓が ${mk.crowd.mid.crowdedPct}%（目安 ${MIX_RULES.midCrowdWarnPct}% 未満）。ギター 2 本・鍵盤・リードの音域が重なっています`);
  for (const r of fin.advice.rows.filter((x) => x.status === "off")) rest.push(`全体: ${r.name} が ${r.value}（目標 ${r.target}）`);
  for (const a of fin.plan.advisories) rest.push(`${a.target}: ${a.text}`);
  for (const w of fin.warnings.filter((x) => /重なっています|合計|集まっています/.test(x)).slice(0, 6)) rest.push(`楽譜の点検: ${w}`);
  if (rest.length) for (const t of rest) L.push(`- ${t}`); else L.push("- 測った範囲では、目標から外れた所はありません。");
  L.push("");
  L.push("### 限界（この自動ミックスで分かっていないこと）");
  L.push("- **耳での確認はしていません。** 数字が「すっきり」でも、実際に聞いて濁って聞こえることがあります（逆もあります）。");
  L.push("- 目標値のうち【出】は実際の録音の測定や記事の数字ですが、対象は主にパンク5曲・歌ありです。歌のない曲のリードや、鍵盤・弦・ブラスの値は【推】です。");
  L.push("- パートの音は、MIDI の残響の送り（reverb）・全体の EQ／圧縮／ホール残響の前で測っています。全体の音との差は、全体の測定（第 4 節）で見ます。");
  L.push(`- 目標との比較に使った大きさは「鳴っている間の左右の力の平均」（RMS）です。LUFS（K 特性）とは低域・高域の重みが違います。volume の変更量は SoundFont の 2 乗則（${MIX_RULES.volumeDbPerDecade}·log10）で見積もっており、実測と合わないときは --loop で追い込みます。`);
  L.push("- ぐじゃぐじゃ指数は、このツールで決めた目安の合成値（濁り・中域の混み・低域のぶつかり・リードの埋もれの平均）で、耳での「ぐじゃぐじゃ感」と照らして校正したものではありません。");
  void GROUP_TARGETS;
  return L.join("\n") + "\n";
}
