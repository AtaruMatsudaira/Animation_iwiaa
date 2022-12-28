from PIL import Image, ImageDraw,ImageFont
import numpy as np
import sys

def make_map(str_list):
    l=[]
    font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf", 20)
    for i in str_list:
        im = Image.new("L",(20,20),"white")
        draw = ImageDraw.Draw(im)
        draw.text((0,0),i,font=font)
        l.append(np.asarray(im).mean())
    l_as=np.argsort(l)
    lenl=len(l)
    l2256=np.r_[np.repeat(l_as[:-(256%lenl)],256//lenl),np.repeat(l_as[-(256%lenl):],256//lenl+1)]
    chr_map=np.array(str_list)[l2256]
    return chr_map

def get_2d_array(im_array):
    chr_map = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz +-*/%'"+'"!?#&()~^|@;:.,[]{}<>_0123456789'

def output(chr_map,imarray,isOutText,out_path):
    aa=chr_map[imarray].tolist()
    if isOutText:
        with open(out_path,"w") as f:
            for i in range(len(imarray)):
                f.write(''.join(aa[i])+"\n")
    else:
        for i in range(len(imarray)):
            print(''.join(aa[i]))

def make_AA(file_path,str_list="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz +-*/%'"+'"!?#&()~^|@;:.,[]{}<>_0123456789',width=150,isOutText=False,out_path="aa.txt",isFW=False):
    imag=Image.open(file_path).convert('L')
    if isFW:str_list=list(str_list.translate(str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)})))
    else:str_list=list(str_list)
    imarray=np.asarray(imag.resize((width,width*imag.height//imag.width//(2-int(isFW)))))
    output(make_map(str_list),imarray,isOutText,out_path)
    return imarray

if __name__ == "__main__":
    print(make_AA(sys.argv[1]))
    