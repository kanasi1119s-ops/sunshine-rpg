import { readdirSync, statSync } from "node:fs";
import { join } from "node:path";

/**
 * 本編一式（`dist/`、公開ビルド）が32メガビット（4MiB）の容量予算に収まっているかを確認する
 * （`docs/decisions.md`・`.claude/skills/rpg-cycle/game-design.md` 2-4 参照）。
 * 1メガビット=128KiBとして、32メガビット=4MiB。
 */
const BUDGET_BYTES = 32 * 128 * 1024; // 32メガビット = 4MiB
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
    `[容量チェック] NG: ${DIST_DIR}/ が ${usedKiB}KiB で、32メガビット予算（${budgetKiB}KiB）を超えています。`,
  );
  process.exit(1);
}

console.log(`[容量チェック] OK: ${DIST_DIR}/ は ${usedKiB}KiB（32メガビット予算の${percent}%）。`);
