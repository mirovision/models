from src.models.dict_models import dict_models
from src.path.stream import Stream
from src.path.try_out import Try_out
from flask import Flask, send_file, Response, request


app = Flask(__name__)


def choosing_models_by_parameters(parameters):
    models  = []

    for param in parameters:
        try :
            models.append(dict_models[param]())
        except:
            print("invalid model name")        
    return models

@app.route('/try_out', methods = ['GET', 'POST'])
def try_out_output():
    models = choosing_models_by_parameters(request.args)
    image = False
    if request.method == 'POST':
        image = request.files['image']
        try_out = Try_out(image)
        return send_file(try_out.output(models), mimetype='image/jpeg')
    
    return send_file('src/images/404.jpg', mimetype='image/gif')


@app.route('/', methods=['GET'])
def webpage_output():
    models = choosing_models_by_parameters(request.args)
    st = Stream("https://cph-p2p-msl.akamaized.net/hls/live/2000341/test/master.m3u8")
    return Response(st.output(models), mimetype='multipart/x-mixed-replace; boundary=frame')




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8069)