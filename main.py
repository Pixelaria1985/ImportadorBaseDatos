import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

# Configura aquí tus datos de conexión a MySQL
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_PATH = "C:/xampp/mysql/bin/mysql.exe"  # Ajusta si tienes otra ruta

class SQLImporterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Importar archivo SQL a XAMPP")
        self.root.geometry("550x250")

        self.sql_file_path = tk.StringVar()
        self.db_name = tk.StringVar()

        tk.Label(root, text="Nombre de la base de datos:").pack(pady=5)
        self.db_entry = tk.Entry(root, textvariable=self.db_name, width=50)
        self.db_entry.pack(pady=5)

        tk.Label(root, text="Archivo SQL:").pack(pady=5)
        self.file_entry = tk.Entry(root, textvariable=self.sql_file_path, width=50)
        self.file_entry.pack(pady=5)

        tk.Button(root, text="Seleccionar archivo", command=self.select_file).pack(pady=5)
        tk.Button(root, text="Crear base de datos e importar", command=self.create_db_and_import).pack(pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos SQL", "*.sql")])
        if file_path:
            self.sql_file_path.set(file_path)

    def create_db_and_import(self):
        db_name = self.db_name.get().strip()
        file_path = self.sql_file_path.get().strip()

        if not db_name:
            messagebox.showerror("Error", "Por favor ingresa un nombre para la base de datos.")
            return

        if not os.path.exists(file_path):
            messagebox.showerror("Error", "Archivo SQL no encontrado.")
            return

        if not os.path.exists(MYSQL_PATH):
            messagebox.showerror("Error", "No se encontró mysql.exe en la ruta especificada.")
            return

        # Comando para crear la base de datos si no existe
        create_db_command = f'"{MYSQL_PATH}" -u{MYSQL_USER} {"-p" + MYSQL_PASSWORD if MYSQL_PASSWORD else ""} -e "CREATE DATABASE IF NOT EXISTS {db_name};"'
        import_command = f'"{MYSQL_PATH}" -u{MYSQL_USER} {"-p" + MYSQL_PASSWORD if MYSQL_PASSWORD else ""} {db_name} < "{file_path}"'

        try:
            subprocess.run(create_db_command, shell=True, check=True)
            result = subprocess.run(import_command, shell=True, stderr=subprocess.PIPE, text=True)

            if result.returncode == 0:
                messagebox.showinfo("Éxito", f"La base de datos '{db_name}' fue creada/importada correctamente.")
            else:
                messagebox.showerror("Error al importar", f"Ocurrió un error:\n{result.stderr}")

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error al ejecutar comandos MySQL", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = SQLImporterApp(root)
    root.mainloop()
