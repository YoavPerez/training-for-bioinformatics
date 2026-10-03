# Base development image for the onboarding program.
# All versions are pinned; bump them deliberately and note it in the PR.
FROM ubuntu:24.04

ARG GTSAM_VERSION=4.3.0
ARG ARGO_VERSION=v4.1.4
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential cmake ninja-build git curl ca-certificates \
        libeigen3-dev clang-tidy gdb valgrind linux-tools-generic \
        python3 python3-venv python3-dev \
    && rm -rf /var/lib/apt/lists/*

# GTSAM, built without Boost features.
RUN curl -sL https://github.com/borglab/gtsam/archive/refs/tags/${GTSAM_VERSION}.tar.gz | tar xz -C /tmp \
    && cmake -S /tmp/gtsam-${GTSAM_VERSION} -B /tmp/gtsam-build -G Ninja \
        -DCMAKE_BUILD_TYPE=Release \
        -DGTSAM_USE_SYSTEM_EIGEN=ON \
        -DGTSAM_ENABLE_BOOST_SERIALIZATION=OFF \
        -DGTSAM_USE_BOOST_FEATURES=OFF \
        -DGTSAM_WITH_TBB=OFF \
        -DGTSAM_BUILD_TESTS=OFF \
        -DGTSAM_BUILD_EXAMPLES_ALWAYS=OFF \
        -DGTSAM_BUILD_UNSTABLE=OFF \
        -DGTSAM_BUILD_TYPE_POSTFIXES=OFF \
    && cmake --build /tmp/gtsam-build && cmake --install /tmp/gtsam-build \
    && rm -rf /tmp/gtsam-* && ldconfig

# Argo CLI (for `argo lint --offline` and submitting workflows).
RUN curl -sL https://github.com/argoproj/argo-workflows/releases/download/${ARGO_VERSION}/argo-linux-amd64.gz \
        | gunzip > /usr/local/bin/argo && chmod +x /usr/local/bin/argo

# Python environment.
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY infra/docker/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /workspace
