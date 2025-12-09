from pymavlink import mavutil
import time

# Connect to PX4 via MAVLink
print("Connecting to PX4...")
master = mavutil.mavlink_connection('udpout:172.0.0.1:14580')

master.wait_heartbeat()
print("Heartbeat received from PX4!")

# Request telemetry
master.mav.request_data_stream_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_DATA_STREAM_ALL,
    10, 1
)

print("Listening for altitude messages...")
for _ in range(20):
    msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True, timeout=2)
    if msg:
        altitude = msg.relative_alt / 1000.0   # mm → m
        print(f"Altitude: {altitude:.2f} m")
    time.sleep(0.2)

print("Test complete ✔️")
