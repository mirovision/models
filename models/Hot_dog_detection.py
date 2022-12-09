from transformers import AutoFeatureExtractor, AutoModelForImageClassification
from PIL import Image, ImageDraw, ImageFont
import requests
from CVModel import CVModel


class HotDog(CVModel):
    def __init__(self):
        self.extractor = AutoFeatureExtractor.from_pretrained("julien-c/hotdog-not-hotdog")

        self.model = AutoModelForImageClassification.from_pretrained("julien-c/hotdog-not-hotdog")
        super().__init__()

    def try_out(self, image):

        encoded_output = self.extractor(images=image,return_tensors="pt")
        output = self.model(**encoded_output)
        logits = output.logits
        predicted_class_idx = logits.argmax(-1).item()
        self. hot_dog = self.model.config.id2label[predicted_class_idx]

    def edit_frame(self, image, position, font,  font_size):
            
        edit_img = ImageDraw.Draw(image) 
        print("hola")       
        font = ImageFont.truetype(font , font_size)
        edit_img.text((position[0], position[1]),  self.hot_dog, font=font, fill=(255,255,255))
        image.save("edited_foto.jpg")
       # to see the result you need to save it as this example
        #image.save("edited_butifarra.jpg")s