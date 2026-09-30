import { JOBS_BY_ID } from "../game/job/jobs";
import { starsOf } from "../game/job/mastery";
import type { JobMenuState } from "../game/job/job-menu";
import type { JobId, JobState } from "../game/job/types";

/** 一度に見せるジョブの行数（多いときは、カーソルのまわりを見せる）。 */
const MAX_VISIBLE_JOBS = 12;

const LINE = 12;
const PAD = 6;

export interface JobMenuMember {
  id: string;
  name: string;
}

export function renderJobMenu(
  ctx: CanvasRenderingContext2D,
  state: JobMenuState,
  members: JobMenuMember[],
  jobStates: Record<string, JobState>,
  jobIds: JobId[],
  screenWidth: number,
  screenHeight: number,
): void {
  if (!state.open) {
    return;
  }
  const rows = state.stage === "member" ? members.length : Math.min(jobIds.length, MAX_VISIBLE_JOBS);
  const boxW = Math.min(screenWidth - 16, 260);
  const boxH = (rows + 3) * LINE + PAD * 2;
  const x = (screenWidth - boxW) / 2;
  const y = Math.max(4, (screenHeight - boxH) / 2);
  ctx.fillStyle = "rgba(20, 16, 6, 0.95)";
  ctx.fillRect(x, y, boxW, boxH);
  ctx.strokeStyle = "#f2c14e";
  ctx.strokeRect(x, y, boxW, boxH);
  ctx.font = "10px monospace";
  ctx.textBaseline = "top";

  const member = members[state.memberCursor];
  const mState = member ? jobStates[member.id] : undefined;
  ctx.fillStyle = "#f2c14e";
  ctx.fillText(
    state.stage === "member" ? "ジョブ：だれを変える？（Xで閉じる）" : `${member?.name ?? ""}のジョブを選ぶ`,
    x + PAD,
    y + PAD,
  );

  if (state.stage === "member") {
    members.forEach((m, i) => {
      const equipped = jobStates[m.id]?.equipped;
      const jobName = equipped ? `${JOBS_BY_ID[equipped].name} ☆${starsOf(jobStates[m.id], equipped)}` : "ジョブなし";
      ctx.fillStyle = i === state.memberCursor ? "#f2c14e" : "#f0f0f0";
      ctx.fillText(`${i === state.memberCursor ? "▶" : " "} ${m.name}　${jobName}`, x + PAD, y + PAD + LINE * (i + 1));
    });
    return;
  }
  const start = Math.max(0, Math.min(state.jobCursor - Math.floor(MAX_VISIBLE_JOBS / 2), jobIds.length - MAX_VISIBLE_JOBS));
  jobIds.slice(start, start + MAX_VISIBLE_JOBS).forEach((jobId, row) => {
    const i = start + row;
    const job = JOBS_BY_ID[jobId];
    const stars = mState ? starsOf(mState, job.id) : 1;
    const now = mState?.equipped === job.id ? "（装備中）" : "";
    ctx.fillStyle = i === state.jobCursor ? "#f2c14e" : "#f0f0f0";
    ctx.fillText(`${i === state.jobCursor ? "▶" : " "} ${job.name} ☆${stars}${now}`, x + PAD, y + PAD + LINE * (row + 1));
  });
  const cur = JOBS_BY_ID[jobIds[state.jobCursor]];
  const shown = Math.min(jobIds.length, MAX_VISIBLE_JOBS);
  ctx.fillStyle = "#c8c8c8";
  ctx.fillText(cur.role.slice(0, 26), x + PAD, y + PAD + LINE * (shown + 1));
  const stars = mState ? starsOf(mState, cur.id) : 1;
  const next = cur.skills.find((skill) => skill.requiredStars > stars);
  ctx.fillText(next ? `次の特技：${next.name}（☆${next.requiredStars}）` : "特技はすべて習得ずみ", x + PAD, y + PAD + LINE * (shown + 2));
}
