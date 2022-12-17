FROM python:3.8

COPY ./freeze.txt app/freeze.txt

WORKDIR /app

RUN pip install -r freeze.txt

RUN apt-get update

RUN apt-get install ffmpeg libsm6 libxext6  -y

EXPOSE 8096

COPY . /app

#ENTRYPOINT [ "python3" ]

CMD ["python3", "server.py"]


