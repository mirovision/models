"""
    mirovision AI Team
    main.py
    Example usage of our models

"""

from models.base import *

def main():
    models: list[CVModel] = [ObjectDetection()]
    image = "image"
    
    for model in models:
        model.input(image=image)
        model.output()
    return


if __name__ == "__main__":
    main()