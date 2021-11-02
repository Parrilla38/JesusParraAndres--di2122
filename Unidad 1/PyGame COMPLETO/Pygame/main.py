# Importamos los modulos del pygame y los necesarios para el programa
import pygame
import random
import os
import pygame.constants
import time
from pygame.constants import  RLEACCEL, K_p
import sqlite3

carpeta = os.path.dirname(__file__) # Variable que usaremos para acceder a la carpeta
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



# ------------------------------ VARIABLES ------------------------------ #
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
color = (135, 206, 250)
ROJO = (255, 45, 0)
BLANCO = (255,255,255)
NEGRO = (0,0,0)
VERDE = (41, 218, 65)
consolas = pygame.font.match_font('consolas')


# Iniciamos el juego
pygame.mixer.init()
pygame.init()

# Carga del fondo y de la musica
pygame.mixer.music.load(os.path.join(carpeta,"resources/Apoxode_-_Electric_1.wav"))
pygame.mixer.music.play(loops=-1)


# Carga de archivos de musica
move_up_sound = pygame.mixer.Sound(os.path.join(carpeta, "resources/Rising_putter.wav"))
move_down_sound = pygame.mixer.Sound(os.path.join(carpeta, "resources/Falling_putter.wav"))
collision_sound = pygame.mixer.Sound(os.path.join(carpeta, "resources/Collision.wav"))


# Creamos el objeto screen para la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# ------------------------------ SISTEMA DE EXPLOSIONES ------------------------------ # [BETA]
explosion_anim = []
for i in range(9):
	file = (os.path.join(carpeta, "resources/regularExplosion0{}.png".format(i)))
	img = pygame.image.load(file).convert()
	img.set_colorkey(NEGRO)
	img_scale = pygame.transform.scale(img, (70, 70))
	explosion_anim.append(img_scale)




# ------------------------------ SISTEMA DE NIVELES ------------------------------ #

nivel = 1
nivel_antiguo = 1


# ------------------------------ SISTEMA DE NIVELES 2 ------------------------------ #

vel_desp_enemigos = 500
vel_crea_enemigos = 250

# ------------------------------ SISTEMA DE BASE DE DATOS ------------------------------ #

def crear_conexion(base_datos):
    
    try:
        conexion = sqlite3.connect(base_datos)

        return conexion

    except sqlite3.Error as error:
        print('Se ha producido un error al crear la conexión: ', error)


def crear_tabla(conexion, definicion):

    cursor = conexion.cursor()
    cursor.execute(definicion)
    conexion.commit()

def insertar_puntuacion(conexion):

    sql = 'INSERT INTO puntuacion (puntos) VALUES (' + str(puntuacion) + ')'

    cursor = conexion.cursor()
    cursor.execute(sql)

    conexion.commit()

def actualizar_puntos(conexion):

    sql = "UPDATE puntuacion SET puntos = '%s';" %(puntuacion) 

def recuperar_puntuacion(conexion):

    sql = "SELECT MAX(puntos) FROM puntuacion;"

    cursor = conexion.cursor()
    cursor.execute(sql)

    puntuacion = cursor.fetchall()

    return puntuacion

def comprobar_tabla(conexion):

    sql = "SELECT count(*) FROM puntuacion";

    cursor = conexion.cursor()
    cursor.execute(sql)

    vacio = cursor.fetchall()

    return vacio

# Conexion a la base de datos
conexion = crear_conexion((os.path.join(carpeta,"resources/puntuaciones.db")))

# Creamos la tabla puntuacion
sql = """
CREATE TABLE if not exists puntuacion(
    puntos INTEGER NOT NULL
);
"""


crear_tabla(conexion, sql)

# Funcion para comprobar si el numero es multiplico de X

def es_multiplo(numero, multiplo):
    # Si el residuo es 0, es múltiplo

    if numero != 0:
        if numero % multiplo == 0:
            return True
            
        else:
            return False

# Funcion para el escudo del jugador

def draw_shield_bar(surface, x, y, porcentaje):
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (porcentaje / 100) * BAR_LENGTH
    border = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, VERDE, fill)
    pygame.draw.rect(surface, BLANCO, border, 2)

