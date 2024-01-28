FROM python:latest
LABEL authors="Christoph Greger"
WORKDIR /home
RUN apt-get update && \
    apt-get install curl unzip git nodejs -y && \
    git clone https://github.com/ChristophGreger/AlgoPage.git
WORKDIR /home/AlgoPage
RUN python3 -m venv .venv && \
    /bin/bash -c "source .venv/bin/activate" && \
    pip install --upgrade pip && \
    pip install -r requirements.txt
RUN reflex init
EXPOSE 8000/tcp
EXPOSE 3000/tcp
# ENTRYPOINT ["screen -AmdS myreflex reflex run"]
