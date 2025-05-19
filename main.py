import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

while running:
    # Press X to close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Game rendering

    # Update the display
    pygame.display.flip()
    # Cap the frame rate
    clock.tick(60)

pygame.quit()