# src/quadratic_solver.py
import cmath

def solve_quadratic_equation(a, b, c):
    """
    Resuelve una ecuación cuadrática ax^2 + bx + c = 0 y retorna las soluciones
    y una cadena con el procedimiento paso a paso.
    """
    procedure = []
    solutions = None

    procedure.append("Procedimiento para resolver ax² + bx + c = 0")
    procedure.append(f"Valores ingresados: a = {a}, b = {b}, c = {c}")

    if a == 0:
        procedure.append("\nEl valor de 'a' es 0. Esto no es una ecuación cuadrática.")
        if b != 0:
            x_linear = -c / b
            procedure.append(f"Se trata de una ecuación lineal: {b}x + {c} = 0")
            procedure.append(f"Despejando x: {b}x = -{c}")
            procedure.append(f"x = -{c} / {b}")
            procedure.append(f"x = {x_linear}")
            solutions = (x_linear,) # Tupla de una solución
        else:
            if c == 0:
                procedure.append("La ecuación es 0 = 0. Tiene infinitas soluciones.")
                solutions = "infinitas"
            else:
                procedure.append(f"La ecuación es 0 = {c}. No tiene solución.")
                solutions = "sin_solucion"
        return solutions, "\n".join(procedure)


    procedure.append("\nPaso 1: La fórmula general es:")
    procedure.append("x = [-b ± √(b² - 4ac)] / 2a")

    # Paso 2: Calcular el discriminante (delta)
    procedure.append("\nPaso 2: Calcular el discriminante (Δ = b² - 4ac)")
    discriminante = (b**2) - 4*(a*c)
    procedure.append(f"Sustituyendo valores:")
    procedure.append(f"Δ = ({b})² - 4 * ({a}) * ({c})")
    procedure.append(f"Δ = {b**2} - ({4*a*c})")
    procedure.append(f"Δ = {discriminante}")

    # Paso 3: Analizar el discriminante y calcular las soluciones
    procedure.append("\nPaso 3: Analizar el discriminante para encontrar las soluciones:")

    if discriminante > 0:
        procedure.append(f"Como el discriminante ({discriminante}) es mayor que 0, hay dos soluciones reales distintas.")
        sqrt_discriminante = discriminante**0.5
        procedure.append(f"√(Δ) = √({discriminante}) = {sqrt_discriminante:.4f}") # Formateo para 4 decimales

        # Calcular x1
        x1_numerador = -b - sqrt_discriminante
        x1_denominador = 2 * a
        x1 = x1_numerador / x1_denominador

        procedure.append(f"\nCalculando x1:")
        procedure.append(f"x1 = (-{b} - √{discriminante}) / (2 * {a})")
        procedure.append(f"x1 = ({x1_numerador:.4f}) / ({x1_denominador:.4f})")
        procedure.append(f"x1 = {x1:.4f}")

        # Calcular x2
        x2_numerador = -b + sqrt_discriminante
        x2_denominador = 2 * a
        x2 = x2_numerador / x2_denominador

        procedure.append(f"\nCalculando x2:")
        procedure.append(f"x2 = (-{b} + √{discriminante}) / (2 * {a})")
        procedure.append(f"x2 = ({x2_numerador:.4f}) / ({x2_denominador:.4f})")
        procedure.append(f"x2 = {x2:.4f}")

        solutions = (x1, x2)

    elif discriminante == 0:
        procedure.append(f"Como el discriminante ({discriminante}) es igual a 0, hay una única solución real.")

        # Calcular x
        x_numerador = -b
        x_denominador = 2 * a
        x = x_numerador / x_denominador

        procedure.append(f"\nCalculando x:")
        procedure.append(f"x = (-{b}) / (2 * {a})")
        procedure.append(f"x = ({x_numerador:.4f}) / ({x_denominador:.4f})")
        procedure.append(f"x = {x:.4f}")

        solutions = (x,) # Tupla de una solución

    else: # discriminante < 0
        procedure.append(f"Como el discriminante ({discriminante}) es menor que 0, hay dos soluciones complejas conjugadas.")
        sqrt_discriminante_complejo = cmath.sqrt(discriminante)
        procedure.append(f"√(Δ) = √({discriminante}) = {sqrt_discriminante_complejo}")

        # Calcular x1 (complejo)
        x1_numerador_complejo = -b - sqrt_discriminante_complejo
        x1_denominador_complejo = 2 * a
        x1 = x1_numerador_complejo / x1_denominador_complejo

        procedure.append(f"\nCalculando x1:")
        procedure.append(f"x1 = (-{b} - √{discriminante}) / (2 * {a})")
        procedure.append(f"x1 = ({x1_numerador_complejo}) / ({x1_denominador_complejo})")
        procedure.append(f"x1 = {x1}")

        # Calcular x2 (complejo)
        x2_numerador_complejo = -b + sqrt_discriminante_complejo
        x2_denominador_complejo = 2 * a
        x2 = x2_numerador_complejo / x2_denominador_complejo

        procedure.append(f"\nCalculando x2:")
        procedure.append(f"x2 = (-{b} + √{discriminante}) / (2 * {a})")
        procedure.append(f"x2 = ({x2_numerador_complejo}) / ({x2_denominador_complejo})")
        procedure.append(f"x2 = {x2}")

        solutions = (x1, x2)

    return solutions, "\n".join(procedure)

if __name__ == "__main__":
    # Ejemplo de uso
    sol, proc = solve_quadratic_equation(1, -3, 2)
    print("\n--- EJEMPLO 1 ---")
    print("Soluciones:", sol)
    print("Procedimiento:\n", proc)

    sol, proc = solve_quadratic_equation(1, 2, 1)
    print("\n--- EJEMPLO 2 ---")
    print("Soluciones:", sol)
    print("Procedimiento:\n", proc)

    sol, proc = solve_quadratic_equation(1, 1, 1)
    print("\n--- EJEMPLO 3 ---")
    print("Soluciones:", sol)
    print("Procedimiento:\n", proc)

    sol, proc = solve_quadratic_equation(0, 5, 10)
    print("\n--- EJEMPLO 4 (a=0, lineal) ---")
    print("Soluciones:", sol)
    print("Procedimiento:\n", proc)