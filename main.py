"""
    mirovision AI Team
    main.py
    Example usage of our models

"""

from models.base import *


from io import BytesIO
from PIL import Image, ImageFile
import numpy
from rawkit import raw
def convert_cr2_to_jpg(raw_image):
    raw_image_process = raw.Raw(raw_image)
    buffered_image = numpy.array(raw_image_process.to_buffer())
    if raw_image_process.metadata.orientation == 0:
        jpg_image_height = raw_image_process.metadata.height
        jpg_image_width = raw_image_process.metadata.width
    else:
        jpg_image_height = raw_image_process.metadata.width
        jpg_image_width = raw_image_process.metadata.height
    jpg_image = Image.frombytes('RGB', (jpg_image_width, jpg_image_height), buffered_image)
    return jpg_image


def main():
    models: list[CVModel] = [ObjectDetection()]
    url = "http://images.cocodataset.org/val2017/000000039769.jpg"
    import requests
    from PIL import Image
    from io import BytesIO
    #url="http://192.168.113.232:8081/"
    for model in models:
        image = requests.get(url).raw
        model.input(image=image)
        result = Image.fromarray(model.output().astype("uint8"), "RGB")
        result.save("imagwe.jpg")
    return

if __name__ == "__main__":
    main()