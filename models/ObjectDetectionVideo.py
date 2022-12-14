"""
    mirovision AI Team
    ObejctDetection.py
    End-To-End Object Detection (facebook/detr-resnet-50): 
    https://huggingface.co/facebook/detr-resnet-50

"""

from models.CVModel import CVModel
from time import sleep

class ObjectDetectionVideo(CVModel):

    def __init__(self, stream_url, width, height):
        import subprocess as sp
        super().__init__() 
        self.____feature_extractor = None
        self.__model = None
        self.__image = None
        self.__inputs = None
        self.__outputs = None
        self.__dimensions = {"width": width, "height": height}
        self.parsed_outputs = []
        self.output_video_buffer = None
        self.__numpy_image = None
        self.__stream = stream_url
        self.__pipe = sp.Popen([ "ffmpeg", "-i", stream_url,
           "-loglevel", "quiet", # no text output
           "-an",   # disable audio
           "-f", "image2pipe",
           "-pix_fmt", "bgr24",
           "-vcodec", "rawvideo", "-"],
           stdin = sp.PIPE, stdout = sp.PIPE)

    
        from transformers import DetrFeatureExtractor, DetrForObjectDetection
        self.__feature_extractor = DetrFeatureExtractor.from_pretrained("facebook/detr-resnet-50")
        self.__model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")
        return
    
    def __parse_input(self, frame):
        from PIL import Image
        import io
        import numpy
        #self.__image = Image.open(io.BytesIO(frame))
        self.__numpy_image = None
        self.__numpy_image = numpy.fromstring(frame, dtype='uint8').reshape((self.__dimensions["height"],self.__dimensions["width"],3))
        self.__image = Image.fromarray(numpy.fromstring(frame, dtype='uint8').reshape((self.__dimensions["height"],self.__dimensions["width"],3)))
        self.__inputs = self.__feature_extractor(images=self.__image, return_tensors="pt")

    def __get_output(self):
        self.__outputs = self.__model(**self.__inputs)
    

    def output(self):
        super().output()
        import torch
        target_sizes = torch.tensor([self.__image.size[::-1]])
        results = self.__feature_extractor.post_process_object_detection(self.__outputs, target_sizes=target_sizes)[0]
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            box = [round(i, 2) for i in box.tolist()]
            # let's only keep detections with score > 0.9
            if score > 0.5:
                print(
                    f"Detected {self.__model.config.id2label[label.item()]} with confidence "
                    f"{round(score.item(), 3)} at location {box}"
                )
                self.parsed_outputs.append({"box": [int(box[0]), int(box[1]), int(box[2]), int(box[3])], "item": self.__model.config.id2label[label.item()], "confidence": round(score.item(), 3)})
        
        return True
    
    def draw_output(self):
        import cv2
        import numpy as np
        #img_draw = ImageDraw.Draw(self.__image)
        for output in self.parsed_outputs:
            #img_draw.rectangle(((self.parsed_outputs[0], self.parsed_outputs[1]),(logo_x+logo_width, logo_y+logo_height)), outline='Red')
            if output["confidence"] > 0.6:
                #img_draw.rectangle(((output["box"][0], output["box"][1]),(output["box"][2], output["box"][3])), outline='Red')
                cv2.rectangle(self.__numpy_image, (output["box"][0], output["box"][1]), (output["box"][2], output["box"][3]), (0, 255, 0), 2)
                text = output["item"] + ": " + str(output["confidence"])
                cv2.putText(self.__numpy_image, text, (output["box"][0],output["box"][1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        self.parsed_outputs = []
        cv2.imshow("CV VIZ",self.__numpy_image)
        

    def run(self):
        import cv2
        super().input(image=None)
        cv2.namedWindow("CV VIZ")
        while True:
            raw_image = self.__pipe.stdout.read(self.__dimensions["width"]*self.__dimensions["height"]*3) # read 432*240*3 bytes (= 1 frame)
            self.__parse_input(frame=raw_image)
            #image = numpy.fromstring(raw_image, dtype='uint8').reshape((576,1024,3))
            #cv2.imshow("VLC COPY",image)
            self.__get_output()
            self.output()
            #sleep(1)
            self.draw_output()
            #self.__pipe.stdout.flush()
            if cv2.waitKey(1) == 27:
                break
        cv2.destroyAllWindows()
        return True