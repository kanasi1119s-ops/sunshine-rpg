import json, sys, os
from PIL import Image
HERE=os.path.dirname(os.path.abspath(__file__))
def img(name, z=8, bg=(70,130,190)):
    rows=[l for l in open(os.path.join(HERE,name+".txt")).read().split("\n") if l]; pal=json.load(open(os.path.join(HERE,"pal-"+name+".json")))
    w=max(map(len,rows)); h=len(rows); im=Image.new("RGB",(w,h),bg)
    for y,r in enumerate(rows):
        for x,c in enumerate(r):
            if c in pal: im.putpixel((x,y),tuple(int(pal[c][i:i+2],16) for i in (1,3,5)))
    return im.resize((w*z,h*z),Image.NEAREST)
if __name__=="__main__":
    ims=[img(n, int(sys.argv[1])) for n in sys.argv[2:]]
    W=sum(i.width for i in ims)+10*len(ims); H=max(i.height for i in ims)
    out=Image.new("RGB",(W,H),(30,30,40)); x=0
    for i in ims: out.paste(i,(x,0)); x+=i.width+10
    out.save("/tmp/claude-0/as.png")
