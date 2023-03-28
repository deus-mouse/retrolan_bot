FROM python:3.8-slim

RUN mkdir -p /usr/src/retrolan-bot/
RUN apt update

WORKDIR /usr/src/retrolan-bot/

COPY . /usr/src/retrolan-bot/
RUN pip install --no-cache-dir -r req.txt

CMD ["python", "run.py"]