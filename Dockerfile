FROM python:3.8.10

WORKDIR .

ADD . .

RUN pip install -r freeze.txt

CMD ["./server.py"]
