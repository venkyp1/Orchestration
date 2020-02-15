FROM alpine
RUN  mkdir /app & apk update &&  \
     apk upgrade && apk add bash && \
     apk add python && apk add py-pip && \
     pip install flask
ADD  webapiV1.py /app
ADD  make_cpu_busy.sh /app
EXPOSE 5000
WORKDIR /app
ENTRYPOINT ["python", "/app/webapiV1.py"]
