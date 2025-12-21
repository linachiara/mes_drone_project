#include <systemc.h>
#include "drone_defs.h"

SC_MODULE(ProcessingModule) {
    sc_in<bool> clk;
    sc_fifo_in<float> error_in;
    sc_fifo_out<float> cmd_out;

    int latency_ms; // Internal variable

    SC_CTOR(ProcessingModule) : latency_ms(0) {
        SC_THREAD(control_loop);
        sensitive << clk.pos();
    }

    // Public method to change simulation scenarios
    void set_latency(int ms) {
        latency_ms = ms;
    }

    void control_loop() {
        while (true) {
            float error = 0;
            if (error_in.num_available() > 0) {
                error_in.read(error);
            }

            // P-Control Logic
            float cmd = error * KP_YAW;

            // Clamp
            if (cmd > 60) cmd = 60;
            if (cmd < -60) cmd = -60;

            // Simulated Latency
            if (latency_ms > 0) {
                wait(latency_ms, SC_MS);
            }

            cmd_out.write(cmd);
            wait(SC_ZERO_TIME); // Sync
        }
    }
};