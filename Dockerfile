# syntax=docker/dockerfile:1

FROM python:3.11-slim-buster

WORKDIR /app

RUN apt-get -qq update && DEBIAN_FRONTEND=noninteractive apt-get -y install \
    cmake \
    curl \
    ghostscript \
    git \
    libjpeg-turbo-progs \
    libjpeg62-turbo-dev \
    liblcms2-dev \
    meson \
    netpbm \
    python3-dev \
    python3-setuptools \
    sudo \
    tcl8.6-dev \
    tk8.6-dev \
    virtualenv \
    wget \
    xvfb \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]