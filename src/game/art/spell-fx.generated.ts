// 自動生成（tools/pixel-art/fx/export-spell-sheets.py）。手で書きかえない。
// 術のエフェクトのコマ（ドット絵エディタで書き出したシート src/assets/spell-fx/<属性>-<種類>.png）の、大きさ・足もとの点・コマごとの [長さms, 光, 揺れ]。
// （エディタへの描き入れが終わるまでは空。空のあいだは、これまでのコードで描くエフェクトを使う）
export interface SpellFxSheet { w: number; h: number; ax: number; ay: number; flashColor: string; frames: [number, number, number][] }
export const SPELL_FX: Record<string, SpellFxSheet> = {};
