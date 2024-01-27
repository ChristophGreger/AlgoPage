FROM ubuntu:latest
LABEL authors="Christoph Greger"
WORKDIR /home
RUN apt-get update && \
    apt-get install -y curl unzip python3 git nodejs pip && \
    git clone https://github.com/ChristophGreger/AlgoPage.git && \
    cd AlgoPage/ && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    reflex init
EXPOSE 8000/tcp
EXPOSE 3000/tcp
ENTRYPOINT ["reflex", "run"]
