"""
=============================================================================
JUEGO ARCADE DE COCHES TOP-DOWN (ESQUIVAR TRÁFICO) EN PYTHON CON PYGAME
=============================================================================

REQUISITOS E INSTALACIÓN:
    1. Asegúrate de tener Python 3 instalado.
    2. Instala la librería pygame mediante el siguiente comando en tu terminal:
           pip install pygame

CÓMO EJECUTAR EL SCRIPT:
    python coches.py
    (o bien: py coches.py)

CONTROLES:
    - Flecha Izquierda (←) o tecla 'A': Mover el coche a la izquierda.
    - Flecha Derecha (→)   o tecla 'D': Mover el coche a la derecha.
    - Flecha Arriba (↑)    o tecla 'W': Acelerar ligeramente.
    - Flecha Abajo (↓)     o tecla 'S': Frenar ligeramente.
    - Tecla 'R':                        Reiniciar la partida tras Game Over.
    - Tecla ESC:                        Salir del juego.

CARACTERÍSTICAS IMPLEMENTADAS:
    - Carretera vertical de 4 carriles con líneas discontinuas animadas (efecto de velocidad).
    - Coche del jugador con diseño detallado (luces, parabrisas, neumáticos y alerón).
    - Generación continua y aleatoria de tráfico con variedad de colores y velocidades.
    - Detección precisa de colisiones mediante rectángulos ajustados.
    - Sistema de puntuación progresivo basado en tiempo de supervivencia y coches esquivados.
    - Aumento progresivo de la dificultad según avanza la partida.
=============================================================================
"""

import sys
import random
import pygame

# ---------------------------------------------------------------------------
# CONSTANTES DE PANTALLA Y CARRETERA
# ---------------------------------------------------------------------------
ANCHO_VENTANA = 600
ALTO_VENTANA = 750
FPS = 60

# Dimensiones de la pista
ANCHO_CARRETERA = 380
BORDE_IZQ_CARRETERA = (ANCHO_VENTANA - ANCHO_CARRETERA) // 2
BORDE_DER_CARRETERA = BORDE_IZQ_CARRETERA + ANCHO_CARRETERA
NUM_CARRILES = 4
ANCHO_CARRIL = ANCHO_CARRETERA // NUM_CARRILES

# Dimensiones de los vehículos
ANCHO_COCHE = 44
ALTO_COCHE = 80

# ---------------------------------------------------------------------------
# PALETA DE COLORES (RGB)
# ---------------------------------------------------------------------------
COLOR_CESPED = (34, 139, 34)
COLOR_ASFALTO = (45, 45, 50)
COLOR_LINEA_LATERAL = (240, 240, 240)
COLOR_LINEA_CARRIL = (255, 215, 0)
COLOR_QUITAMIEDOS = (180, 50, 50)
COLOR_TEXTO = (250, 250, 250)
COLOR_HUD_FONDO = (20, 20, 25, 210)

COLORES_TRAFICO = [
    (220, 50, 50),    # Rojo deportivo
    (50, 100, 230),   # Azul eléctrico
    (240, 180, 20),   # Amarillo taxi
    (220, 220, 225),  # Blanco perla
    (140, 40, 180),   # Morado
    (30, 180, 100),   # Verde esmeralda
]


