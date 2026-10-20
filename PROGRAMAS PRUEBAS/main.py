import math
import random
import sys
import pygame

# ==============================================================================
# CONFIGURACIÓN GBA Y PYGAME
# ==============================================================================
pygame.init()
pygame.font.init()

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
FPS = 60

# Paleta de Colores Estilo GBA Esmeralda
C_BG_GBA = (18, 22, 28)
C_EMERALD = (0, 150, 95)
C_EMERALD_LIGHT = (46, 213, 115)
C_DARK_PANEL = (24, 28, 38)
C_BORDER = (45, 55, 72)
C_WHITE = (245, 246, 250)
C_GRAY = (149, 165, 166)
C_YELLOW = (241, 196, 15)
C_RED = (231, 76, 60)
C_BLUE = (52, 152, 219)
C_BLACK = (10, 12, 16)
C_HP_GREEN = (46, 204, 113)
C_HP_ORANGE = (230, 126, 34)

FONT_CONSOLE = pygame.font.SysFont("consolas", 14)
FONT_CONSOLE_BOLD = pygame.font.SysFont("consolas", 14, bold=True)
FONT_RETRO_TITLE = pygame.font.SysFont("consolas", 18, bold=True)
FONT_STATUS = pygame.font.SysFont("consolas", 12)

# ==============================================================================
# BASE DE DATOS POKÉMON ESMERALDA (3ª GENERACIÓN)
# ==============================================================================
TABLA_TIPOS = {
    "Normal":   {"Roca": 0.5, "Fantasma": 0.0, "Acero": 0.5},
    "Fuego":    {"Fuego": 0.5, "Agua": 0.5, "Planta": 2.0, "Hielo": 2.0, "Bicho": 2.0, "Roca": 0.5, "Dragon": 0.5, "Acero": 2.0},
    "Agua":     {"Fuego": 2.0, "Agua": 0.5, "Planta": 0.5, "Tierra": 2.0, "Roca": 2.0, "Dragon": 0.5},
    "Planta":   {"Fuego": 0.5, "Agua": 2.0, "Planta": 0.5, "Veneno": 0.5, "Tierra": 2.0, "Volador": 0.5, "Bicho": 0.5, "Roca": 2.0, "Dragon": 0.5, "Acero": 0.5},
    "Electrico":{"Agua": 2.0, "Planta": 0.5, "Electrico": 0.5, "Tierra": 0.0, "Volador": 2.0, "Dragon": 0.5},
    "Siniestro":{"Lucha": 0.5, "Psiquico": 2.0, "Fantasma": 2.0, "Siniestro": 0.5, "Acero": 0.5},
    "Bicho":    {"Fuego": 0.5, "Planta": 2.0, "Lucha": 0.5, "Veneno": 0.5, "Volador": 0.5, "Psiquico": 2.0, "Fantasma": 0.5, "Siniestro": 2.0, "Acero": 0.5}
}

