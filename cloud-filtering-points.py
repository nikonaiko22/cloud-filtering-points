import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class PointFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Filtrado de Nube de Puntos (X, Y, Z)")
        self.root.geometry("1000x700")
        self.root.configure(bg="#ecf0f1")

        self.df = None
        self.filtered_df = None

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self.root, text="Filtrado Inteligente de Nube de Puntos",
                         font=("Segoe UI", 22, "bold"), bg="#ecf0f1", fg="#2c3e50")
        title.pack(pady=10)

        frame_controls = tk.Frame(self.root, bg="#dfe6e9")
        frame_controls.pack(pady=10)

        # Botón importar
        btn_import = tk.Button(frame_controls, text="Importar TXT", font=("Segoe UI", 12),
                               command=self.import_txt, bg="#0984e3", fg="white")
        btn_import.grid(row=0, column=0, padx=10, pady=5)

        # Entradas de límites
        for i, label in enumerate(["Xmin", "Xmax", "Ymin", "Ymax"]):
            tk.Label(frame_controls, text=label, font=("Segoe UI", 12), bg="#dfe6e9").grid(row=0, column=1 + i * 2)
            entry = tk.Entry(frame_controls, width=8)
            entry.grid(row=0, column=2 + i * 2)
            setattr(self, f"entry_{label.lower()}", entry)

        # Botón Filtrar
        btn_filter = tk.Button(frame_controls, text="Filtrar", font=("Segoe UI", 12),
                               command=self.filtrar_puntos, bg="#00b894", fg="white")
        btn_filter.grid(row=0, column=9, padx=10, pady=5)

        # Botón exportar
        btn_export = tk.Button(frame_controls, text="Exportar TXT", font=("Segoe UI", 12),
                               command=self.export_txt, bg="#6c5ce7", fg="white")
        btn_export.grid(row=0, column=10, padx=10, pady=5)

        # Gráfico matplotlib
        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(pady=10)

    def import_txt(self):
        file_path = filedialog.askopenfilename(filetypes=[("TXT Files", "*.txt")])
        if file_path:
            try:
                self.df = pd.read_csv(file_path, sep=r'\s+', engine='python', header=None, names=["X", "Y", "Z"])
                self.filtered_df = None
                self.plot_points(self.df)
                messagebox.showinfo("Éxito", "Archivo importado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo:\n{e}")

    def filtrar_puntos(self):
        if self.df is None:
            messagebox.showwarning("Advertencia", "Primero debes importar un archivo.")
            return

        try:
            xmin = float(self.entry_xmin.get())
            xmax = float(self.entry_xmax.get())
            ymin = float(self.entry_ymin.get())
            ymax = float(self.entry_ymax.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos.")
            return

    # Validar que los límites estén bien definidos
        if xmin > xmax or ymin > ymax:
            messagebox.showwarning("Límites inválidos", "Los valores de mínimo no pueden ser mayores que los de máximo.\n" "Verifica Xmin < Xmax y Ymin < Ymax.")
            return
        
        self.filtered_df = self.df[
            (self.df["X"] >= xmin) & (self.df["X"] <= xmax) &
            (self.df["Y"] >= ymin) & (self.df["Y"] <= ymax)
        ]
        self.plot_points(self.filtered_df, title="Puntos Filtrados")

    def export_txt(self):
        if self.filtered_df is None or self.filtered_df.empty:
            messagebox.showwarning("Advertencia", "No hay puntos filtrados para exportar.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("TXT Files", "*.txt")])
        if file_path:
            try:
                self.filtered_df.to_csv(file_path, sep='\t', index=False, header=False)
                messagebox.showinfo("Éxito", f"Archivo exportado:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar el archivo:\n{e}")

    def plot_points(self, df, title="Puntos Originales"):
        self.ax.clear()

        # Mostrar cuadrícula con estilo suave
        self.ax.grid(True, linestyle="--", alpha=0.3)

        # Dibujar puntos con tamaño aumentado, borde negro y zorder para que estén sobre la cuadrícula
        self.ax.scatter(df["X"], df["Y"], s=30, alpha=0.8, c="dodgerblue", edgecolors="black", linewidths=0.5, zorder=3)

        self.ax.set_title(title, fontsize=14, fontweight="bold")
        self.ax.set_xlabel("X", fontsize=12)
        self.ax.set_ylabel("Y", fontsize=12)

        # Ajuste automático de ejes con margen
        x_margin = (df["X"].max() - df["X"].min()) * 0.05
        y_margin = (df["Y"].max() - df["Y"].min()) * 0.05

        self.ax.set_xlim(df["X"].min() - x_margin, df["X"].max() + x_margin)
        self.ax.set_ylim(df["Y"].min() - y_margin, df["Y"].max() + y_margin)

        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = PointFilterApp(root)
    root.mainloop()
