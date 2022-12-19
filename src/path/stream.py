import subprocess as sp
import io
import numpy as np
from PIL import Image
import io
import aiohttp
from aioflask import Response
import asyncio
from keras.preprocessing import image
from multipart_reader import MultipartReader

class Stream():
    def __init__(self, url) -> None:
        self.url = url

    def __process_image(self,  models):
        for model in models:
            model.calculate(self.image)      
        for model in models:
            self.image = model.draw(self.image)

    def __transform_image_into_byte(self, image):
        image_io =  io.BytesIO()
        image.save(image_io,  'JPEG', quality=70)
        image_io.seek(0)
        return image_io
    
    async def output(self, models): 
            async with aiohttp.request(url=self.url, method="GET") as resp:
                while True:
                    reader = aiohttp.MultipartReader.from_response(resp)
                    part = await reader.next()
                    content = await part.read()
                    print (part.headers[aiohttp.hdrs.CONTENT_TYPE])
                    print (type(content))
                    self.image = Image.open(io.BytesIO(content))
                    self.__process_image(models)
                    self.image_io = self.__transform_image_into_byte(self.image)
                    yield((self.image_io))
                    if part is None:
                        break
