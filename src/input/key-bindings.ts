/**
 * パソコンの操作キーの設定。ゲームの中の操作を「動作」（うごく・決定・もどる…）に分け、動作ごとにキーを割り当てる。
 * 初期設定は、これまでのキー（矢印・WASD、決定=Enter/Space/Z、もどる=X、メニュー=Tab/Esc、ジョブ=C、地図=V）。
 * 設定をかえたときだけ、キーを「元のゲームが読むキー」にいれかえて（`attachKeyRemap`）、ゲーム本体は変えずに使う。
 * 設定はこのブラウザ（localStorage）に保存する。
 */
export type ControlAction = "up" | "down" | "left" | "right" | "confirm" | "back" | "menu" | "job" | "map";

export const CONTROL_ACTIONS: { id: ControlAction; label: string }[] = [
  { id: "up", label: "うえへ" },
  { id: "down", label: "したへ" },
  { id: "left", label: "ひだりへ" },
  { id: "right", label: "みぎへ" },
  { id: "confirm", label: "決定・調べる" },
  { id: "back", label: "もどる" },
  { id: "menu", label: "メニュー" },
  { id: "job", label: "ジョブ画面" },
  { id: "map", label: "世界地図の全体図" },
];

export type KeyBindings = Record<ControlAction, string[]>;

export const DEFAULT_BINDINGS: KeyBindings = {
  up: ["ArrowUp", "w"],
  down: ["ArrowDown", "s"],
  left: ["ArrowLeft", "a"],
  right: ["ArrowRight", "d"],
  confirm: ["Enter", " ", "z"],
  back: ["x"],
  menu: ["Tab", "Escape"],
  job: ["c"],
  map: ["v"],
};

/** ゲーム本体が読むキー（動作ごとの代表）。設定をかえたとき、押されたキーを、これにいれかえてゲームに渡す。 */
export const CANONICAL_KEY: Record<ControlAction, string> = {
  up: "ArrowUp",
  down: "ArrowDown",
  left: "ArrowLeft",
  right: "ArrowRight",
  confirm: "Enter",
  back: "x",
  menu: "Escape",
  job: "c",
  map: "v",
};

const STORAGE_KEY = "sunshine-rpg-key-bindings";

/** 文字キーは大文字小文字を区別しない（Shiftを押していても同じキーとして扱う）。 */
export function normalizeKey(key: string): string {
  return key.length === 1 ? key.toLowerCase() : key;
}

export function cloneBindings(b: KeyBindings): KeyBindings {
  return Object.fromEntries(Object.entries(b).map(([k, v]) => [k, [...v]])) as KeyBindings;
}

export function isDefaultBindings(b: KeyBindings): boolean {
  return CONTROL_ACTIONS.every(({ id }) => b[id].length === DEFAULT_BINDINGS[id].length && b[id].every((k, i) => k === DEFAULT_BINDINGS[id][i]));
}

/** その動作に、そのキーだけを割り当てる。同じキーをほかの動作が使っていたら、そちらからはずす。 */
export function rebind(bindings: KeyBindings, action: ControlAction, key: string): KeyBindings {
  const k = normalizeKey(key);
  const next = cloneBindings(bindings);
  const previous = bindings[action].filter((x) => x !== k);
  for (const { id } of CONTROL_ACTIONS) {
    const had = next[id].includes(k);
    next[id] = next[id].filter((x) => x !== k);
    // キーをとられて空になった動作（もどる・メニューなど）には、かわりに元のキーをわたす（操作できなくなるのを防ぐ）
    if (had && id !== action && next[id].length === 0) next[id] = [...previous];
  }
  next[action] = [k];
  return next;
}

export function resetBindings(): KeyBindings {
  return cloneBindings(DEFAULT_BINDINGS);
}

/** そのキーに割り当てられている動作（なければ空）。 */
export function actionsForKey(bindings: KeyBindings, key: string): ControlAction[] {
  const k = normalizeKey(key);
  return CONTROL_ACTIONS.filter(({ id }) => bindings[id].includes(k)).map(({ id }) => id);
}

/** 画面に出すキーの名前。 */
export function keyLabel(key: string): string {
  const names: Record<string, string> = {
    ArrowUp: "↑", ArrowDown: "↓", ArrowLeft: "←", ArrowRight: "→", " ": "スペース", Enter: "Enter", Escape: "Esc", Tab: "Tab",
    Shift: "Shift", Control: "Ctrl", Backspace: "BackSpace",
  };
  return names[key] ?? (key.length === 1 ? key.toUpperCase() : key);
}

