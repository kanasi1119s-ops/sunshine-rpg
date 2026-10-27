import numpy as np, cv2, sys, os
src="/mnt/user-data/attachments/945c1fd5-bcd9-525d-8abc-22b5d22e1041/2c61ef6d-image.jpg"
img=cv2.imread(src).astype(np.float32); H,W=img.shape[:2]
g=cv2.cvtColor(img.astype(np.uint8),cv2.COLOR_BGR2GRAY).astype(np.float32)
k=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(25,25))
bgm=cv2.GaussianBlur(cv2.morphologyEx(g,cv2.MORPH_OPEN,k),(0,0),6)
S=np.clip(g-bgm-14,0,None)
m=np.zeros((H,W),np.float32)
pts=np.array([(566,632),(568,560),(580,490),(598,420),(598,380),(580,330),(546,290),(542,240),(578,190),(560,130),(502,100),(470,60),(440,0)],np.int32)
cv2.polylines(m,[pts],False,1.0,thickness=64)
m=cv2.GaussianBlur(m,(0,0),8)
m[612:]=0; S*=m
Sc=np.clip(img-np.clip(img-S[...,None],0,None),0,None)
B=img-Sc
if len(sys.argv)>1 and sys.argv[1]=="dbg":
    cv2.imwrite("S.png",np.clip(S*4,0,255).astype(np.uint8)); sys.exit()
N=72; yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
os.makedirs("fr",exist_ok=True)
for i in range(N):
    t=i/N
    h=np.clip((640.0-yy)/640.0,0,1)
    dx=0.75*(10*np.sin(2*np.pi*(yy/170.0-2*t))+5*np.sin(2*np.pi*(yy/97.0-3*t)+1.3))*(0.25+h*1.1)
    Sw=cv2.remap(S,(xx-dx).astype(np.float32),yy.astype(np.float32),cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
    Sw=Sw*(0.92+0.14*np.sin(2*np.pi*(t*2-yy/260.0)))
    sc=np.clip(Sc/np.maximum(S[...,None],1e-3),0.6,1.6)
    out=B+Sw[...,None]*sc
    out=np.clip(out*(1+0.02*np.sin(2*np.pi*t*3)),0,255).astype(np.uint8)
    cv2.imwrite(f"fr/{i:03d}.png",out)
print("ok")
