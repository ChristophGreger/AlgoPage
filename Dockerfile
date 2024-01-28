FROM alpine:latest
LABEL authors="Christoph Greger"
WORKDIR /home
RUN apk update && \
    apk add curl unzip git nodejs python3 py3-pip gcc python3-dev musl-dev linux-headers bash && \
    git clone https://github.com/ChristophGreger/AlgoPage.git
WORKDIR /home/AlgoPage
RUN python3 -m venv .venv && \
    /bin/ash -c "source .venv/bin/activate" && \
    pip install --break-system-packages --upgrade pip && \
    pip install --break-system-packages -r requirements.txt
RUN reflex init
EXPOSE 8000/tcp
EXPOSE 3000/tcp
ENTRYPOINT ["reflex run"]
