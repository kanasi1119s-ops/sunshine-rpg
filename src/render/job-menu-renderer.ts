import { INITIAL_JOBS, JOBS_BY_ID } from "../game/job/jobs";
import { starsOf } from "../game/job/mastery";
import type { JobMenuState } from "../game/job/job-menu";
import type { JobState } from "../game/job/types";

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
  screenWidth: number,
  screenHeight: number,
): void {
  if (!state.open) {
    return;
  }
  const rows = state.stage === "member" ? members.length : INITIAL_JOBS.length;
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
  INITIAL_JOBS.forEach((job, i) => {
    const stars = mState ? starsOf(mState, job.id) : 1;
    const now = mState?.equipped === job.id ? "（装備中）" : "";
    ctx.fillStyle = i === state.jobCursor ? "#f2c14e" : "#f0f0f0";
    ctx.fillText(`${i === state.jobCursor ? "▶" : " "} ${job.name} ☆${stars}${now}`, x + PAD, y + PAD + LINE * (i + 1));
  });
  const cur = INITIAL_JOBS[state.jobCursor];
  ctx.fillStyle = "#c8c8c8";
  ctx.fillText(cur.role.slice(0, 26), x + PAD, y + PAD + LINE * (INITIAL_JOBS.length + 1));
  const stars = mState ? starsOf(mState, cur.id) : 1;
  const next = cur.skills.find((s) => s.requiredStars > stars);
  ctx.fillText(next ? `次の特技：${next.name}（☆${next.requiredStars}）` : "特技はすべて習得ずみ", x + PAD, y + PAD + LINE * (INITIAL_JOBS.length + 2));
}
