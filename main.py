import pygame
from os.path import join
from random import randint, uniform

class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.image.load(join("spaceShooterResources", "images", "player.png")).convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.Vector2()
        self.speed = 500

        self.canShoot = True
        self.laserShootTime = 0
        self.cooldownDuration = 400

    def laserTimer(self):
        if not self.canShoot:
            currentTime = pygame.time.get_ticks()
            if currentTime - self.laserShootTime >= self.cooldownDuration:
                self.canShoot = True
    
    def update(self, dt):
        keys = pygame.key.get_pressed()
        recentKeys = pygame.key.get_just_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a]) 
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w]) 
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.speed * self.direction * dt
        if recentKeys[pygame.K_SPACE] and self.canShoot:
            Laser((allSprites, laserSprites), laserSurface, self.rect.midtop)
            self.canShoot = False
            self.laserShootTime = pygame.time.get_ticks()
        self.laserTimer()
        
class Star(pygame.sprite.Sprite):
    def __init__(self, group, surface):
        super().__init__(group)
        self.image = surface
        self.rect = self.image.get_frect(center=pygame.Vector2(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, group, surface, position):
        super().__init__(group)
        self.image = surface
        self.rect = self.image.get_frect(midbottom=position)
        self.speed = 500

    def update(self, dt):
        self.rect.centery -= self.speed * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, group, surface, position):
        super().__init__(group)
        self.image = surface
        self.rect = self.image.get_frect(center=position)
        self.direction = pygame.Vector2((uniform(-0.5, 0.5), 1))
        self.speed = randint(600, 700)
        self.birthTime = pygame.time.get_ticks()
        self.lifeTime = 2000

    def update(self, dt):
        self.rect.center += self.speed * self.direction * dt
        if pygame.time.get_ticks() - self.birthTime > self.lifeTime:
            self.kill()

def collisions():
    global running
    if pygame.sprite.spritecollide(player, meteorSprites, True):
        running = False
    for laser in laserSprites:
        if pygame.sprite.spritecollide(laser, meteorSprites, True):
            laser.kill()

def displayScore():
    currentTime = pygame.time.get_ticks() // 20
    textSurface = font.render(str(currentTime), True, (200, 200, 200))
    textRect = textSurface.get_frect(midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
    pygame.draw.rect(displaySurface, (250, 250, 250), textRect.inflate(20, 10).move(0, -8), 5, 10)
    displaySurface.blit(textSurface, textRect)

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
displaySurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
running = True
gameFPS = 60

starSurface = pygame.image.load(join("spaceShooterResources", "images", "star.png")).convert_alpha()
meteorSurface = pygame.image.load(join("spaceShooterResources", "images", "meteor.png")).convert_alpha()
laserSurface = pygame.image.load(join("spaceShooterResources", "images", "laser.png")).convert_alpha()
# dafont.com
font = pygame.font.Font(join("spaceShooterResources", "images", "Oxanium-Bold.ttf"), 40)

allSprites = pygame.sprite.Group()
meteorSprites = pygame.sprite.Group()
laserSprites = pygame.sprite.Group()
for _ in range(20):
    Star(allSprites, starSurface)
player = Player(allSprites)

meteorEvent = pygame.event.custom_type()
pygame.time.set_timer(meteorEvent, 500)

while running:
    dt = clock.tick(gameFPS) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if event.type == meteorEvent:
            Meteor((allSprites, meteorSprites), meteorSurface, (randint(0, WINDOW_WIDTH), randint(-150, -50)))
    
    allSprites.update(dt)
    collisions()

    displaySurface.fill("#3e005a")
    allSprites.draw(displaySurface)
    displayScore()

    pygame.display.flip()

pygame.quit()