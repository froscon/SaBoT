FROM python:2.7
RUN apt update
RUN apt upgrade -y
RUN apt install vim -y
RUN mkdir /sabot
WORKDIR /sabot
ADD . /sabot
RUN pip install -r requirements.txt
EXPOSE 8000
