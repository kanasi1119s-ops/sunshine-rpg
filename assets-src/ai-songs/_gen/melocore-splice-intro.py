# 使い方: python3 melocore-splice-intro.py <本編.wav(48k)> <出だし.wav(48kに変換済み)> <出力.wav>
# 本編(melocore-pluck-v2-main.json の書き出し)は先頭の無音が削られるので、最初の音（4小節目のスネア連打）が 4.186 秒に来るよう無音を足し、
# tools/soundfont/intro-swell-synth.mjs で作った出だし(-12dB)を重ねる。
import sys,wave,numpy as np
def load(p):
    w=wave.open(p);ch=w.getnchannels();sr=w.getframerate();x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(float)/32768
    return x.reshape(-1,ch),sr,ch
a,sr,ch=load(sys.argv[1]);b,sr2,_=load(sys.argv[2]);assert sr==sr2
t0=np.argmax(np.abs(a).max(1)>0.002)/sr;pad=int(round((3*4*60/172-t0)*sr))
a=np.vstack([np.zeros((pad,ch)),a]);n=min(len(b),len(a));a[:n]+=b[:n]*10**(-12/20)
pk=np.abs(a).max()
if pk>0.97:a*=0.97/pk
w=wave.open(sys.argv[3],"wb");w.setnchannels(ch);w.setsampwidth(2);w.setframerate(sr);w.writeframes((a*32767).astype(np.int16).tobytes());w.close()
