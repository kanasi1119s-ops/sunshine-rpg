import json,re
def beats(s):
    t=0
    for tok in s.split():
        if tok.startswith('g:'): t+=0.25*len(tok[2:])
        else: t+=float(tok.split(':')[1])
    return t
def bar(s,n=4):
    assert abs(beats(s)-n)<1e-6,(s,beats(s)); return s
def seq(*bars): return ' '.join(bars)
def rep(s,n): return ' '.join([s]*n)
REST8='R:32'
def build(path,meta,sections,parts):
    """sections: list of names (8 bars each). parts: list of dict(instrument,role,volume,pan,amp,[sustain,push], lines: {sectionName: 8-bar string or None})"""
    out=[]
    for p in parts:
        chunks=[]
        for sname in sections:
            line=p['lines'].get(sname)
            if line is None: line=p['lines'].get('*')
            if line is None: chunks.append('R:32' if not p.get('drum') else 'g:'+'.'*128)
            else:
                assert abs(beats(line)-32)<1e-6,(p['role'],sname,beats(line)); chunks.append(line)
        d={k:v for k,v in p.items() if k not in('lines','drum')}
        d['notes']=' '.join(chunks); out.append(d)
    n=len(sections)
    song=dict(meta); song['repeats']=n; song['barsPerChord']=1; song['beats']=4; song['autoAccompaniment']=False; song['parts']=out
    json.dump(song,open(path,'w'),ensure_ascii=False,indent=1)
    secs=n*8*4*60/meta['bpm']; print(path,round(secs,1),'秒',n*8,'小節')
def P(i,r,v,pan,amp,lines,**k):
    d=dict(instrument=i,role=r,volume=v,pan=pan,amp=amp,lines=lines); d.update(k); return d
def D(i,r,v,pan,lines,**k):
    return P(i,r,v,pan,'auto',lines,drum=True,**k)
def gbars(*bs): return ' '.join('g:'+b for b in bs)
