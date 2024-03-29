FROM python:latest
LABEL authors="Christoph Greger"
WORKDIR /home
RUN apt-get update && \
    apt-get install curl unzip git nodejs screen -y && \
    git clone https://github.com/ChristophGreger/AlgoPage.git
WORKDIR /home/AlgoPage
RUN bash /home/AlgoPage/install.sh
EXPOSE 8000/tcp
EXPOSE 3000/tcp
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
