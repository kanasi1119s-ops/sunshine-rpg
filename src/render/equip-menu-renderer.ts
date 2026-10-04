import type { EquipMenuState } from "../game/menu/equip-menu";
import { drawWindow } from "./ui-frame";
import { getPortraitIcon } from "./portrait-icons";

export interface EquipStatsView {
  level: number;
  maxHp: number;
  attack: number;
  defense: number;
  speed: number;
}

export interface EquipMemberView {
  id: string;
  name: string;
  stats: EquipStatsView;
  /** ぶき・ぼうぐ・かざり の順に、いまつけている品の名前と効果（なければ「なし」）。 */
  slots: { label: string; itemText: string }[];
}

export interface EquipCandidateView {
  /** 「はずす」か、品の名前。 */
  label: string;
  bonusText: string;
  /** 「[レト]」（その人がつけている）など。 */
  note?: string;
  /** これにかえたときの能力値（いまの人）。 */
  after?: EquipStatsView;
}

export interface EquipMenuView {
  members: EquipMemberView[];
  candidates: EquipCandidateView[];
  message: string | null;
}

const STAT_NAMES: [keyof EquipStatsView, string][] = [
  ["maxHp", "HP"],
  ["attack", "こうげき"],
  ["defense", "ぼうぎょ"],
  ["speed", "すばやさ"],
];

/** そうび画面。左に仲間、右上にその人の装備、右下に選べる品と、かえたときの強さの変化。 */
export function renderEquipMenu(ctx: CanvasRenderingContext2D, state: EquipMenuState, view: EquipMenuView, screenWidth: number, screenHeight: number): void {
  if (!state.open) return;
  drawWindow(ctx, 4, 4, screenWidth - 8, screenHeight - 8);
  ctx.textBaseline = "top";
  ctx.textAlign = "left";
  ctx.font = "10px monospace";
  ctx.fillStyle = "#f2c14e";
  const help = state.stage === "member" ? "だれの そうびを かえる？" : state.stage === "slot" ? "どれを かえる？" : "なにを つける？";
  ctx.fillText(`そうび（${help}　もどる: X）`, 12, 10);

  // 左: 仲間の一覧（顔アイコンつき）
  view.members.forEach((m, i) => {
    const y = 26 + i * 30;
    const selected = i === state.member;
    const icon = getPortraitIcon(m.name, true);
    ctx.fillStyle = "#2a2140";
    ctx.fillRect(12, y - 2, 28, 28);
    if (icon) {
      ctx.imageSmoothingEnabled = true;
      ctx.imageSmoothingQuality = "high";
      ctx.drawImage(icon, 12, y - 2, 28, 28);
      ctx.imageSmoothingEnabled = false;
    }
    ctx.strokeStyle = selected ? "#f2c14e" : "#6a5a3a";
    ctx.strokeRect(11.5, y - 2.5, 29, 29);
    ctx.fillStyle = selected ? (state.stage === "member" ? "#f2c14e" : "#ffffff") : "#a8a8c0";
    ctx.fillText(`${selected && state.stage === "member" ? "▶" : "　"}${m.name}`, 46, y);
    ctx.fillStyle = "#c8c8e0";
    ctx.fillText(`　Lv${m.stats.level}`, 46, y + 12);
  });

  const member = view.members[state.member];
  if (!member) return;
  const rx = 150;
  ctx.fillStyle = "#f0f0f0";
  ctx.fillText(`${member.name}　HP${member.stats.maxHp}　攻${member.stats.attack}　防${member.stats.defense}　速${member.stats.speed}`, rx, 26);

  // 右上: いまの装備
  member.slots.forEach((slot, i) => {
    const y = 44 + i * 15;
    const selected = i === state.slot && state.stage !== "member";
    ctx.fillStyle = selected ? "#f2c14e" : "#c8c8e0";
    ctx.fillText(`${selected && state.stage === "slot" ? "▶" : "　"}${slot.label}　${slot.itemText}`, rx, y);
  });

  // 右下: 選べる品
  if (state.stage === "item") {
    ctx.fillStyle = "#f2c14e";
    ctx.fillText("もっている品", rx, 98);
    const perPage = 6;
    const page = Math.floor(state.item / perPage);
    view.candidates.slice(page * perPage, page * perPage + perPage).forEach((c, i) => {
      const index = page * perPage + i;
      const y = 112 + i * 14;
      const selected = index === state.item;
      ctx.fillStyle = selected ? "#f2c14e" : "#f0f0f0";
      ctx.fillText(`${selected ? "▶" : "　"}${c.label}　${c.bonusText}${c.note ? `　${c.note}` : ""}`, rx, y);
    });
    const current = view.candidates[state.item];
    if (current?.after) {
      const parts = STAT_NAMES.filter(([k]) => current.after![k] !== member.stats[k]).map(([k, name]) => `${name} ${member.stats[k]}→${current.after![k]}`);
      ctx.fillStyle = "#88ff88";
      ctx.fillText(parts.length > 0 ? `かえると: ${parts.join("　")}` : "かえても、強さは変わらない", rx, 198);
    }
  }
  if (view.message) {
    ctx.fillStyle = "#88ff88";
    ctx.fillText(view.message, 12, screenHeight - 20);
  }
}
