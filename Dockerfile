FROM python:3.7-alpine
RUN apk update && apk add graphviz xdg-utils
RUN apk add build-base python-dev py-pip jpeg-dev zlib-dev
RUN mkdir /code
WORKDIR /code
COPY ./src/requirements.txt .
RUN pip install -r requirements.txt
COPY ./src/ .
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
