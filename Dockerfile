FROM python:3.7-alpine
RUN apk update && apk add graphviz xdg-utils
RUN apk add build-base python-dev py-pip freetype-dev jpeg-dev zlib-dev
RUN mkdir /code
WORKDIR /code
COPY ./src/requirements.txt .
RUN pip install -r requirements.txt
COPY ./src/ .
CMD ["gunicorn", "-b", "0.0.0.0:5000", "wsgi"]
