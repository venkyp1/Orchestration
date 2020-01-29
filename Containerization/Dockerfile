FROM alpine
RUN  mkdir /app & apk update &&  \
     apk upgrade && apk add bash && \
     apk add python && apk add py-pip && \
     pip install flask
ADD  webapi.py /app
EXPOSE 5000
WORKDIR /app
ENTRYPOINT ["python", "/app/webapi.py"]
