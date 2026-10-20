"""
=============================================================================
JUEGO CLÁSICO DE TETRIS EN PYTHON CON PYGAME
=============================================================================

REQUISITOS E INSTALACIÓN:
    1. Asegúrate de tener Python 3 instalado.
    2. Instala la librería pygame mediante el siguiente comando en tu terminal:
           pip install pygame

CÓMO EJECUTAR EL SCRIPT:
    python tetris.py
    (o bien: py tetris.py)

CONTROLES:
    - Flecha Izquierda: Mover la pieza a la izquierda.
    - Flecha Derecha:   Mover la pieza a la derecha.
    - Barra Espaciadora: Rotar la pieza 90 grados.
    - Flecha Abajo:     Descenso rápido (soft drop).
    - Tecla R:          Reiniciar la partida en caso de Game Over.
    - Tecla ESC:        Salir del juego.
=============================================================================
"""

import sys
import random
import pygame

# ---------------------------------------------------------------------------
# CONFIGURACIÓN GENERAL Y CONSTANTES DEL TABLERO
# ---------------------------------------------------------------------------
COLUMNAS = 10
FILAS = 20
TAMANO_BLOQUE = 30  # Tamaño en píxeles de cada celda

# Dimensiones de la pantalla (área de juego + panel lateral de información)
ANCHO_TABLERO = COLUMNAS * TAMANO_BLOQUE
ALTO_TABLERO = FILAS * TAMANO_BLOQUE
ANCHO_PANEL = 220
ANCHO_VENTANA = ANCHO_TABLERO + ANCHO_PANEL
ALTO_VENTANA = ALTO_TABLERO

FPS = 60
VELOCIDAD_NORMAL_MS = 500  # Intervalo de caída automática estándar (medio segundo)
VELOCIDAD_RAPIDA_MS = 50   # Intervalo de caída con soft drop presionado

# ---------------------------------------------------------------------------
# PALETA DE COLORES (RGB)
# ---------------------------------------------------------------------------
COLOR_FONDO = (18, 18, 24)
COLOR_TABLERO = (28, 28, 38)
COLOR_LINEAS_GRILLA = (40, 40, 55)
COLOR_TEXTO = (235, 235, 240)
COLOR_TEXTO_SECUNDARIO = (160, 160, 180)
COLOR_GAME_OVER = (235, 60, 60)

# Colores para los 7 tetrominós clásicos
COLORES_PIEZAS = [
    (0, 240, 240),   # I: Cyan
    (0, 100, 240),   # J: Azul
    (240, 160, 0),   # L: Naranja
    (240, 240, 0),   # O: Amarillo
    (0, 220, 0),     # S: Verde
    (160, 0, 240),   # T: Violeta
    (240, 0, 0),     # Z: Rojo
]

# ---------------------------------------------------------------------------
# DEFINICIÓN DE FORMAS DE LOS TETROMINÓS (Matriz 4x4 o 3x3 representada)
# ---------------------------------------------------------------------------
FORMAS = [
    # I
    [
        [(0, 1), (1, 1), (2, 1), (3, 1)],
        [(2, 0), (2, 1), (2, 2), (2, 3)],
        [(0, 2), (1, 2), (2, 2), (3, 2)],
        [(1, 0), (1, 1), (1, 2), (1, 3)],
    ],
    # J
    [
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 0), (1, 1), (0, 2), (1, 2)],
    ],
    # L
    [
        [(2, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 2)],
        [(0, 1), (1, 1), (2, 1), (0, 2)],
        [(0, 0), (1, 0), (1, 1), (1, 2)],
    ],
    # O (no cambia con rotación)
    [
        [(1, 0), (2, 0), (1, 1), (2, 1)],
    ],
    # S
    [
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(1, 0), (1, 1), (2, 1), (2, 2)],
        [(1, 1), (2, 1), (0, 2), (1, 2)],
        [(0, 0), (0, 1), (1, 1), (1, 2)],
    ],
    # T
    [
        [(1, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (2, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (1, 2)],
        [(1, 0), (0, 1), (1, 1), (1, 2)],
    ],
    # Z
    [
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(2, 0), (1, 1), (2, 1), (1, 2)],
        [(0, 1), (1, 1), (1, 2), (2, 2)],
        [(1, 0), (0, 1), (1, 1), (0, 2)],
    ],
]


