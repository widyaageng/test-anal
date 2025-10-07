FROM ubuntu:20.04

RUN apt-get update -y && apt-get install curl vim jq -y && \
    curl --proto '=https' --tlsv1.2 -sSfL https://sh.vector.dev | bash -s -- -y --prefix /usr/local

ENV RUST_BACKTRACE="full"
ENV PATH="/usr/local/bin:${PATH}"

RUN mkdir -p /etc/vector

COPY vector.yaml /etc/vector/vector.yaml

RUN mkdir -p /var/vector/data

EXPOSE 8080 8686

ENTRYPOINT ["/usr/local/bin/vector"]
CMD ["--config", "/etc/vector/vector.yaml"]