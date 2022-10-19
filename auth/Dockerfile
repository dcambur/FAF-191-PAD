FROM python:3.10.7-bullseye
ARG DEBIAN_FRONTEND=noninteractive
RUN mkdir "/app"
WORKDIR "/app"
COPY . .

RUN pip install -r requirements.txt
CMD ["gunicorn"  , "-t", "30", "-w", "3", "-b", "0.0.0.0:8000", "wsgi:app"]
EXPOSE 8000