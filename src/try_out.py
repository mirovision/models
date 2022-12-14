from PIL import Image
import io

class Try_out():
    def __init__(self):
        self.image = None

    def check_if_is_image():
        
       return True
    
    def input(self, image):
        image_io =  io.BytesIO()
        image.save(image_io,  'JPEG', quality=70)
        image_io.seek(0)
        return image_io

    def output(self, request):
        image_raw = Image.open(request)
        image = self.input(image_raw)
        return image


        
    