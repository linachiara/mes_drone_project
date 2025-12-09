#!/usr/bin/env python3


import asyncio

from mavsdk import System
from mavsdk.offboard import OffboardError, VelocityBodyYawspeed


async def move(drone, forward=0.0, right=0.0, down=0.0, yaw_rate=0.0, duration=1.0):
    """
    Bewegt den Drohnenkörper in eine Richtung für eine kurze Dauer.
    """
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(
            forward_m_s=forward,
            right_m_s=right,
            down_m_s=down,
            yawspeed_deg_s=yaw_rate
        )
    )
    await asyncio.sleep(duration)
    # Stoppen nach der Bewegung
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0)
    )


async def run():
    """Does Offboard control using velocity body coordinates."""

    drone = System()
    await drone.connect(system_address="udpin://0.0.0.0:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("-- Connected to drone!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")
            break

    print("-- Arming")
    await drone.action.arm()

    
    # Takeoff to 2 meters
    print("Taking off...")
    await drone.action.takeoff()
    await asyncio.sleep(6)  # wait for the drone to lift off

    print("-- Setting initial setpoint")
    await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))

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
    



    print("\nManual control keys:")
    print(" w/s : forward/backward")
    print(" a/d : left/right")
    print(" r/f : up/down")
    print(" q/e : yaw left/right")
    print(" x   : exit\n")

    try:
        while True:
            key = input("Enter Command: ").lower()

            if key == "w":
                await move(drone, forward=1.0, duration=1.0)
            elif key == "s":
                await move(drone, forward=-1.0, duration=1.0)
            elif key == "a":
                await move(drone, right=-1.0, duration=1.0)
            elif key == "d":
                await move(drone, right=1.0, duration=1.0)
            elif key == "r":
                await move(drone, down=-0.5, duration=1.0)  # up
            elif key == "f":
                await move(drone, down=0.5, duration=1.0)   # down
            elif key == "q":
                await move(drone, yaw_rate=-30.0, duration=1.0)
            elif key == "e":
                await move(drone, yaw_rate=30.0, duration=1.0)
            elif key == "x":
                break
            else:
                print("Invalid Command!")

    except Exception as e:
        print(f"Exception: {e}")





    
    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(
            f"Stopping offboard mode failed with error code: \
              {error._result.result}"
        )
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
    # Run the asyncio loop
    asyncio.run(run())