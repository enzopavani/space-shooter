import pygame

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_suface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
running = True
dt = 0

playerPos = pygame.Vector2(display_suface.get_width() / 2, display_suface.get_height() / 2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_suface.fill((0, 0, 0))

    pygame.draw.circle(display_suface, (255, 0, 0), playerPos, 40)

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