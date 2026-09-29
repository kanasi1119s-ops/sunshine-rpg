// 画面（作曲ソフト）に、デスクトップ版だけの機能（APIキーの保存とAI作曲）を渡す窓口。キーそのものは画面に返さない。
const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("sunshineDesktop", {
  keyStatus: () => ipcRenderer.invoke("key:status"),
  setKey: (key) => ipcRenderer.invoke("key:set", key),
  clearKey: () => ipcRenderer.invoke("key:clear"),
  /** { model, effort, request, system, schema, continue } → { text, usage } */
  compose: (req) => ipcRenderer.invoke("ai:compose", req),
  /** 「名前を付けて保存」。保存した場所（やめたら null）を返す。 */
  saveFile: (name, data) => ipcRenderer.invoke("file:save", name, data),
  /** アンプの追加フォルダにある、アンプ定義ファイルの一覧 [{ file, text }]。 */
  listAmpPlugins: () => ipcRenderer.invoke("amp:list"),
  openAmpFolder: () => ipcRenderer.invoke("amp:open-folder"),
});