class Tetromino:
    """Representa una pieza activa en el juego."""
    def __init__(self, tipo_indice=None):
        if tipo_indice is None:
            self.tipo_indice = random.randint(0, len(FORMAS) - 1)
        else:
            self.tipo_indice = tipo_indice
        self.color = COLORES_PIEZAS[self.tipo_indice]
        self.rotaciones = FORMAS[self.tipo_indice]
        self.rotacion_actual = 0
        # Posición inicial centrada en la parte superior
        self.x = COLUMNAS // 2 - 2
        self.y = 0

    @property
    def bloques(self):
        """Retorna las coordenadas globales (col, fila) de los 4 bloques."""
        forma = self.rotaciones[self.rotacion_actual]
        return [(self.x + bx, self.y + by) for (bx, by) in forma]

    def rotar(self):
        """Rota la pieza al siguiente estado de orientación."""
        self.rotacion_actual = (self.rotacion_actual + 1) % len(self.rotaciones)

    def rotar_inverso(self):
        """Deshace la rotación previa."""
        self.rotacion_actual = (self.rotacion_actual - 1) % len(self.rotaciones)


class Tetris:
    """Lógica central y estado del juego Tetris."""
    def __init__(self):
        # Grilla representada como matriz [FILAS][COLUMNAS], None si está vacía
        self.grilla = [[None for _ in range(COLUMNAS)] for _ in range(FILAS)]
        self.puntuacion = 0
        self.lineas_eliminadas = 0
        self.nivel = 1
        self.game_over = False

        self.pieza_siguiente = Tetromino()
        self.pieza_actual = Tetromino()

        # Si al nacer ya colisiona, es Game Over de inmediato
        if not self.es_posicion_valida(self.pieza_actual):
            self.game_over = True

    def es_posicion_valida(self, pieza):
        """Verifica colisiones con paredes, suelo y bloques fijos."""
        for col, fila in pieza.bloques:
            # Límites laterales y suelo
            if col < 0 or col >= COLUMNAS or fila >= FILAS:
                return False
            # Si está dentro de la grilla visible y la celda está ocupada
            if fila >= 0 and self.grilla[fila][col] is not None:
                return False
        return True

    def mover(self, dx, dy):
        """Intenta desplazar la pieza activa. Retorna True si tuvo éxito."""
        if self.game_over:
            return False

        self.pieza_actual.x += dx
        self.pieza_actual.y += dy

        if not self.es_posicion_valida(self.pieza_actual):
            # Revertir movimiento
            self.pieza_actual.x -= dx
            self.pieza_actual.y -= dy
            return False
        return True

    def rotar_pieza(self):
        """Intenta rotar con asistencia contra paredes (wall kicks simples)."""
        if self.game_over:
            return

        self.pieza_actual.rotar()

        # Si tras rotar es válido, genial
        if self.es_posicion_valida(self.pieza_actual):
            return

        # Ajuste lateral en caso de chocar contra el borde
        for desplazamiento in [-1, 1, -2, 2]:
            self.pieza_actual.x += desplazamiento
            if self.es_posicion_valida(self.pieza_actual):
                return
            self.pieza_actual.x -= desplazamiento

        # Si no hubo posición válida, deshacer la rotación
        self.pieza_actual.rotar_inverso()

    def fijar_pieza(self):
        """Fija la pieza actual en la grilla y genera la siguiente."""
        for col, fila in self.pieza_actual.bloques:
            if fila >= 0:
                self.grilla[fila][col] = self.pieza_actual.color

        self.eliminar_lineas_completas()

        # Cargar la siguiente pieza
        self.pieza_actual = self.pieza_siguiente
        self.pieza_siguiente = Tetromino()

        # Comprobar condición de Game Over
        if not self.es_posicion_valida(self.pieza_actual):
            self.game_over = True

    def eliminar_lineas_completas(self):
        """Detecta líneas llenas, las elimina y otorga puntuación."""
        filas_a_mantener = [
            fila for fila in self.grilla if any(celda is None for celda in fila)
        ]
        lineas_eliminadas = FILAS - len(filas_a_mantener)

        if lineas_eliminadas > 0:
            # Crear nuevas filas vacías en la parte superior
            nuevas_filas = [
                [None for _ in range(COLUMNAS)] for _ in range(lineas_eliminadas)
            ]
            self.grilla = nuevas_filas + filas_a_mantener

            # Sistema de puntuación clásico por número de líneas
            tabla_puntos = {1: 100, 2: 300, 3: 500, 4: 800}
            self.puntuacion += tabla_puntos.get(lineas_eliminadas, 100) * self.nivel
            self.lineas_eliminadas += lineas_eliminadas
            self.nivel = (self.lineas_eliminadas // 10) + 1


def dibujar_bloque(superficie, x, y, color, tamano=TAMANO_BLOQUE):
    """Dibuja un bloque con relieve y sombreado estético."""
    rect = pygame.Rect(x, y, tamano, tamano)
    pygame.draw.rect(superficie, color, rect)

    # Brillo superior/izquierdo
    color_brillo = tuple(min(255, c + 50) for c in color)
    pygame.draw.line(superficie, color_brillo, (x, y), (x + tamano - 1, y), 2)
    pygame.draw.line(superficie, color_brillo, (x, y), (x, y + tamano - 1), 2)

    # Sombra inferior/derecha
    color_sombra = tuple(max(0, c - 60) for c in color)
    pygame.draw.line(superficie, color_sombra, (x, y + tamano - 1), (x + tamano - 1, y + tamano - 1), 2)
    pygame.draw.line(superficie, color_sombra, (x + tamano - 1, y), (x + tamano - 1, y + tamano - 1), 2)


def renderizar(pantalla, juego, fuentes):
    """Renderiza todos los componentes gráficos en pantalla."""
    pantalla.fill(COLOR_FONDO)

    # 1. Dibujar fondo de la grilla de juego
    rect_tablero = pygame.Rect(0, 0, ANCHO_TABLERO, ALTO_TABLERO)
    pygame.draw.rect(pantalla, COLOR_TABLERO, rect_tablero)

    # 2. Dibujar líneas guía de la grilla
    for c in range(COLUMNAS + 1):
        x = c * TAMANO_BLOQUE
        pygame.draw.line(pantalla, COLOR_LINEAS_GRILLA, (x, 0), (x, ALTO_TABLERO), 1)
    for f in range(FILAS + 1):
        y = f * TAMANO_BLOQUE
        pygame.draw.line(pantalla, COLOR_LINEAS_GRILLA, (0, y), (ANCHO_TABLERO, y), 1)

    # 3. Dibujar bloques ya fijados en el tablero
    for f in range(FILAS):
        for c in range(COLUMNAS):
            color = juego.grilla[f][c]
            if color is not None:
                dibujar_bloque(pantalla, c * TAMANO_BLOQUE, f * TAMANO_BLOQUE, color)

    # 4. Dibujar pieza activa si la partida está en curso
    if not juego.game_over:
        for col, fila in juego.pieza_actual.bloques:
            if fila >= 0:
                dibujar_bloque(
                    pantalla,
                    col * TAMANO_BLOQUE,
                    fila * TAMANO_BLOQUE,
                    juego.pieza_actual.color,
                )

    # 5. Panel lateral de información
    x_panel = ANCHO_TABLERO + 20
    fuente_titulo, fuente_normal, fuente_destacada = fuentes

    titulo = fuente_titulo.render("TETRIS", True, (0, 240, 240))
    pantalla.blit(titulo, (x_panel, 20))

    # Puntuación
    txt_score_lbl = fuente_normal.render("Puntuación:", True, COLOR_TEXTO_SECUNDARIO)
    pantalla.blit(txt_score_lbl, (x_panel, 80))
    txt_score_val = fuente_destacada.render(str(juego.puntuacion), True, COLOR_TEXTO)
    pantalla.blit(txt_score_val, (x_panel, 105))

    # Líneas
    txt_lines_lbl = fuente_normal.render("Líneas:", True, COLOR_TEXTO_SECUNDARIO)
    pantalla.blit(txt_lines_lbl, (x_panel, 150))
    txt_lines_val = fuente_destacada.render(str(juego.lineas_eliminadas), True, COLOR_TEXTO)
    pantalla.blit(txt_lines_val, (x_panel, 175))

    # Nivel
    txt_level_lbl = fuente_normal.render("Nivel:", True, COLOR_TEXTO_SECUNDARIO)
    pantalla.blit(txt_level_lbl, (x_panel, 220))
    txt_level_val = fuente_destacada.render(str(juego.nivel), True, COLOR_TEXTO)
    pantalla.blit(txt_level_val, (x_panel, 245))

    # Previsualización de la siguiente pieza
    txt_next_lbl = fuente_normal.render("Siguiente:", True, COLOR_TEXTO_SECUNDARIO)
    pantalla.blit(txt_next_lbl, (x_panel, 300))

    forma_siguiente = juego.pieza_siguiente.rotaciones[0]
    tam_preview = 22
    preview_box_x = x_panel + 10
    preview_box_y = 340
    for bx, by in forma_siguiente:
        dibujar_bloque(
            pantalla,
            preview_box_x + bx * tam_preview,
            preview_box_y + by * tam_preview,
            juego.pieza_siguiente.color,
            tamano=tam_preview,
        )

    # Controles en pantalla
    y_ayuda = 460
    controles = [
        "Espacio : Rotar",
        "Flecha ↓: Bajar rápido",
        "← / →   : Mover",
        "ESC     : Salir",
    ]
    for linea in controles:
        txt_c = fuente_normal.render(linea, True, COLOR_TEXTO_SECUNDARIO)
        pantalla.blit(txt_c, (x_panel, y_ayuda))
        y_ayuda += 22

    # 6. Cartel de GAME OVER
    if juego.game_over:
        overlay = pygame.Surface((ANCHO_TABLERO, ALTO_TABLERO), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        pantalla.blit(overlay, (0, 0))

        go_txt = fuente_titulo.render("GAME OVER", True, COLOR_GAME_OVER)
        go_rect = go_txt.get_rect(center=(ANCHO_TABLERO // 2, ALTO_TABLERO // 2 - 20))
        pantalla.blit(go_txt, go_rect)

        reiniciar_txt = fuente_normal.render("Presiona 'R' para reiniciar", True, COLOR_TEXTO)
        r_rect = reiniciar_txt.get_rect(center=(ANCHO_TABLERO // 2, ALTO_TABLERO // 2 + 25))
        pantalla.blit(reiniciar_txt, r_rect)

    pygame.display.flip()


def main():
    # Inicialización de Pygame
    pygame.init()
    pygame.display.set_caption("Tetris en Python")
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    reloj = pygame.time.Clock()

    # Fuentes del sistema
    fuentes = (
        pygame.font.SysFont("Arial", 28, bold=True),
        pygame.font.SysFont("Arial", 16),
        pygame.font.SysFont("Arial", 22, bold=True),
    )

    # Instancia del juego
    juego = Tetris()
    ultimo_tiempo_caida = pygame.time.get_ticks()

    # Bucle principal de ejecución
    corriendo = True
    while corriendo:
        tiempo_actual = pygame.time.get_ticks()

        # Detección de caída rápida (soft drop) manteniendo pulsada la flecha abajo
        teclas_pulsadas = pygame.key.get_pressed()
        descenso_rapido = teclas_pulsadas[pygame.K_DOWN]

        # Calcular el intervalo de caída según el nivel y si se pulsa soft drop
        velocidad_base = max(100, VELOCIDAD_NORMAL_MS - (juego.nivel - 1) * 35)
        intervalo_caida = VELOCIDAD_RAPIDA_MS if descenso_rapido else velocidad_base

        # Gestión de eventos de entrada
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    corriendo = False

                elif evento.key == pygame.K_r and juego.game_over:
                    # Reiniciar la partida
                    juego = Tetris()
                    ultimo_tiempo_caida = tiempo_actual

                elif not juego.game_over:
                    if evento.key == pygame.K_LEFT:
                        juego.mover(-1, 0)
                    elif evento.key == pygame.K_RIGHT:
                        juego.mover(1, 0)
                    elif evento.key == pygame.K_SPACE:
                        # Rotar la pieza actual
                        juego.rotar_pieza()

        # Caída automática periódica de la pieza
        if not juego.game_over and tiempo_actual - ultimo_tiempo_caida >= intervalo_caida:
            exito = juego.mover(0, 1)
            if not exito:
                # Si no pudo descender más, se fija la pieza en el suelo/bloques
                juego.fijar_pieza()
            ultimo_tiempo_caida = tiempo_actual

        # Dibujar frame actual
        renderizar(pantalla, juego, fuentes)
        reloj.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

