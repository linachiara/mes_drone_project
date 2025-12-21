#include <systemc.h>
#include <cmath>
#include "drone_defs.h"

SC_MODULE(SensorModule) {
    sc_in<bool> clk;
    sc_fifo_in<float> cmd_in;     // Input: Yaw Command
    sc_fifo_out<float> error_out; // Output: Calculated Error
    
    // Additional ports for the Monitor to see internal state
    sc_out<float> current_yaw_out;
    sc_out<float> current_target_out;

    float drone_yaw;
    int tick_count;

    SC_CTOR(SensorModule) : drone_yaw(0), tick_count(0) {
        SC_THREAD(update_physics);
        sensitive << clk.pos();
    }

    void update_physics() {
        while (true) {
            // 1. Generate Target (Sine Wave)
            float target_yaw = 50.0f * sin(tick_count * 0.1f);
            
            // 2. Read Command
            float cmd = 0;
            if (cmd_in.num_available() > 0) cmd_in.read(cmd);

            // 3. Physics Integration
            drone_yaw += cmd * SIM_STEP * 10.0f; 

            // 4. Calculate Error
            float error = target_yaw - drone_yaw;

            // 5. Output Data
            error_out.write(error);
            
            // Send state to Monitor
            current_yaw_out.write(drone_yaw);
            current_target_out.write(target_yaw);

            tick_count++;
            wait();
        }
    }
};