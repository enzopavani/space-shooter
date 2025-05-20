import pygame
from os.path import join
from random import randint

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
displaySurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
running = True

surface = pygame.Surface((100, 200))
surface.fill('blue')
x = 100

playerSurface = pygame.image.load(join("spaceShooterResources", "images", "player.png")).convert_alpha()
playerPosition = pygame.Vector2(displaySurface.get_width() / 2, displaySurface.get_height() / 2)
playerRect = playerSurface.get_frect(center=playerPosition)
playerHorizontalDirection = 1
playerVerticalDirection = 1
playerSpeed = 1

starSurface = pygame.image.load(join("spaceShooterResources", "images", "star.png")).convert_alpha()
starPositions = [pygame.Vector2(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)) for _ in range(20)]

meteorSurface = pygame.image.load(join("spaceShooterResources", "images", "meteor.png")).convert_alpha()
meteorPosition = pygame.Vector2(displaySurface.get_width() / 2, displaySurface.get_height() / 2)
meteorRect = meteorSurface.get_frect(center=meteorPosition)

laserSurface = pygame.image.load(join("spaceShooterResources", "images", "laser.png")).convert_alpha()
laserPosition = pygame.Vector2(20 , displaySurface.get_height() - 20)
laserRect = laserSurface.get_frect(bottomleft=laserPosition)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    displaySurface.fill('lightblue')
    for position in starPositions:
        displaySurface.blit(starSurface, position)
    displaySurface.blit(meteorSurface, meteorRect)
    displaySurface.blit(laserSurface, laserRect)
    
    playerRect.right += (playerSpeed * playerHorizontalDirection)
    if playerRect.right > WINDOW_WIDTH or playerRect.left < 0:
        playerHorizontalDirection *= -1
    playerRect.bottom += (playerSpeed * playerVerticalDirection)
    if playerRect.bottom > WINDOW_HEIGHT or playerRect.top < 0:
        playerVerticalDirection *= -1
    displaySurface.blit(playerSurface, playerRect)
    
    pygame.display.flip()

pygame.quit()