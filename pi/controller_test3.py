from mavsdk import System
import asyncio

async def main():
    drone = System()
    await drone.connect(system_address="udp://127.0.0.1:18570")

    print("Waiting for connection...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Connected! System ID: {state.system_id}")
            break

asyncio.run(main())
