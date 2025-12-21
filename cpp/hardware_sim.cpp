#include <systemc.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <iostream>
#include <string>
#include <vector>
#include <sstream>

using namespace std;

SC_MODULE(DroneController) {
    // Tuning Constants
    const float KP_YAW = 0.15f;
    const float KP_DIST = 0.0003f;
    const float TARGET_AREA = 6000.0f;
    
    // Sockets
    int sock_in, sock_out;
    struct sockaddr_in addr_in, addr_out;

    SC_CTOR(DroneController) {
        SC_THREAD(process_loop);
        setup_sockets();
    }

    void setup_sockets() {
        // 1. Input Socket (Listen on 6000 from Vision)
        sock_in = socket(AF_INET, SOCK_DGRAM, 0);
        int opt = 1;
        setsockopt(sock_in, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)); // Fix "Port In Use" error
        
        addr_in.sin_family = AF_INET;
        addr_in.sin_port = htons(6000);
        addr_in.sin_addr.s_addr = INADDR_ANY;
        bind(sock_in, (struct sockaddr*)&addr_in, sizeof(addr_in));

        // 2. Output Socket (Send to 7000 for Python)
        sock_out = socket(AF_INET, SOCK_DGRAM, 0);
        addr_out.sin_family = AF_INET;
        addr_out.sin_port = htons(7000);
        inet_pton(AF_INET, "127.0.0.1", &addr_out.sin_addr);
        
        cout << "[SystemC] Controller Started. Listening on 6000, sending to 7000." << endl;
    }

    void process_loop() {
        char buffer[1024];
        char temp_buffer[1024]; // Temp bucket for flushing
        
        while (true) {
            int last_n = -1;

            // --- THE FIX: FLUSH THE BUFFER ---
            // Keep reading until the mailbox is empty to get the LATEST packet
            while(true) {
                int n = recv(sock_in, temp_buffer, 1024, MSG_DONTWAIT);
                if (n < 0) break; // Buffer is empty, stop reading
                
                // Save the latest valid packet
                last_n = n;
                memcpy(buffer, temp_buffer, n);
            }

            // Only process if we actually got new data
            if (last_n > 0) {
                buffer[last_n] = '\0';
                string msg(buffer);
                
                // ... Your Existing Parsing Logic ...
                float cmd_fwd = 0.0f;
                float cmd_yaw = 0.0f;

                if (msg.find("DATA") == 0) {
                    stringstream ss(msg);
                    string tag;
                    int error_x, area;
                    ss >> tag >> error_x >> area;

                    // Math (Your code was correct here)
                    cmd_yaw = error_x * KP_YAW;
                    float dist_error = TARGET_AREA - area;
                    cmd_fwd = dist_error * KP_DIST;

                    // Clamps
                    if (cmd_yaw > 60) cmd_yaw = 60;
                    if (cmd_yaw < -60) cmd_yaw = -60;
                    if (cmd_fwd > 2.0) cmd_fwd = 2.0;
                    if (cmd_fwd < -2.0) cmd_fwd = -2.0;

                    // Send to Python
                    string out_msg = "MOVE " + to_string(cmd_fwd) + " " + to_string(cmd_yaw);
                    sendto(sock_out, out_msg.c_str(), out_msg.size(), 0, (struct sockaddr*)&addr_out, sizeof(addr_out));
                }
            }
            wait(10, SC_MS); // 100Hz
        }
    }
};

int sc_main(int argc, char* argv[]) {
    DroneController controller("DroneController");
    sc_start();
    return 0;
}