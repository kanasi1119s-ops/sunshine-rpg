import sys, json, numpy as np, pickle, collections
sys.path.insert(0, "/home/claude/wt-mix/tools/singer")
import sing
FP = sing.FP; ROWS = []
_rp = sing.render_piece
def rp(oto, out_len, f0_target, vel, sr_out, opts=None):
    r = _rp(oto, out_len, f0_target, vel, sr_out, opts)
    o = opts or {}
    if o.get("_tail"): return r
    C = oto["consonant"]; L = out_len * 1000; k = len(f0_target); tau = np.arange(k) * FP
    P_out = min(oto.get("_pre_out", oto["pre"]), C); fs = P_out / max(min(oto["pre"], C), 1e-6); C_out = C * fs if fs < 0.999 else C
    lsp, ap, fo, sr = sing._frames(oto, tau, L, P_out, C_out)
    en = np.exp(lsp).sum(1); fin = r["f0"]
    vow = (tau >= C_out) & (fin > 0); vref = np.median(en[vow]) if vow.sum() > 2 else np.median(en)
    lost = (fo > 0) & (fin == 0)                       # もとは声ありなのに、こちらの処理で「声なし」にした
    kept_unv = (fo == 0) & (fin == 0)                  # もとから声なし
    def stat(m):
        if not m.any(): return (0, None)
        return (int(m.sum()) * FP, float(10 * np.log10(en[m].mean() / vref + 1e-20)))
    head = tau < max(P_out - 60, 0)
    ROWS.append(dict(lyric=o.get("_lyric"), wav=oto["wav"].split("/")[-1], P=P_out, C=C_out, L=L, ovl=oto["ovl"],
                     lost_head=stat(lost & head), lost_cons=stat(lost & ~head), unv=stat(kept_unv),
                     lost_head_loud=int(((10 * np.log10(en / vref + 1e-20) > -6) & lost & head).sum()) * FP))
    return r
sing.render_piece = rp
song = json.load(open(sys.argv[1])); sing.render_song(song, 48000, dry=True)
pickle.dump(ROWS, open(sys.argv[2], "wb")); print(len(ROWS))
