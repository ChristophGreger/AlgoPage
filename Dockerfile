FROM python:latest
LABEL authors="Christoph Greger"
WORKDIR /home
RUN apt-get update && \
    apt-get install curl unzip git nodejs -y && \
    git clone --branch Docker https://github.com/ChristophGreger/AlgoPage.git
WORKDIR /home/AlgoPage
RUN bash /home/AlgoPage/install.sh
# RUN reflex init
EXPOSE 8000/tcp
EXPOSE 3000/tcp
ENTRYPOINT ["./entrypoint.sh"]
