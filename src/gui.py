# src/gui.py (VERSIÓN CON ESTILOS Y DISPOSICIÓN SIMILAR A LA IMAGEN)
import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk
import os
import sys
import re # Para procesar la entrada de soluciones y detectar complejos


# Importar las funciones de nuestros módulos
from src.problem_generator import generate_random_problem
from src.quadratic_solver import solve_quadratic_equation
from src.validation_utils import parse_user_solution, compare_solutions

class QuadraticFormulaApp:
    def __init__(self, master):
        self.master = master
        master.title("Calculadora y Ejercicios de Fórmula General")
        master.geometry("1200x800") # Un tamaño inicial que permita ver ambos paneles
        master.resizable(True, True) # Permitir redimensionar para mayor flexibilidad

        # --- Colores y Fuentes (Basados en la imagen proporcionada) ---
        self.bg_color_main = "#FFFFFF" # Gris claro de fondo general
        self.bg_color_left_panel = "#F4C6EC" # Rosado claro / Lavanda para el panel izquierdo
        self.bg_color_right_sections = "#FFFFFF" # Blanco para las secciones del panel derecho
        self.bg_color_header = "#F4C6EC" # Morado claro para los títulos de sección
        self.text_color_header = "#69003C" # Morado oscuro para texto de títulos
        self.button_bg_color = "#B93142" # Rosa vibrante para botones
        self.button_fg_color = "#FFFFFF" # Texto blanco en botones
        self.border_color = "#69003C" # Gris para bordes de frames/widgets
        self.success_color = "#4CAF50" # Verde para mensajes de éxito
        self.error_color = "#D32F2F" # Rojo para mensajes de error
        self.info_color = "#1976D2" # Azul para información

        self.font_title = ("Arial", 18, "bold")
        self.font_section_header = ("Arial", 14, "bold")
        self.font_problem = ("Consolas", 16, "bold") # Monoespaciado para la ecuación
        self.font_input = ("Arial", 12)
        self.font_button = ("Arial", 12, "bold")
        self.font_feedback = ("Arial", 10, "italic")
        self.font_solution = ("Consolas", 12, "bold") # Monoespaciado para soluciones
        self.font_procedure = ("Consolas", 10) # Monoespaciado para el procedimiento

        master.configure(bg=self.bg_color_main)

        self.a, self.b, self.c = None, None, None
        self.correct_solutions = None
        self.procedure_text = ""
        self.discriminant_value = None

        self._create_widgets()
        self.load_formula_image()

    def _get_asset_path(self, relative_path):
        """Obtiene la ruta absoluta de un recurso dentro de la carpeta 'assets'."""
        try:
            # PyInstaller crea un atributo _MEIPASS para el directorio temporal
            base_path = sys._MEIPASS
        except AttributeError:
            # Si no está empaquetado, estamos en el entorno de desarrollo
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        
        return os.path.join(base_path, relative_path)

    def _create_widgets(self):
        # --- Frame Principal que contendrá los dos paneles laterales ---
        main_layout_frame = tk.Frame(self.master, bg=self.bg_color_main)
        main_layout_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Configurar las columnas para expansión (2 columnas)
        main_layout_frame.grid_columnconfigure(0, weight=1) # Columna izquierda: 1/3 de ancho
        main_layout_frame.grid_columnconfigure(1, weight=2) # Columna derecha: 2/3 de ancho
        main_layout_frame.grid_rowconfigure(0, weight=1) # Fila única que se expande

        # --- Panel Izquierdo ---
        left_panel = tk.Frame(main_layout_frame, bg=self.bg_color_left_panel, bd=2, relief="flat", padx=15, pady=15)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        left_panel.grid_rowconfigure(0, weight=0) # Para el título "Fórmula General"
        left_panel.grid_rowconfigure(1, weight=0) # Para la imagen
        left_panel.grid_rowconfigure(2, weight=1) # Espacio flexible (botones abajo)

        tk.Label(left_panel, text="Fórmula General", font=self.font_section_header,
                 bg=self.bg_color_left_panel, fg=self.text_color_header).grid(row=0, column=0, pady=(0,10))

        # Contenedor para la imagen de la fórmula
        formula_image_container = tk.Frame(left_panel, bg=self.bg_color_left_panel)
        formula_image_container.grid(row=1, column=0, pady=(10, 20))
        self.formula_label = tk.Label(formula_image_container, bg=self.bg_color_left_panel)
        self.formula_label.pack()

        # Frame para los botones (centrados y con padding)
        button_frame_left = tk.Frame(left_panel, bg=self.bg_color_left_panel)
        button_frame_left.grid(row=2, column=0, sticky="n", pady=(20,0)) # Alineado arriba en su celda, deja espacio abajo

        btn_width = 20 # Ancho fijo para los botones

        tk.Button(button_frame_left, text="Generar nuevo problema", command=self.generate_problem,
                  font=self.font_button, bg=self.button_bg_color, fg=self.button_fg_color,
                  width=btn_width, height=2, bd=0, relief="flat").pack(pady=5)

        tk.Button(button_frame_left, text="Calificar", command=self.check_solution,
                  font=self.font_button, bg=self.button_bg_color, fg=self.button_fg_color,
                  width=btn_width, height=2, bd=0, relief="flat").pack(pady=5)

        tk.Button(button_frame_left, text="Mostrar Solución", command=self.display_correct_solution_and_procedure,
                  font=self.font_button, bg=self.button_bg_color, fg=self.button_fg_color,
                  width=btn_width, height=2, bd=0, relief="flat").pack(pady=5)
        
        tk.Button(button_frame_left, text="Mostrar Procedimiento", command=self.display_procedure_only,
                  font=self.font_button, bg=self.button_bg_color, fg=self.button_fg_color,
                  width=btn_width, height=2, bd=0, relief="flat").pack(pady=5)
        
        tk.Button(button_frame_left, text="Discriminante", command=self.display_discriminant_only,
                  font=self.font_button, bg=self.button_bg_color, fg=self.button_fg_color,
                  width=btn_width, height=2, bd=0, relief="flat").pack(pady=5)


        # --- Panel Derecho ---
        right_panel = tk.Frame(main_layout_frame, bg=self.bg_color_main)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        right_panel.grid_rowconfigure(0, weight=0) # Problema
        right_panel.grid_rowconfigure(1, weight=0) # Entrada
        right_panel.grid_rowconfigure(2, weight=0) # Solución
        right_panel.grid_rowconfigure(3, weight=1) # Procedimiento 
        right_panel.grid_rowconfigure(4, weight=0) # Discriminante

        # --- Sección: Problema actual ---
        problem_section = tk.Frame(right_panel, bg=self.bg_color_right_sections, bd=1, relief="solid")
        problem_section.pack(fill=tk.X, pady=5, padx=5)

        tk.Label(problem_section, text="Problema actual", font=self.font_section_header,
                 bg=self.bg_color_header, fg=self.text_color_header, width=50).pack(fill=tk.X, pady=(0, 5))
        
        self.problem_label = tk.Label(problem_section, text="Haz clic en 'Generar nuevo problema'",
                                      font=self.font_problem, bg=self.bg_color_right_sections, fg=self.text_color_header)
        self.problem_label.pack(pady=15)

        # --- Sección: Ingresa la solución ---
        input_section = tk.Frame(right_panel, bg=self.bg_color_right_sections, bd=1, relief="solid")
        input_section.pack(fill=tk.X, pady=5, padx=5)

        tk.Label(input_section, text="Ingresa la solución", font=self.font_section_header,
                 bg=self.bg_color_header, fg=self.text_color_header, width=50).pack(fill=tk.X, pady=(0, 5))
        
        self.user_input_entry = tk.Entry(input_section, font=self.font_input, width=40, bd=2, relief="solid")
        self.user_input_entry.pack(pady=10)
        self.feedback_label = tk.Label(input_section, text="", font=self.font_feedback, bg=self.bg_color_right_sections)
        self.feedback_label.pack(pady=(0,10))

        # --- Sección: Solución ---
        self.solution_section = tk.Frame(right_panel, bg=self.bg_color_right_sections, bd=1, relief="solid")
        self.solution_section.pack(fill=tk.X, pady=5, padx=5) # Inicialmente visible

        tk.Label(self.solution_section, text="Solución", font=self.font_section_header,
                 bg=self.bg_color_header, fg=self.text_color_header, width=50).pack(fill=tk.X, pady=(0, 5))
        
        self.correct_solution_label = tk.Label(self.solution_section, text="N/A",
                                              font=self.font_solution, bg=self.bg_color_right_sections, fg=self.text_color_header)
        self.correct_solution_label.pack(pady=15)

        # --- Sección: Procedimiento ---
        self.procedure_section = tk.Frame(right_panel, bg=self.bg_color_right_sections, bd=1, relief="solid")
        self.procedure_section.pack(fill=tk.BOTH, expand=True, pady=5, padx=5) # Esto debe expandirse

        tk.Label(self.procedure_section, text="Procedimiento", font=self.font_section_header,
                 bg=self.bg_color_header, fg=self.text_color_header, width=50).pack(fill=tk.X, pady=(0, 5))
        
        self.procedure_text_widget = scrolledtext.ScrolledText(self.procedure_section, wrap=tk.WORD,
                                                               font=self.font_procedure,
                                                               bg="#F8F8F8", fg="#333333", bd=1, relief="solid",
                                                               padx=10, pady=10)
        self.procedure_text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.procedure_text_widget.config(state=tk.DISABLED)

        # --- Sección: Discriminante ---
        self.discriminant_section = tk.Frame(right_panel, bg=self.bg_color_right_sections, bd=1, relief="solid")
        self.discriminant_section.pack(fill=tk.X, pady=5, padx=5) # Inicialmente visible

        tk.Label(self.discriminant_section, text="Discriminante", font=self.font_section_header,
                 bg=self.bg_color_header, fg=self.text_color_header, width=50).pack(fill=tk.X, pady=(0, 5))
        
        self.discriminant_label = tk.Label(self.discriminant_section, text="N/A",
                                           font=self.font_solution, bg=self.bg_color_right_sections, fg=self.text_color_header)
        self.discriminant_label.pack(pady=15)
        
        # Ocultar secciones al inicio, solo se mostrarán con los botones específicos
        self.hide_all_result_sections()


    def load_formula_image(self):
        """Carga y muestra la imagen de la fórmula."""
        try:
            image_path = self._get_asset_path('assets/formula_image.jpg')
            img = Image.open(image_path)
            # Asegurar que la imagen es pequeña y de buena calidad para la GUI
            img = img.resize((int(img.width * 0.3), int(img.height * 0.3)), Image.Resampling.LANCZOS) # Reducir un poco
            self.formula_photo = ImageTk.PhotoImage(img)
            self.formula_label.config(image=self.formula_photo)
        except FileNotFoundError:
            messagebox.showerror("Error de Imagen", f"No se encontró la imagen: {image_path}. Asegúrate de que 'formula_image.png' esté en la carpeta 'assets'.")
        except Exception as e:
            messagebox.showerror("Error de Imagen", f"No se pudo cargar la imagen: {e}")

    def generate_problem(self):
        """Genera un nuevo problema aleatorio y actualiza la interfaz."""
        self.a, self.b, self.c = generate_random_problem()
        
        # Formatear la ecuación para mostrarla
        problem_str = ""
        if self.a == 1:
            problem_str += "x²"
        elif self.a == -1:
            problem_str += "-x²"
        else:
            problem_str += f"{self.a}x²"

        if self.b > 0:
            problem_str += f" + {self.b}x"
        elif self.b < 0:
            problem_str += f" - {abs(self.b)}x"

        if self.c > 0:
            problem_str += f" + {self.c}"
        elif self.c < 0:
            problem_str += f" - {abs(self.c)}"
        
        problem_str += " = 0"

        self.problem_label.config(text=problem_str)
        
        # Resolver el problema para obtener la solución correcta y el procedimiento
        self.correct_solutions, self.procedure_text = solve_quadratic_equation(self.a, self.b, self.c)
        
        # Limpiar campos anteriores y ocultar resultados
        self.user_input_entry.delete(0, tk.END)
        self.feedback_label.config(text="")
        self.hide_all_result_sections() # Ocultar resultados al generar nuevo problema

        # Actualizar discriminante para mostrarlo si se pulsa el botón
        if isinstance(self.correct_solutions, tuple) and len(self.correct_solutions) in [1, 2]:
            # Extraer discriminante del procedimiento (un poco hacky pero funciona)
            match = re.search(r"Δ = (-?\d+(\.\d+)?)\n", self.procedure_text)
            if match:
                self.discriminant_value = float(match.group(1))
            else:
                self.discriminant_value = "No calculado"
        else:
            self.discriminant_value = "N/A" # Para casos como a=0 o sin solución

        self.discriminant_label.config(text=str(self.discriminant_value)) # Asegurar que se actualice

    def hide_all_result_sections(self):
        """Oculta las secciones de solución, procedimiento y discriminante."""
        self.solution_section.pack_forget()
        self.procedure_section.pack_forget()
        self.discriminant_section.pack_forget()

    def check_solution(self):
        """Comprueba la solución ingresada por el usuario."""
        if self.a is None:
            messagebox.showwarning("No hay problema", "Por favor, genera un problema primero.")
            return

        user_input_str = self.user_input_entry.get()
        user_parsed_solutions = parse_user_solution(user_input_str)

        if user_parsed_solutions is None:
            self.feedback_label.config(text="Formato de entrada inválido. Ej: -5, 5 o 1+2i", fg=self.error_color)
            self.hide_all_result_sections() # Ocultar si la entrada es inválida
            return

        is_correct = compare_solutions(user_parsed_solutions, self.correct_solutions)

        if is_correct:
            self.feedback_label.config(text="¡Correcto! :) ", fg=self.success_color)
        else:
            self.feedback_label.config(text="Resultado incorrecto. Vuelve a intentarlo. :)", fg=self.error_color)
        self.display_correct_solution() 

    def display_correct_solution(self):
        """Muestra la sección de solución y su valor."""
        self.hide_all_result_sections()
        self.solution_section.pack(fill=tk.X, pady=5, padx=5)

        sol_str = ""
        if isinstance(self.correct_solutions, tuple):
            if not self.correct_solutions:
                sol_str = "No hay soluciones numéricas."
            elif len(self.correct_solutions) == 1:
                if isinstance(self.correct_solutions[0], (float, int)):
                    sol_str = f"x = {self.correct_solutions[0]:.4f}"
                else: # asume complejo
                    sol_str = f"x = {self.correct_solutions[0]}"
            elif len(self.correct_solutions) == 2:
                sol_parts = []
                for s in self.correct_solutions:
                    if isinstance(s, (float, int)):
                        sol_parts.append(f"{s:.4f}")
                    else: # asume complejo
                        sol_parts.append(str(s))
                sol_str = f"x1 = {sol_parts[0]}, x2 = {sol_parts[1]}"
        elif self.correct_solutions == "infinitas":
            sol_str = "Infinitas soluciones"
        elif self.correct_solutions == "sin_solucion":
            sol_str = "No tiene solución"
        else:
            sol_str = "Error al determinar la solución."

        self.correct_solution_label.config(text=sol_str, fg=self.info_color)

    def display_procedure_only(self):
        """Muestra solo la sección del procedimiento."""
        if self.a is None:
            messagebox.showwarning("Sin Problema", "Por favor, genera un problema primero.")
            return

        self.hide_all_result_sections()
        self.procedure_section.pack(fill=tk.BOTH, expand=True, pady=5, padx=5)

        self.procedure_text_widget.config(state=tk.NORMAL)
        self.procedure_text_widget.delete(1.0, tk.END)
        self.procedure_text_widget.insert(tk.END, self.procedure_text)
        self.procedure_text_widget.config(state=tk.DISABLED)

    def display_discriminant_only(self):
        """Muestra solo la sección del discriminante."""
        if self.a is None:
            messagebox.showwarning("Sin Problema", "Por favor, genera un problema primero.")
            return
            
        self.hide_all_result_sections()
        self.discriminant_section.pack(fill=tk.X, pady=5, padx=5)
        self.discriminant_label.config(text=str(self.discriminant_value), fg=self.info_color)


    # Este método se llama desde el botón "Mostrar Solución"
    # Asegúrate de que este se llama para la lógica de los botones si quieres que los botones
    # individuales muestren sus secciones.
    def display_correct_solution_and_procedure(self):
        """
        Este método es una versión para el botón "Mostrar Solución" que ahora solo llama
        a display_correct_solution(). Si se quiere que este botón muestre AMBOS,
        entonces se debería modificar su lógica y llamar a pack() para ambos frames.
        Por el diseño de la imagen, cada botón es individual.
        """
        if self.a is None:
            messagebox.showwarning("Sin Problema", "Por favor, genera un problema primero.")
            return
        
        # Según la imagen, el botón "Mostrar Solución" solo muestra la sección de Solución
        self.display_correct_solution()
        # Si quisieras que mostrara también el procedimiento, descomentarías:
        self.display_procedure_only()