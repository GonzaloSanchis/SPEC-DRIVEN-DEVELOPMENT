# Spec-Driven Development (SDD): Unit Converter Application

## 1. Project Overview & Aesthetic Vision
This document outlines the technical specification for a Python-based unit converter supporting **millimeters (mm)**, **centimeters (cm)**, and **meters (m)**. 

To ensure the app looks **"beautiful"**, modern UI principles will be applied:
* **Layout:** Clean, card-based centered layout with ample padding and breathing room.
* **Color Palette:** Soft neutrals (slate/zinc) paired with an engaging primary accent (indigo/blue) for buttons and clear visual hierarchy.
* **Typography:** Modern, legible sans-serif font family.
* **Interactivity:** Smooth hover effects and clear status/error messages.

---

## 2. Functional Requirements

The graphical user interface (GUI) or frontend must contain the following components:
1. **Input Field:** A dedicated text box to enter the numeric value to be converted.
2. **Source Unit Selector:** A dropdown or selector to choose the starting unit (`Millimeters`, `Centimeters`, `Meters`).
3. **Target Unit Selector:** A dropdown or selector to choose the destination unit (`Millimeters`, `Centimeters`, `Meters`).
4. **Convert Button:** An action button to trigger the calculation and display the result nicely.
5. **Clear Button:** A reset button to wipe inputs, selectors, and results back to the default state.
6. **Result Display Area:** A stylish output card showing the converted value with its corresponding unit.

---

## 3. Mathematical Specifications & Formulas

All conversions are normalized through millimeters ($mm$) as the base unit for absolute precision.

* **Base Factors:**
  * $1 \text{ cm} = 10 \text{ mm}$
  * $1 \text{ m} = 1000 \text{ mm}$

* **Conversion Algorithm:**
  1. Convert input value $V_{in}$ from source unit to millimeters ($V_{mm}$):
     * If source is **mm**: $V_{mm} = V_{in}$
     * If source is **cm**: $V_{mm} = V_{in} \times 10$
     * If source is **m**: $V_{mm} = V_{in} \times 1000$

  2. Convert $V_{mm}$ to target unit ($V_{out}$):
     * If target is **mm**: $V_{out} = V_{mm}$
     * If target is **cm**: $V_{out} = \frac{V_{mm}}{10}$
     * If target is **m**: $V_{out} = \frac{V_{mm}}{1000}$

---

## 4. Python Implementation Reference

Below is a complete, beautifully styled Python script using `tkinter` and `ttkbootstrap` (or custom themed styles) to meet your layout and design criteria.

