import subprocess as sp
import numpy as np
import io
import time
from models.Hot_dog_detection import HotDog
from models.ObjectDetection import ObjectDetection
from PIL import Image
from flask import Flask, render_template, Response
import cv2


app = Flask(__name__)



class Stream():
    def __init__(self, url) -> None:
        self.pipe_input = sp.Popen([ "ffmpeg", "-i", url,
           "-loglevel", "quiet", # no text output
           "-an",   # disable audio
           "-f", "image2pipe",
           "-pix_fmt", "bgr24",
           "-vcodec", "rawvideo", "-"],
           stdin = sp.PIPE, stdout = sp.PIPE)

    def input(self,widht=1024, height=576):
        raw_image = self.pipe_input.stdout.read(widht*height*3)
        image =  np.fromstring(raw_image, dtype='uint8')
        image = image.reshape(height,widht,3)
        return image


    def __process_image(self, input, models):
        image = Image.fromarray(input)
        for model in models:
            model.calculate(image)       
        for model in models:
            image = model.draw(image)
        img_byte = io.BytesIO()
        image.save(img_byte, format = 'PNG')
        return img_byte.getvalue()

        #here goes all the threads logic, but for now we just calculate all the frames

    def output(self, models):
        while True:
            input = self.input()
            image = self.__process_image(input, models)
            yield((b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n'))
    

@app.route('/')
def webpage_output():
    models = []
    models.append(HotDog())
    models.append(ObjectDetection())
    st = Stream("https://s6.hopslan.com/orf11/tracks-v1a1/mono.m3u8")
    return Response(st.output(models), mimetype='multipart/x-mixed-replace; boundary=frame')




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8069)