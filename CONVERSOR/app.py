import sys
import tkinter as tk
from tkinter import ttk


# -------------------------------------------------------------
# LÓGICA DE CONVERSIÓN PURA (Común para GUI y CLI)
# -------------------------------------------------------------
UNIT_FACTORS_TO_MM = {
    "mm": 1.0,
    "cm": 10.0,
    "m": 1000.0,
    "millimeters": 1.0,
    "centimeters": 10.0,
    "meters": 1000.0,
}


def convert_units(value: float, from_unit: str, to_unit: str) -> float:
    """Convierte un valor numérico entre mm, cm y m basándose en mm como unidad base."""
    def normalize_unit(unit_str: str) -> str:
        s = unit_str.lower().strip()
        if "mm" in s or "milli" in s:
            return "mm"
        if "cm" in s or "centi" in s:
            return "cm"
        if "m" in s or "meter" in s or "metro" in s:
            return "m"
        raise ValueError(f"Unidad no soportada: {unit_str}")

    src = normalize_unit(from_unit)
    dst = normalize_unit(to_unit)

    val_mm = value * UNIT_FACTORS_TO_MM[src]
    val_out = val_mm / UNIT_FACTORS_TO_MM[dst]
    return val_out


# -------------------------------------------------------------
# MODO INTERFAZ GRÁFICA (GUI)
# -------------------------------------------------------------
class UnitConverterApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Modern Unit Converter")
        self.root.geometry("450x520")
        self.root.config(bg="#1a1a2e")
        self.root.resizable(False, False)

        # Styling variables (Dark Theme)
        self.font_family = "Segoe UI"
        self.bg_color = "#1a1a2e"
        self.card_color = "#16213e"
        self.primary_color = "#4f8ef7"  # Light Blue
        self.primary_hover = "#3b6fd4"  # Darker Blue
        self.text_color = "#ffffff"
        self.muted_color = "#a0aec0"
        self.error_color = "#fc8181"

        self.create_widgets()

    def validate_numeric_input(self, proposed_text):
        """Bloquea la entrada si no es un número válido (solo dígitos y a lo sumo un punto)."""
        if proposed_text == "":
            return True
        # Permitir números enteros o decimales con un único punto
        parts = proposed_text.split(".")
        if len(parts) > 2:
            return False
        return all(part == "" or part.isdigit() for part in parts)

    def create_widgets(self):
        # Main container frame (Card effect)
        container = tk.Frame(
            self.root, bg=self.card_color, bd=0, highlightthickness=0
        )
        container.place(
            relx=0.5, rely=0.5, anchor="center", width=390, height=460
        )

        # Inner frame with padding
        inner_frame = tk.Frame(container, bg=self.card_color, padx=25, pady=25)
        inner_frame.pack(fill="both", expand=True)

        # Title
        title_label = tk.Label(
            inner_frame,
            text="Unit Converter",
            font=(self.font_family, 20, "bold"),
            bg=self.card_color,
            fg=self.text_color,
        )
        title_label.pack(anchor="w", pady=(0, 5))

        subtitle_label = tk.Label(
            inner_frame,
            text="Convert mm, cm, and meters instantly",
            font=(self.font_family, 10),
            bg=self.card_color,
            fg=self.muted_color,
        )
        subtitle_label.pack(anchor="w", pady=(0, 20))

        # Value Input Section
        lbl_value = tk.Label(
            inner_frame,
            text="Enter Value (numbers only)",
            font=(self.font_family, 10, "bold"),
            bg=self.card_color,
            fg=self.text_color,
        )
        lbl_value.pack(anchor="w", pady=(0, 5))

        # Validación en tiempo real para no permitir caracteres no numéricos
        vcmd = (self.root.register(self.validate_numeric_input), "%P")

        self.entry_value = tk.Entry(
            inner_frame,
            font=(self.font_family, 12),
            bd=1,
            relief="solid",
            highlightcolor=self.primary_color,
            bg="#0f3460",
            fg="#ffffff",
            insertbackground="#ffffff",
            validate="key",
            validatecommand=vcmd,
        )
        self.entry_value.pack(fill="x", ipady=6, pady=(0, 15))

        # From & To Dropdowns in a grid
        selectors_frame = tk.Frame(inner_frame, bg=self.card_color)
        selectors_frame.pack(fill="x", pady=(0, 15))

        # From Unit
        lbl_from = tk.Label(
            selectors_frame,
            text="From",
            font=(self.font_family, 9, "bold"),
            bg=self.card_color,
            fg=self.muted_color,
        )
        lbl_from.grid(row=0, column=0, sticky="w", pady=(0, 3))

        self.from_unit_var = tk.StringVar(value="Millimeters (mm)")
        self.combo_from = ttk.Combobox(
            selectors_frame,
            textvariable=self.from_unit_var,
            values=["Millimeters (mm)", "Centimeters (cm)", "Meters (m)"],
            state="readonly",
            font=(self.font_family, 10),
        )
        self.combo_from.grid(row=1, column=0, sticky="ew", padx=(0, 5))

        # Swap Button (center column)
        self.btn_swap = tk.Button(
            selectors_frame,
            text="⇄",
            font=(self.font_family, 14, "bold"),
            bg=self.card_color,
            fg=self.primary_color,
            activebackground=self.card_color,
            activeforeground=self.primary_hover,
            relief="flat",
            cursor="hand2",
            command=self.swap_units,
        )
        self.btn_swap.grid(row=1, column=1, padx=2)

        # To Unit
        lbl_to = tk.Label(
            selectors_frame,
            text="To",
            font=(self.font_family, 9, "bold"),
            bg=self.card_color,
            fg=self.muted_color,
        )
        lbl_to.grid(row=0, column=2, sticky="w", pady=(0, 3))

        self.to_unit_var = tk.StringVar(value="Centimeters (cm)")
        self.combo_to = ttk.Combobox(
            selectors_frame,
            textvariable=self.to_unit_var,
            values=["Millimeters (mm)", "Centimeters (cm)", "Meters (m)"],
            state="readonly",
            font=(self.font_family, 10),
        )
        self.combo_to.grid(row=1, column=2, sticky="ew", padx=(5, 0))

        selectors_frame.columnconfigure(0, weight=1)
        selectors_frame.columnconfigure(1, weight=0)
        selectors_frame.columnconfigure(2, weight=1)

        # Buttons Frame (Convert & Clear)
        btn_frame = tk.Frame(inner_frame, bg=self.card_color)
        btn_frame.pack(fill="x", pady=(10, 15))

        self.btn_convert = tk.Button(
            btn_frame,
            text="Convert",
            font=(self.font_family, 10, "bold"),
            bg=self.primary_color,
            fg="white",
            activebackground=self.primary_hover,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.perform_conversion,
        )
        self.btn_convert.pack(
            side="left", fill="x", expand=True, ipady=8, padx=(0, 5)
        )

        self.btn_clear = tk.Button(
            btn_frame,
            text="Clear",
            font=(self.font_family, 10),
            bg="#2d3748",
            fg="#ffffff",
            activebackground="#4a5568",
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            command=self.clear_fields,
        )
        self.btn_clear.pack(
            side="right", fill="x", expand=True, ipady=8, padx=(5, 0)
        )

        # Result Card Area
        self.result_frame = tk.Frame(inner_frame, bg="#0f3460", padx=10, pady=10)
        self.result_frame.pack(fill="x", pady=(5, 0))

        self.lbl_result_title = tk.Label(
            self.result_frame,
            text="Result",
            font=(self.font_family, 8, "bold"),
            bg="#0f3460",
            fg=self.muted_color,
        )
        self.lbl_result_title.pack(anchor="w")

        self.lbl_result_value = tk.Label(
            self.result_frame,
            text="---",
            font=(self.font_family, 14, "bold"),
            bg="#0f3460",
            fg=self.primary_color,
        )
        self.lbl_result_value.pack(anchor="w", pady=(2, 0))

    def swap_units(self):
        """Intercambia las unidades 'From' y 'To' entre sí."""
        from_val = self.from_unit_var.get()
        to_val = self.to_unit_var.get()
        self.from_unit_var.set(to_val)
        self.to_unit_var.set(from_val)

    def perform_conversion(self):
        raw_input = self.entry_value.get().strip()
        if not raw_input:
            self.lbl_result_value.config(text="Introduce un número", fg=self.muted_color)
            return

        try:
            val = float(raw_input)
        except ValueError:
            self.lbl_result_value.config(text="Valor no válido", fg=self.error_color)
            return

        from_unit = self.from_unit_var.get()
        to_unit = self.to_unit_var.get()

        try:
            result = convert_units(val, from_unit, to_unit)
            unit_label = (
                "mm"
                if "Millimeters" in to_unit
                else ("cm" if "Centimeters" in to_unit else "m")
            )
            formatted_result = (
                f"{result:g} {unit_label}"
                if isinstance(result, float)
                else f"{result} {unit_label}"
            )
            self.lbl_result_value.config(text=formatted_result, fg=self.primary_color)
        except Exception:
            self.lbl_result_value.config(text="Error de conversión", fg=self.error_color)

    def clear_fields(self):
        self.entry_value.delete(0, tk.END)
        self.from_unit_var.set("Millimeters (mm)")
        self.to_unit_var.set("Centimeters (cm)")
        self.lbl_result_value.config(text="---", fg=self.primary_color)


