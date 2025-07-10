import pygame
import random

# Inicialización de Pygame
pygame.init()

# Dimensiones de la pantalla
ancho_pantalla = 0  # Se ajustará automáticamente
alto_pantalla = 0
pantalla = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# Obtener dimensiones reales de la pantalla
info = pygame.display.Info()
ancho_pantalla = info.current_w
alto_pantalla = info.current_h

# Título de la ventana
pygame.display.set_caption("Mi Primer Juego con Pygame")

# Colores (formato RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)

# Reloj para controlar los FPS
reloj = pygame.time.Clock()

# Propiedades del jugador
jugador_pos_x = 370
jugador_pos_y = 480
jugador_ancho = 50
jugador_alto = 50
jugador_velocidad = 5

# Lista de disparos
# Cada bala será [x, y, dx, dy]
balas = []
bala_ancho = 5
bala_alto = 15
bala_velocidad = 10

# Munición inicial
balas_disponibles = 40  # Más balas al inicio

# Power-up de balas (ahora aparece como el de vida)
bala_powerup_color = (150, 150, 150)
bala_powerup_ancho = 30
bala_powerup_alto = 30
bala_powerup_x = random.randint(0, ancho_pantalla - bala_powerup_ancho)
bala_powerup_y = random.randint(0, alto_pantalla - bala_powerup_alto)
bala_powerup_visible = False
bala_powerup_timer = 0
bala_powerup_intervalo = 1200  # Igual que vida

# Crear lista de enemigos (vacía al inicio)
enemigos = []

# Tiempo de espera antes de que aparezcan los enemigos (en frames)
ticks_espera_enemigos = 180  # 3 segundos a 60 FPS
contador_espera = 0

# Propiedades del enemigo
# Ahora usaremos una lista de enemigos para poder expandir fácilmente
class Enemigo:
    def __init__(self):
        self.ancho = 50
        self.alto = 50
        self.reset()
        self.vida = 2  # Ahora necesitan dos disparos
    def reset(self):
        # Aparece fuera de la pantalla
        borde = random.choice(['arriba', 'abajo', 'izquierda', 'derecha'])
        if borde == 'arriba':
            self.x = random.randint(0, ancho_pantalla - self.ancho)
            self.y = -self.alto
        elif borde == 'abajo':
            self.x = random.randint(0, ancho_pantalla - self.ancho)
            self.y = alto_pantalla
        elif borde == 'izquierda':
            self.x = -self.ancho
            self.y = random.randint(0, alto_pantalla - self.alto)
        else:
            self.x = ancho_pantalla
            self.y = random.randint(0, alto_pantalla - self.alto)
        self.velocidad = 2.5  # Más rápido
        self.vida = 2
    def mover_hacia_jugador(self, jugador_x, jugador_y):
        dx = jugador_x - self.x
        dy = jugador_y - self.y
        distancia = max(1, (dx**2 + dy**2) ** 0.5)
        self.x += self.velocidad * dx / distancia
        self.y += self.velocidad * dy / distancia
    def rect(self):
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)

# Vidas del jugador
vidas = 3

# Puntaje
puntaje = 0

# Fuente para mostrar el puntaje
fuente = pygame.font.SysFont(None, 36)

# Power-up de velocidad
powerup_activo = False
powerup_duracion = 180  # frames (~3 segundos a 60 FPS)
powerup_timer = 0
powerup_color = (0, 255, 0)
powerup_ancho = 30
powerup_alto = 30
powerup_x = random.randint(0, ancho_pantalla - powerup_ancho)
powerup_y = random.randint(0, alto_pantalla - powerup_alto)
powerup_visible = True

# Power-up de vida
vida_color = (255, 0, 255)
vida_ancho = 30
vida_alto = 30
vida_x = random.randint(0, ancho_pantalla - vida_ancho)
vida_y = random.randint(0, alto_pantalla - vida_alto)
vida_visible = False
vida_timer = 0
vida_intervalo = 1200  # frames (~20 segundos a 60 FPS)

# Sonido de disparo
pygame.mixer.init()
try:
    sonido_disparo = pygame.mixer.Sound('disparo.wav')
except:
    sonido_disparo = None  # Si no existe el archivo, no suena

# Contador para ataque especial
eliminados_para_especial = 0
especial_disponible = False

