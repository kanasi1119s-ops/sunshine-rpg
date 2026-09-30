// Google ドライブへ、サービスアカウントでファイルを送る（rclone がなくても動く。Node だけで動く）。
//   環境変数 GDRIVE_SA_JSON   … サービスアカウントの鍵（JSON の中身全体）
//   環境変数 GDRIVE_FOLDER_ID … 送り先フォルダのID（サービスアカウントを「編集者」で共有したフォルダ）
//   node tools/drive-upload/upload.mjs <ファイル> [<ファイル> ...]
import crypto from "crypto";
import fs from "fs";
import path from "path";

const MIME = { ".mp3": "audio/mpeg", ".flac": "audio/flac", ".mid": "audio/midi", ".wav": "audio/wav", ".json": "application/json" };
const b64url = (b) => Buffer.from(b).toString("base64url");

async function accessToken(sa) {
  const now = Math.floor(Date.now() / 1000);
  const head = b64url(JSON.stringify({ alg: "RS256", typ: "JWT" }));
  const body = b64url(JSON.stringify({ iss: sa.client_email, scope: "https://www.googleapis.com/auth/drive", aud: "https://oauth2.googleapis.com/token", iat: now, exp: now + 3600 }));
  const sig = crypto.createSign("RSA-SHA256").update(`${head}.${body}`).sign(sa.private_key);
  const res = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST",
    headers: { "content-type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ grant_type: "urn:ietf:params:oauth:grant-type:jwt-bearer", assertion: `${head}.${body}.${b64url(sig)}` }),
  });
  const json = await res.json();
  if (!json.access_token) throw new Error("認証に失敗: " + JSON.stringify(json));
  return json.access_token;
}

async function upload(token, folderId, file) {
  const data = fs.readFileSync(file);
  const name = path.basename(file);
  const start = await fetch("https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable&supportsAllDrives=true&fields=id,name,size,webViewLink", {
    method: "POST",
    headers: { authorization: `Bearer ${token}`, "content-type": "application/json; charset=UTF-8", "x-upload-content-type": MIME[path.extname(name)] ?? "application/octet-stream", "x-upload-content-length": String(data.length) },
    body: JSON.stringify({ name, parents: [folderId] }),
  });
  if (!start.ok) throw new Error(`${name}: 開始に失敗 ${start.status} ${await start.text()}`);
  const put = await fetch(start.headers.get("location"), { method: "PUT", headers: { "content-length": String(data.length) }, body: data });
  const json = await put.json();
  if (!put.ok) throw new Error(`${name}: 送信に失敗 ${put.status} ${JSON.stringify(json)}`);
  if (Number(json.size) !== data.length) throw new Error(`${name}: サイズが合わない（送信 ${data.length} / ドライブ ${json.size}）`);
  console.log(`○ ${json.name}（${json.size}バイト、サイズ一致） ${json.webViewLink}`);
}

const files = process.argv.slice(2);
if (!process.env.GDRIVE_SA_JSON || !process.env.GDRIVE_FOLDER_ID || files.length === 0) {
  console.error("使い方: GDRIVE_SA_JSON と GDRIVE_FOLDER_ID を環境変数に入れて、node tools/drive-upload/upload.mjs <ファイル>...");
  process.exit(1);
}
const token = await accessToken(JSON.parse(process.env.GDRIVE_SA_JSON));
for (const f of files) await upload(token, process.env.GDRIVE_FOLDER_ID, f);
