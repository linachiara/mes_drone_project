#include <systemc.h>
#include "sensor_module.h"
#include "processing_module.h"
#include "actuator_module.h"

int sc_main(int argc, char* argv[]) {
    // 1. Signals & Clock
    sc_clock clk("sys_clk", 33, SC_MS); // 30Hz
    
    sc_fifo<float> fifo_err(10);
    sc_fifo<float> fifo_cmd(10);
    
    sc_signal<float> sig_yaw;
    sc_signal<float> sig_target;

    // 2. Instantiate
    SensorModule plant("Plant");
    ProcessingModule ctrl("Controller");
    ActuatorModule mon("Monitor");

    // 3. Connect
    plant.clk(clk);
    plant.cmd_in(fifo_cmd);
    plant.error_out(fifo_err);
    plant.current_yaw_out(sig_yaw);
    plant.current_target_out(sig_target);

    ctrl.clk(clk);
    ctrl.error_in(fifo_err);
    ctrl.cmd_out(fifo_cmd);

    mon.clk(clk);
    mon.yaw_in(sig_yaw);
    mon.target_in(sig_target);

    // ===========================
    // 4. RUN TEST SCENARIOS
    // ===========================

    // --- Scenario A: 10ms (Ideal) ---
    std::cout << "\n[Test 1] Simulating FPGA Architecture (10ms)..." << std::endl;
    ctrl.set_latency(10);
    mon.start_log("results_10ms.csv"); 
    sc_start(30, SC_SEC); // Run 0-10s

    // --- Scenario B: 50ms (Raspberry Pi) ---
    // Note: We don't reset the drone position to 0 here, 
    // so the drone continues from where it left off, but the control logic changes.
    std::cout << "\n[Test 2] Simulating Raspberry Pi Architecture (50ms)..." << std::endl;
    ctrl.set_latency(50);
    mon.start_log("results_50ms.csv");
    sc_start(30, SC_SEC); // Run 10-20s

    // --- Scenario C: 300ms (Overload) ---
    std::cout << "\n[Test 3] Simulating System Failure (300ms)..." << std::endl;
    ctrl.set_latency(300);
    mon.start_log("results_300ms.csv");
    sc_start(30, SC_SEC); // Run 20-30s

    std::cout << "\nAll Tests Complete." << std::endl;
    return 0;
}