FROM arm64v8/debian:bullseye

# ---- Basic system tools ----
RUN apt update && apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-setuptools \
    python3-dev \
    git \
    nano \
    curl \
    iputils-ping \
    net-tools \
    libatlas-base-dev \
    && apt clean

# ---- PX4 / MAVLink communication ----
RUN pip3 install \
    pymavlink \
    mavsdk \
    pyserial \
    numpy \
    opencv-python 

# ---- Create working directory for mounted Pi code ----
WORKDIR /pi