# Bucle principal del juego
ejecutando = True
while ejecutando:
    # Manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        # Disparar bala con WASD
        if evento.type == pygame.KEYDOWN:
            if evento.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]:
                if balas_disponibles > 0:
                    if evento.key == pygame.K_w:
                        balas.append([jugador_pos_x + jugador_ancho // 2 - bala_ancho // 2, jugador_pos_y, 0, -bala_velocidad])
                    if evento.key == pygame.K_s:
                        balas.append([jugador_pos_x + jugador_ancho // 2 - bala_ancho // 2, jugador_pos_y + jugador_alto, 0, bala_velocidad])
                    if evento.key == pygame.K_a:
                        balas.append([jugador_pos_x, jugador_pos_y + jugador_alto // 2 - bala_ancho // 2, -bala_velocidad, 0])
                    if evento.key == pygame.K_d:
                        balas.append([jugador_pos_x + jugador_ancho, jugador_pos_y + jugador_alto // 2 - bala_ancho // 2, bala_velocidad, 0])
                    balas_disponibles -= 1
                    if sonido_disparo: sonido_disparo.play()
            # Ataque especial con E
            if evento.key == pygame.K_e and especial_disponible:
                centro_x = jugador_pos_x + jugador_ancho // 2 - bala_ancho // 2
                centro_y = jugador_pos_y + jugador_alto // 2 - bala_ancho // 2
                direcciones = [
                    (0, -bala_velocidad), (0, bala_velocidad),
                    (-bala_velocidad, 0), (bala_velocidad, 0),
                    (-bala_velocidad, -bala_velocidad), (bala_velocidad, -bala_velocidad),
                    (-bala_velocidad, bala_velocidad), (bala_velocidad, bala_velocidad)
                ]
                if balas_disponibles >= 8:
                    for dx, dy in direcciones:
                        balas.append([centro_x, centro_y, dx, dy])
                        if sonido_disparo: sonido_disparo.play()
                    balas_disponibles -= 8
                    especial_disponible = False
                    eliminados_para_especial = 0

    # Espera antes de que aparezcan los enemigos
    if contador_espera < ticks_espera_enemigos:
        contador_espera += 1
        # Dibujar pantalla y power-up si está visible
        pantalla.fill(NEGRO)
        pygame.draw.rect(pantalla, AZUL, (jugador_pos_x, jugador_pos_y, jugador_ancho, jugador_alto))
        if powerup_visible:
            pygame.draw.rect(pantalla, powerup_color, (powerup_x, powerup_y, powerup_ancho, powerup_alto))
        texto_espera = fuente.render("Prepárate...", True, BLANCO)
        pantalla.blit(texto_espera, (ancho_pantalla//2 - 80, alto_pantalla//2 - 20))
        pygame.display.update()
        reloj.tick(60)
        continue
    # Cuando termina la espera, crear los enemigos si aún no existen
    if not enemigos:
        enemigos.extend([Enemigo() for _ in range(6)])  # Más enemigos

    # Captura de teclas presionadas
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and jugador_pos_x > 0:
        jugador_pos_x -= jugador_velocidad
    if teclas[pygame.K_RIGHT] and jugador_pos_x < ancho_pantalla - jugador_ancho:
        jugador_pos_x += jugador_velocidad
    if teclas[pygame.K_UP] and jugador_pos_y > 0:
        jugador_pos_y -= jugador_velocidad
    if teclas[pygame.K_DOWN] and jugador_pos_y < alto_pantalla - jugador_alto:
        jugador_pos_y += jugador_velocidad

    # Lógica del juego
    # Mover enemigos hacia el jugador
    for enemigo in enemigos:
        enemigo.mover_hacia_jugador(jugador_pos_x, jugador_pos_y)

    # Mover balas
    for bala in balas:
        bala[0] += bala[2]
        bala[1] += bala[3]
    # Eliminar balas fuera de pantalla
    balas = [bala for bala in balas if 0 <= bala[0] <= ancho_pantalla and 0 <= bala[1] <= alto_pantalla]

    # Detección de colisiones
    jugador_rect = pygame.Rect(jugador_pos_x, jugador_pos_y, jugador_ancho, jugador_alto)
    for enemigo in enemigos:
        if jugador_rect.colliderect(enemigo.rect()):
            vidas -= 1
            enemigo.reset()
            if vidas <= 0:
                ejecutando = False

    # Colisión bala-enemigo
    for bala in balas[:]:
        if bala[2] == 0:
            rect_bala = pygame.Rect(bala[0], bala[1], bala_ancho, bala_alto)
        else:
            rect_bala = pygame.Rect(bala[0], bala[1], bala_alto, bala_ancho)
        for enemigo in enemigos:
            if rect_bala.colliderect(enemigo.rect()):
                enemigo.vida -= 1
                if enemigo.vida <= 0:
                    puntaje += 1
                    enemigo.reset()
                    eliminados_para_especial += 1
                    if eliminados_para_especial >= 10:
                        especial_disponible = True
                balas.remove(bala)
                break

    # Power-up de velocidad: si está visible y el jugador lo toma
    if powerup_visible:
        powerup_rect = pygame.Rect(powerup_x, powerup_y, powerup_ancho, powerup_alto)
        jugador_rect = pygame.Rect(jugador_pos_x, jugador_pos_y, jugador_ancho, jugador_alto)
        if jugador_rect.colliderect(powerup_rect):
            powerup_activo = True
            powerup_timer = powerup_duracion
            powerup_visible = False
            jugador_velocidad = 10
    # Si el power-up de velocidad está activo, cuenta regresiva
    if powerup_activo:
        powerup_timer -= 1
        if powerup_timer <= 0:
            powerup_activo = False
            jugador_velocidad = 5
            # Aparece un nuevo power-up de velocidad
            powerup_x = random.randint(0, ancho_pantalla - powerup_ancho)
            powerup_y = random.randint(0, alto_pantalla - powerup_alto)
            powerup_visible = True

    # Power-up de vida: aparece cada cierto tiempo
    if not vida_visible:
        vida_timer += 1
        if vida_timer >= vida_intervalo:
            vida_x = random.randint(0, ancho_pantalla - vida_ancho)
            vida_y = random.randint(0, alto_pantalla - vida_alto)
            vida_visible = True
            vida_timer = 0
    if vida_visible:
        vida_rect = pygame.Rect(vida_x, vida_y, vida_ancho, vida_alto)
        jugador_rect = pygame.Rect(jugador_pos_x, jugador_pos_y, jugador_ancho, jugador_alto)
        if jugador_rect.colliderect(vida_rect):
            vidas += 1
            vida_visible = False

    # Power-up de balas: aparece cada cierto tiempo
    if not bala_powerup_visible:
        bala_powerup_timer += 1
        if bala_powerup_timer >= bala_powerup_intervalo:
            bala_powerup_x = random.randint(0, ancho_pantalla - bala_powerup_ancho)
            bala_powerup_y = random.randint(0, alto_pantalla - bala_powerup_alto)
            bala_powerup_visible = True
            bala_powerup_timer = 0
    if bala_powerup_visible:
        powerup_rect = pygame.Rect(bala_powerup_x, bala_powerup_y, bala_powerup_ancho, bala_powerup_alto)
        jugador_rect = pygame.Rect(jugador_pos_x, jugador_pos_y, jugador_ancho, jugador_alto)
        if jugador_rect.colliderect(powerup_rect):
            balas_disponibles += 10
            bala_powerup_visible = False

    # Dibujar en la pantalla
    pantalla.fill(NEGRO)  # Fondo negro
    pygame.draw.rect(pantalla, AZUL, (jugador_pos_x, jugador_pos_y, jugador_ancho, jugador_alto))
    for enemigo in enemigos:
        pygame.draw.rect(pantalla, ROJO, (enemigo.x, enemigo.y, enemigo.ancho, enemigo.alto))
    # Dibujar balas
    for bala in balas:
        if bala[2] == 0:  # vertical
            pygame.draw.rect(pantalla, BLANCO, (bala[0], bala[1], bala_ancho, bala_alto))
        else:  # horizontal
            pygame.draw.rect(pantalla, BLANCO, (bala[0], bala[1], bala_alto, bala_ancho))
    # Dibujar power-up de velocidad si está visible
    if powerup_visible:
        pygame.draw.rect(pantalla, powerup_color, (powerup_x, powerup_y, powerup_ancho, powerup_alto))
    # Dibujar power-up de vida si está visible
    if vida_visible:
        pygame.draw.rect(pantalla, vida_color, (vida_x, vida_y, vida_ancho, vida_alto))
    # Dibujar power-up de balas si está visible
    if bala_powerup_visible:
        pygame.draw.rect(pantalla, bala_powerup_color, (bala_powerup_x, bala_powerup_y, bala_powerup_ancho, bala_powerup_alto))
    # Mostrar puntaje y vidas
    texto_puntaje = fuente.render(f"Puntaje: {puntaje}", True, BLANCO)
    pantalla.blit(texto_puntaje, (10, 10))
    texto_vidas = fuente.render(f"Vidas: {vidas}", True, BLANCO)
    pantalla.blit(texto_vidas, (10, 50))
    # Mostrar si el especial está disponible
    if especial_disponible:
        texto_especial = fuente.render("Especial listo: E", True, (0,255,255))
        pantalla.blit(texto_especial, (ancho_pantalla-250, 10))
    # Mostrar munición
    texto_municion = fuente.render(f"Balas: {balas_disponibles}", True, (200,200,200))
    pantalla.blit(texto_municion, (10, 90))

    # Actualizar la pantalla
    pygame.display.update()

    # Controlar los FPS
    reloj.tick(60)

# Finalizar Pygame
pygame.quit()
