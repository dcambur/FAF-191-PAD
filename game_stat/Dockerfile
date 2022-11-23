FROM python:3.10.7-bullseye
ARG DEBIAN_FRONTEND=noninteractive
RUN mkdir "/app"
WORKDIR "/app"
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8003

ENTRYPOINT ["bash", "-c", "./entrypoint.sh"]