# ---------------------------------------------------------------------------
# FUNCIÓN AUXILIAR PARA DIBUJAR VEHÍCULOS PROCEDURALMENTE
# ---------------------------------------------------------------------------
def dibujar_coche(superficie, rect, color_carroceria, es_jugador=False):
    """Renderiza un coche top-down con ruedas, lunas, luces y alerón."""
    x, y, w, h = rect.x, rect.y, rect.width, rect.height

    # 1. Neumáticos (4 esquinas)
    color_rueda = (20, 20, 20)
    ancho_r, alto_r = 7, 16
    pygame.draw.rect(superficie, color_rueda, (x - 2, y + 10, ancho_r, alto_r), border_radius=3)
    pygame.draw.rect(superficie, color_rueda, (x + w - 5, y + 10, ancho_r, alto_r), border_radius=3)
    pygame.draw.rect(superficie, color_rueda, (x - 2, y + h - 26, ancho_r, alto_r), border_radius=3)
    pygame.draw.rect(superficie, color_rueda, (x + w - 5, y + h - 26, ancho_r, alto_r), border_radius=3)

    # 2. Carrocería principal con bordes redondeados
    pygame.draw.rect(superficie, color_carroceria, (x, y, w, h), border_radius=10)

    # 3. Parabrisas delantero y trasero
    color_cristal = (50, 70, 95)
    # Luna delantera
    pygame.draw.rect(superficie, color_cristal, (x + 6, y + 18, w - 12, 14), border_radius=3)
    # Luna trasera
    pygame.draw.rect(superficie, color_cristal, (x + 7, y + h - 24, w - 14, 10), border_radius=2)
    # Techo
    color_techo = tuple(max(0, c - 25) for c in color_carroceria)
    pygame.draw.rect(superficie, color_techo, (x + 7, y + 34, w - 14, 20), border_radius=2)

    # 4. Luces delanteras y traseras
    if es_jugador:
        # Luces frontales encendidas (hacia arriba)
        pygame.draw.circle(superficie, (255, 255, 180), (x + 7, y + 4), 4)
        pygame.draw.circle(superficie, (255, 255, 180), (x + w - 7, y + 4), 4)
        # Pilotos traseros rojos
        pygame.draw.rect(superficie, (240, 20, 20), (x + 6, y + h - 3, 8, 3))
        pygame.draw.rect(superficie, (240, 20, 20), (x + w - 14, y + h - 3, 8, 3))
    else:
        # Los coches del tráfico van hacia abajo: faros abajo, pilotos arriba
        pygame.draw.circle(superficie, (255, 255, 180), (x + 7, y + h - 4), 4)
        pygame.draw.circle(superficie, (255, 255, 180), (x + w - 7, y + h - 4), 4)
        pygame.draw.rect(superficie, (240, 20, 20), (x + 6, y, 8, 3))
        pygame.draw.rect(superficie, (240, 20, 20), (x + w - 14, y, 8, 3))


# ---------------------------------------------------------------------------
# CLASE DEL COCHE DEL JUGADOR
# ---------------------------------------------------------------------------
class CocheJugador:
    def __init__(self):
        # Iniciar centrado en la carretera cerca del borde inferior
        self.rect = pygame.Rect(
            ANCHO_VENTANA // 2 - ANCHO_COCHE // 2,
            ALTO_VENTANA - ALTO_COCHE - 40,
            ANCHO_COCHE,
            ALTO_COCHE
        )
        self.color = (30, 200, 240)  # Cian deportivo
        self.velocidad_lateral = 7.0
        self.velocidad_vertical = 4.0

    def update(self, teclas):
        # Desplazamiento lateral (flechas o A / D)
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.rect.x -= int(self.velocidad_lateral)
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.rect.x += int(self.velocidad_lateral)

        # Ajuste de velocidad vertical opcional (W / S o Flechas Arriba / Abajo)
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.rect.y -= int(self.velocidad_vertical)
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.rect.y += int(self.velocidad_vertical)

        # LÍMITES ESTRICTOS DE LA CARRETERA (no salir a los laterales)
        if self.rect.left < BORDE_IZQ_CARRETERA + 6:
            self.rect.left = BORDE_IZQ_CARRETERA + 6
        if self.rect.right > BORDE_DER_CARRETERA - 6:
            self.rect.right = BORDE_DER_CARRETERA - 6

        # Límites verticales para mantenerse en la mitad inferior
        if self.rect.top < ALTO_VENTANA // 2:
            self.rect.top = ALTO_VENTANA // 2
        if self.rect.bottom > ALTO_VENTANA - 15:
            self.rect.bottom = ALTO_VENTANA - 15

    def draw(self, superficie):
        dibujar_coche(superficie, self.rect, self.color, es_jugador=True)


