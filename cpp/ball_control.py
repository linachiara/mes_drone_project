#!/usr/bin/env python3
import pygame
import subprocess
import time

# --- CONFIGURATION ---
MOVE_SPEED = 0.2  # Meters per keystroke
BALL_NAME = "red_ball"

# Initial Position (Meters)
# We start it 2 meters in front of the drone so the camera sees it immediately
pos_x = 2.0
pos_y = 0.0
pos_z = 1.5

def move_ball_in_gazebo(x, y, z):
    # Construct the command to teleport the model
    # command: gz model -m red_ball -x 2.0 -y 0.0 -z 1.5
    cmd = [
        "gz", "model", 
        "-m", BALL_NAME, 
        "-x", str(round(x, 2)), 
        "-y", str(round(y, 2)), 
        "-z", str(round(z, 2))
    ]
    # Run it silently
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def run():
    global pos_x, pos_y, pos_z
    
    # 1. Init Pygame
    pygame.display.init()
    pygame.font.init()
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("BALL CONTROLLER (The Drone Follows This)")
    
    font = pygame.font.SysFont(None, 24)
    
    # 2. Control Loop
    print(f"--> Controlling '{BALL_NAME}'...")
    print("--> WASD: Move Flat | Space/Shift: Up/Down")
    
    running = True
    clock = pygame.time.Clock()

    while running:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Continuous Key Check
        keys = pygame.key.get_pressed()
        moved = False

        if keys[pygame.K_w]: 
            pos_x += MOVE_SPEED
            moved = True
        if keys[pygame.K_s]: 
            pos_x -= MOVE_SPEED
            moved = True
        if keys[pygame.K_a]: 
            pos_y -= MOVE_SPEED
            moved = True
        if keys[pygame.K_d]: 
            pos_y += MOVE_SPEED
            moved = True
        if keys[pygame.K_SPACE]: 
            pos_z += MOVE_SPEED
            moved = True
        if keys[pygame.K_LSHIFT]: 
            pos_z -= MOVE_SPEED
            moved = True

        # Only send command to Gazebo if we actually moved
        # (Prevents spamming the system)
        if moved:
            move_ball_in_gazebo(pos_x, pos_y, pos_z)
        
        # Render Text
        screen.fill((0, 0, 0))
        img = font.render(f"Ball Pos: X={pos_x:.1f} Y={pos_y:.1f} Z={pos_z:.1f}", True, (255, 50, 50))
        screen.blit(img, (20, 20))
        img2 = font.render("The drone will chase this coordinate.", True, (150, 150, 150))
        screen.blit(img2, (20, 50))
        
        pygame.display.flip()
        clock.tick(30) # 30 FPS

    pygame.quit()

if __name__ == "__main__":
    run()