```python
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class UnitConverterApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Modern Unit Converter")
    self.root.geometry("450x520")
    self.root.config(bg="#f0f7ff")
    self.root.resizable(False, False)

    # Styling variables
    self.font_family = "Segoe UI"
    self.bg_color = "#f0f7ff"
    self.card_color = "#ffffff"
    self.primary_color = "#2563eb"  # Blue
    self.primary_hover = "#1d4ed8"
    self.text_color = "#1e293b"
    self.muted_color = "#64748b"

    self.create_widgets()

  def create_widgets(self):
    # Main container frame (Card effect)
    container = tk.Frame(
        self.root, bg=self.card_color, bd=0, highlightthickness=0
    )
    container.place(relx=0.5, rely=0.5, anchor="center", width=390, height=460)

    # Add a soft border / shadow illusion via frame nesting or padding
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
        text="Enter Value",
        font=(self.font_family, 10, "bold"),
        bg=self.card_color,
        fg=self.text_color,
    )
    lbl_value.pack(anchor="w", pady=(0, 5))

    self.entry_value = tk.Entry(
        inner_frame,
        font=(self.font_family, 12),
        bd=1,
        relief="solid",
        highlightcolor=self.primary_color,
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

    # To Unit
    lbl_to = tk.Label(
        selectors_frame,
        text="To",
        font=(self.font_family, 9, "bold"),
        bg=self.card_color,
        fg=self.muted_color,
    )
    lbl_to.grid(row=0, column=1, sticky="w", pady=(0, 3))

    self.to_unit_var = tk.StringVar(value="Centimeters (cm)")
    self.combo_to = ttk.Combobox(
        selectors_frame,
        textvariable=self.to_unit_var,
        values=["Millimeters (mm)", "Centimeters (cm)", "Meters (m)"],
        state="readonly",
        font=(self.font_family, 10),
    )
    self.combo_to.grid(row=1, column=1, sticky="ew", padx=(5, 0))

    selectors_frame.columnconfigure(0, weight=1)
    selectors_frame.columnconfigure(1, weight=1)

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
    self.btn_convert.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 5))

    self.btn_clear = tk.Button(
        btn_frame,
        text="Clear",
        font=(self.font_family, 10),
        bg="#e2e8f0",
        fg="#334155",
        activebackground="#cbd5e1",
        activeforeground="#1e293b",
        relief="flat",
        cursor="hand2",
        command=self.clear_fields,
    )
    self.btn_clear.pack(
        side="right", fill="x", expand=True, ipady=8, padx=(5, 0)
    )

    # Result Card Area
    self.result_frame = tk.Frame(inner_frame, bg="#f1f5f9", padx=10, pady=10)
    self.result_frame.pack(fill="x", pady=(5, 0))

    self.lbl_result_title = tk.Label(
        self.result_frame,
        text="Result",
        font=(self.font_family, 8, "bold"),
        bg="#f1f5f9",
        fg=self.muted_color,
    )
    self.lbl_result_title.pack(anchor="w")

    self.lbl_result_value = tk.Label(
        self.result_frame,
        text="---",
        font=(self.font_family, 14, "bold"),
        bg="#f1f5f9",
        fg=self.primary_color,
    )
    self.lbl_result_value.pack(anchor="w", pady=(2, 0))

  def perform_conversion(self):
    raw_input = self.entry_value.get().strip()
    if not raw_input:
      messagebox.showerror(
          "Error", "Please enter a value to convert.", parent=self.root
      )
      return

    try:
      val = float(raw_input)
    except ValueError:
      messagebox.showerror(
          "Invalid Input",
          "Please enter a valid numeric value.",
          parent=self.root,
      )
      return

    from_unit = self.from_unit_var.get()
    to_unit = self.to_unit_var.get()

    # Convert source to mm
    if "Millimeters" in from_unit:
      val_mm = val
    elif "Centimeters" in from_unit:
      val_mm = val * 10.0
    elif "Meters" in from_unit:
      val_mm = val * 1000.0
    else:
      val_mm = val

    # Convert mm to target unit
    if "Millimeters" in to_unit:
      result = val_mm
      unit_label = "mm"
    elif "Centimeters" in to_unit:
      result = val_mm / 10.0
      unit_label = "cm"
    elif "Meters" in to_unit:
      result = val_mm / 1000.0
      unit_label = "m"
    else:
      result = val_mm
      unit_label = ""

    # Format output nicely (remove redundant trailing zeros)
    formatted_result = (
        f"{result:g} {unit_label}"
        if isinstance(result, float)
        else f"{result} {unit_label}"
    )
    self.lbl_result_value.config(text=formatted_result)

  def clear_fields(self):
    self.entry_value.delete(0, tk.END)
    self.from_unit_var.set("Millimeters (mm)")
    self.to_unit_var.set("Centimeters (cm)")
    self.lbl_result_value.config(text="---")


if __name__ == "__main__":
  root = tk.Tk()
  app = UnitConverterApp(root)
  root.mainloop()
```

---

## 5. Next Steps & Questions
* Would you prefer this built as a web application (HTML/Tailwind CSS) or kept as a Python desktop script?
* Let me know if you'd like to add extra units like inches or feet!