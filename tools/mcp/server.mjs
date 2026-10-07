// サンシャイン作曲ソフトのコネクタ（MCPサーバー）。Claude Code や Claude デスクトップから、道具として作曲ソフトを使える。
// APIキーはいらない（曲は、つないだ Claude が書く）。起動: node tools/mcp/server.mjs（標準入出力でやりとりする）
//
// 道具:
//   song_guide          曲の書き方（AIソング形式）・楽器・ジャンル別アンプの一覧
//   compose_song        曲（AIソング形式）を確かめて、作曲ソフトのプロジェクト・MIDI・WAV を作る
//   register_game_song  作った曲を、ゲームの曲として登録する
//   list_game_songs     ゲームの曲の一覧（ID・場面）
//   composer_path       作曲ソフト（1ファイルのHTML）の場所。なければ作る
import fs from "fs";
import path from "path";
import { execSync } from "child_process";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { openSongKit, ROOT } from "../composer/song-lib.mjs";

let kitPromise = null;
const kit = () => (kitPromise ??= openSongKit());
const text = (t) => ({ content: [{ type: "text", text: t }] });
const fail = (t) => ({ content: [{ type: "text", text: t }], isError: true });
const NAME = z.string().regex(/^[a-z0-9][a-z0-9-]*$/).describe("ファイル名に使う名前（英小文字・数字・-）。同じ名前で呼ぶと上書き（曲の直し）");

const server = new McpServer({ name: "sunshine-composer", version: "1.0.0" });

server.registerTool("song_guide", {
  title: "曲の書き方を読む",
  description: "サンシャイン作曲ソフトで曲を作る前に必ず読む。AIソング形式（コード進行＋「音名:拍」で書くパート）の書き方、使える楽器、ジャンル別アンプの一覧、よい曲にするコツ、既存曲をまねしない決まり。",
  inputSchema: {},
}, async () => {
  const k = await kit();
  return text(`${await k.guide()}\n\n## 見本\n${fs.readFileSync(path.join(ROOT, "assets-src/ai-songs/harbor-night.json"), "utf8")}`);
});

server.registerTool("compose_song", {
  title: "曲を作る（書き出す）",
  description: "AIソング形式の曲を確かめて、作曲ソフトで開けるプロジェクト（.sunshine-song.json）・MIDI・WAV（任意）を dist-songs/ に書き出す。曲の元（JSON）は assets-src/ai-songs/<name>.json に保存する。まちがいがあれば、場所つきで返すので、直してもう一度呼ぶ。先に song_guide を読むこと。",
  inputSchema: {
    name: NAME,
    song: z.record(z.string(), z.unknown()).describe("AIソング形式の曲（title, description, bpm, beats, chords, barsPerChord, repeats, autoAccompaniment, feel, tone, parts）"),
    edition: z.enum(["real", "ps2", "modern"]).optional().describe("サウンドの版（既定 real＝実楽器）"),
    wav: z.boolean().optional().describe("WAVも作るか（既定 true。Playwright が必要）"),
    bass: z.enum(["std", "finger", "pick"]).optional().describe("WAVのベース音源。std＝標準（既定）、finger＝エレキベース指弾き、pick＝エレキベースのピック弾き（FreePats、CC0）"),
    drums: z.enum(["std", "muldjord"]).optional().describe("WAVのドラム音源。std＝標準（既定）、muldjord＝生ドラム Muldjord Kit（CC BY 4.0）"),
    soundfont: z.enum(["game", "gu"]).optional().describe("WAVの録音音源。game＝ゲームと同じ FluidR3（既定）、gu＝GeneralUser GS（作曲ソフトだけ）"),
  },
}, async ({ name, song, edition, wav, soundfont, bass, drums }) => {
  try {
    const k = await kit();
    const src = path.join(ROOT, "assets-src/ai-songs", `${name}.json`);
    let r;
    try {
      r = await k.build(song, { name, edition: edition ?? "real", wav: wav ?? true, soundfont: soundfont ?? "game", bass: bass ?? "std", drums: drums ?? "std" });
    } catch (e) {
      if (!/Playwright/.test(e.message)) throw e;
      r = await k.build(song, { name, edition: edition ?? "real", wav: false });
      r.warnings.push(e.message);
    }
    fs.mkdirSync(path.dirname(src), { recursive: true });
    fs.writeFileSync(src, JSON.stringify(song, null, 2) + "\n");
    return text([
      `○ 「${r.title}」を作りました（${r.tracks}トラック・${r.seconds}秒・テンポ${r.bpm}）`,
      r.description,
      ...r.warnings.map((w) => `注意: ${w}`),
      `曲の元: ${src}`,
      `プロジェクト: ${r.files.project}（作曲ソフトの「プロジェクトを読み込む」で開ける）`,
      `MIDI: ${r.files.midi}`,
      r.files.wav ? `WAV: ${r.files.wav}` : "WAV: 作っていません",
    ].join("\n"));
  } catch (e) {
    return fail(`× 曲を組み立てられませんでした。次を直して、もう一度 compose_song を呼んでください:\n${e.message}`);
  }
});

server.registerTool("register_game_song", {
  title: "ゲームの曲として登録する",
  description: "compose_song で作った曲（dist-songs/<name>.sunshine-song.json）を、ゲームの曲一覧に登録する（src/audio/songs/<id>.sunshine-song.json）。既存の曲IDとは重ねられない。人間に頼まれたときだけ使う。",
  inputSchema: {
    name: NAME,
    id: z.string().regex(/^[a-z0-9][a-z0-9-]*$/).describe("ゲームでの曲ID"),
    scene: z.string().describe("どの場面の曲か（例: 雪の港町）"),
  },
}, async ({ name, id, scene }) => {
  try {
    const project = JSON.parse(fs.readFileSync(path.join(ROOT, "dist-songs", `${name}.sunshine-song.json`), "utf8"));
    const target = await (await kit()).register(project.score, { id, title: project.name, scene });
    return text(`○ 登録しました: ${target}\n鳴らす場面は、ゲーム側の bgmId に「${id}」を書いて決めます。`);
  } catch (e) {
    return fail(`× 登録できませんでした: ${e.message}`);
  }
});

server.registerTool("list_game_songs", {
  title: "ゲームの曲の一覧",
  description: "ゲームに入っている曲（ID・曲名・場面・曲調）の一覧。新しい曲の場面や雰囲気を決めるときの参考、IDの重なりの確認に使う。",
  inputSchema: {},
}, async () => {
  const list = await (await kit()).listGameSongs();
  return text(list.map((s) => `${s.id}｜${s.title}｜${s.scene}｜${s.style}`).join("\n"));
});

server.registerTool("composer_path", {
  title: "作曲ソフトの場所",
  description: "作曲ソフト（ブラウザで開く1ファイルのHTML）の場所を返す。まだなければ作る。人間が曲を聴いたり手直ししたりするときに案内する。",
  inputSchema: {},
}, async () => {
  const html = path.join(ROOT, "dist-composer/index.html");
  if (!fs.existsSync(html)) execSync(`node ${JSON.stringify(path.join(ROOT, "tools/composer/build.mjs"))}`, { stdio: "ignore" });
  return text(`作曲ソフト: ${html}\nブラウザで開き、「プロジェクトを読み込む」で dist-songs/ の .sunshine-song.json を開くと、聴いたり直したりできます。`);
});

await server.connect(new StdioServerTransport());
