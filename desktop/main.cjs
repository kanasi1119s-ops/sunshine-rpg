// サンシャイン作曲ソフト（デスクトップ版）の本体。
// 画面（app/index.html）は、ブラウザ版と同じ作曲ソフト。AIで作曲するときの Anthropic APIキーは、この本体の側だけで扱う。
// - キーは、OSの暗号化のしくみ（Windows の DPAPI・macOS のキーチェーンなど、Electron の safeStorage）で暗号化して保存する
// - 画面の側には、キーそのものを返さない（「保存してあるか」と、末尾4文字だけ）
// - AIとのやりとりは、この本体から api.anthropic.com へ直接行う
const { app, BrowserWindow, ipcMain, safeStorage, shell, Menu, dialog, session } = require("electron");
const fs = require("fs");
const path = require("path");
const { composeWithClaude } = require("./ai.cjs");
const { encodeMp3 } = require("./mp3.cjs");

const keyFile = () => path.join(app.getPath("userData"), "anthropic-key.bin");
/** アンプの追加フォルダ。ここに置いた .sunshine-amp.json を、起動時に読み込む。 */
const ampFolder = () => path.join(app.getPath("userData"), "amp-plugins");
let memoryKey = null; // 暗号化が使えない環境では、保存せず、起動中だけ覚える

/** 本当にOSの機能で暗号化できるか（Linux で鍵の保管庫がないときの「basic_text」は、暗号化と見なさない）。 */
function canEncrypt() {
  if (!safeStorage.isEncryptionAvailable()) return false;
  if (process.platform === "linux" && typeof safeStorage.getSelectedStorageBackend === "function") return safeStorage.getSelectedStorageBackend() !== "basic_text";
  return true;
}

function readKey() {
  if (memoryKey) return memoryKey;
  try {
    if (!canEncrypt()) return null;
    return safeStorage.decryptString(fs.readFileSync(keyFile()));
  } catch {
    return null;
  }
}

