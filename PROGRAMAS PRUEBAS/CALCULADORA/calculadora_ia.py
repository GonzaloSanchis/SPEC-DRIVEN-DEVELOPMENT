"""
=============================================================================
CALCULADORA MODERNA DARK THEME (PYTHON + IA)
=============================================================================

REQUISITOS E INSTALACIÓN:
    1. Instala la librería customtkinter:
           pip install customtkinter pillow

CÓMO EJECUTAR EL SCRIPT:
    python calculadora_ia.py

CARACTERÍSTICAS:
    - Diseño moderno Dark Theme con tarjeta redondeada central.
    - Encabezados: 'PYTHON + IA' y 'El objetivo, en tus manos'.
    - Campos de entrada: 'Primer número' y 'Segundo número'.
    - Menú desplegable con operaciones: Sumar, Restar, Multiplicar, Dividir.
    - Botones con estilo exacto: 'Calcular' (verde esmeralda claro) y 'Limpiar' (gris oscuro).
    - Sección inferior con 'Resultado: —'.
    - Efecto visual emergente temporal (2 segundos) animado con un avatar/mascota
      digital guiñando el ojo al calcular.
=============================================================================
"""

import math
import customtkinter as ctk

# Configuración visual global
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class VentanaAnimacionGuino(ctk.CTkToplevel):
    """Ventana emergente que reproduce una animación digital de guiño durante exactamente 2 segundos."""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Procesando con IA")
        self.geometry("260x220")
        self.resizable(False, False)
        self.configure(fg_color="#18181f")

        # Mantener al frente y sin decoraciones pesadas
        self.attributes("-topmost", True)
        self.transient(parent)

        # Centrar respecto a la ventana principal
        parent.update_idletasks()
        px = parent.winfo_x() + (parent.winfo_width() // 2) - 130
        py = parent.winfo_y() + (parent.winfo_height() // 2) - 110
        self.geometry(f"+{px}+{py}")

        # Título superior
        lbl_info = ctk.CTkLabel(
            self,
            text="¡Cálculo procesado!",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            text_color="#2ed573"
        )
        lbl_info.pack(pady=(12, 6))

        # Canvas para dibujar el avatar digital animado con guiño
        import tkinter as tk
        self.canvas = tk.Canvas(self, width=120, height=120, bg="#18181f", highlightthickness=0)
        self.canvas.pack()

        self.fotograma = 0
        self.animar()

        # Cerrar automáticamente tras 2 segundos exactos (2000 ms)
        self.after(2000, self.destroy)

    def dibujar_avatar(self, ojo_derecho_cerrado=False):
        self.canvas.delete("all")
        cx, cy, r = 60, 60, 48

        # Cabeza (Avatar cibernético/asistente)
        self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="#2f3542", outline="#2ed573", width=3)

        # Ojo izquierdo (siempre abierto, brillante)
        self.canvas.create_oval(cx - 24, cy - 14, cx - 10, cy + 2, fill="#2ed573", outline="")
        self.canvas.create_oval(cx - 19, cy - 11, cx - 13, cy - 5, fill="#ffffff", outline="")

        # Ojo derecho (abierto o guiñando)
        if ojo_derecho_cerrado:
            # Ojo guiñado (arco curvo)
            self.canvas.create_arc(
                cx + 10, cy - 12, cx + 24, cy + 2,
                start=0, extent=180, style="arc", outline="#2ed573", width=3
            )
        else:
            # Ojo abierto
            self.canvas.create_oval(cx + 10, cy - 14, cx + 24, cy + 2, fill="#2ed573", outline="")
            self.canvas.create_oval(cx + 15, cy - 11, cx + 21, cy - 5, fill="#ffffff", outline="")

        # Sonrisa
        self.canvas.create_arc(
            cx - 16, cy + 4, cx + 16, cy + 26,
            start=190, extent=160, style="arc", outline="#ffffff", width=3
        )

    def animar(self):
        # Ciclo de animación: abrir -> guiño (cerrado) -> abrir
        if not self.winfo_exists():
            return

        if 4 <= self.fotograma <= 14:
            self.dibujar_avatar(ojo_derecho_cerrado=True)
        else:
            self.dibujar_avatar(ojo_derecho_cerrado=False)

        self.fotograma += 1
        self.after(80, self.animar)


class CalculadoraApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculadora - PYTHON + IA")
        self.geometry("440x600")
        self.resizable(False, False)
        self.configure(fg_color="#0e0e12")

        # Contenedor / Tarjeta redondeada central
        self.tarjeta = ctk.CTkFrame(
            self,
            fg_color="#18181f",
            corner_radius=20,
            border_width=1,
            border_color="#2b2b36"
        )
        self.tarjeta.pack(padx=25, pady=25, fill="both", expand=True)

        self.construir_interfaz()

    def construir_interfaz(self):
        # 1. Encabezados superiores
        self.lbl_titulo = ctk.CTkLabel(
            self.tarjeta,
            text="PYTHON + IA",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color="#ffffff"
        )
        self.lbl_titulo.pack(pady=(28, 2))

        self.lbl_subtitulo = ctk.CTkLabel(
            self.tarjeta,
            text="El objetivo, en tus manos",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color="#8a8a9e"
        )
        self.lbl_subtitulo.pack(pady=(0, 20))

        # Contenedor para los campos
        form_frame = ctk.CTkFrame(self.tarjeta, fg_color="transparent")
        form_frame.pack(padx=30, fill="x")

        # 2. Primer número
        lbl_n1 = ctk.CTkLabel(
            form_frame,
            text="Primer número",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color="#d0d0dc"
        )
        lbl_n1.pack(anchor="w", pady=(6, 2))

        self.entry_num1 = ctk.CTkEntry(
            form_frame,
            placeholder_text="Ej: 10",
            height=38,
            corner_radius=10,
            fg_color="#23232c",
            border_color="#363645",
            text_color="#ffffff"
        )
        self.entry_num1.pack(fill="x", pady=(0, 10))

        # 3. Operación (Combobox)
        lbl_op = ctk.CTkLabel(
            form_frame,
            text="Operación",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color="#d0d0dc"
        )
        lbl_op.pack(anchor="w", pady=(4, 2))

        self.combo_op = ctk.CTkComboBox(
            form_frame,
            values=["Sumar", "Restar", "Multiplicar", "Dividir"],
            height=38,
            corner_radius=10,
            fg_color="#23232c",
            button_color="#363645",
            border_color="#363645",
            dropdown_fg_color="#23232c",
            state="readonly"
        )
        self.combo_op.set("Sumar")
        self.combo_op.pack(fill="x", pady=(0, 10))

        # 4. Segundo número
        lbl_n2 = ctk.CTkLabel(
            form_frame,
            text="Segundo número",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color="#d0d0dc"
        )
        lbl_n2.pack(anchor="w", pady=(4, 2))

        self.entry_num2 = ctk.CTkEntry(
            form_frame,
            placeholder_text="Ej: 5",
            height=38,
            corner_radius=10,
            fg_color="#23232c",
            border_color="#363645",
            text_color="#ffffff"
        )
        self.entry_num2.pack(fill="x", pady=(0, 18))

        # 5. Botones de acción: 'Calcular' y 'Limpiar'
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(0, 15))

        self.btn_calcular = ctk.CTkButton(
            btn_frame,
            text="Calcular",
            command=self.calcular,
            fg_color="#2ed573",          # Verde esmeralda claro
            hover_color="#26af5f",
            text_color="#0e1b12",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            height=40,
            corner_radius=10
        )
        self.btn_calcular.pack(side="left", expand=True, fill="x", padx=(0, 6))

        self.btn_limpiar = ctk.CTkButton(
            btn_frame,
            text="Limpiar",
            command=self.limpiar,
            fg_color="#2f3542",          # Gris oscuro
            hover_color="#404859",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            height=40,
            corner_radius=10
        )
        self.btn_limpiar.pack(side="right", expand=True, fill="x", padx=(6, 0))

        # 6. Sección inferior: 'Resultado: —'
        self.lbl_resultado = ctk.CTkLabel(
            self.tarjeta,
            text="Resultado: —",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color="#a4b0be"
        )
        self.lbl_resultado.pack(pady=(10, 20))

    def calcular(self):
        txt1 = self.entry_num1.get().strip().replace(",", ".")
        txt2 = self.entry_num2.get().strip().replace(",", ".")

        if not txt1 or not txt2:
            self.lbl_resultado.configure(text="Resultado: Por favor, llena ambos campos", text_color="#ff6b6b")
            return

        try:
            n1 = float(txt1)
            n2 = float(txt2)
        except ValueError:
            self.lbl_resultado.configure(text="Resultado: Introduce valores válidos", text_color="#ff6b6b")
            return

        operacion = self.combo_op.get()

        if operacion == "Sumar":
            res = n1 + n2
        elif operacion == "Restar":
            res = n1 - n2
        elif operacion == "Multiplicar":
            res = n1 * n2
        elif operacion == "Dividir":
            if n2 == 0:
                self.lbl_resultado.configure(text="Resultado: No se puede dividir por cero", text_color="#ff6b6b")
                return
            res = n1 / n2
        else:
            res = 0

        # Formatear si es entero exacto
        if res.is_integer():
            res_str = str(int(res))
        else:
            res_str = f"{res:.4f}".rstrip("0").rstrip(".")

        self.lbl_resultado.configure(text=f"Resultado: {res_str}", text_color="#2ed573")

        # Disparar animación de guiño de 2 segundos exactos
        VentanaAnimacionGuino(self)

    def limpiar(self):
        self.entry_num1.delete(0, "end")
        self.entry_num2.delete(0, "end")
        self.combo_op.set("Sumar")
        self.lbl_resultado.configure(text="Resultado: —", text_color="#a4b0be")


if __name__ == "__main__":
    app = CalculadoraApp()
    app.mainloop()

