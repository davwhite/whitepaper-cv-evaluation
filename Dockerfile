# hadolint global ignore=DL3041
FROM quay.io/centos/centos:stream9

ARG MINIO_CLIENT_URL=https://dl.min.io/client/mc/release/linux-amd64

RUN dnf -y --setopt=tsflags=nodocs upgrade && \
    dnf install -y git wget libGL python3-pip && \
    dnf clean all && \
    curl -s -L "${MINIO_CLIENT_URL}/mc" -o ${APP_ROOT}/bin/mc && \
    chmod +x ${APP_ROOT}/bin/mc

# set no-cache-dir for pip
ENV PIP_NO_CACHE_DIR=1

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

USER 1001

VOLUME /models

CMD ["/opt/app-root/src/app.sh"]