# Creacion de la clase jugador (nave principal)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        jet = os.path.join(carpeta, "resources/jet.png")
        self.surf = pygame.image.load(jet).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(

            center = (100, 300)

        )
        self.shield = 100

        



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


# Creacion de la clase Enemy (misiles enemigos)
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        if nivel < 4:
            missile = os.path.join(carpeta, "resources/missile.png")
        elif nivel >= 4:
            missile = os.path.join(carpeta, "resources/meteorGrey_small1.png")
        self.surf = pygame.image.load(missile).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(2 * nivel, 10 + 3 * nivel)   
        

    
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0: # Si pasa del borde izquierdo , se destruye el misil
           self.kill()

        

# Creacion de la clase Cloud (Nubes decorativas)
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        if nivel < 4:
            cloud = os.path.join(carpeta, "resources/cloud.png")
        elif nivel >= 4:
            cloud = os.path.join(carpeta, "resources/regularExplosion03.png")
        self.surf = pygame.image.load(cloud).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = 5
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:# Si pasa del borde izquierdo , se destruye la nube
           self.kill()

# Definimos la clase para las explosiones
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50 # Velocidad de la explosión

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim):
                self.kill() 
            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


# ------------------------------ PANTALLA DE INICIO ------------------------------ #

# Variable para el bucle de la pantalla de inicio
running_inicio = True


# Bucle para la pantalla de inicio

while running_inicio:

    screen.fill(BLANCO)

    fuente_menu = pygame.font.Font(os.path.join(carpeta, "resources/fast99.ttf"), 32)
    texto_menu = fuente_menu.render("BIENVENIDO AL JUEGO DE PYGAME", True, ROJO)
    screen.blit(texto_menu, (120, 90))

    cohete = pygame.image.load((os.path.join(carpeta, "resources/jet.png")))
    screen.blit(cohete, (69 ,288))

    texto_inicio = fuente_menu.render("Pulsa la tecla P para iniciar el juego", True, ROJO)
    screen.blit(texto_inicio, (110, 490))

    pygame.display.flip()

    for event in pygame.event.get():

        if event.type == KEYDOWN:

            if event.key == K_p:

                running_inicio = False


        elif event.type == QUIT:

            running_inicio = False


# Creacion de ventana
pantalla = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))


# Funcion para mostrar texto por pantalla
def muestra_texto(pantalla, fuente, texto, color, dimensiones, x, y):
    
    tipo_letra = pygame.font.Font(fuente, dimensiones)
    superficie = tipo_letra.render(texto, True, color)
    rectangulo = superficie.get_rect()
    rectangulo.center = (x, y)
    pantalla.blit(superficie, rectangulo)

# Sistema de Puntuaciones
puntuacion = 0
nuevapuntuacion = 0

# Grupos de Sprites
sprites = pygame.sprite.Group()
enemigos = pygame.sprite.Group()

# Creacion de la Instancia del Enemigo
enemigo1 = Enemy()
enemigos.add(enemigo1)

# Instancia para el Jugador Principal
jugador = Player()
sprites.add(jugador)


# Creamos un evento para añadir los enemigos
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, vel_crea_enemigos)

# Creamos un evento para añadir las nubes
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# Iniciamos la clase Player
player = Player()

# Creamos un evento para añadir el fondo en negro cada 20 segundos
ADDNIGHT = pygame.USEREVENT + 3
pygame.time.set_timer(ADDNIGHT, 20000)

# Creamos un evento para añadir el fondo en negro cada 40 segundos
ADDDAY = pygame.USEREVENT + 4
pygame.time.set_timer(ADDDAY, 40000)


# Iniciamos cada uno de los grupos y añadimos Player a all_sprites
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Creacion de variable para el bucle principal y reloj para el framerate
running = True
clock = pygame.time.Clock()

# Bucle principal del juego
while running:

# Recorremos cada evento del juego
    for event in pygame.event.get():

# Comprobamos si el usuario a pulsado alguna tecla
        if event.type == KEYDOWN:

# Si la tecla pulsada es ESC, sale
            if event.key == K_ESCAPE:
                running = False

