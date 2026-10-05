import { deserializeSaveData, serializeSaveData } from "../game/save/serializer";
import type { SaveData } from "../game/save/types";

export interface BackupDialogOptions {
  /** セーブ画面から開いたときは書き出し（ファイル・テキスト）、ロード画面から開いたときは読み込み（ファイル・貼り付け）を出す。 */
  mode: "save" | "load";
  getSave: () => SaveData;
  exportFile: () => Promise<boolean>;
  pickFile: () => void;
  onLoad: (data: SaveData) => void;
}

/**
 * バックアップ用の入力欄つき画面（HTML）。スマホのアーティファクトでは、ファイル選択やダウンロードが使えないことがあるため、
 * セーブデータを「テキスト」としてコピー・貼り付けすることでも、書き出し・読み込みができるようにする。
 */
export function openBackupDialog(opts: BackupDialogOptions): void {
  const root = document.createElement("div");
  root.style.cssText = "position:fixed;inset:0;z-index:99999;background:rgba(8,6,20,.92);color:#f0f0f0;font:14px/1.5 sans-serif;display:flex;align-items:center;justify-content:center;padding:12px;box-sizing:border-box";
  const panel = document.createElement("div");
  panel.style.cssText = "width:100%;max-width:520px;max-height:100%;overflow:auto;background:#1c1840;border:2px solid #f2c14e;border-radius:8px;padding:12px;box-sizing:border-box";
  root.appendChild(panel);
  // ゲームのキー入力に、ここの文字入力が混ざらないようにする
  for (const type of ["keydown", "keyup", "keypress"]) root.addEventListener(type, (e) => e.stopPropagation());

  const title = document.createElement("div");
  title.textContent = opts.mode === "save" ? "セーブのバックアップ" : "バックアップから読み込む";
  title.style.cssText = "font-weight:bold;color:#f2c14e;margin-bottom:8px";
  const status = document.createElement("div");
  status.style.cssText = "min-height:20px;margin:6px 0;color:#88ff88;word-break:break-all";
  const area = document.createElement("textarea");
  area.style.cssText = "width:100%;height:110px;box-sizing:border-box;font:12px monospace;background:#0c0a1c;color:#f0f0f0;border:1px solid #6a6a9a;border-radius:4px";
  const say = (t: string, bad = false): void => {
    status.textContent = t;
    status.style.color = bad ? "#ff9a9a" : "#88ff88";
  };
  const btn = (label: string, fn: () => void): HTMLButtonElement => {
    const b = document.createElement("button");
    b.textContent = label;
    b.style.cssText = "display:block;width:100%;margin:6px 0;padding:10px;font-size:15px;border-radius:6px;border:1px solid #f2c14e;background:#2e2866;color:#fff";
    b.addEventListener("click", fn);
    return b;
  };
  panel.appendChild(title);
  if (opts.mode === "save") {
    area.placeholder = "「テキストを表示」を押すと、ここにセーブデータが出ます";
    area.readOnly = true;
    panel.appendChild(btn("ファイルに書き出す", () => void opts.exportFile().then((ok) => say(ok ? "ファイルに書き出しました" : "ファイルに書き出せませんでした。下の「テキスト」をお使いください", !ok))));
    panel.appendChild(btn("テキストを表示（コピー用）", () => {
      area.value = serializeSaveData(opts.getSave());
      area.focus();
      area.select();
      say("ぜんぶ選びました。コピーして、メモ帳などに貼り付けて残してください");
    }));
    panel.appendChild(btn("テキストをコピーする", () => {
      area.value = area.value || serializeSaveData(opts.getSave());
      const done = (): void => say("コピーしました。メモ帳などに貼り付けて残してください");
      const fail = (): void => { area.focus(); area.select(); say("自動でコピーできませんでした。選んだ文字を、長押ししてコピーしてください", true); };
      if (navigator.clipboard?.writeText) navigator.clipboard.writeText(area.value).then(done, fail);
      else fail();
    }));
    panel.appendChild(area);
  } else {
    area.placeholder = "コピーしておいたセーブデータのテキストを、ここに貼り付けます";
    panel.appendChild(btn("ファイルから読み込む", () => { opts.pickFile(); root.remove(); }));
    panel.appendChild(area);
    panel.appendChild(btn("貼り付けたテキストから読み込む", () => {
      try {
        const data = deserializeSaveData(area.value.trim());
        root.remove();
        opts.onLoad(data);
      } catch (e) {
        say(`読み込めませんでした（${e instanceof Error ? e.message.slice(0, 40) : "形式がちがう"}）`, true);
      }
    }));
  }
  panel.appendChild(status);
  panel.appendChild(btn("とじる", () => root.remove()));
  document.body.appendChild(root);
}
