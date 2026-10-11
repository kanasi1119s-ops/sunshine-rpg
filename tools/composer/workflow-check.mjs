// build（song-lib.mjs）の終わりに足す、曲作りの流れの注意。直前の曲と同じ選択・和音とのぶつかり・同じ4小節の反復。
// song は前処理ずみ（aiSongToScore が返す song）。曲が作れなくなるものではない（警告だけ）。
import path from "path";
import { checkNovelty, loadRecentFull } from "./novelty.mjs";
import { collectFacts } from "../audio-check/score-facts.mjs";

export function workflowWarnings(song, name, root, { n = 3 } = {}) {
  const out = [];
  try {
    const others = loadRecentFull(path.join(root, "assets-src", "ai-songs"), n, name);
    if (others.length) out.push(...checkNovelty(song, name, others).warnings);
    const f = collectFacts(song).facts;
    const avoid = f.filter((x) => x.kind === "アヴォイドノート");
    if (avoid.length) out.push(`旋律の強拍・長い音が和音の半音上でぶつかる所が${avoid.length}か所あります（最初は${avoid[0].bar}小節目: ${avoid[0].detail}）。小節ごとの一覧: node tools/audio-check/score-check.mjs <曲.json> --facts`);
    const rep = f.filter((x) => x.kind === "同じ4小節の反復");
    if (rep.length) out.push(`旋律に「同じ4小節」が3回以上出る所があります（${rep[0].detail}）。`);
  } catch (e) {
    out.push(`（曲作りの流れの点検で読み込みに失敗: ${e.message}）`);
  }
  return out;
}
