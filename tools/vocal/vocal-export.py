#!/usr/bin/env python3
"""歌の旋律と歌詞（vocal モジュール: bars() と notes() と ORDER を持つ Python ファイル）を、歌声ソフト用に書き出す。
  - OpenUtau のプロジェクト（.ustx。古い書式 0.6 で書く＝古い OpenUtau でも開ける。新しい OpenUtau は開くときに自動で直す）
    歌のトラック（歌い手・発音の変換を指定）と、伴奏の音声トラック（同じフォルダの WAV）を入れる。
  - MusicXML（歌詞つきの楽譜。OpenUtau・Synthesizer V などで読める）
  - 歌詞カード（テキスト）
使い方: python3 tools/vocal/vocal-export.py <vocal.py> --out <フォルダ> --name <曲名> --bpm 150 --key 2
        [--singer 重音テト] [--phonemizer OpenUtau.Core.DefaultPhonemizer] [--wave <伴奏.wav>] [--sections "イントロ,Aメロ,..."]
音の決まり: 1拍＝480。1音＝1文字（ひらがな）。長い音（1拍以上）にだけ、やわらかいビブラートを付ける（--no-vibrato で付けない）。
"""
import argparse, importlib.util, json, os, shutil, subprocess, wave

PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def midi(p):
    n = PC[p[0]]; i = 1
    if p[1] in "#b": n += 1 if p[1] == "#" else -1; i = 2
    return n + 12 * (int(p[i:]) + 1)

def q(s):  # YAML の文字列（単一引用符）
    return "'" + str(s).replace("'", "''") + "'"

def write_ustx(path, name, bpm, key, notes, total_beats, singer, phonemizer, wave_name, wave_ms, vibrato=True):
    T = 480
    L = []
    L += [f"name: {q(name)}", "comment: ''", "output_dir: Vocal", "cache_dir: UCache", "ustx_version: '0.6'",
          f"bpm: {bpm}", "beat_per_bar: 4", "beat_unit: 4", f"key: {key}",
          "time_signatures:", "- bar_position: 0", "  beat_per_bar: 4", "  beat_unit: 4",
          "tempos:", "- position: 0", f"  bpm: {bpm}",
          "tracks:",
          f"- singer: {q(singer)}", f"  phonemizer: {phonemizer}", f"  track_name: {q('歌（' + singer + '）')}", "  track_color: Pink",
          "  mute: false", "  solo: false", "  volume: 0", "  pan: 0"]
    if wave_name:
        L += [f"- track_name: {q('伴奏')}", "  track_color: Blue", "  mute: false", "  solo: false", "  volume: -3", "  pan: 0"]
    L += ["voice_parts:", f"- name: {q('歌')}", "  comment: ''", "  track_no: 0", "  position: 0", f"  duration: {int(total_beats * T)}", "  notes:"]
    for start, dur, pitch, kana in notes:
        long_note = dur >= 1 and vibrato
        L += [f"  - position: {int(round(start * T))}", f"    duration: {int(round(dur * T))}", f"    tone: {midi(pitch)}", f"    lyric: {q(kana)}",
              "    pitch:", "      data:", "      - {x: -25, y: 0, shape: io}", "      - {x: 25, y: 0, shape: io}", "      snap_first: true",
              ("    vibrato: {length: 45, period: 180, depth: 15, in: 20, out: 20, shift: 0, drift: 0}" if long_note
               else "    vibrato: {length: 0, period: 175, depth: 25, in: 10, out: 10, shift: 0, drift: 0}"),
              "    note_expressions: []", "    phoneme_expressions: []", "    phoneme_overrides: []"]
    L += ["  curves: []"]
    if wave_name:
        L += ["wave_parts:", f"- name: {q(wave_name)}", "  comment: ''", "  track_no: 1", "  position: 0",
              f"  relative_path: {q(wave_name)}", f"  file_duration_ms: {wave_ms:.1f}", "  skip: 0", "  trim: 0"]
    open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")