function createWindow() {
  const win = new BrowserWindow({
    width: 1480, height: 960, minWidth: 900, minHeight: 600, backgroundColor: "#05080e", title: "サンシャイン作曲ソフト",
    webPreferences: { preload: path.join(__dirname, "preload.cjs"), contextIsolation: true, sandbox: true, nodeIntegration: false, webSecurity: true, spellcheck: false },
  });
  // 画面の中で別のページへ移ったり、新しい窓を開いたりさせない（リンクは、ふだんのブラウザで開く）
  win.webContents.on("will-navigate", (e) => e.preventDefault());
  win.webContents.setWindowOpenHandler(({ url }) => {
    if (/^https:\/\//.test(url)) void shell.openExternal(url);
    return { action: "deny" };
  });
  void win.loadFile(path.join(__dirname, "app", "index.html"));
}

function buildMenu() {
  // 配布物では、ライセンス文と規約は resources の下（OSのファイル画面で開けるよう、アーカイブの外）に置く
  const res = (name) => (app.isPackaged ? path.join(process.resourcesPath, name) : path.join(__dirname, name));
  const licenses = res("licenses");
  Menu.setApplicationMenu(Menu.buildFromTemplate([
    ...(process.platform === "darwin" ? [{ role: "appMenu" }] : []),
    { label: "ファイル", submenu: [{ role: "quit", label: "終了" }] },
    { label: "編集", submenu: [{ role: "undo", label: "元に戻す" }, { role: "redo", label: "やり直す" }, { type: "separator" }, { role: "cut", label: "切り取り" }, { role: "copy", label: "コピー" }, { role: "paste", label: "貼り付け" }, { role: "selectAll", label: "すべて選択" }] },
    { label: "表示", submenu: [{ role: "resetZoom", label: "実際の大きさ" }, { role: "zoomIn", label: "拡大" }, { role: "zoomOut", label: "縮小" }, { type: "separator" }, { role: "togglefullscreen", label: "全画面" }] },
    {
      label: "ヘルプ",
      submenu: [
        { label: "このソフトについて", click: () => void dialog.showMessageBox({ type: "info", title: "サンシャイン作曲ソフト", message: `サンシャイン作曲ソフト ${app.getVersion()}`, detail: "© サンシャインソフトウェア\n\n使っている部品のライセンスは、「ヘルプ」→「ライセンス」で見られます。" }) },
        { label: "ライセンス", click: () => void shell.openPath(licenses) },
        { label: "利用規約", click: () => void shell.openPath(path.join(res("legal"), "terms-ja.md")) },
        { label: "プライバシーポリシー", click: () => void shell.openPath(path.join(res("legal"), "privacy-ja.md")) },
        { label: "アンプの追加フォルダを開く", click: () => openAmpFolder() },
      ],
    },
  ]));
}

function openAmpFolder() {
  fs.mkdirSync(ampFolder(), { recursive: true });
  void shell.openPath(ampFolder());
}

// 保存: 「名前を付けて保存」の画面で場所を選んでもらい、そこへ書く
const FILTERS = { mp3: "MP3", wav: "WAV", flac: "FLAC", opus: "Ogg Opus", mid: "MIDI", musicxml: "MusicXML", csv: "CSV", json: "JSON" };
ipcMain.handle("file:save", async (e, name, data) => {
  if (typeof name !== "string" || !(data instanceof Uint8Array)) throw new Error("保存するデータが違います");
  const ext = path.extname(name).slice(1).toLowerCase();
  const win = BrowserWindow.fromWebContents(e.sender);
  const r = await dialog.showSaveDialog(win, {
    defaultPath: path.join(app.getPath("documents"), path.basename(name)),
    filters: [{ name: FILTERS[ext] ?? ext.toUpperCase(), extensions: [ext] }, { name: "すべてのファイル", extensions: ["*"] }],
  });
  if (r.canceled || !r.filePath) return null;
  fs.writeFileSync(r.filePath, data);
  return r.filePath;
});

// アンプの追加フォルダの中身（アンプ定義ファイル）を返す。形のチェックは画面の側で行う
ipcMain.handle("amp:list", () => {
  fs.mkdirSync(ampFolder(), { recursive: true });
  const out = [];
  for (const f of fs.readdirSync(ampFolder())) {
    if (!f.endsWith(".sunshine-amp.json")) continue;
    try {
      const text = fs.readFileSync(path.join(ampFolder(), f), "utf8");
      if (text.length < 20_000_000) out.push({ file: f, text });
    } catch {
      // 読めないファイルはとばす
    }
  }
  return out;
});
ipcMain.handle("amp:open-folder", () => openAmpFolder());

// MP3 に変換する（LAME は本体の側で、別のファイルのまま使う）
ipcMain.handle("mp3:encode", async (_e, channels, sampleRate, kbps) => {
  if (!Array.isArray(channels) || !channels.every((c) => c instanceof Float32Array) || typeof sampleRate !== "number") throw new Error("変換するデータが違います");
  return encodeMp3(channels, sampleRate, kbps);
});

ipcMain.handle("key:status", () => {
  const key = readKey();
  return { hasKey: !!key, last4: key ? key.slice(-4) : "", canSave: canEncrypt() };
});
ipcMain.handle("key:set", (_e, key) => {
  if (typeof key !== "string" || !/^sk-ant-[A-Za-z0-9_-]{10,}$/.test(key.trim())) throw new Error("APIキーの形が違います（sk-ant- で始まります）");
  const k = key.trim();
  if (canEncrypt()) {
    fs.mkdirSync(path.dirname(keyFile()), { recursive: true });
    fs.writeFileSync(keyFile(), safeStorage.encryptString(k), { mode: 0o600 });
    memoryKey = null;
  } else {
    memoryKey = k;
  }
  return { hasKey: true, last4: k.slice(-4), canSave: canEncrypt() };
});
ipcMain.handle("key:clear", () => {
  memoryKey = null;
  try {
    fs.rmSync(keyFile(), { force: true });
  } catch {
    // 消せなくても続ける
  }
  return { hasKey: false, last4: "", canSave: canEncrypt() };
});

// やりとりの記録は、窓ごとに本体の側で持つ（「直して」と頼むときに続きから話せるように）
const histories = new Map();
ipcMain.handle("ai:compose", async (e, req) => {
  const key = readKey();
  if (!key) throw new Error("APIキーが保存されていません");
  const id = e.sender.id;
  const history = req && req.continue ? histories.get(id) ?? [] : [];
  const result = await composeWithClaude({ apiKey: key, history, ...req });
  histories.set(id, result.history);
  return { text: result.text, usage: result.usage };
});

app.whenReady().then(() => {
  // 使ってよいのは、MIDIキーボードと、音の入力（オーディオインターフェース・マイク）だけ。カメラ・位置などは出さない
  session.defaultSession.setPermissionRequestHandler((_wc, permission, cb, details) => {
    if (permission === "midi") return cb(true);
    if (permission === "media") {
      const types = (details && details.mediaTypes) || [];
      return cb(types.length > 0 && types.every((t) => t === "audio"));
    }
    cb(false);
  });
  session.defaultSession.setPermissionCheckHandler((_wc, permission, _origin, details) => permission === "midi" || (permission === "media" && (!details || !details.mediaType || details.mediaType === "audio")));
  buildMenu();
  createWindow();
  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});
app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});
