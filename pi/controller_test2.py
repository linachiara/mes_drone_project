import asyncio
import logging

from mavsdk import System

# Enable INFO level logging by default so that INFO messages are shown
logging.basicConfig(level=logging.INFO)

async def main():
    drone = System()
    print("Connecting...")
    await drone.connect(system_address="udpin://0.0.0.0:14540")

    print("Waiting for connection...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Connected!")
            break

    print("Waiting for GPS...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok:
            print("GPS OK")
            break

    print("Taking off...")
    await drone.action.takeoff()
    await asyncio.sleep(10)

    print("Moving forward...")
    await drone.action.goto_location(
        47.3977420,  # latitude
        8.5455940,   # longitude
        5,           # altitude
        0            # yaw
    )
    await asyncio.sleep(10)

    print("Landing...")
    await drone.action.land()

    print("Done.")

if __name__ == "__main__":
    asyncio.run(main())