POKEDEX = {
    "Treecko": {
        "num": "001", "tipos": ["Planta"], "cat": "Pokémon Geco Arbóreo",
        "altura": 0.5, "peso": 5.0,
        "base": {"ps": 40, "atq": 45, "def": 35, "sp_atq": 65, "sp_def": 55, "vel": 70},
        "catch_rate": 45, "exp_base": 65,
        "desc": "Con 0.5m, le llega a las rodillas al entrenador. Posee ganchos en los pies para trepar paredes.",
        "color": (46, 204, 113)
    },
    "Torchic": {
        "num": "004", "tipos": ["Fuego"], "cat": "Pokémon Polluelo",
        "altura": 0.4, "peso": 2.5,
        "base": {"ps": 45, "atq": 60, "def": 40, "sp_atq": 70, "sp_def": 50, "vel": 45},
        "catch_rate": 45, "exp_base": 65,
        "desc": "Con 0.4m, es un pequeño polluelo cálido cubierto de plumas esponjosas que lanza bolas de fuego.",
        "color": (230, 126, 34)
    },
    "Mudkip": {
        "num": "007", "tipos": ["Agua"], "cat": "Pokémon Pez Lodo",
        "altura": 0.4, "peso": 7.6,
        "base": {"ps": 50, "atq": 70, "def": 50, "sp_atq": 50, "sp_def": 50, "vel": 40},
        "catch_rate": 45, "exp_base": 65,
        "desc": "Con 0.4m, su aleta en la cabeza actúa como un radar ultrasensible que detecta corrientes de agua.",
        "color": (52, 152, 219)
    },
    "Poochyena": {
        "num": "010", "tipos": ["Siniestro"], "cat": "Pokémon Mordisco",
        "altura": 0.5, "peso": 13.6,
        "base": {"ps": 35, "atq": 55, "def": 35, "sp_atq": 30, "sp_def": 30, "vel": 35},
        "catch_rate": 255, "exp_base": 55,
        "desc": "Con 0.5m, este cánido gruñe ferozmente persiguiendo a sus presas hasta agotarlas.",
        "color": (108, 122, 137)
    },
    "Zigzagoon": {
        "num": "012", "tipos": ["Normal"], "cat": "Pokémon Mapachito",
        "altura": 0.4, "peso": 17.5,
        "base": {"ps": 38, "atq": 30, "def": 41, "sp_atq": 30, "sp_def": 41, "vel": 60},
        "catch_rate": 255, "exp_base": 60,
        "desc": "Con 0.4m, corretea en zigzag husmeando el suelo en busca de objetos curiosos.",
        "color": (160, 130, 90)
    },
    "Wurmple": {
        "num": "014", "tipos": ["Bicho"], "cat": "Pokémon Gusano",
        "altura": 0.3, "peso": 3.6,
        "base": {"ps": 45, "atq": 45, "def": 35, "sp_atq": 20, "sp_def": 30, "vel": 20},
        "catch_rate": 255, "exp_base": 54,
        "desc": "Con apenas 0.3m, habita en arbustos y ramas altas despidiendo veneno por su aguijón.",
        "color": (214, 48, 49)
    }
}

MOVIMIENTOS = {
    "Placaje":      {"tipo": "Normal", "poder": 35, "precision": 95, "cat": "fisico"},
    "Arañazo":      {"tipo": "Normal", "poder": 40, "precision": 100, "cat": "fisico"},
    "Destructor":   {"tipo": "Normal", "poder": 40, "precision": 100, "cat": "fisico"},
    "Absorber":     {"tipo": "Planta", "poder": 20, "precision": 100, "cat": "especial"},
    "Ascuas":       {"tipo": "Fuego", "poder": 40, "precision": 100, "cat": "especial"},
    "Pistola Agua": {"tipo": "Agua", "poder": 40, "precision": 100, "cat": "especial"},
    "Mordisco":     {"tipo": "Siniestro", "poder": 60, "precision": 100, "cat": "especial"},
    "Picotazo":     {"tipo": "Volador", "poder": 35, "precision": 100, "cat": "fisico"}
}


def calcular_mult(tipo_mov, tipos_def):
    mult = 1.0
    for td in tipos_def:
        mult *= TABLA_TIPOS.get(tipo_mov, {}).get(td, 1.0)
    return mult


