FROM python:3.10.7-bullseye
ARG DEBIAN_FRONTEND=noninteractive
RUN mkdir "/app"
WORKDIR "/app"
COPY . .

RUN pip install -r requirements.txt
CMD ["gunicorn"  , "-b", "0.0.0.0:8002", "wsgi:app"]
EXPOSE 8002