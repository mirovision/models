"""
    mirovision AI Team
    ObejctDetection.py
    End-To-End Object Detection (facebook/detr-resnet-50): 
    https://huggingface.co/facebook/detr-resnet-50

"""

from models.CVModel import CVModel

class ObjectDetection(CVModel):

    def __init__(self):
        super().__init__() 
        self.____feature_extractor = None
        self.__model = None
        self.__image = None
        self.__inputs = None
        self.__outputs = None
    
        from transformers import DetrFeatureExtractor, DetrForObjectDetection
        self.__feature_extractor = DetrFeatureExtractor.from_pretrained("facebook/detr-resnet-50")
        self.__model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")
        return
    
    def __parse_input(self, image):
        from PIL import Image
        self.__image = Image.open(image)
        self.__inputs = self.__feature_extractor(images=self.__image, return_tensors="pt")
    
    def __get_output(self):
        self.__outputs = self.__model(**self.__inputs)
    
    def input(self, image):
        super().input(image=None)
        self.__parse_input(image=image)
        self.__get_output()
        
        return True
    
    def output(self):
        super().output()
        import torch
        target_sizes = torch.tensor([self.__image.size[::-1]])
        results = self.__feature_extractor.post_process_object_detection(self.__outputs, target_sizes=target_sizes)[0]
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            box = [round(i, 2) for i in box.tolist()]
            # let's only keep detections with score > 0.9
            if score > 0.9:
                print(
                    f"Detected {self.__model.config.id2label[label.item()]} with confidence "
                    f"{round(score.item(), 3)} at location {box}"
                )
        return True