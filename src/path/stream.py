import subprocess as sp
import io
import numpy as np
from PIL import Image

class Stream():
    def __init__(self, url) -> None:
        self.pipe_input = sp.Popen([ "ffmpeg", "-i", url,
           "-loglevel", "quiet", # no text output
           "-an",   # disable audio
           "-f", "image2pipe",
           "-pix_fmt", "bgr24",
           "-vcodec", "rawvideo", "-"],
           stdin = sp.PIPE, stdout = sp.PIPE)

    def __take_raw_frame(self,widht=1024, height=576):
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
        return image

    def __transform_image_into_byte(self, frame):
        img_byte = io.BytesIO()
        frame.save(img_byte, format = 'PNG')
        return img_byte.getvalue()
    
    def output(self, models):
        while True:
            raw_frame = self.__take_raw_frame()
            frame = self.__process_image(raw_frame, models)
            image_byte = self.__transform_image_into_byte(frame)
            yield((b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + image_byte + b'\r\n'))
