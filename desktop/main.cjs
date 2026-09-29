// サンシャイン作曲ソフト（デスクトップ版）の本体。
// 画面（app/index.html）は、ブラウザ版と同じ作曲ソフト。AIで作曲するときの Anthropic APIキーは、この本体の側だけで扱う。
// - キーは、OSの暗号化のしくみ（Windows の DPAPI・macOS のキーチェーンなど、Electron の safeStorage）で暗号化して保存する
// - 画面の側には、キーそのものを返さない（「保存してあるか」と、末尾4文字だけ）
// - AIとのやりとりは、この本体から api.anthropic.com へ直接行う
const { app, BrowserWindow, ipcMain, safeStorage, shell, Menu, dialog } = require("electron");
const fs = require("fs");
const path = require("path");
const { composeWithClaude } = require("./ai.cjs");

const keyFile = () => path.join(app.getPath("userData"), "anthropic-key.bin");
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
  const licenses = path.join(__dirname, "licenses");
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
      ],
    },
  ]));
}

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
  buildMenu();
  createWindow();
  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});
app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});
