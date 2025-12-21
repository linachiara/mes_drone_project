#!/usr/bin/env python3
import asyncio
import pygame
import sys
from mavsdk import System
from mavsdk.offboard import OffboardError, VelocityBodyYawspeed

# --- CONFIGURATION ---
SPEED_XY = 2.0    # Meters per second (Forward/Right)
SPEED_Z  = 1.5    # Meters per second (Up/Down)
YAW_SENSITIVITY = 3.0 # Mouse sensitivity for rotation

async def run():
    # 1. Initialize Pygame (For Input Capture)
    pygame.display.init()
    pygame.font.init()
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Drone Manual Control (Click here to fly)")
    
    # Render some text
    font = pygame.font.SysFont(None, 24)
    img = font.render('Click here to capture mouse', True, (255, 255, 255))
    screen.blit(img, (20, 20))
    img2 = font.render('WASD: Move | Space/Shift: Up/Down | Mouse: Turn', True, (200, 200, 200))
    screen.blit(img2, (20, 50))
    img3 = font.render('ESC: Quit & Land', True, (200, 50, 50))
    screen.blit(img3, (20, 80))
    pygame.display.flip()

    # 2. Connect to Drone
    drone = System()
    print("--> Connecting to drone...")
    await drone.connect(system_address="udpin://0.0.0.0:14540")

    print("--> Waiting for drone connection...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("--> Connected!")
            break

    print("--> Arming & Taking Off...")
    await drone.action.arm()
    await drone.action.takeoff()
    
    print("--> Waiting for altitude (8s)...")
    for _ in range(80): # 80 * 0.1s = 8 seconds
        await asyncio.sleep(0.1)
        pygame.event.pump() # <--- Tells Ubuntu "I am still alive"

    # 3. Start Offboard Mode
    print("--> Starting Manual Control")
    
    # Send initial setpoint (required)
    await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))

    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Offboard failed: {error._result.result}")
        return

    # 4. Control Loop
    pygame.event.set_grab(True) # Lock mouse to window
    pygame.mouse.set_visible(False)
    
    running = True
    while running:
        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Read Inputs
        keys = pygame.key.get_pressed()
        
        # Calculate Velocities
        fwd_speed = 0.0
        right_speed = 0.0
        up_speed = 0.0
        yaw_rate = 0.0

        # WASD
        if keys[pygame.K_w]: fwd_speed = SPEED_XY
        if keys[pygame.K_s]: fwd_speed = -SPEED_XY
        if keys[pygame.K_a]: right_speed = -SPEED_XY
        if keys[pygame.K_d]: right_speed = SPEED_XY
        
        # Space / Shift (Up/Down)
        # Note: In NED coordinates, Negative is UP!
        if keys[pygame.K_SPACE]: up_speed = -SPEED_Z
        if keys[pygame.K_LSHIFT]: up_speed = SPEED_Z

        # Mouse (Yaw)
        mouse_dx, mouse_dy = pygame.mouse.get_rel()
        yaw_rate = mouse_dx * YAW_SENSITIVITY

        # Send to Drone
        await drone.offboard.set_velocity_body(
            VelocityBodyYawspeed(fwd_speed, right_speed, up_speed, yaw_rate)
        )
        
        # Update Display (Just to keep window alive)
        pygame.display.flip()
        await asyncio.sleep(0.05) # 20Hz update rate

    # 5. Cleanup
    print("--> Stopping...")
    try:
        await drone.offboard.stop()
        await drone.action.land()
    except:
        pass
    
    pygame.quit()

if __name__ == "__main__":
    asyncio.run(run())