# ==============================================================================
# CLASE POKÉMON
# ==============================================================================
class Pokemon:
    def __init__(self, especie, nivel=5):
        self.especie = especie
        self.info = POKEDEX[especie]
        self.nivel = nivel
        self.tipos = self.info["tipos"]
        self.estado = "OK"

        b = self.info["base"]
        self.ps_max = math.floor(((2 * b["ps"] + 15) * self.nivel) / 100) + self.nivel + 10
        self.atq = math.floor(((2 * b["atq"] + 15) * self.nivel) / 100) + 5
        self.defe = math.floor(((2 * b["def"] + 15) * self.nivel) / 100) + 5
        self.sp_atq = math.floor(((2 * b["sp_atq"] + 15) * self.nivel) / 100) + 5
        self.sp_def = math.floor(((2 * b["sp_def"] + 15) * self.nivel) / 100) + 5
        self.vel = math.floor(((2 * b["vel"] + 15) * self.nivel) / 100) + 5

        self.ps_actuales = self.ps_max
        self.exp = 0
        self.exp_siguiente = self.nivel ** 3

        if especie == "Treecko":
            self.movimientos = ["Destructor", "Absorber"]
        elif especie == "Torchic":
            self.movimientos = ["Arañazo", "Ascuas"]
        elif especie == "Mudkip":
            self.movimientos = ["Placaje", "Pistola Agua"]
        elif especie == "Poochyena":
            self.movimientos = ["Placaje", "Mordisco"]
        else:
            self.movimientos = ["Placaje"]

    def barra_ascii(self):
        ratio = max(0.0, min(1.0, self.ps_actuales / self.ps_max))
        llenos = int(round(ratio * 10))
        return "█" * llenos + "░" * (10 - llenos)


