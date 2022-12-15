from PIL import Image
import io

class Try_out():
    def __init__(self, request):
        self.image_raw = Image.open(request)

    def check_if_is_image():
        
       return True
    
    def __process_image(self, image, models):
        for model in models:
            model.calculate(image)      
        for model in models:
            image = model.draw(image)
        return image

    def __transform_image_into_byte(self, image):
        image_io =  io.BytesIO()
        image.save(image_io,  'JPEG', quality=70)
        image_io.seek(0)
        return image_io

    def output(self, models):
        image = self.__process_image(self.image_raw, models)
        return self.__transform_image_into_byte(image)



        
    