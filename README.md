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
sudo apt install gazebo11
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
git clone <your-repo-url> mes_drone_project
cd mes_drone_project
```

2. Initialize and update submodules recursively:

```bash
git submodule update --init --recursive
```

3. Verify submodules:

```bash
git submodule status
```

4. Pull latest changes from submodules (optional):

```bash
git submodule update --remote --merge
```

---

## Build and Run Simulation

### Build without camera window

```bash
cd ~/mes_drone_project/simulation/px4
make px4_sitl gazebo
```

### Build with camera window

```bash
cd ~/mes_drone_project/simulation/px4
source /opt/ros/humble/setup.bash
make px4_sitl gazebo
```

---

## Start Camera Script (in a separate terminal)

```bash
cd ~/mes_drone_project/scripts/
python3 camera_view.py
```

---

## Notes

- PX4 is included as a **submodule**. Always use `--recursive` when cloning the repository.
- For any changes inside the PX4 submodule, commit inside the submodule first, then update the reference in the main repo.
- Recommended Ubuntu version: 22.04 LTS.
