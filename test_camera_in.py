
import io
import aiohttp
import asyncio
from PIL import Image
from keras.preprocessing import image
from multipart_reader import MultipartReader


counter = 0
server_url = "http://a412-163-5-23-104.ngrok.io/"

async def function():
    async with aiohttp.request(url=server_url, method="GET") as resp:
        reader = aiohttp.MultipartReader.from_response(resp)
        while True:
            part = await reader.next()
            content = await part.read()

            print("==========")
            print (part.headers[aiohttp.hdrs.CONTENT_TYPE])
            print("==========")
            print (type(content))
            print("==========")

            img = Image.open(io.BytesIO(content))#.convert("RGBA")
            img = img.save("ARENTWASUP" + str(counter) + ".jpg")
            if part is None:
                break
            
    

asyncio.run(function())
# response = None
# print ("---- START ----")
# while True:
#     print("--- HEAD ---")
#     response = requests.get("http://fcbc-163-5-23-104.ngrok.io/")
#     image = response.content
#     print (image)
# print ("---- END ----")
# URL = "http://2143-163-5-23-104.ngrok.io"
# http =  urllib3.PoolManager()
# response = http.request("GET", URL)

# mybytes = response.read()

# mystr = mybytes.decode("utf8")
# fp.close()

# print(mystr)

# http = urllib3.PoolManager()
# r = http.request('GET', "http://7f69-163-5-23-104.ngrok.io/")
# print (r)
#response = urllib3.urlopen("http://7f69-163-5-23-104.ngrok.io/")

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # now connect to the web server on port 80 - the normal http port
# s.connect(("http://7f69-163-5-23-104.ngrok.io/", 8080))


# conn = httplib.HTTPConnection("8080")
# while True:
# 	conn.request("GET","http://7f69-163-5-23-104.ngrok.io/")
# 	respon1 = conn.getresponse()
# 	print (respon1)

# print ("You got Error!!")



# h1 = http.client.HTTPConnection('http://7f69-163-5-23-104.ngrok.io/')
# print (h1)
# r = requests.get(settings.STATICMAP_URL.format(**data), stream=True)
# if r.status_code == 200:
#     with open(path, 'wb') as f:
#         for chunk in r:
#             f.write(chunk)

# import shutil

# import requests

# url = 'http://330c-163-5-23-104.ngrok.io/'
# response = requests.get(url, stream=True)
# with open('img.png', 'wb') as out_file:
#     shutil.copyfileobj(response.raw, out_file)
# del response