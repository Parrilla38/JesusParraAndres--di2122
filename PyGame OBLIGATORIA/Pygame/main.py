# Import the pygame module
import pygame
import random
import os
import pygame.constants
import time

carpeta = os.path.dirname(__file__)
# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    RLEACCEL
)



# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# Initialize pygame
pygame.mixer.init()
pygame.init()

# Load and play background music
pygame.mixer.music.load(os.path.join(carpeta,"resources/Apoxode_-_Electric_1.wav"))
pygame.mixer.music.play(loops=-1)
# Load all sound files
# Sound sources: Jon Fincher
move_up_sound = pygame.mixer.Sound(os.path.join(carpeta, "resources/Rising_putter.wav"))
move_down_sound = pygame.mixer.Sound(os.path.join(carpeta, "resources/Falling_putter.wav"))
collision_sound = pygame.mixer.Sound(os.path.join(carpeta, "resources/Collision.wav"))
# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        jet = os.path.join(carpeta, "resources/jet.png")
        self.surf = pygame.image.load(jet).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

        



    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


# The surface you draw on the screen is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        missile = os.path.join(carpeta, "resources/missile.png")
        self.surf = pygame.image.load(missile).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)
    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
           self.kill()


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        cloud = os.path.join(carpeta, "resources/cloud.png")
        self.surf = pygame.image.load(cloud).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = 5
    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
           self.kill()


## CREACION DE VENTANA
pantalla = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

ROJO = (255, 45, 0)
consolas = pygame.font.match_font('consolas')

def muestra_texto(pantalla, fuente, texto, color, dimensiones, x, y):
    
    tipo_letra = pygame.font.Font(fuente, dimensiones)
    superficie = tipo_letra.render(texto, True, color)
    rectangulo = superficie.get_rect()
    rectangulo.center = (x, y)
    pantalla.blit(superficie, rectangulo)
    

## SISTEMA DE PUNTUACIONES
puntuacion = 0

# GRUPOS DE SPRITES
sprites = pygame.sprite.Group()
enemigos = pygame.sprite.Group()

# INSTANCIA DE ENEMIGOS

enemigo1 = Enemy()
enemigos.add(enemigo1)

# INSTANCIA JUGADOR PRINCIPAL

jugador = Player()
sprites.add(jugador)

# COLISIONES




# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

# Instancia para evento de cloud

ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)
# Instantiate player. Right now, this is just a rectangle.
player = Player()


# Instantiate player. Right now, this is just a rectangle.
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Variable to keep the main loop running
running = True
clock = pygame.time.Clock()

# Main loop
while running:
# Look at every event in the queue
    for event in pygame.event.get():
# Did the user hit a key?
        if event.type == KEYDOWN:
# Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False
# Did the user click the window close button? If so, stop the loop
        elif event.type == QUIT:
            running = False

        # Add a new enemy?
        elif event.type == ADDENEMY:
        # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

            if new_enemy.rect.right < 0:
                puntuacion += 1

        # Add clouds

        elif event.type == ADDCLOUD:

            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)


        


        # Get all the keys currently pressed
    pressed_keys = pygame.key.get_pressed()
    # Update the player sprite based on user keypresses
    player.update(pressed_keys)

    # Update enemy position
    
    enemies.update()
    
    clouds.update() 
    # Fill the screen with black
    screen.fill((135, 206, 250))
    # Draw all sprites
    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
    # If so, then remove the player and stop the loop
        collision_sound.play()
        time.sleep(2)
        player.kill()        
        running = False

    for e in enemies:

        if (e.rect.right < 0):
            puntuacion += 1
    
    
    
    # MARCADOR PARTE 2

     # muestra_texto(pantalla, consolas, str(puntuacion), ROJO, 40, 400, 50)

    # Flip everything to the display
    pygame.display.flip()
    # Ensure program maintains a rate of 30 frames per second
    clock.tick(60)  

pygame.mixer.music.stop()
pygame.mixer.quit()