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
    models = []
    models.append(HotDog())
    models.append(ObjectDetection())
    image = False
    if request.method == 'POST':
        image = request.files['image']
        try_out = Try_out(image)
        return send_file(try_out.output(models), mimetype='image/jpeg')
    
    return send_file('src/images/404.jpg', mimetype='image/gif')

@app.route('/')
def webpage_output():
    models = []
    models.append(HotDog())
    models.append(ObjectDetection())
    st = Stream("https://cph-p2p-msl.akamaized.net/hls/live/2000341/test/master.m3u8")
    return Response(st.output(models), mimetype='multipart/x-mixed-replace; boundary=frame')




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8069)