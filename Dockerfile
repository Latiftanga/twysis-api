FROM python:3.8-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk  add --update --no-cache postgresql-client jpeg-dev
RUN apk  add --update --no-cache --virtual .temp-build-deps gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install -r /requirements.txt
RUN apk del .temp-build-deps

RUN mkdir /api
WORKDIR /api
COPY ./api /api

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser -D user
RUN chown user:user /vol/
RUN chmod -R 755 /vol/web/
USER user
