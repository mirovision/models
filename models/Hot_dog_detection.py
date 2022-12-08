from transformers import AutoFeatureExtractor, AutoModelForImageClassification
from PIL import Image
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
        return self.model.config.id2label[predicted_class_idx]