#!/bin/bash

# 1. Enter the build folder (Updated for your 'cpp' folder)
cd ~/mes_drone_project/cpp/build || { echo "Build folder missing! Did you run cmake/make?"; exit 1; }

# 2. Cleanup old processes so they don't pile up
echo "--- Cleaning up old processes ---"
killall -9 drone_vision flight_controller 2>/dev/null

sleep 1

# 3. Start SystemC Bridge (The Flight Controller)
echo "--- Starting Flight Controller ---"
./flight_controller & 

sleep 1

# 4. Start Vision (The Camera/OpenCV)
echo "--- Starting Vision Node ---"
./drone_vision