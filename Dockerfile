# Start with the base ROS image
FROM osrf/ros:humble-desktop-full

# 1. Install System Tools & Python Dependencies
RUN apt-get update && apt-get install -y \
    git wget build-essential ccache \
    python3-pip python3-jinja2 python3-numpy \
    python3-empy python3-toml python3-packaging python3-jsonschema

# 2. Install Gazebo 11 (Classic)
RUN sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable jammy main" > /etc/apt/sources.list.d/gazebo-stable.list' && \
    wget https://packages.osrfoundation.org/gazebo.key -O - | apt-key add - && \
    apt-get update && \
    apt-get install -y gazebo

# 3. (Optional) Install the missing pip tool you found earlier
RUN pip3 install kconfiglib

# 4. Set the default folder when you log in
WORKDIR /root/mes_drone_project
