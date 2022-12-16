from src.models.dict_models import dict_models
from src.path.stream import Stream
from src.path.try_out import Try_out
from flask import Flask, send_file, Response, request, render_template, abort


app = Flask(__name__)


def choosing_models_by_parameters(parameters):
    models  = []
    parameters = parameters.split('+')
    for param in parameters:
        print(parameters)
        try :
            models.append(dict_models[param]())
        except Exception as e:
            print(e)
            print("invalid model name")        
    return models

@app.route('/try_out/<models>/', methods = ['GET', 'POST'])
def try_out_output(models):
    models = choosing_models_by_parameters(models)
    image = False
    if request.method == 'POST':
        image = request.files['image']
        try_out = Try_out(image)
        return send_file(try_out.output(models), mimetype='image/jpeg')   
    return abort(404)

@app.route('/webcam/<models>/', methods = ['GET', 'POST'])
def webcam(models): 
    models = choosing_models_by_parameters(models)
    url = request.args.get('url')
    if url == None:
        return abort(404)
    try:
        st = Stream(url=url)
    except:
        return abort(404)
    return Response(st.output(models), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8069)