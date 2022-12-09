"""
    mirovision AI Team
    main.py
    Example usage of our models

"""

from models.base import *

def main():
    models: list[CVModel] = [ObjectDetection()]
    url = "http://images.cocodataset.org/val2017/000000039769.jpg"
    import requests
    #url="http://192.168.113.232:8081/"
    for model in models:
        image = requests.get(url, stream=True).raw
        model.input(image=image)
        model.output()
    return

if __name__ == "__main__":
    main()