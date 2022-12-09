from fastapi import FastAPI, File, UploadFile, Response
from models.base import *

models = {"1": ObjectDetection()}

app = FastAPI()

@app.post("/tryout/{model_id}")
async def try_out(model_id: int, file: UploadFile = File()):
    from PIL import Image
    contents = await file.read()
    models[str(model_id)].input(image=contents)
    result = models[str(model_id)].output()
    #(model.output().astype("uint8"), "RGB")
    result = Image.fromarray(result.astype("uint8"), "RGB")
    return Response(content=result, media_type="image/jpg")