#include <systemc.h>
#include <iostream>
#include <fstream>
#include <iomanip> // For precision

SC_MODULE(ActuatorModule) {
    sc_in<bool> clk;
    sc_in<float> target_in;
    sc_in<float> yaw_in;

    std::ofstream file;

    SC_CTOR(ActuatorModule) {
        SC_METHOD(log_data);
        sensitive << clk.pos();
        // Do not open file in constructor anymore
    }

    ~ActuatorModule() {
        if(file.is_open()) file.close();
    }

    // Call this before each simulation run
    void start_log(const char* filename) {
        if (file.is_open()) file.close();
        
        file.open(filename);
        // Write CSV Header
        file << "Time,TargetYaw,DroneYaw,Error" << std::endl;
        std::cout << "--> Logging to: " << filename << std::endl;
    }

    void log_data() {
        if (file.is_open()) {
            float t = target_in.read();
            float y = yaw_in.read();
            float err = t - y;

            file << std::fixed << std::setprecision(4) 
                 << sc_time_stamp().to_seconds() << "," 
                 << t << "," 
                 << y << "," 
                 << err << std::endl;
        }
    }
};