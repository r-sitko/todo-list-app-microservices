FROM ubuntu:disco

RUN apt-get update \
  && apt-get install --no-install-recommends -y \
  build-essential \
  git \
  && rm -rf /var/lib/apt/lists/*

RUN  apt-get update \
  && apt-get install --no-install-recommends -y \
  protobuf-compiler \
  protobuf-compiler-grpc \
  libprotobuf-dev

ENTRYPOINT ["./buildAll.sh"]
