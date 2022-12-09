"""
    mirovision AI Team
    main.py
    Example usage of our models

"""

from models.base import *

def main():
    models: list[CVModel] = [ObjectDetectionVideo(stream_url="https://s6.hopslan.com/orf11/tracks-v1a1/mono.m3u8")]
    models[0].run()
    

if __name__ == "__main__":
    main()