#include <opencv2/opencv.hpp>
#include <iostream>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

using namespace cv;
using namespace std;

// --- CONFIGURATION ---
const string SYSTEMC_IP = "127.0.0.1";
const int SYSTEMC_PORT = 6000;

// --- UDP SETUP ---
int sock;
struct sockaddr_in dest_addr;

void setupUDP() {
    sock = socket(AF_INET, SOCK_DGRAM, 0);
    dest_addr.sin_family = AF_INET;
    dest_addr.sin_port = htons(SYSTEMC_PORT);
    inet_pton(AF_INET, SYSTEMC_IP.c_str(), &dest_addr.sin_addr);
}

void sendCommand(string msg) {
    sendto(sock, msg.c_str(), msg.size(), 0, (struct sockaddr*)&dest_addr, sizeof(dest_addr));
}

int main() {
    setupUDP();

    string gst_pipeline = 
        "udpsrc port=5600 caps=\"application/x-rtp, media=(string)video, encoding-name=(string)H264, payload=(int)96\" ! "
        "rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink drop=true sync=false max-buffers=1";
        
    /*string gst_pipeline = 
        "udpsrc port=5600 caps=\"application/x-rtp, media=(string)video, encoding-name=(string)H264, payload=(int)96\" ! "
        "rtph264depay ! h264parse ! avdec_h264 ! "
        "videoconvert ! video/x-raw, format=BGR ! " 
        "appsink drop=true sync=false";*/

    VideoCapture cap(gst_pipeline, CAP_GSTREAMER);

    if (!cap.isOpened()) {
        cerr << "Error: Waiting for stream..." << endl;
        return -1;
    }

    Mat frame, hsv, mask1, mask2, mask;
    cout << "Starting Proportional Vision..." << endl;

    while (true) {
        // Flush buffer for low latency
        //for(int i=0; i<5; i++) cap.grab();
        // 1. Read frame
        if (!cap.read(frame)) {
            cout << "Waiting for video packets..." << endl;
            continue; 
        }
        if (frame.empty()) break;

        // 1. HSV Conversion
        cvtColor(frame, hsv, COLOR_BGR2HSV);

        // 2. Red Detection (Using your tuned values)
        inRange(hsv, Scalar(0, 50, 20), Scalar(10, 255, 255), mask1);
        inRange(hsv, Scalar(160, 50, 20), Scalar(180, 255, 255), mask2);
        mask = mask1 | mask2; 

        // 3. Clean Noise
        erode(mask, mask, Mat(), Point(-1, -1), 2);
        dilate(mask, mask, Mat(), Point(-1, -1), 2);

        // 4. Find Contours
        vector<vector<Point>> contours;
        findContours(mask, contours, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);

        double maxArea = 0;
        int maxIdx = -1;

        for (size_t i = 0; i < contours.size(); i++) {
            double area = contourArea(contours[i]);
            if (area > maxArea) {
                maxArea = area;
                maxIdx = i;
            }
        }

        string packet = "NoData";

        if (maxIdx >= 0 && maxArea > 200) { 
            Rect r = boundingRect(contours[maxIdx]);
            rectangle(frame, r, Scalar(0, 255, 0), 2);
            
            // --- MATH TIME ---
            int centerX = r.x + (r.width / 2);
            int imageCenter = frame.cols / 2;
            
            // Error X: Negative = Ball is on Left, Positive = Ball is on Right
            int errorX = centerX - imageCenter; 
            
            // Send the raw data: "DATA <ErrorX> <AreaSize>"
            packet = "DATA " + to_string(errorX) + " " + to_string((int)maxArea);
            
            // Visual Debug
            line(frame, Point(imageCenter, 0), Point(imageCenter, frame.rows), Scalar(255, 255, 255), 1);
            putText(frame, "Err: " + to_string(errorX), Point(10, 30), FONT_HERSHEY_SIMPLEX, 0.7, Scalar(0, 255, 255), 2);
        } else {
            // Ball lost
            packet = "LOST";
        }

        // Send to Python
        sendCommand(packet);

        imshow("Drone Vision", frame);
        imshow("Mask", mask);
        
        if (waitKey(1) == 27) break;
    }

    close(sock);
    return 0;
}
