FROM python:3.10-alpine
ENV PYTHONBUFFERED 1
RUN mkdir /rik_test_jfenko
WORKDIR /rik_test_jfenko
COPY . .
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN adduser -D user
USER user