# ---------------------------------------------------------------------------
# CLASE DE VEHÍCULOS DEL TRÁFICO (OBSTÁCULOS)
# ---------------------------------------------------------------------------
class CocheTrafico:
    def __init__(self, carril_indice, velocidad_base):
        # Calcular posición X según el carril
        pos_x = BORDE_IZQ_CARRETERA + (carril_indice * ANCHO_CARRIL) + (ANCHO_CARRIL - ANCHO_COCHE) // 2
        self.rect = pygame.Rect(pos_x, -ALTO_COCHE - random.randint(10, 80), ANCHO_COCHE, ALTO_COCHE)
        self.color = random.choice(COLORES_TRAFICO)
        # Cada coche tiene una ligera variación de velocidad propia
        self.velocidad = velocidad_base + random.uniform(-0.8, 1.2)

    def update(self, velocidad_carretera):
        # Descenso continuo combinando la velocidad relativa del tráfico
        self.rect.y += int(self.velocidad + velocidad_carretera)

    def draw(self, superficie):
        dibujar_coche(superficie, self.rect, self.color, es_jugador=False)


# ---------------------------------------------------------------------------
# GESTOR PRINCIPAL DEL JUEGO
# ---------------------------------------------------------------------------
class JuegoCoches:
    def __init__(self):
        self.jugador = CocheJugador()
        self.trafico = []
        self.puntuacion = 0
        self.tiempo_inicio = pygame.time.get_ticks()
        self.game_over = False

        # Parámetros de la carretera y desplazamiento
        self.velocidad_carretera = 7.0
        self.offset_lineas = 0.0
        self.largo_segmento_linea = 40
        self.espacio_segmento_linea = 30

        # Temporizador de generación de tráfico
        self.tiempo_ultimo_coche = pygame.time.get_ticks()
        self.intervalo_spawn = 1200  # ms entre cada coche generado

    def spawn_coche(self):
        """Genera un coche en un carril disponible evitando superposiciones inmediatas."""
        carril_aleatorio = random.randint(0, NUM_CARRILES - 1)

        # Comprobar que no haya otro coche ya cerca en la entrada del mismo carril
        for otro in self.trafico:
            if otro.rect.y < 120:
                dist_x = abs(otro.rect.x - (BORDE_IZQ_CARRETERA + carril_aleatorio * ANCHO_CARRIL))
                if dist_x < ANCHO_CARRIL:
                    return

        nuevo_coche = CocheTrafico(carril_aleatorio, self.velocidad_carretera * 0.4)
        self.trafico.append(nuevo_coche)

    def update(self, teclas):
        if self.game_over:
            return

        tiempo_actual = pygame.time.get_ticks()

        # Actualizar jugador
        self.jugador.update(teclas)

        # Animar el desplazamiento de la carretera hacia abajo
        self.offset_lineas = (self.offset_lineas + self.velocidad_carretera) % (
            self.largo_segmento_linea + self.espacio_segmento_linea
        )

        # Generar tráfico periódicamente
        if tiempo_actual - self.tiempo_ultimo_coche >= self.intervalo_spawn:
            self.spawn_coche()
            self.tiempo_ultimo_coche = tiempo_actual

        # Actualizar posición del tráfico y comprobar colisiones
        for coche in self.trafico[:]:
            coche.update(self.velocidad_carretera * 0.5)

            # DETECCIÓN DE COLISIÓN (usando un rectángulo ligeramente ajustado para mayor precisión)
            hitbox_jugador = self.jugador.rect.inflate(-6, -6)
            hitbox_obstaculo = coche.rect.inflate(-6, -6)
            if hitbox_jugador.colliderect(hitbox_obstaculo):
                self.game_over = True

            # Si el coche sale de la parte inferior de la pantalla, sumamos puntos extra
            if coche.rect.top > ALTO_VENTANA + 50:
                self.trafico.remove(coche)
                self.puntuacion += 50

        # Sistema de puntuación por tiempo de supervivencia
        self.puntuacion += 1

        # Aumento dinámico de dificultad progresiva
        if self.puntuacion % 400 == 0:
            self.velocidad_carretera = min(15.0, self.velocidad_carretera + 0.4)
            self.intervalo_spawn = max(550, self.intervalo_spawn - 40)

    def draw_carretera(self, superficie):
        # 1. Bordes laterales (césped)
        superficie.fill(COLOR_CESPED)

        # 2. Asfalto principal
        rect_asfalto = pygame.Rect(BORDE_IZQ_CARRETERA, 0, ANCHO_CARRETERA, ALTO_VENTANA)
        pygame.draw.rect(superficie, COLOR_ASFALTO, rect_asfalto)

        # 3. Quitamiedos / Arcén lateral (bordillo rojo y blanco)
        ancho_borde = 12
        pygame.draw.rect(superficie, COLOR_QUITAMIEDOS, (BORDE_IZQ_CARRETERA - ancho_borde, 0, ancho_borde, ALTO_VENTANA))
        pygame.draw.rect(superficie, COLOR_QUITAMIEDOS, (BORDE_DER_CARRETERA, 0, ancho_borde, ALTO_VENTANA))
        pygame.draw.line(superficie, COLOR_LINEA_LATERAL, (BORDE_IZQ_CARRETERA, 0), (BORDE_IZQ_CARRETERA, ALTO_VENTANA), 3)
        pygame.draw.line(superficie, COLOR_LINEA_LATERAL, (BORDE_DER_CARRETERA, 0), (BORDE_DER_CARRETERA, ALTO_VENTANA), 3)

        # 4. Líneas discontinuas entre carriles con animación continua hacia abajo
        paso_total = self.largo_segmento_linea + self.espacio_segmento_linea
        for c in range(1, NUM_CARRILES):
            x_carril = BORDE_IZQ_CARRETERA + c * ANCHO_CARRIL
            y_actual = -paso_total + self.offset_lineas

            while y_actual < ALTO_VENTANA + paso_total:
                pygame.draw.line(
                    superficie,
                    COLOR_LINEA_CARRIL,
                    (x_carril, y_actual),
                    (x_carril, y_actual + self.largo_segmento_linea),
                    4
                )
                y_actual += paso_total

    def draw(self, superficie, fuentes):
        fuente_grande, fuente_normal, fuente_destacada = fuentes

        # Dibujar carretera animada
        self.draw_carretera(superficie)

        # Dibujar tráfico generado
        for coche in self.trafico:
            coche.draw(superficie)

        # Dibujar coche del jugador
        self.jugador.draw(superficie)

        # --- INTERFAZ HUD (PUNTUACIÓN Y VELOCIDAD) ---
        hud_surface = pygame.Surface((ANCHO_VENTANA, 50), pygame.SRCALPHA)
        hud_surface.fill(COLOR_HUD_FONDO)
        superficie.blit(hud_surface, (0, 0))

        txt_puntos = fuente_destacada.render(f"PUNTOS: {self.puntuacion:06d}", True, COLOR_TEXTO)
        superficie.blit(txt_puntos, (25, 12))

        kmh = int(self.velocidad_carretera * 16)
        txt_vel = fuente_normal.render(f"VEL: {kmh} KM/H", True, (255, 215, 0))
        superficie.blit(txt_vel, (ANCHO_VENTANA - 170, 15))

        # --- PANTALLA DE GAME OVER ---
        if self.game_over:
            overlay = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            superficie.blit(overlay, (0, 0))

            t_go = fuente_grande.render("¡ACCIDENTE!", True, (240, 50, 50))
            t_go_rect = t_go.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 40))
            superficie.blit(t_go, t_go_rect)

            t_score = fuente_destacada.render(f"Puntuación Final: {self.puntuacion}", True, COLOR_TEXTO)
            t_sc_rect = t_score.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 15))
            superficie.blit(t_score, t_sc_rect)

            t_reintentar = fuente_normal.render("Presiona 'R' para jugar de nuevo o ESC para salir", True, (200, 200, 200))
            t_re_rect = t_reintentar.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 65))
            superficie.blit(t_reintentar, t_re_rect)


# ---------------------------------------------------------------------------
# BUCLE PRINCIPAL
# ---------------------------------------------------------------------------
def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Traffic Racer - Arcade Retro")
    reloj = pygame.time.Clock()

    fuentes = (
        pygame.font.SysFont("Arial", 40, bold=True),
        pygame.font.SysFont("Arial", 18),
        pygame.font.SysFont("Arial", 22, bold=True),
    )

    juego = JuegoCoches()
    corriendo = True

    while corriendo:
        teclas = pygame.key.get_pressed()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    corriendo = False

                elif evento.key == pygame.K_r and juego.game_over:
                    # Reiniciar la partida
                    juego = JuegoCoches()

        # Actualizar lógica y física
        juego.update(teclas)

        # Renderizar gráfico
        juego.draw(pantalla, fuentes)

        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

