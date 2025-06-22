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

        # Contadores de puntos
        self.label_total = tk.Label(self.root, text="Total points: 0", font=("Segoe UI", 12), bg="#ecf0f1", fg="#2c3e50")
        self.label_total.pack()

        self.label_filtered = tk.Label(self.root, text="Filtered points: 0", font=("Segoe UI", 12), bg="#ecf0f1", fg="#2c3e50")
        self.label_filtered.pack()

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

    def detectar_duplicados(self):
        if self.df is None:
            return
        
        duplicados = self.df.duplicated()
        cantidad = duplicados.sum()

        if cantidad > 0:
            respuesta = messagebox.askyesno("Puntos duplicados", f"Se detectaron {cantidad} puntos duplicados.\n¿Deseas eliminarlos?")
            
            if respuesta:
                self.df = self.df.drop_duplicates().reset_index(drop=True)
                messagebox.showinfo("Limpieza completada", f"Se eliminaron {cantidad} duplicados.")
            else:
                messagebox.showinfo("Aviso", "Los duplicados se han conservado")
            
    def import_txt(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de texto o CSV", "*.txt *.csv")])
        if not file_path:
            return

        # Preguntar formato de entrada
        formato = tk.StringVar()

        def seleccionar_formato():
            ventana.destroy()

        ventana = tk.Toplevel(self.root)
        ventana.title("Seleccionar formato de archivo")
        ventana.geometry("400x300")
        ventana.grab_set()
        tk.Label(ventana, text="¿Qué formato tiene el archivo?", font=("Segoe UI", 12)).pack(pady=20)

        formatos = [ ("PNEZD (Punto, Norte, Este, Cota, Descripción)", "PNEZD"),("PENZD (Punto, Este, Norte, Cota, Descripción)", "PENZD"),("ENZD (Este, Norte, Cota, Descripción)", "ENZD"),("NEZD (Norte, Este, Cota, Descripción)", "NEZD"),]

        for texto, valor in formatos:
            tk.Radiobutton(ventana, text=texto, variable=formato, value=valor, font=("Segoe UI", 11)).pack(anchor="w", padx=20)
        
        tk.Button(ventana, text="Aceptar", command=seleccionar_formato, bg="#00b894", fg="white").pack(pady=10)
        ventana.wait_window()

        if not formato.get():
            return

        try:           
            if formato.get() in ["PNEZD", "PENZD"]:
                columnas = ["Punto", "A", "B", "Z", "Descripción"] #A y B Serán Intercambiados
            else: #ENZD o NEZD
                columnas = ["A", "B", "Z", "Descripción"]

            df = pd.read_csv(file_path, sep=',', header=None, names=columnas)

            #asignar columnas x, y dependiendo formato
            if formato.get() == "PNEZD":
                df.rename(columns={"A": "Y", "B": "X"}, inplace=True)
            elif formato.get() == "PENZD":
                df.rename(columns={"A": "X", "B": "Y"}, inplace=True)  # Este = X, Norte = Y
            elif formato.get() == "ENZD":
                df.rename(columns={"A": "X", "B": "Y"}, inplace=True)  # Este = X, Norte = Y
            elif formato.get() == "NEZD":
                df.rename(columns={"A": "Y", "B": "X"}, inplace=True)  # Norte = Y, Este = X

            columnas_validas = ["X", "Y", "Z"]
            if "Descripción" in df.columns and not df["Descripción"].isnull().all():
                columnas_validas.append("Descripción")
            
            self.df = df[columnas_validas].dropna(subset=["X", "Y", "Z"])
            self.filtered_df = None
                
            self.detectar_duplicados()
            self.plot_points(self.df)

            self.label_total.config(text=f"Total points: {len(self.df)}")
            self.label_filtered.config(text="Filtered points: 0")

            for field in ["xmin", "xmax", "ymin", "ymax"]:
                getattr(self, f"entry_{field}").delete(0, tk.END)

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
        self.label_filtered.config(text=f"Filtered points: {len(self.filtered_df)}")

    def export_txt(self):
        if self.df is None:
            messagebox.showwarning("Advertencia", "Primero debes importar un archivo.")
            return

        data_to_export = self.filtered_df if self.filtered_df is not None else self.df

        # Seleccionar formato
        formato = tk.StringVar()
        delimitador = tk.StringVar()

        def confirmar():
            opciones.destroy()

        opciones = tk.Toplevel(self.root)
        opciones.title("Opciones de Exportación")
        opciones.geometry("400x400")
        opciones.grab_set()

        tk.Label(opciones, text="Selecciona el formato de exportación:", font=("Segoe UI", 12)).pack(pady=10)

        formatos = [("PNEZD (Punto, Norte, Este, Cota, Descripción)", "PNEZD"), ("PENZD (Punto, Este, Norte, Cota, Descripción)", "PENZD"), ("ENZD (Este, Norte, Cota, Descripción)", "ENZD"), ("NEZD (Norte, Este, Cota, Descripción)", "NEZD")]

        for texto, valor in formatos:
            tk.Radiobutton(opciones, text=texto, variable=formato, value=valor).pack(anchor="w", padx=20)

        tk.Label(opciones, text="Selecciona el delimitador:", font=("Segoe UI", 12)).pack(pady=10)

        delimitadores = [("Coma (,)", ","), ("Punto y coma (;)", ";"), ("Espacio", " ")]

        for texto, valor in delimitadores:
            tk.Radiobutton(opciones, text=texto, variable=delimitador, value=valor).pack(anchor="w", padx=20)

        tk.Button(opciones, text="Aceptar", command=confirmar, bg="#0984e3", fg="white").pack(pady=20)

        opciones.wait_window()

        if not formato.get() or not delimitador.get():
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("TXT Files", "*.txt")])
        if not file_path:
            return

        try:
            export_df = pd.DataFrame()

            if formato.get() == "PNEZD":
                export_df["Punto"] = range(1, len(data_to_export) + 1)
                export_df["Norte"] = data_to_export["Y"]
                export_df["Este"] = data_to_export["X"]
                export_df["Cota"] = data_to_export["Z"]
                if "Descripción" in data_to_export.columns:
                    export_df["Descripción"] = data_to_export["Descripción"]

            elif formato.get() == "PENZD":
                export_df["Punto"] = range(1, len(data_to_export) + 1)
                export_df["Este"] = data_to_export["X"]
                export_df["Norte"] = data_to_export["Y"]
                export_df["Cota"] = data_to_export["Z"]
                if "Descripción" in data_to_export.columns:
                    export_df["Descripción"] = data_to_export["Descripción"]

            elif formato.get() == "ENZD":
                export_df["Este"] = data_to_export["X"]
                export_df["Norte"] = data_to_export["Y"]
                export_df["Cota"] = data_to_export["Z"]
                if "Descripción" in data_to_export.columns:
                    export_df["Descripción"] = data_to_export["Descripción"]

            elif formato.get() == "NEZD":
                export_df["Norte"] = data_to_export["Y"]
                export_df["Este"] = data_to_export["X"]
                export_df["Cota"] = data_to_export["Z"]
                if "Descripción" in data_to_export.columns:
                    export_df["Descripción"] = data_to_export["Descripción"]

            export_df.to_csv(file_path, sep=delimitador.get(), index=False, header=False)

            messagebox.showinfo("Éxito", f"Archivo exportado correctamente:\n{file_path}")

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
    