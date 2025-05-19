import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
# delta time, used for frame rate independent movement
dt = 0

playerPos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    pygame.draw.circle(screen, (255, 0, 0), playerPos, 40)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        playerPos.y -= 300 * dt
    if keys[pygame.K_a]:
        playerPos.x -= 300 * dt
    if keys[pygame.K_s]:
        playerPos.y += 300 * dt
    if keys[pygame.K_d]:
        playerPos.x += 300 * dt
    
    if keys[pygame.K_ESCAPE]:
        running = False
    
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()