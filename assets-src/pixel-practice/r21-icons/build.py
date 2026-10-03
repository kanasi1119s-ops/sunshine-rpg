#!/usr/bin/env python3
"""r21-icons 生成スクリプト。

使い方:  python3 build.py
- icons_*.py の絵を組み立て、自動で縁取りを足し、<種類>-<名前>.txt と pal-<種類>-<名前>.json を書き出す
- 色数・文字の抜け・大きさを自動確認する（失敗したら終了コード1）
- preview.png（種類ごとに並べて6倍拡大・ラベルつき）と icons.json（一覧）を書き出す
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from common import ART, COLORS, SIZE  # noqa: E402
import icons_equip  # noqa: E402,F401
import icons_items  # noqa: E402,F401
import icons_jobs  # noqa: E402,F401
import icons_skills  # noqa: E402,F401

MAX_COLORS = 10
KIND_ORDER = ['weapon', 'armor', 'item', 'job', 'skill', 'coin']
KIND_TITLE = {
    'weapon': '武器', 'armor': '防具', 'item': '消耗品・どうぐ',
    'job': 'ジョブのしるし', 'skill': '特技・呪文の種類', 'coin': '灯貨（お金）',
}
SCALE = 6
FONT_PATH = '/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf'


def check(kind, name, rows, pre):
    errs = []
    if len(rows) != SIZE:
        errs.append(f'行数 {len(rows)} (16であるべき)')
    for i, r in enumerate(rows):
        if len(r) != SIZE:
            errs.append(f'行{i} の長さ {len(r)}')
    used = sorted({ch for r in rows for ch in r if ch != '.'})
    for ch in used:
        if ch not in COLORS:
            errs.append(f'未定義の文字 {ch!r}')
    if len(used) > MAX_COLORS:
        errs.append(f'色が多すぎる {len(used)} > {MAX_COLORS}')
    filled = sum(1 for r in rows for ch in r if ch != '.')
    if filled < 24 or filled > 230:
        errs.append(f'塗り面積が変 {filled}')
    # 端に触れていないか（縁取りの余白）
    if any(pre[0][x] != '.' or pre[SIZE - 1][x] != '.' for x in range(SIZE)) or \
       any(pre[y][0] != '.' or pre[y][SIZE - 1] != '.' for y in range(SIZE)):
        errs.append('画像の端まで塗っている（1マスの余白がほしい）')
    return used, errs


def main():
    meta = []
    bad = 0
    for (kind, name), (desc, fn) in ART.items():
        label, use = desc.split('|', 1)
        c = fn()
        pre = c.rows()
        c.outline()
        rows = c.rows()
        used, errs = check(kind, name, rows, pre)
        if errs:
            bad += 1
            print(f'NG {kind}-{name}: ' + ' / '.join(errs))
        base = f'{kind}-{name}'
        with open(os.path.join(HERE, base + '.txt'), 'w', encoding='utf-8') as f:
            f.write('\n'.join(rows) + '\n')
        pal = {ch: COLORS[ch] for ch in used if ch in COLORS}
        with open(os.path.join(HERE, f'pal-{base}.json'), 'w', encoding='utf-8') as f:
            json.dump(pal, f, ensure_ascii=False)
        meta.append({'kind': kind, 'name': name, 'label': label, 'use': use,
                     'colors': len(used), 'rows': rows, 'pal': pal})
    with open(os.path.join(HERE, 'icons.json'), 'w', encoding='utf-8') as f:
        json.dump([{k: v for k, v in m.items() if k not in ('rows', 'pal')} for m in meta],
                  f, ensure_ascii=False, indent=1)
    render_preview(meta)
    print(f'{len(meta)} 個を書き出し。問題あり: {bad}')
    return 1 if bad else 0


def render_icon(m, bg):
    im = Image.new('RGBA', (SIZE, SIZE), bg)
    for y, r in enumerate(m['rows']):
        for x, ch in enumerate(r):
            if ch != '.':
                im.putpixel((x, y), tuple(int(m['pal'][ch][i:i + 2], 16) for i in (1, 3, 5)) + (255,))
    return im.resize((SIZE * SCALE, SIZE * SCALE), Image.NEAREST)


def render_preview(meta):
    font = ImageFont.truetype(FONT_PATH, 11)
    title_font = ImageFont.truetype(FONT_PATH, 14)
    cell_w, cell_h = SIZE * SCALE + 12, SIZE * SCALE + 24
    cols = 10
    bg = (74, 82, 100, 255)
    page_bg = (40, 44, 56)
    sections = []
    for kind in KIND_ORDER:
        items = [m for m in meta if m['kind'] == kind]
        if items:
            sections.append((kind, items))
    height = 8
    for kind, items in sections:
        height += 26 + ((len(items) + cols - 1) // cols) * cell_h + 6
    img = Image.new('RGB', (cols * cell_w + 16, height), page_bg)
    d = ImageDraw.Draw(img)
    y = 8
    for kind, items in sections:
        d.text((8, y + 2), f'{KIND_TITLE[kind]}（{len(items)}個）', font=title_font, fill=(255, 235, 170))
        y += 26
        for i, m in enumerate(items):
            cx, cy = 8 + (i % cols) * cell_w, y + (i // cols) * cell_h
            img.paste(render_icon(m, bg), (cx + 6, cy), None)
            lab = m['label']
            w = d.textlength(lab, font=font)
            d.text((cx + 6 + (SIZE * SCALE - w) / 2, cy + SIZE * SCALE + 4), lab, font=font, fill=(235, 235, 240))
        y += ((len(items) + cols - 1) // cols) * cell_h + 6
    img.save(os.path.join(HERE, 'preview.png'))
    # 実寸（1倍）の確認用: 暗い・明るい背景
    small = Image.new('RGB', (len(meta) * 18 + 4, 2 * 18 + 4), page_bg)
    for i, m in enumerate(meta):
        for j, b in enumerate(((30, 30, 40, 255), (230, 225, 210, 255))):
            im = Image.new('RGBA', (SIZE, SIZE), b)
            for yy, r in enumerate(m['rows']):
                for xx, ch in enumerate(r):
                    if ch != '.':
                        im.putpixel((xx, yy), tuple(int(m['pal'][ch][k:k + 2], 16) for k in (1, 3, 5)) + (255,))
            small.paste(im.convert('RGB'), (2 + i * 18, 2 + j * 18))
    small.resize((small.width * 2, small.height * 2), Image.NEAREST).save(os.path.join(HERE, 'preview-actual.png'))


if __name__ == '__main__':
    sys.exit(main())
