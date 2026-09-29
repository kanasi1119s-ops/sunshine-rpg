// 画面（作曲ソフト）に、デスクトップ版だけの機能（APIキーの保存とAI作曲）を渡す窓口。キーそのものは画面に返さない。
const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("sunshineDesktop", {
  keyStatus: () => ipcRenderer.invoke("key:status"),
  setKey: (key) => ipcRenderer.invoke("key:set", key),
  clearKey: () => ipcRenderer.invoke("key:clear"),
  /** { model, effort, request, system, schema, continue } → { text, usage } */
  compose: (req) => ipcRenderer.invoke("ai:compose", req),
});
