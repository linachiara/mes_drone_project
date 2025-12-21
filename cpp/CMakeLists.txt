cmake_minimum_required(VERSION 3.10)
project(DroneProject)

# ==========================================
# 1. Global Settings
# ==========================================
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# ==========================================
# 2. Find Dependencies
# ==========================================
# A. OpenCV
find_package(OpenCV REQUIRED)
message(STATUS "Found OpenCV: ${OpenCV_VERSION}")

# B. SystemC
find_package(Threads REQUIRED) # SystemC needs threads

# Check for manual SystemC path or system install
if(EXISTS "/usr/local/systemc-2.3.3")
    set(SC_HOME "/usr/local/systemc-2.3.3")
    include_directories(${SC_HOME}/include)
    link_directories(${SC_HOME}/lib-linux64)
    set(SC_LIB_NAME "systemc")
    message(STATUS "Using Manual SystemC Path: ${SC_HOME}")
else()
    # Try finding it in standard system paths (apt install)
    find_library(SC_LIB_NAME systemc)
    find_path(SC_INCLUDE_DIR systemc.h)
    if (SC_LIB_NAME AND SC_INCLUDE_DIR)
        include_directories(${SC_INCLUDE_DIR})
    	message(STATUS "Using System Install of SystemC")
    else()
        message(FATAL_ERROR "SystemC not found! Please check your path.")
    endif()
endif()

# ==========================================
# 3. Target 1: The Vision System (OpenCV)
# ==========================================
# This is your "Face Tracker" / "Drone Eye"
add_executable(drone_vision main_vision.cpp)
target_link_libraries(drone_vision ${OpenCV_LIBS})

# ==========================================
# 4. Target 2: The Hardware Simulator (SystemC)
# ==========================================
# This is your "Constraint Checker" / "Flight Controller"
add_executable(flight_controller hardware_sim.cpp)
target_link_libraries(flight_controller ${SC_LIB_NAME} Threads::Threads)