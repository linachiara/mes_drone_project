import asyncio
from mavsdk import System
import keyboard  # pip install keyboard

async def manual_controls_keyboard():
    drone = System()
    await drone.connect(system_address="udpin://0.0.0.0:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("-- Connected to drone!")
            break

    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position state is good enough for flying.")
            break
        
    # setze initiale Werte direkt vor start_position_control
    await drone.manual_control.set_manual_control_input(0.0, 0.0, 0.5, 0.0)
    await asyncio.sleep(0.1)  # kurz warten, damit der Input registriert wird
    await drone.manual_control.start_position_control()

    await drone.action.arm()
    print("-- Taking off")
    await drone.action.takeoff()
    await asyncio.sleep(5)

    print("-- Starting manual control")
    await drone.manual_control.start_position_control()

    throttle = 0.5
    pitch = roll = yaw = 0

    while True:
        # Roll: A/D, Pitch: W/S, Yaw: Q/E, Throttle: R/F
        roll = -1 if keyboard.is_pressed('a') else 1 if keyboard.is_pressed('d') else 0
        pitch = -1 if keyboard.is_pressed('w') else 1 if keyboard.is_pressed('s') else 0
        yaw = -1 if keyboard.is_pressed('q') else 1 if keyboard.is_pressed('e') else 0
        if keyboard.is_pressed('r'):
            throttle = min(throttle + 0.01, 1)
        elif keyboard.is_pressed('f'):
            throttle = max(throttle - 0.01, 0)

        await drone.manual_control.set_manual_control_input(pitch, roll, throttle, yaw)
        await asyncio.sleep(0.05)  # Steuerung wird alle 50ms aktualisiert

if __name__ == "__main__":
    asyncio.run(manual_controls_keyboard())
