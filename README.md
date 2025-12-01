Make sure you have all neccessary installations: 
sudo apt update
sudo apt install git wget python3-pip python3-jinja2 python3-numpy \
                 python3-empy python3-toml python3-packaging python3-jsonschema \
                 build-essential ccache


Gazebo Classic for Ubuntu 22.04
sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable jammy main" > /etc/apt/sources.list.d/gazebo-stable.list'
wget https://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -
sudo apt update
sudo apt install gazebo11

confirm: 
gazebo --version
Gazebo multi-robot simulator, version 11.x.x

Then, to clone the repository and start the project: 
1. Clone main project
  git clone <your-repo-url> mes_drone_project
  cd mes_drone_project

2. Initialize and update submodules recursively
   git submodule update --init --recursive

3. Verify submodules
   git submodule status

4. pull latest changes from submodules
   git submodule update --remote --merge

5. Build project without camera window
   cd ~/mes_drone_project/simulation/px4
   make px4_sitl gazebo

5. Build project with camera window
  cd ~/mes_drone_project/simulation/px4
  source /opt/ros/humble/setup.bash
  make px4_sitl gazebo

  start camera script in another window:
  cd ~/mes_drone_project/scripts/
  python3 camera_view.py

