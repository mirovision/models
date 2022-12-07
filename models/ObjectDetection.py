"""
    mirovision AI Team
    ObejctDetection.py
    End-To-End Object Detection (facebook/detr-resnet-50): 
    https://huggingface.co/facebook/detr-resnet-50

"""

from models.CVModel import CVModel

class ObjectDetection(CVModel):
    
    def __init__(self):
        return
    
    def input(self, image):
        print ("INPUT")
        return True
    
    def output(self):
        print ("OUTPUT")
        return True