import pygame
from os.path import join
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.image.load(join("spaceShooterResources", "images", "player.png")).convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.Vector2()
        self.speed = 500
    
    def update(self, dt):
        keys = pygame.key.get_pressed()
        recentKeys = pygame.key.get_just_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a]) 
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w]) 
        self.direction = self.direction.normalize() if self.direction else self.direction
        if recentKeys[pygame.K_SPACE]:
            print("Fire laser!")
        self.rect.center += self.speed * self.direction * dt

class Star(pygame.sprite.Sprite):
    def __init__(self, group, surface):
        super().__init__(group)
        self.image = surface
        self.rect = self.image.get_frect(center=pygame.Vector2(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
displaySurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
running = True
gameFPS = 120

starSurface = pygame.image.load(join("spaceShooterResources", "images", "star.png")).convert_alpha()

meteorSurface = pygame.image.load(join("spaceShooterResources", "images", "meteor.png")).convert_alpha()
meteorPosition = pygame.Vector2(displaySurface.get_width() / 2, displaySurface.get_height() / 2)
meteorRect = meteorSurface.get_frect(center=meteorPosition)

laserSurface = pygame.image.load(join("spaceShooterResources", "images", "laser.png")).convert_alpha()
laserPosition = pygame.Vector2(20 , displaySurface.get_height() - 20)
laserRect = laserSurface.get_frect(bottomleft=laserPosition)

allSprites = pygame.sprite.Group()
for _ in range(20):
    Star(allSprites, starSurface)
player = Player(allSprites)

while running:
    dt = clock.tick(gameFPS) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    
    allSprites.update(dt)

    displaySurface.fill('lightblue')
    allSprites.draw(displaySurface)

    pygame.display.flip()

pygame.quit()