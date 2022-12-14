"""
    mirovision AI Team
    ObejctDetection.py
    End-To-End Object Detection (facebook/detr-resnet-50): 
    https://huggingface.co/facebook/detr-resnet-50

"""
from transformers import DetrFeatureExtractor, DetrForObjectDetection
from models.CVModel import CVModel
from PIL import Image
import numpy as np
import cv2
from PIL import Image
from io import BytesIO
import numpy as np
from matplotlib import cm
import torch

class ObjectDetection(CVModel):

    def __init__(self):
        super().__init__() 
        self.____feature_extractor = None
        self.__model = None
        self.__image = None
        self.__inputs = None
        self.__outputs = None
        self.__results = None
        self.__result_image = None
        self.__feature_extractor = DetrFeatureExtractor.from_pretrained("facebook/detr-resnet-50")
        self.__model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")
        return
    
    def  calculate(self, image):
        self.__image = image
        self.__result_image = np.array(self.__image)
        self.__inputs = self.__feature_extractor(images=self.__image, return_tensors="pt")
        self.__outputs = self.__model(**self.__inputs)
        target_sizes = torch.tensor([self.__image.size[::-1]])
        self.__results = self.__feature_extractor.post_process_object_detection(self.__outputs, target_sizes=target_sizes)[0]
    
    def draw(self, image):
        self.__result_image = np.array(self.__image)
        for score, label, box in zip(self.__results["scores"], self.__results["labels"], self.__results["boxes"]):
            box = [round(i, 2) for i in box.tolist()]
            # let's only keep detections with score > 0.
            # 9
            if score > 0.5:
                print(
                    f"Detected {self.__model.config.id2label[label.item()]} with confidence "
                    f"{round(score.item(), 3)} at location {box}"
                )
                #self.parsed_outputs.append({"box": [int(box[0]), int(box[1]), int(box[2]), int(box[3])], "item": self.__model.config.id2label[label.item()], "confidence": round(score.item(), 3)})
                cv2.rectangle(self.__result_image, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 255, 0), 2)
                text = self.__model.config.id2label[label.item()] + ": " + str(round(score.item(), 3))
                cv2.putText(self.__result_image, text, (int(box[0]+5),int(box[1]+13)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        result  = Image.fromarray(self.__result_image)
        return result

    
    def output(self):
        super().output()
        target_sizes = torch.tensor([self.__image.size[::-1]])
        self.__results = self.__feature_extractor.post_process_object_detection(self.__outputs, target_sizes=target_sizes)[0]
        # image = self.__draw_output()
        # image.save("sample.jpg")
        result = self.__draw_output()
        #success, encoded_image = cv2.imencode('.jpg', result)
        return result