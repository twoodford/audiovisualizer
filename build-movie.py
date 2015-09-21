import os
import os.path
import subprocess
import sys
from PIL import Image

LISTF = "_list.txt"
def get_dimensions(fpath):
    #print(fpath)
    return Image.open(fpath).size

def run(folder, outfile, framerate=30, outres=(1920,1080)):
    jpglist = [os.path.join(folder, f) for f in os.listdir(folder) if f.startswith("frame_")]
    dimen = get_dimensions(jpglist[0])
    ratio = float(outres[1])/outres[0]
    if dimen[0]*ratio < dimen[1]:
        crop = (dimen[0], int(dimen[0]*ratio))
    else:
        crop = (int(dimen[1]/ratio), dimen[1])
    with open(LISTF, "w") as ltxt:
        for f in jpglist:
            ltxt.write("file '"+f+"'\n")
    fsel_args = ["-f", "concat", "-i", LISTF]
    rs_str = "".join(("crop=", str(crop[0]), ":", str(crop[1]),":0:0,scale=",str(outres[0]),":",str(outres[1])))
    enc_flags = ["-pix_fmt", "yuv420p", "-preset", "veryslow", "-crf", "18"]
    args_final = ["ffmpeg", "-r", str(framerate)] + fsel_args + ["-vf", rs_str] + enc_flags + [outfile]
    print(" ".join(args_final))
    subprocess.call(args_final)
    os.remove(LISTF)

if __name__=="__main__":
    jpglist = [os.path.join(sys.argv[1], f) for f in os.listdir(sys.argv[1]) if f.startswith("frame_")]
    dimen = get_dimensions(jpglist[0])
    dimen = (dimen[0] if dimen[0]%2==0 else dimen[0]-1, dimen[1] if dimen[1]%2==0 else dimen[1]-1)
    run(sys.argv[1], sys.argv[2], outres=dimen)

