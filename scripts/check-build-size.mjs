import { readdirSync, statSync } from "node:fs";
import { join } from "node:path";

/**
 * 本編一式（`dist/`、公開ビルド）が容量予算（現在128メガビット=16MiB。もとは32メガビット）に収まっているかを確認する
 * （`docs/decisions.md`・`.claude/skills/rpg-cycle/game-design.md` 2-4 参照）。
 * 1メガビット=128KiBとして、128メガビット=16MiB。
 */
const BUDGET_MEGABITS = 128; // 2026-09-30 に人間の指示（「容量が足りなくなったら増やしてよい」）で 32 → 64 → 128 に拡大（録音音源・実楽器版の追加。docs/decisions.md）
const BUDGET_BYTES = BUDGET_MEGABITS * 128 * 1024;
const DIST_DIR = "dist";

function totalSize(dir) {
  let total = 0;
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) {
      total += totalSize(path);
    } else {
      total += statSync(path).size;
    }
  }
  return total;
}

const used = totalSize(DIST_DIR);
const usedKiB = (used / 1024).toFixed(1);
const budgetKiB = (BUDGET_BYTES / 1024).toFixed(0);
const percent = ((used / BUDGET_BYTES) * 100).toFixed(1);

if (used > BUDGET_BYTES) {
  console.error(
    `[容量チェック] NG: ${DIST_DIR}/ が ${usedKiB}KiB で、${BUDGET_MEGABITS}メガビット予算（${budgetKiB}KiB）を超えています。`,
  );
  process.exit(1);
}

console.log(`[容量チェック] OK: ${DIST_DIR}/ は ${usedKiB}KiB（${BUDGET_MEGABITS}メガビット予算の${percent}%）。`);