TYPES = {0.25: ("16th", 0), 0.5: ("eighth", 0), 0.75: ("eighth", 1), 1: ("quarter", 0), 1.5: ("quarter", 1), 2: ("half", 0), 3: ("half", 1), 4: ("whole", 0)}
def write_musicxml(path, name, bpm, key_fifths, bars):
    X = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 3.1 Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">',
         '<score-partwise version="3.1">', f'<work><work-title>{name}</work-title></work>',
         '<part-list><score-part id="P1"><part-name>Vocal</part-name></score-part></part-list>', '<part id="P1">']
    for i, bar in enumerate(bars):
        X.append(f'<measure number="{i + 1}">')
        if i == 0:
            X.append(f'<attributes><divisions>4</divisions><key><fifths>{key_fifths}</fifths></key><time><beats>4</beats><beat-type>4</beat-type></time><clef><sign>G</sign><line>2</line></clef></attributes>')
            X.append(f'<direction placement="above"><direction-type><metronome><beat-unit>quarter</beat-unit><per-minute>{bpm}</per-minute></metronome></direction-type><sound tempo="{bpm}"/></direction>')
        for tok in bar.split():
            if tok.startswith("R:"):
                d = float(tok[2:]); t, dot = TYPES.get(d, ("quarter", 0))
                X.append(f'<note><rest/><duration>{int(round(d * 4))}</duration><type>{t}</type>{"<dot/>" * dot}</note>')
                continue
            kana, p, d = tok.split(":"); d = float(d); t, dot = TYPES.get(d, ("quarter", 0))
            step = p[0]; alter = 1 if p[1] == "#" else (-1 if p[1] == "b" else 0); octv = p[-1]
            X.append(f'<note><pitch><step>{step}</step>{f"<alter>{alter}</alter>" if alter else ""}<octave>{octv}</octave></pitch>'
                     f'<duration>{int(round(d * 4))}</duration><type>{t}</type>{"<dot/>" * dot}'
                     f'<lyric number="1"><syllabic>single</syllabic><text>{kana}</text></lyric></note>')
        X.append('</measure>')
    X += ['</part>', '</score-partwise>']
    open(path, "w", encoding="utf-8").write("\n".join(X) + "\n")

def write_lyrics(path, name, vocal, sections):
    out = [f"『{name}』 歌詞（ひらがな＝歌声ソフトに入れる文字）", ""]
    for idx, key in enumerate(vocal.ORDER):
        label = sections[idx] if sections and idx < len(sections) else f"{idx * 8 + 1}〜{idx * 8 + 8}小節"
        if key is None:
            out.append(f"［{label}］（歌なし）"); out.append(""); continue
        out.append(f"［{label}］")
        line = ""
        for bar in vocal.V[key]:
            for ti, tok in enumerate(bar.split()):
                if tok.startswith("R:"):
                    if (float(tok[2:]) >= 1 or ti == 0) and line: out.append("  " + line); line = ""
                    elif line and not line.endswith(" "): line += " "
                else: line += tok.split(":")[0]
        if line.strip(): out.append("  " + line.strip())
        out.append("")
    open(path, "w", encoding="utf-8").write("\n".join(out))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vocal"); ap.add_argument("--out", required=True); ap.add_argument("--name", required=True)
    ap.add_argument("--bpm", type=float, required=True); ap.add_argument("--key", type=int, default=0)
    ap.add_argument("--singer", default="重音テト"); ap.add_argument("--phonemizer", default="OpenUtau.Core.DefaultPhonemizer")
    ap.add_argument("--wave"); ap.add_argument("--sections", default=""); ap.add_argument("--no-vibrato", action="store_true")
    a = ap.parse_args()
    spec = importlib.util.spec_from_file_location("vocal", a.vocal); vocal = importlib.util.module_from_spec(spec); spec.loader.exec_module(vocal)
    os.makedirs(a.out, exist_ok=True)
    notes = vocal.notes(); bars = vocal.bars()
    wave_name, wave_ms = None, 0.0
    if a.wave:
        wave_name = os.path.basename(a.wave)
        if os.path.abspath(os.path.dirname(a.wave)) != os.path.abspath(a.out): shutil.copy(a.wave, os.path.join(a.out, wave_name))
        with wave.open(a.wave) as w: wave_ms = w.getnframes() / w.getframerate() * 1000
    bpm = int(a.bpm) if a.bpm == int(a.bpm) else a.bpm
    write_ustx(os.path.join(a.out, a.name + ".ustx"), a.name, bpm, a.key, notes, len(bars) * 4, a.singer, a.phonemizer, wave_name, wave_ms, not a.no_vibrato)
    fifths = {0: 0, 7: 1, 2: 2, 9: 3, 4: 4, 11: 5, 5: -1, 10: -2, 3: -3, 8: -4}.get(a.key, 0)
    write_musicxml(os.path.join(a.out, a.name + ".musicxml"), a.name, bpm, fifths, bars)
    write_lyrics(os.path.join(a.out, a.name + "-歌詞.txt"), a.name, vocal, [s for s in a.sections.split(",") if s])
    print("書き出し:", a.out, len(notes), "音", len(bars), "小節")

if __name__ == "__main__":
    main()
