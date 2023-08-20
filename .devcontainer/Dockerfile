FROM node:18-bullseye

ENV DEBIAN_FRONTEND noninteractive
ENV DISPLAY $DISPLAY

RUN apt-get update \
    && apt-get install -y \
    python3 \
    python3-pip \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

COPY requirements.txt package-lock.json package.json ./

RUN pip install -r requirements.txt && \
    npm install
