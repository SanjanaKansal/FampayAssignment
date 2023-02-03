FROM python:3.6
RUN apt-get update && apt-get install -y netcat
RUN mkdir /youtube
WORKDIR /youtube
ADD . /youtube/
RUN pip install --upgrade pip && pip install -r requirements.txt