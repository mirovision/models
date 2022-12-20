from transformers import AutoFeatureExtractor, AutoModelForImageClassification
from PIL import Image, ImageDraw, ImageFont
import requests 
import io
from models.CVModel import CVModel


class HotDog(CVModel):
    def   __init__(self):
        self.extractor = AutoFeatureExtractor.from_pretrained("julien-c/hotdog-not-hotdog")
        self.model = AutoModelForImageClassification.from_pretrained("julien-c/hotdog-not-hotdog")
        super().__init__()

    def calculate(self, image):
        encoded_output = self.extractor(images=image,return_tensors="pt")
        output = self.model(**encoded_output)
        logits = output.logits
        predicted_class_idx = logits.argmax(-1).item()
        self.hot_dog = self.model.config.id2label[predicted_class_idx]

    def draw(self, image):
        edit_img = ImageDraw.Draw(image)
        font = ImageFont.truetype('src/fonts/hot_dog_font.ttf' , 20)
        edit_img.text((400,400), text=self.hot_dog ,font=font, fill=(255,255,255))
        return image

       # to see the result you need to save it as this example
        #image.save("edited_butifarra.jpg")