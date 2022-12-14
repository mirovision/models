import cv2
import subprocess as sp
import numpy
import sys
from time import sleep

VIDEO_URL = "https://ztnr.rtve.es/ztnr/1688877.m3u8"

cv2.namedWindow("VLC COPY")

pipe = sp.Popen([ "ffmpeg", "-i", VIDEO_URL,
           "-loglevel", "quiet", # no text output
           "-an",   # disable audio
           "-f", "image2pipe",
           "-pix_fmt", "bgr24",
           "-vcodec", "rawvideo", "-"],
           stdin = sp.PIPE, stdout = sp.PIPE)

while True:
    #bytes = sys.stdin.read()
    raw_image = pipe.stdout.read(1280*726*3) # read 432*240*3 bytes (= 1 frame)
    image =  numpy.fromstring(raw_image, dtype='uint8').reshape((726,1280,3))
    cv2.imshow("VLC COPY",image)
    #sleep(1)
    #pipe.stdout.flush()
    #if cv2.waitKey(5) == 27:
         #  break
cv2.destroyAllWindows()