export function describeBinding(bindings: KeyBindings, action: ControlAction): string {
  return bindings[action].length > 0 ? bindings[action].map(keyLabel).join(" / ") : "（なし）";
}

export function loadBindings(storage: Pick<Storage, "getItem"> | undefined): KeyBindings {
  try {
    const raw = storage?.getItem(STORAGE_KEY);
    if (!raw) return resetBindings();
    const data = JSON.parse(raw) as Partial<Record<ControlAction, unknown>>;
    const result = resetBindings();
    for (const { id } of CONTROL_ACTIONS) {
      const list = data[id];
      if (Array.isArray(list) && list.every((x) => typeof x === "string")) {
        result[id] = (list as string[]).map(normalizeKey);
      }
    }
    return result;
  } catch {
    return resetBindings();
  }
}

export function saveBindings(storage: Pick<Storage, "setItem"> | undefined, bindings: KeyBindings): void {
  try {
    storage?.setItem(STORAGE_KEY, JSON.stringify(bindings));
  } catch {
    // 保存できなくても、遊べる
  }
}

/** ゲーム本体がもともと読むキー（設定をかえたとき、割り当てのないこれらのキーは無効にする）。 */
function allDefaultKeys(): Set<string> {
  return new Set(CONTROL_ACTIONS.flatMap(({ id }) => DEFAULT_BINDINGS[id]));
}

interface RemapEvent extends KeyboardEvent {
  __remapped?: boolean;
}

export interface KeyRemapController {
  /** 次に押されたキーを、設定の入力として受けとる（ゲームには渡さない）。 */
  captureNextKey(callback: (key: string) => void): void;
  cancelCapture(): void;
  isCapturing(): boolean;
}

/**
 * キーの入れかえ層。ほかのキー入力処理より先に動くよう、最初に呼ぶ（capture）。
 *  - 設定が初期のままなら、何もしない。
 *  - 設定をかえていたら、割り当てのあるキーを「元のゲームが読むキー」にいれかえて送り直し、元のキーは止める。
 *    どの動作にも割り当てのない、元のゲームのキーは、無効にする。
 */
export function attachKeyRemap(getBindings: () => KeyBindings): KeyRemapController {
  let capture: ((key: string) => void) | null = null;
  const handler = (event: KeyboardEvent): void => {
    const e = event as RemapEvent;
    if (e.__remapped) return;
    if (capture && event.type === "keydown") {
      event.preventDefault();
      event.stopImmediatePropagation();
      if (event.repeat) return;
      const cb = capture;
      capture = null;
      cb(event.key);
      return;
    }
    const target = event.target as HTMLElement | null;
    if (target && (target.tagName === "INPUT" || target.tagName === "TEXTAREA")) return;
    if (event.ctrlKey || event.metaKey || event.altKey) return;
    const bindings = getBindings();
    if (isDefaultBindings(bindings)) return;
    const key = normalizeKey(event.key);
    const custom = new Set(CONTROL_ACTIONS.flatMap(({ id }) => bindings[id]));
    if (!allDefaultKeys().has(key) && !custom.has(key)) return;
    event.preventDefault();
    event.stopImmediatePropagation();
    for (const action of actionsForKey(bindings, key)) {
      const sent = new KeyboardEvent(event.type, { key: CANONICAL_KEY[action], repeat: event.repeat, bubbles: true, cancelable: true }) as RemapEvent;
      sent.__remapped = true;
      window.dispatchEvent(sent);
    }
  };
  window.addEventListener("keydown", handler, true);
  window.addEventListener("keyup", handler, true);
  return {
    captureNextKey: (cb) => {
      capture = cb;
    },
    cancelCapture: () => {
      capture = null;
    },
    isCapturing: () => capture !== null,
  };
}

/** ゲーム本体に送るキーの合図（画面のボタン・コントローラーが使う）。設定の入れかえをとおらない。 */
export function sendGameKey(type: "keydown" | "keyup", action: ControlAction): void {
  const sent = new KeyboardEvent(type, { key: CANONICAL_KEY[action], bubbles: true, cancelable: true }) as RemapEvent;
  sent.__remapped = true;
  window.dispatchEvent(sent);
}