# ==============================================================================
# MOTOR Y SIMULADOR PYGAME
# ==============================================================================
class EmeraldGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pokémon Edición Esmeralda - Motor Determinista GBA (Pygame)")
        self.clock = pygame.time.Clock()
        self.running = True

        # Estado del jugador
        self.jugador = "Ruby"
        self.genero = "Chico"
        self.pokedolares = 300
        self.medallas = 0
        self.ubicacion = "Villa Raíz"
        self.clima = "Soleado"
        self.mochila = {"Pokéball": 5, "Poción": 3}
        self.equipo = []

        # Historial de mensajes en consola
        self.mensajes = []

        # Estado y Modos
        self.estado_juego = "INTRO"  # INTRO, SELECCION, MUNDO, COMBATE
        self.enemigo = None
        self.botones = []
        self.ficha_mostrada = None

        self.iniciar_intro()

    def add_log(self, texto):
        lineas = texto.split("\n")
        for l in lineas:
            self.mensajes.append(l)
        if len(self.mensajes) > 200:
            self.mensajes = self.mensajes[-200:]

    def generar_ficha_biologica(self, especie):
        info = POKEDEX[especie]
        b = info["base"]
        debs = []
        res = []
        for t_atq in TABLA_TIPOS:
            m = calcular_mult(t_atq, info["tipos"])
            if m >= 2.0:
                debs.append(f"{t_atq}(x{int(m) if m.is_integer() else m})")
            elif m < 1.0 and m > 0.0:
                res.append(f"{t_atq}(x{m})")

        texto_ficha = [
            f"┌── 🐙 FICHA POKÉDEX: {especie.upper()} (#{info['num']} Hoenn) ──────────────────────────",
            f"│ Tipo: {'/'.join(info['tipos'])} | Altura: {info['altura']} m | Peso: {info['peso']} kg | Cat: {info['cat']}",
            f"│ STATS: PS:{b['ps']} | ATQ:{b['atq']} | DEF:{b['def']} | SP.ATQ:{b['sp_atq']} | SP.DEF:{b['sp_def']} | VEL:{b['vel']}",
            f"│ DEBILIDADES: {', '.join(debs) if debs else 'Ninguna'}",
            f"│ RESISTENCIAS: {', '.join(res) if res else 'Ninguna'}",
            f"│ ESCALA: {info['desc']}",
            f"└────────────────────────────────────────────────────────────────────────"
        ]
        return "\n".join(texto_ficha)

    # --------------------------------------------------------------------------
    # FASES DEL JUEGO
    # --------------------------------------------------------------------------
    def iniciar_intro(self):
        self.add_log("================ POKÉMON EDICIÓN ESMERALDA (GBA) ================")
        self.add_log("PROFESOR ABEDUL: «¡Hola! ¡Te doy la bienvenida al mundo POKÉMON!»")
        self.add_log("«Mi nombre es ABEDUL. ¡Este mundo está habitado por criaturas llamadas Pokémon!»")
        self.add_log(self.generar_ficha_biologica("Zigzagoon"))
        self.add_log("\nABEDUL: «Dime, ¿eres un chico o una chica?»")

        self.botones = [
            {"rect": pygame.Rect(30, 560, 210, 48), "texto": "[A] Chico (Ruby)", "accion": lambda: self.set_personaje("Ruby", "Chico")},
            {"rect": pygame.Rect(260, 560, 210, 48), "texto": "[B] Chica (Sapphire)", "accion": lambda: self.set_personaje("Sapphire", "Chica")},
            {"rect": pygame.Rect(490, 560, 210, 48), "texto": "[C] Explorar Fichas", "accion": self.mostrar_todas_fichas},
            {"rect": pygame.Rect(720, 560, 210, 48), "texto": "[D] Salto Rápido", "accion": lambda: self.set_personaje("Ruby", "Chico")}
        ]

    def mostrar_todas_fichas(self):
        for sp in ["Treecko", "Torchic", "Mudkip"]:
            self.add_log(self.generar_ficha_biologica(sp))

    def set_personaje(self, nombre, genero):
        self.jugador = nombre
        self.genero = genero
        self.ubicacion = "Villa Raíz - Ruta 101"
        self.estado_juego = "SELECCION"

        self.add_log(f"\n¡Bienvenido, {self.jugador}! Tu mudanza a Villa Raíz ha finalizado.")
        self.add_log("Caminas hacia la Ruta 101 y escuchas gritos de auxilio:")
        self.add_log("PROFESOR ABEDUL: «¡¡SOCORROOO!! ¡Un Poochyena salvaje me persigue!»")
        self.add_log("«¡Abre mi maletín y escoge una Pokéball para ayudarme!»")
        self.add_log(self.generar_ficha_biologica("Poochyena"))

        self.botones = [
            {"rect": pygame.Rect(30, 560, 210, 48), "texto": "[A] Treecko (Planta)", "accion": lambda: self.elegir_inicial("Treecko")},
            {"rect": pygame.Rect(260, 560, 210, 48), "texto": "[B] Torchic (Fuego)", "accion": lambda: self.elegir_inicial("Torchic")},
            {"rect": pygame.Rect(490, 560, 210, 48), "texto": "[C] Mudkip (Agua)", "accion": lambda: self.elegir_inicial("Mudkip")},
            {"rect": pygame.Rect(720, 560, 210, 48), "texto": "[D] Ver Iniciales", "accion": self.mostrar_todas_fichas}
        ]

    def elegir_inicial(self, sp):
        p = Pokemon(sp, nivel=5)
        self.equipo.append(p)
        self.add_log(f"\n¡Has elegido a {sp.upper()} de Nivel 5!")
        self.add_log(self.generar_ficha_biologica(sp))
        self.iniciar_combate(Pokemon("Poochyena", nivel=2))

    def iniciar_combate(self, salvaje):
        self.estado_juego = "COMBATE"
        self.enemigo = salvaje
        self.add_log(f"\n⚔️ ¡Un {salvaje.especie.upper()} salvaje (Nv {salvaje.nivel}) aparece amenazante!")
        self.add_log(self.generar_ficha_biologica(salvaje.especie))
        self.actualizar_botones_combate()

    def actualizar_botones_combate(self):
        p = self.equipo[0]
        m1 = p.movimientos[0] if len(p.movimientos) > 0 else "Placaje"
        m2 = p.movimientos[1] if len(p.movimientos) > 1 else "—"

        self.botones = [
            {"rect": pygame.Rect(30, 560, 210, 48), "texto": f"[A] {m1}", "accion": lambda: self.turno_ataque(m1)},
            {"rect": pygame.Rect(260, 560, 210, 48), "texto": f"[B] {m2}", "accion": lambda: self.turno_ataque(m2) if m2 != "—" else None},
            {"rect": pygame.Rect(490, 560, 210, 48), "texto": f"[C] Pokéball (x{self.mochila['Pokéball']})", "accion": self.intentar_captura},
            {"rect": pygame.Rect(720, 560, 210, 48), "texto": f"[D] Poción (x{self.mochila['Poción']})", "accion": self.usar_pocion}
        ]

    def calcular_dano_gen3(self, atacante, defensor, mov_name):
        m = MOVIMIENTOS.get(mov_name, {"poder": 40, "precision": 100, "tipo": "Normal", "cat": "fisico"})
        if random.randint(1, 100) > m["precision"]:
            return 0, 1.0, False, "fallo"

        if m["tipo"] in ["Normal", "Lucha", "Volador", "Veneno", "Tierra", "Roca", "Bicho", "Fantasma", "Acero"]:
            atq_stat = atacante.atq
            def_stat = defensor.defe
        else:
            atq_stat = atacante.sp_atq
            def_stat = defensor.sp_def

        stab = 1.5 if m["tipo"] in atacante.tipos else 1.0
        efect = calcular_mult(m["tipo"], defensor.tipos)
        variacion = random.uniform(0.85, 1.00)
        crit = random.random() < 0.0625
        mod_crit = 2.0 if crit else 1.0

        dano = (((((2 * atacante.nivel / 5) + 2) * m["poder"] * (atq_stat / max(1, def_stat))) / 50) + 2) * stab * efect * variacion * mod_crit
        return max(1, math.floor(dano)), efect, crit, "exito"

    def turno_ataque(self, mov):
        if not self.enemigo or self.estado_juego != "COMBATE":
            return
        p = self.equipo[0]
        e = self.enemigo

        if p.vel >= e.vel:
            self.ejecutar_golpe(p, e, mov, es_jugador=True)
            if e.ps_actuales > 0:
                self.ejecutar_golpe(e, p, random.choice(e.movimientos), es_jugador=False)
        else:
            self.ejecutar_golpe(e, p, random.choice(e.movimientos), es_jugador=False)
            if p.ps_actuales > 0:
                self.ejecutar_golpe(p, e, mov, es_jugador=True)

        self.verificar_combate()

    def ejecutar_golpe(self, atq, defe, mov, es_jugador):
        dano, ef, crit, res = self.calcular_dano_gen3(atq, defe, mov)
        nombre = f"¡{atq.especie} de {self.jugador}" if es_jugador else f"¡{atq.especie} salvaje"

        if res == "fallo":
            self.add_log(f"{nombre} usó {mov.upper()}, ¡pero falló!")
            return

        defe.ps_actuales = max(0, defe.ps_actuales - dano)
        self.add_log(f"{nombre} usó {mov.upper()}! Causó {dano} PS de daño.")
        if crit:
            self.add_log("💥 ¡Un golpe crítico!")
        if ef > 1.0:
            self.add_log("✨ ¡Es súper eficaz!")
        elif 0.0 < ef < 1.0:
            self.add_log("🛡️ No es muy eficaz...")

    def intentar_captura(self):
        if self.mochila["Pokéball"] <= 0:
            self.add_log("¡No tienes Pokéballs restantes!")
            return

        self.mochila["Pokéball"] -= 1
        e = self.enemigo
        self.add_log(f"¡{self.jugador} lanzó una POKÉBALL!")

        a = (((3 * e.ps_max - 2 * e.ps_actuales) * e.info["catch_rate"] * 1.0) / (3 * e.ps_max))
        if a >= 255 or random.randint(0, 255) <= a:
            self.add_log(f"🎉 ¡CLIC! ¡El {e.especie.upper()} salvaje fue capturado!")
            if len(self.equipo) < 6:
                self.equipo.append(e)
                self.add_log(f"¡{e.especie} se unió a tu equipo Pokémon!")
            self.victoria_combate()
        else:
            self.add_log("💨 ¡Oh, no! ¡El Pokémon rompió la Pokéball!")
            self.ejecutar_golpe(e, self.equipo[0], random.choice(e.movimientos), es_jugador=False)
            self.verificar_combate()

    def usar_pocion(self):
        if self.mochila["Poción"] <= 0:
            self.add_log("¡No tienes pociones restantes!")
            return
        self.mochila["Poción"] -= 1
        p = self.equipo[0]
        curado = min(20, p.ps_max - p.ps_actuales)
        p.ps_actuales += curado
        self.add_log(f"🧪 Usaste una Poción en {p.especie}. ¡Recuperó {curado} PS!")
        self.ejecutar_golpe(self.enemigo, p, random.choice(self.enemigo.movimientos), es_jugador=False)
        self.verificar_combate()

    def verificar_combate(self):
        p = self.equipo[0]
        e = self.enemigo
        if e.ps_actuales <= 0:
            self.add_log(f"\n💀 ¡El {e.especie} salvaje se ha debilitado!")
            exp = math.floor((e.info["exp_base"] * e.nivel) / 7)
            self.add_log(f"⭐ ¡{p.especie} ganó {exp} puntos de experiencia!")
            p.exp += exp
            if p.exp >= p.exp_siguiente:
                p.nivel += 1
                p.exp_siguiente = p.nivel ** 3
                self.add_log(f"🆙 ¡SUBIDA DE NIVEL! ¡{p.especie} alcanzó el Nivel {p.nivel}!")
            self.victoria_combate()
        elif p.ps_actuales <= 0:
            self.add_log(f"\n☠️ ¡A {p.especie} no le quedan fuerzas! Te has desmayado...")
            p.ps_actuales = p.ps_max
            self.add_log("Te despiertas sano y salvo en el Centro Pokémon.")
            self.menu_mundo()
        else:
            self.actualizar_botones_combate()

    def victoria_combate(self):
        self.pokedolares += 150
        self.menu_mundo()

    def menu_mundo(self):
        self.estado_juego = "MUNDO"
        self.ubicacion = "Ruta 101"
        self.add_log("\n¿Qué deseas hacer ahora en la RUTA 101?")

        self.botones = [
            {"rect": pygame.Rect(30, 560, 210, 48), "texto": "[A] Hierba Alta (Luchar)", "accion": self.explorar_hierba},
            {"rect": pygame.Rect(260, 560, 210, 48), "texto": "[B] Centro Pokémon (Curar)", "accion": self.curar_equipo},
            {"rect": pygame.Rect(490, 560, 210, 48), "texto": "[C] Tienda (3 Balls $600)", "accion": self.comprar_balls},
            {"rect": pygame.Rect(720, 560, 210, 48), "texto": "[D] Ficha del Equipo", "accion": self.ver_fichas_equipo}
        ]

    def explorar_hierba(self):
        sp = random.choice(["Poochyena", "Zigzagoon", "Wurmple"])
        nv = random.choice([2, 3, 4])
        self.iniciar_combate(Pokemon(sp, nivel=nv))

    def curar_equipo(self):
        for p in self.equipo:
            p.ps_actuales = p.ps_max
            p.estado = "OK"
        self.add_log("💖 ¡Todo tu equipo Pokémon ha sido completamente curado!")

    def comprar_balls(self):
        if self.pokedolares >= 600:
            self.pokedolares -= 600
            self.mochila["Pokéball"] += 3
            self.add_log("¡Compraste 3 Pokéballs por $600!")
        else:
            self.add_log("¡No tienes suficiente dinero ($600 requerido)!")

    def ver_fichas_equipo(self):
        for p in self.equipo:
            self.add_log(self.generar_ficha_biologica(p.especie))

    # --------------------------------------------------------------------------
    # RENDERIZADO VISUAL
    # --------------------------------------------------------------------------
    def render(self):
        self.screen.fill(C_BG_GBA)

        # 1. Cabecera GBA Esmeralda
        pygame.draw.rect(self.screen, C_EMERALD, (0, 0, SCREEN_WIDTH, 42))
        lbl_head = FONT_RETRO_TITLE.render("GAME BOY ADVANCE ❖ POKÉMON ESMERALDA ENGINE ❖ PYGAME", True, C_WHITE)
        self.screen.blit(lbl_head, (20, 10))

        # 2. Marco del Visualizador Gráfico / Escena (Izquierda)
        escena_rect = pygame.Rect(20, 52, 450, 260)
        pygame.draw.rect(self.screen, C_DARK_PANEL, escena_rect, border_radius=8)
        pygame.draw.rect(self.screen, C_BORDER, escena_rect, 2, border_radius=8)

        # Dibujo de escenario Pokémon dinámico
        if self.estado_juego == "COMBATE" and self.enemigo and self.equipo:
            # Pokémon Rival (Arriba Derecha de la caja)
            e_col = self.enemigo.info.get("color", C_RED)
            pygame.draw.circle(self.screen, e_col, (370, 120), 38)
            pygame.draw.ellipse(self.screen, (20, 24, 30), (330, 150, 80, 20))
            
            # Caja de estado Rival
            lbl_e_nom = FONT_CONSOLE_BOLD.render(f"{self.enemigo.especie.upper()}  Nv:{self.enemigo.nivel}", True, C_WHITE)
            self.screen.blit(lbl_e_nom, (40, 75))
            
            # Barra HP Rival
            pygame.draw.rect(self.screen, C_BLACK, (40, 95, 160, 14), border_radius=4)
            pct_e = max(0.0, self.enemigo.ps_actuales / self.enemigo.ps_max)
            col_hp_e = C_HP_GREEN if pct_e > 0.5 else (C_HP_ORANGE if pct_e > 0.2 else C_RED)
            pygame.draw.rect(self.screen, col_hp_e, (42, 97, int(156 * pct_e), 10), border_radius=3)

            # Pokémon del Jugador (Abajo Izquierda de la caja)
            p = self.equipo[0]
            p_col = p.info.get("color", C_EMERALD_LIGHT)
            pygame.draw.circle(self.screen, p_col, (100, 230), 45)
            pygame.draw.ellipse(self.screen, (20, 24, 30), (55, 265, 90, 22))

            # Caja de estado Jugador
            lbl_p_nom = FONT_CONSOLE_BOLD.render(f"{p.especie.upper()}  Nv:{p.nivel}", True, C_WHITE)
            self.screen.blit(lbl_p_nom, (230, 210))
            lbl_p_ps = FONT_STATUS.render(f"PS: {p.ps_actuales:02d} / {p.ps_max:02d}", True, C_WHITE)
            self.screen.blit(lbl_p_ps, (230, 228))

            # Barra HP Jugador
            pygame.draw.rect(self.screen, C_BLACK, (230, 248, 160, 14), border_radius=4)
            pct_p = max(0.0, p.ps_actuales / p.ps_max)
            col_hp_p = C_HP_GREEN if pct_p > 0.5 else (C_HP_ORANGE if pct_p > 0.2 else C_RED)
            pygame.draw.rect(self.screen, col_hp_p, (232, 250, int(156 * pct_p), 10), border_radius=3)
        else:
            # Pantalla de Mundo / Profesor Abedul
            pygame.draw.circle(self.screen, C_EMERALD, (245, 160), 60)
            pygame.draw.circle(self.screen, C_WHITE, (245, 160), 55, 3)
            lbl_info_esc = FONT_RETRO_TITLE.render("HOENN REGION ENGINE", True, C_EMERALD_LIGHT)
            self.screen.blit(lbl_info_esc, (135, 150))

        # 3. Consola de Texto / Registro de Batalla y Pokédex (Derecha)
        consola_rect = pygame.Rect(485, 52, 455, 260)
        pygame.draw.rect(self.screen, C_BLACK, consola_rect, border_radius=8)
        pygame.draw.rect(self.screen, C_BORDER, consola_rect, 2, border_radius=8)

        # Renderizar últimas 12 líneas de mensajes
        ultimas = self.mensajes[-13:]
        y_off = 60
        for linea in ultimas:
            col_txt = C_EMERALD_LIGHT if "┌" in linea or "└" in linea or "FICHA" in linea else (C_YELLOW if "¡" in linea or "⚔️" in linea else C_WHITE)
            surf_linea = FONT_CONSOLE.render(linea[:54], True, col_txt)
            self.screen.blit(surf_linea, (495, y_off))
            y_off += 19

        # 4. HUD Continuo Obligatorio (Panel Central Completo)
        hud_rect = pygame.Rect(20, 322, 920, 218)
        pygame.draw.rect(self.screen, C_DARK_PANEL, hud_rect, border_radius=8)
        pygame.draw.rect(self.screen, C_EMERALD, hud_rect, 2, border_radius=8)

        # Líneas de HUD
        hud_l1 = f"📍 UBICACIÓN: {self.ubicacion} | CLIMA: {self.clima} | 👤 JUGADOR: {self.jugador} ({self.genero}) | 💰 ${self.pokedolares} | 🏅 MEDALLAS: {self.medallas}/8"
        surf_h1 = FONT_CONSOLE_BOLD.render(hud_l1, True, (0, 206, 201))
        self.screen.blit(surf_h1, (34, 332))

        # Separador HUD
        pygame.draw.line(self.screen, C_BORDER, (34, 355), (926, 355), 1)

        # Equipo en HUD
        self.screen.blit(FONT_CONSOLE_BOLD.render("🎒 EQUIPO POKÉMON:", True, C_WHITE), (34, 362))
        if not self.equipo:
            self.screen.blit(FONT_CONSOLE.render("1. (Vacío - Elige a tu Pokémon inicial)", True, C_GRAY), (44, 384))
        else:
            y_eq = 384
            for i, p in enumerate(self.equipo[:3], 1):
                eq_str = f"{i}. {p.especie} Lvl:{p.nivel} | PS: [{p.ps_actuales:02d}/{p.ps_max:02d}] [{p.barra_ascii()}] | Estado: [{p.estado}]"
                self.screen.blit(FONT_CONSOLE.render(eq_str, True, C_WHITE), (44, y_eq))
                y_eq += 20

        # Separador HUD 2
        pygame.draw.line(self.screen, C_BORDER, (34, 460), (926, 460), 1)

        # Mochila en HUD
        hud_l3 = f"🎒 MOCHILA DESTACADA: Pokéballs:[{self.mochila.get('Pokéball', 0)}] | Pociones:[{self.mochila.get('Poción', 0)}] | Objetos Clave:[Bolsa de Abedul, Pokédex]"
        self.screen.blit(FONT_CONSOLE_BOLD.render(hud_l3, True, C_YELLOW), (34, 470))

        # 5. Botones Interactivos de Acción (Inferior)
        mouse_pos = pygame.mouse.get_pos()
        for b in self.botones:
            hover = b["rect"].collidepoint(mouse_pos)
            col_btn = C_EMERALD if hover else (35, 45, 60)
            pygame.draw.rect(self.screen, col_btn, b["rect"], border_radius=6)
            pygame.draw.rect(self.screen, C_EMERALD_LIGHT if hover else C_BORDER, b["rect"], 2, border_radius=6)

            txt_surf = FONT_CONSOLE_BOLD.render(b["texto"], True, C_WHITE)
            t_rect = txt_surf.get_rect(center=b["rect"].center)
            self.screen.blit(txt_surf, t_rect)

        pygame.display.flip()

    # --------------------------------------------------------------------------
    # BUCLE DE EVENTOS
    # --------------------------------------------------------------------------
    def run(self):
        while self.running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for b in self.botones:
                        if b["rect"].collidepoint(event.pos):
                            if b["accion"]:
                                b["accion"]()
                                break
                elif event.type == pygame.KEYDOWN:
                    # Mapeo rápido de teclado: A, B, C, D
                    if event.key == pygame.K_a and len(self.botones) > 0 and self.botones[0]["accion"]:
                        self.botones[0]["accion"]()
                    elif event.key == pygame.K_b and len(self.botones) > 1 and self.botones[1]["accion"]:
                        self.botones[1]["accion"]()
                    elif event.key == pygame.K_c and len(self.botones) > 2 and self.botones[2]["accion"]:
                        self.botones[2]["accion"]()
                    elif event.key == pygame.K_d and len(self.botones) > 3 and self.botones[3]["accion"]:
                        self.botones[3]["accion"]()

            self.render()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = EmeraldGame()
    game.run()
