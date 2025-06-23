# src/problem_generator.py
import random

def generate_random_problem():
    """
    Genera coeficientes aleatorios (a, b, c) para una ecuación cuadrática.
    Intenta asegurar que 'a' no sea cero.
    """
    a = 0
    while a == 0:  # Asegura que 'a' no sea cero para que sea una cuadrática
        a = random.randint(-10, 10)

    b = random.randint(-15, 15)
    c = random.randint(-20, 20)

    return a, b, c

if __name__ == "__main__":
    # Ejemplo de uso
    a, b, c = generate_random_problem()
    print(f"Problema aleatorio generado: {a}x² + {b}x + {c} = 0")