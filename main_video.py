"""
    mirovision AI Team
    main.py
    Example usage of our models

"""

from models.base import *

def main():
    #url = "https://iptv-org.github.io/iptv/countries/ad.m3u8"
    #url = "https://s6.hopslan.com/orf11/tracks-v1a1/mono.m3u8"
    url=  "https://s6.hopslan.com/orf11/tracks-v1a1/mono.m3u8"
    models: list[CVModel] = [ObjectDetectionVideo(stream_url=url, width=1024, height=576)]
    models[0].run()
    

if __name__ == "__main__":
    main()