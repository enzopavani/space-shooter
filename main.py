import pygame
from os.path import join
from random import randint

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
displaySurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
running = True
gameFPS = 120

playerSurface = pygame.image.load(join("spaceShooterResources", "images", "player.png")).convert_alpha()
playerPosition = pygame.Vector2(displaySurface.get_width() / 2, displaySurface.get_height() / 2)
playerRect = playerSurface.get_frect(center=playerPosition)
playerDirection = pygame.Vector2()
playerSpeed = 300

starSurface = pygame.image.load(join("spaceShooterResources", "images", "star.png")).convert_alpha()
starPositions = [pygame.Vector2(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)) for _ in range(20)]

meteorSurface = pygame.image.load(join("spaceShooterResources", "images", "meteor.png")).convert_alpha()
meteorPosition = pygame.Vector2(displaySurface.get_width() / 2, displaySurface.get_height() / 2)
meteorRect = meteorSurface.get_frect(center=meteorPosition)

laserSurface = pygame.image.load(join("spaceShooterResources", "images", "laser.png")).convert_alpha()
laserPosition = pygame.Vector2(20 , displaySurface.get_height() - 20)
laserRect = laserSurface.get_frect(bottomleft=laserPosition)

while running:
    dt = clock.tick(gameFPS) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        # Mouse Movement
        # if event.type == pygame.MOUSEMOTION:
        #   playerRect.center = event.pos

    keys = pygame.key.get_pressed()
    recentKeys = pygame.key.get_just_pressed()
    # keys[] returns boolean, 1 true, 0 false
    playerDirection.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
    playerDirection.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
    # if playerDirection is not (0, 0) normalize the vector
    playerDirection = playerDirection.normalize() if playerDirection else playerDirection
    if recentKeys[pygame.K_SPACE]:
        print("Fire laser!")

    playerRect.center += playerDirection * playerSpeed * dt

    displaySurface.fill('lightblue')
    for position in starPositions:
        displaySurface.blit(starSurface, position)
    displaySurface.blit(meteorSurface, meteorRect)
    displaySurface.blit(laserSurface, laserRect)
    
    displaySurface.blit(playerSurface, playerRect)
    
    pygame.display.flip()

pygame.quit()