// 直しの記録（docs/sound/ai-composition-workflow.md の提案 7）。
// 形式（1行）: 「直す前の数字 → 直した点（1つ）→ 直した後の数字 → 耳の印象」。docs/sound/revisions.md に追記する。
//   node tools/composer/song.mjs log <曲ID> --before "LRA 0.9" --change "Bメロ最後の1小節でドラム以外を休み" --after "LRA 4.1" --ear "サビ前に静けさが出た"
import fs from "fs";
import path from "path";

const HEADER = `# 曲の直しの記録

形式: \`- 日付 曲ID: 直す前の数字 → 直した点（1つ）→ 直した後の数字 → 耳の印象\`
追記は \`node tools/composer/song.mjs log <曲ID> --before ... --change ... --after ... --ear ...\`。直しは1回に1点。同じ失敗が3回出たら、ai-composition-workflow.md か AI_SONG_GUIDE に決まりとして追記する。

`;

export const revisionFile = (root) => path.join(root, "docs", "sound", "revisions.md");

export function formatRevision({ id, before, change, after, ear, date = new Date().toISOString().slice(0, 10) }) {
  for (const [k, v] of Object.entries({ before, change, after, ear })) if (!String(v ?? "").trim()) throw new Error(`--${k} が空です。「直す前の数字 → 直した点（1つ）→ 直した後の数字 → 耳の印象」をすべて書いてください`);
  if (!/^[a-z0-9][a-z0-9-]*$/.test(id ?? "")) throw new Error(`曲IDは英小文字・数字・「-」だけ（${id}）`);
  return `- ${date} ${id}: ${before} → ${change} → ${after} → ${ear}`;
}

export function appendRevision(root, entry) {
  const line = formatRevision(entry);
  const file = revisionFile(root);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  if (!fs.existsSync(file)) fs.writeFileSync(file, HEADER);
  const cur = fs.readFileSync(file, "utf8");
  fs.writeFileSync(file, cur + (cur.endsWith("\n") ? "" : "\n") + line + "\n");
  return line;
}

export function hasRevision(root, id) {
  const file = revisionFile(root);
  return fs.existsSync(file) && fs.readFileSync(file, "utf8").split("\n").some((l) => l.startsWith("- ") && new RegExp(`^- \\S+ ${id}:`).test(l));
}

/** build の終わりに出す促し。記録があれば null。 */
export function revisionReminder(root, id) {
  return hasRevision(root, id) ? null : `直しの記録: 「${id}」はまだありません。直したら 1行残してください（node tools/composer/song.mjs log ${id} --before ... --change ... --after ... --ear ...）`;
}
