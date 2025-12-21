#!/usr/bin/env python3
import asyncio
import socket
from mavsdk import System
from mavsdk.offboard import OffboardError, VelocityBodyYawspeed

# LISTEN ON PORT 7000 (Output of SystemC)
UDP_PORT = 7000 

async def run():
    drone = System()
    await drone.connect(system_address="udpin://0.0.0.0:14540")

    print("--> Connecting to drone...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("--> Connected!")
            break

    # --- OFFBOARD SETUP ---
    print("--> Arming & Taking Off...")
    await drone.action.arm()
    await drone.action.takeoff()
    await asyncio.sleep(8)

    print("--> Starting Bridge (Passive Mode)...")
    
    # Send setpoint before starting
    await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))

    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Offboard failed: {error._result.result}")
        return

    # --- UDP LISTENER ---
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", UDP_PORT))
    sock.setblocking(False) # Non-blocking to allow asyncio to run

    while True:
        try:
            # FLUSH BUFFER (Read until empty)
            data = None
            while True:
                try:
                    chunk, _ = sock.recvfrom(1024)
                    data = chunk
                except BlockingIOError:
                    break
            
            # If we got a fresh packet
            if data:
                msg = data.decode('utf-8').strip()
                if msg.startswith("MOVE"):
                    # Parse "MOVE <fwd> <yaw>"
                    _, fwd_str, yaw_str = msg.split()
                    fwd = float(fwd_str)
                    yaw = float(yaw_str)
                    
                    # Command Drone
                    await drone.offboard.set_velocity_body(
                        VelocityBodyYawspeed(fwd, 0.0, 0.0, yaw)
                    )
        except Exception:
            pass

        await asyncio.sleep(0.01) # fast loop

if __name__ == "__main__":
    asyncio.run(run())