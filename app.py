from fastapi import FastAPI, File, UploadFile, Response
from fastapi.responses import FileResponse
from starlette.responses import StreamingResponse
from models.base import *

models = {"1": ObjectDetection()}

app = FastAPI()

@app.post("/tryout/{model_id}")
async def try_out(model_id: int, file: UploadFile = File()):
    from PIL import Image
    import cv2
    import io
    contents = await file.read()
    models[str(model_id)].input(image=contents)
    result = models[str(model_id)].output()
    #(model.output().astype("uint8"), "RGB")
    result_image = Image.fromarray(result)
    result_image.save("result.jpg")
    res, im_jpg = cv2.imencode(".jpg", result)
    # print(im_p)
    if res:
        return Response(content=im_jpg.tobytes(), media_type="image/jpg")
    return "error"