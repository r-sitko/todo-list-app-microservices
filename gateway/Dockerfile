FROM ubuntu:disco

RUN apt-get update \
  && apt-get install --no-install-recommends -y \
  build-essential \
  cmake \
  git \
  libgrpc++-dev \
  libprotobuf-dev \
  openssl \
  libcrypto++6 \
  libssl-dev \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /home/app
COPY . .
RUN chmod +x run.sh

ENTRYPOINT ["./run.sh"]
