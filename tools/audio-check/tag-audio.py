#!/usr/bin/env python3
"""音の分類モデル（CLAP: 音と言葉を結びつけたAI）で、WAV を言葉で説明させる道具。
使い方: python3 tools/audio-check/tag-audio.py <WAV> [--start 秒] [--dur 10] [--labels 追加の言葉,...]
やること: 10秒の窓で、用意した言葉の一覧（楽器・音色・奏法・ジャンル）のどれに近いかを点数にする（ゼロショット）。
注意: 点数は「言葉に近い順位」であって、良し悪しではない。耳の代わりではなく、聞いた人の感想と突き合わせる材料。
初回だけモデル（約600MB）をダウンロードする。HF_HOME で置き場を変えられる。"""
import sys, argparse, subprocess
import numpy as np, torch
from transformers import ClapModel, ClapProcessor

LABELS = {
 "ギター": ["a clean electric guitar","a distorted electric guitar","an overdriven lead guitar solo","a heavily distorted metal guitar","an acoustic guitar","a rubbery stretched guitar note","a synthesizer imitating a guitar","a real recorded electric guitar","a guitar with wide vibrato","a guitar with a string bend","a muted palm-muted guitar","a thin harsh digital guitar"],
 "ドラム": ["a real acoustic drum kit","an electronic drum machine","real recorded toms","synthesized toms","a cymbal crash ringing out","a ride cymbal","a snare drum","a kick drum"],
 "全体": ["a professional studio rock recording","an amateur MIDI sounding track","a muddy messy mix","a clean and clear mix","a live band performance","a synthesized MIDI instrument","punk rock","melodic hardcore punk","progressive metal","pop rock"],
}
def load(path, start, dur, sr=48000):
    cmd = ["ffmpeg","-v","error","-ss",str(start),"-t",str(dur),"-i",path,"-f","f32le","-ac","1","-ar",str(sr),"-"]
    return np.frombuffer(subprocess.run(cmd,capture_output=True).stdout, dtype=np.float32)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("wav"); ap.add_argument("--start",type=float,default=0)
    ap.add_argument("--dur",type=float,default=10); ap.add_argument("--labels",default="")
    a = ap.parse_args()
    x = load(a.wav, a.start, a.dur)
    m = ClapModel.from_pretrained("laion/clap-htsat-unfused").eval(); p = ClapProcessor.from_pretrained("laion/clap-htsat-unfused")
    groups = dict(LABELS)
    if a.labels: groups["追加"] = [s.strip() for s in a.labels.split(",") if s.strip()]
    for g, labs in groups.items():
        inp = p(text=labs, audio=x, sampling_rate=48000, return_tensors="pt", padding=True)
        with torch.no_grad(): out = m(**inp)
        pr = out.logits_per_audio.softmax(-1)[0].numpy()
        print(f"[{g}]")
        for i in np.argsort(-pr): print(f"  {pr[i]*100:5.1f}%  {labs[i]}")
main()
