import pygame

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
displaySurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
running = True
dt = 0

# plain surface
surface = pygame.Surface((100, 200))
surface.fill('blue')
x = 100

# importing an image
playerSurface = pygame.image.load("pygames/game0/space shooter/images/player.png")

playerPosition = pygame.Vector2(displaySurface.get_width() / 2, displaySurface.get_height() / 2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    displaySurface.fill('darkgrey')
    # blit() puts surface on another surface
    x += 1
    displaySurface.blit(playerSurface, (x, 150))

    pygame.draw.circle(displaySurface, (255, 0, 0), playerPosition, 40)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        playerPosition.y -= 300 * dt
    if keys[pygame.K_a]:
        playerPosition.x -= 300 * dt
    if keys[pygame.K_s]:
        playerPosition.y += 300 * dt
    if keys[pygame.K_d]:
        playerPosition.x += 300 * dt
    
    if keys[pygame.K_ESCAPE]:
        running = False
    
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()