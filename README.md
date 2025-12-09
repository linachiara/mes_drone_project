# Drone Simulation Project

This project contains a drone simulation using **PX4 Autopilot** and **Gazebo Classic** on Ubuntu 22.04. It includes scripts and models for running simulations with or without camera view.

---

## Prerequisites

Make sure you have all necessary installations:

```bash
sudo apt update
sudo apt install git wget python3-pip python3-jinja2 python3-numpy \
python3-empy python3-toml python3-packaging python3-jsonschema \
build-essential ccache
```

### Install Gazebo Classic (version 11) on Ubuntu 22.04

```bash
sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable jammy main" > /etc/apt/sources.list.d/gazebo-stable.list'
wget https://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -
sudo apt update
sudo apt install gazebo
```

Confirm installation:

```bash
gazebo --version
# Expected output: Gazebo multi-robot simulator, version 11.x.x
```

---

## Clone and Setup Project

1. Clone the main project:

```bash
git clone git@github.com:linachiara/mes_drone_project.git mes_drone_project --recursive
cd mes_drone_project
```

2. If you forgot the "--recursive" or the submodules haven't loaded 

```bash
git submodule update --init --recursive
```

3. Verify submodules:

```bash
git submodule status
```

---

## To run the simulation with the right Gazebo version

```bash
sudo apt remove gz-harmonic
sudo apt install aptitude
sudo aptitude install gazebo libgazebo11 libgazebo-dev
```

---

## Build and Run Simulation

### Build without camera window

You can always start the simulation with this command:
```bash
cd ~/mes_drone_project/simulation/px4
make px4_sitl gazebo-classic_typhoon_h480
```

Or use the script:

1. Run once
```bash
cd ~/mes_drone_project/simulation/
bash ./Tools/setup/ubuntu.sh
```

2. Start simulation always with
```bash
cd ~/mes_drone_project/simulation/
./simulation/run_sim.sh
```

## Build with camera window

### Installation of QGroundControl

1. Disable Modem Manager
```bash
sudo systemctl stop ModemManager.service
sudo systemctl disable ModemManager.service
```
After the project you can enable it again with the commands
```bash
sudo systemctl enable ModemManager.service
sudo systemctl start ModemManager.service
```
2. Install QGroundControl
   Go to this website and follow the instructions:
   https://docs.qgroundcontrol.com/Stable_V5.0/en/qgc-user-guide/getting_started/download_and_install.html

## Use QGroundControl
Start the simulation in one terminal, QGroundControl in another

```bash
cd to/the/folder/you/put/your/script
./QGroundControl-x86_64.AppImage
```

---

## Build Docker-Image
```bash
cd mes_drone_project/docker
docker build --platform=linux/arm64 -t virtual-pi .
```

## Run Docker-Image

Exchange the path correctly
```bash
docker run --rm -it \
  --platform=linux/arm64 \
  --network=host \
  -v /home/linachiara/mes_drone_project/pi:/pi \    
  virtual-pi
```

## Notes

- You can't commit any changes in submodules that are not forked yet.
- If you want to do that, you must fork the submodule first.
