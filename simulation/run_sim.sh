#!/bin/bash
cd $(dirname "$0")/px4
make px4_sitl gazebo-classic_typhoon_h480
