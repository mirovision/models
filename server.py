from models.Hot_dog_detection import HotDog
from models.ObjectDetection import ObjectDetection
from src.stream import Stream
from PIL import Image
from src.try_out import Try_out
import io
from flask import Flask, send_file, Response, request


app = Flask(__name__)







@app.route('/try_out', methods = ['GET', 'POST'])
def try_out_output():
    try_out = Try_out()
    image = False
    if request.method == 'POST':
        image = request.files['image']
        return send_file(try_out.output(image), mimetype='image/jpeg')
    return send_file('local_test/ciervo.jpg', mimetype='image/gif')

@app.route('/')
def webpage_output():
    models = []
    models.append(HotDog())
    models.append(ObjectDetection())
    st = Stream("https://s6.hopslan.com/orf11/tracks-v1a1/mono.m3u8")
    return Response(st.output(models), mimetype='multipart/x-mixed-replace; boundary=frame')




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8069)