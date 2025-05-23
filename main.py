import pygame
from os.path import join
from random import randint, uniform
import csv

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

        self.mask = pygame.mask.from_surface(self.image)

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
            laserSound.play()
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
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.rect.centery -= self.speed * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, group, surface, position):
        super().__init__(group)
        self.originalSurface = surface
        self.image = self.originalSurface
        self.rect = self.image.get_frect(center=position)
        self.direction = pygame.Vector2((uniform(-0.5, 0.5), 1))
        self.speed = randint(600, 700)
        self.birthTime = pygame.time.get_ticks()
        self.lifeTime = 2000
        self.mask = pygame.mask.from_surface(self.image)
        self.rotationSpeed = randint(30, 100)
        self.rotation = 0

    def update(self, dt):
        self.rect.center += self.speed * self.direction * dt
        if pygame.time.get_ticks() - self.birthTime > self.lifeTime:
            self.kill()
        self.rotation += self.rotationSpeed * dt
        self.image = pygame.transform.rotozoom(self.originalSurface, self.rotation, 1)
        self.rect = self.image.get_frect(center=self.rect.center)

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, group, frames, position):
        super().__init__(group)
        self.frames = frames
        self.frameIndex = 0
        self.image = self.frames[self.frameIndex]
        self.rect = self.image.get_frect(center=position)
        self.speed = 20
        explosionSound.play()

    def update(self, dt):
        self.frameIndex += self.speed * dt
        if self.frameIndex < len(self.frames):
            self.image = self.frames[int(self.frameIndex) % len(self.frames)]
        else:
            self.kill()

class User():
    def __init__(self, surface, rect):
        self.surface = surface
        self.rect = rect

def collisions():
    global pause
    if pygame.sprite.spritecollide(player, meteorSprites, True, pygame.sprite.collide_mask):
        player.kill()
        pause = True
    for laser in laserSprites:
        if pygame.sprite.spritecollide(laser, meteorSprites, True):
            laser.kill()
            AnimatedExplosion(allSprites, explosionFrames, laser.rect.midtop)

def displayScore():
    score = pygame.time.get_ticks() // 20
    textSurface = font.render(str(score), True, "#c8c8c8")
    textRect = textSurface.get_frect(midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
    pygame.draw.rect(displaySurface, "#fafafa", textRect.inflate(20, 10).move(0, -8), 5, 10)
    displaySurface.blit(textSurface, textRect)

def gameOver():
    global running
    gameOverSurface = font.render("GAME OVER!", True, "#ff0000")
    gameOverRect = gameOverSurface.get_frect(center=(WINDOW_WIDTH / 2, 150))
    pygame.draw.rect(displaySurface, "#ffffff", gameOverRect.inflate(200, 450).move(0, 180), 3, 10)
    displaySurface.blit(gameOverSurface, gameOverRect)
    printLeaderboard()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

def printLeaderboard():
    leaderboardSurface = font.render("LEADERBOARD:", True, "#ff0000")
    leaderboardRect = leaderboardSurface.get_frect(center=(WINDOW_WIDTH / 2, 240))
    displaySurface.blit(leaderboardSurface, leaderboardRect)
    with open(join("leaderboard.csv"), newline="") as leaderboardFile:
        reader = csv.reader(leaderboardFile)
        i = 0
        leaderboardMargin = 0
        for data in reader:
            leaderboardMargin += 30
            userSurface = smallerFont.render(f"#{i + 1}. {data[0]} - {data[1]}", True, "#ffffff")
            userRect = userSurface.get_frect(center=(WINDOW_WIDTH / 2, 250 + leaderboardMargin))
            i += 1
            displaySurface.blit(userSurface, userRect)
        
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
displaySurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
running = True
pause = False
gameFPS = 60

starSurface = pygame.image.load(join("spaceShooterResources", "images", "star.png")).convert_alpha()
meteorSurface = pygame.image.load(join("spaceShooterResources", "images", "meteor.png")).convert_alpha()
laserSurface = pygame.image.load(join("spaceShooterResources", "images", "laser.png")).convert_alpha()
font = pygame.font.Font(join("spaceShooterResources", "images", "Oxanium-Bold.ttf"), 40)
smallerFont = pygame.font.Font(join("spaceShooterResources", "images", "Oxanium-Bold.ttf"), 25)
explosionFrames = [pygame.image.load(join("spaceShooterResources", "images", "explosion", f"{i}.png")).convert_alpha() for i in range(21)]

laserSound = pygame.mixer.Sound(join("spaceShooterResources", "audio", "laser.wav"))
laserSound.set_volume(0.2)
explosionSound = pygame.mixer.Sound(join("spaceShooterResources", "audio", "explosion.wav"))
explosionSound.set_volume(0.2)
gameMusic = pygame.mixer.Sound(join("spaceShooterResources", "audio", "game_music.wav"))
gameMusic.set_volume(0.2)
gameMusic.play(loops=-1)

allSprites = pygame.sprite.Group()
meteorSprites = pygame.sprite.Group()
laserSprites = pygame.sprite.Group()
for _ in range(20):
    Star(allSprites, starSurface)
player = Player(allSprites)

meteorEvent = pygame.event.custom_type()
pygame.time.set_timer(meteorEvent, 500)

while running:
    while not pause:
        dt = clock.tick(gameFPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == meteorEvent:
                Meteor((allSprites, meteorSprites), meteorSurface, (randint(0, WINDOW_WIDTH), randint(-150, -50)))
        
        allSprites.update(dt)
        collisions()

        displaySurface.fill("#3e005a")
        allSprites.draw(displaySurface)
        displayScore()

        pygame.display.flip()

    gameOver()
    pygame.display.flip()

pygame.quit()