# Si el usuario pulsa el boton de cerrar ventana, cierra el juego
        elif event.type == QUIT:
            running = False

        # Si el evento trata de añadir nuevo enemigo, lo añade
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # Si el evento trata de añadir nueva nube, la añade
        elif event.type == ADDCLOUD:

            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)


        # Añadir fondo de noche
        elif event.type == ADDNIGHT:
    
            color = (0,0,0)

        # Añadir fondo de dia
        elif event.type == ADDDAY:
    
            color = (135, 206, 250)

    # Guarda todas las teclas pulsadas en una variable
    pressed_keys = pygame.key.get_pressed()

    # Actualiza el player sprites con todos los botones pulsados
    player.update(pressed_keys)

    # Actualiza la posicion del enemigo y las nubes para ver una animacion de movimiento
    enemies.update()
    clouds.update() 


    # Pintamos el fondo de la pantalla 
    screen.fill(color)

    if nivel >= 4:  

        background = pygame.image.load(os.path.join(carpeta, "resources/background.png"))
        screen.blit(background, (0, 0))
    
    # Dibujamos todos los sprites guardados
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Comprobador de choque entre el jugador y el enemigo
    hits = pygame.sprite.spritecollide(player, enemies, True)

    for hit in hits:
        # explosion = Explosion(hit.rect.center)[EN BETA] 
        ## all_sprites.add(explosion)
        collision_sound.play()

        # Si choca rompe parte del escudo
        player.shield -= 25
        if player.shield <= 0:

            if (comprobar_tabla):
                insertar_puntuacion(conexion)
            else:
                if (recuperar_puntuacion(conexion)) < puntuacion:
                    actualizar_puntos(conexion)

            player.kill()
            running = False



        


    # Bucle para recorrer los enemigos creados
    for e in enemies:

        if (e.rect.right < 10):
            puntuacion += 10
            nuevapuntuacion += 10

    
    if es_multiplo(nuevapuntuacion, 500):
    
        nivel += 1
        nuevapuntuacion = 0
        vel_crea_enemigos = 50 + (200 // nivel) # Funcion para cambiar la velocidad de creacion de enemigos
        pygame.time.set_timer(ADDENEMY, vel_crea_enemigos) # Cambiamos el tiempo de creacion

        


          

        
    
     # ----------- MARCADOR DE PUNTOS ----------- #

    muestra_texto(pantalla, consolas, ("Score: " + str(puntuacion)), ROJO, 30, 100, 40)

    # ----------- MARCADOR DE NIVEL ----------- #

    muestra_texto(pantalla, consolas, ("Nivel: " + str(nivel)), ROJO, 30, 700, 40)

    # ----------- MARCADOR DE ESCUDO ----------- #

    draw_shield_bar(screen, 340, 20, player.shield)

    pygame.display.flip()

    # Definimos un framerate de 60fps
    clock.tick(60)  

pygame.mixer.music.stop() 
pygame.mixer.quit()


# ------------------------------ PANTALLA DE INICIO ------------------------------ #

# Variables
running_final = True


# Bucle para la pantalla final

while running_final:

    screen.fill(BLANCO)
    fuente_menu = pygame.font.Font(os.path.join(carpeta, "resources/fast99.ttf"), 32)

    # Texto para el fin del juego
    game_end = fuente_menu.render("FIN DEL JUEGO", True, ROJO)
    screen.blit(game_end, (280, 90))
  
    # Puntuación obtenida en el juego actual
    score = fuente_menu.render("Tu puntuacion: " + str(puntuacion), True, ROJO)
    screen.blit(score, (260 ,170))


    # Puntuación record de dentro de la base de datos
    score = fuente_menu.render("Puntuacion Record: " + str(recuperar_puntuacion(conexion)[0][0]), True, ROJO)
    screen.blit(score, (220 ,270))

    # Nivel que hemos alcanzado
    texto_inicio = fuente_menu.render("Nivel: " + str(nivel), True, ROJO)
    screen.blit(texto_inicio, (330, 490)) 

    pygame.display.flip()

    for event in pygame.event.get():

        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:

                running_final = False


        elif event.type == QUIT:

            running_final = False