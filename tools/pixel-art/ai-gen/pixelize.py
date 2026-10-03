"""AIが描いた「ドット絵風」の画像を、本物のドット絵に仕上げる（背景の除去・マス目合わせ・減色・半透明の除去）。"""
import sys,os
import numpy as np
from PIL import Image
from scipy import ndimage
def remove_bg(im, tol=40):
    a=np.asarray(im.convert('RGB')).astype(int)
    corners=np.array([a[0,0],a[0,-1],a[-1,0],a[-1,-1]])
    bg=np.median(corners,axis=0)
    near=(np.abs(a-bg).sum(2)<tol)
    lab,n=ndimage.label(near)
    edge=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
    mask=~np.isin(lab,list(edge))
    mask=ndimage.binary_opening(mask,iterations=2)
    lab2,n2=ndimage.label(mask)
    if n2>1:  # 一番大きなかたまりと、それに近いものだけ残す
        sizes=ndimage.sum(mask,lab2,range(1,n2+1)); keep=[i+1 for i,s in enumerate(sizes) if s>=sizes.max()*0.03]
        mask=np.isin(lab2,keep)
    rgba=np.dstack([a,(mask*255)]).astype(np.uint8)
    return Image.fromarray(rgba,'RGBA')
def pixelize(src, size=48, colors=12):
    im=remove_bg(Image.open(src))
    bb=im.getbbox(); im=im.crop(bb)
    w,h=im.size; s=size/max(w,h)
    tw,th=max(1,round(w*s)),max(1,round(h*s))
    # マス目合わせ: 1マスの中の平均（BOX）で縮める。透明度は半分を境に、ある／なしにする
    small=im.resize((tw,th),Image.BOX)
    arr=np.asarray(small).copy()
    alpha=arr[:,:,3]>=128
    rgb=Image.fromarray(arr[:,:,:3])
    q=rgb.quantize(colors=colors,method=Image.Quantize.MEDIANCUT,kmeans=3).convert('RGB')
    out=np.dstack([np.asarray(q),alpha*255]).astype(np.uint8)
    canvas=Image.new('RGBA',(size,size),(0,0,0,0))
    canvas.paste(Image.fromarray(out,'RGBA'),((size-tw)//2,size-th))
    return canvas
if __name__=='__main__':
    os.makedirs('px',exist_ok=True)
    for f in sys.argv[1:]:
        n=os.path.splitext(os.path.basename(f))[0]
        p=pixelize(f); p.save(f'px/{n}.png')
        cols=len({c for c in p.getdata() if c[3]})
        print(n,cols,'色')