# -------------------------------------------------------------
# MODO INTERACTIVO POR TERMINAL (CLI)
# -------------------------------------------------------------
def run_cli_interactive():
    print("=" * 45)
    print("   CONVERSOR DE UNIDADES (MM / CM / M)")
    print("=" * 45)
    print("Unidades disponibles: mm (milímetros), cm (centímetros), m (metros)")
    print("Escribe 'salir' para finalizar.\n")

    units_map = {
        "1": "mm",
        "mm": "mm",
        "milimetros": "mm",
        "milímetros": "mm",
        "2": "cm",
        "cm": "cm",
        "centimetros": "cm",
        "centímetros": "cm",
        "3": "m",
        "m": "m",
        "metros": "m",
    }

    while True:
        try:
            raw_val = input("Introduce el valor a convertir (o 'salir'): ").strip()
            if raw_val.lower() in ("salir", "exit", "q"):
                print("¡Hasta luego!")
                break
            if not raw_val:
                continue

            try:
                val = float(raw_val)
            except ValueError:
                # No se reproduce sonido ni modal molesto; mensaje limpio
                continue

            print("Opciones de unidad: [1] mm  [2] cm  [3] m")
            from_u = input("Unidad origen: ").strip().lower()
            if from_u not in units_map:
                continue

            to_u = input("Unidad destino: ").strip().lower()
            if to_u not in units_map:
                continue

            res = convert_units(val, units_map[from_u], units_map[to_u])
            print(
                f"\n✔ Resultado: {val:g} {units_map[from_u]} = {res:g} {units_map[to_u]}\n"
            )
            print("-" * 45)

        except (KeyboardInterrupt, EOFError):
            print("\nOperación cancelada. ¡Hasta luego!")
            break


# -------------------------------------------------------------
# PUNTO DE ENTRADA
# -------------------------------------------------------------
if __name__ == "__main__":
    if "--cli" in sys.argv:
        run_cli_interactive()
    else:
        try:
            root = tk.Tk()
            app = UnitConverterApp(root)
            root.mainloop()
        except Exception:
            run_cli_interactive()
