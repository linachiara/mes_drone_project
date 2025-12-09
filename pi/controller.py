#!/usr/bin/env python3
import asyncio
from mavsdk import System
from mavsdk.offboard import OffboardError, VelocityBodyYawspeed

async def manual_control():
    drone = System()
    await drone.connect(system_address="udpin://0.0.0.0:14540")

    # Wait for connection
    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("-- Connected to drone!")
            break

    # Wait for global position estimate
    print("Waiting for global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")
            break
    await asyncio.sleep(2)
        
    # Arm the drone
    print("Arming...")
    await drone.action.arm()
    
    # send initial setpoint
    await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
    await asyncio.sleep(2)

    # Start in offboard mode
#    try:
#        await drone.offboard.start()
#    except OffboardError as e:
#        print(f"Offboard start failed: {e._result.result}")
    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(
            f"Starting offboard mode failed with error code: \
              {error._result.result}"
        )
        print("-- Disarming")
        await drone.action.disarm()
        return

    # Takeoff to 2 meters
    print("Taking off...")
    await drone.action.takeoff()
    await asyncio.sleep(6)  # wait for the drone to lift off

    print("\nManual control keys:")
    print(" w/s : forward/backward")
    print(" a/d : left/right")
    print(" r/f : up/down")
    print(" q/e : yaw left/right")
    print(" x   : exit\n")

    # Movement state
    velocity_x = 0.0
    velocity_y = 0.0
    velocity_z = 0.0
    yaw_rate = 0.0

    try:
        while True:
            key = input("Enter command: ")

            if key == "w":
                velocity_x = 1.0
            elif key == "s":
                velocity_x = -1.0
            elif key == "a":
                velocity_y = -1.0
            elif key == "d":
                velocity_y = 1.0
            elif key == "r":
                velocity_z = -0.5  # negative = up
            elif key == "f":
                velocity_z = 0.5   # positive = down
            elif key == "q":
                yaw_rate = -30.0
            elif key == "e":
                yaw_rate = 30.0
            elif key == "x":
                break
            else:
                # Reset movement on invalid key
                velocity_x = 0.0
                velocity_y = 0.0
                velocity_z = 0.0
                yaw_rate = 0.0

            # Send the velocity command continuously for 1 second
            for _ in range(10):
                await drone.offboard.set_velocity_body(
                    VelocityBodyYawspeed(
                        forward_m_s=velocity_x,
                        right_m_s=velocity_y,
                        down_m_s=velocity_z,
                        yawspeed_deg_s=yaw_rate
                    )
                )
                await asyncio.sleep(0.1)

    except Exception as e:
        print(f"Exception: {e}")

    finally:
        print("Stopping offboard and disarming...")
        try:
            await drone.offboard.stop()
        except Exception:
            pass
        try:
            await drone.action.land()
        except Exception:
            pass
        try:
            await drone.action.disarm()
        except Exception:
            pass
        print("Manual control session ended.")

if __name__ == "__main__":
    asyncio.run(manual_control())
