FROM ubuntu:disco

RUN apt-get update \
  && apt-get install --no-install-recommends -y \
  git \
  build-essential \
  python3 \
  python3-pip \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /home/app

COPY requirements.txt .

RUN pip3 install --upgrade pip \
  && pip3 install --upgrade setuptools \
  && pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["python3", "todo/main.py"]
