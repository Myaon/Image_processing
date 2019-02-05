#coding: utf-8

import subprocess
from datetime import datetime

def jtalk(t):
    open_jtalk=['open_jtalk']
    mech=['-x','/var/lib/mecab/dic/open-jtalk/naist-jdic']
    htsvoice=['-m','/usr/share/hts-voice/mei/mei_normal.htsvoice']
    speed=['-r','1']
    outwav=['-ow','open_jtalk.wav']
    cmd=open_jtalk+mech+htsvoice+speed+outwav
    c = subprocess.Popen(cmd,stdin=subprocess.PIPE)
    c.stdin.write(t)
    c.stdin.close()
    c.wait()
    aplay = ['aplay','-q','open_jtalk.wav']
    wr = subprocess.Popen(aplay)
"""
def say_datetime():
    
    text = "ここは身障者専用駐車スペースです。今すぐ退いてください。"
    jtalk(text)
    """

code = "text = \"ここは身障者専用駐車スペースです。今すぐ退いてください。\"\njtalk(text)"
exec(code)

if __name__ == '__main__':
    say_datetime()

