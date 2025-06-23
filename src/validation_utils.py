# src/validation_utils.py

def is_valid_float(value_str):
    """
    Verifica si una cadena puede ser convertida a un número flotante.
    """
    try:
        float(value_str)
        return True
    except ValueError:
        return False

def parse_user_solution(solution_str):
    """
    Intenta parsear la entrada del usuario para las soluciones.
    Permite números solos, pares separados por coma, o expresiones simples.
    Retorna una tupla de flotantes o complejos, o None si falla el parsing.
    """
    solution_str = solution_str.replace(" ", "").replace("i", "j") # Manejar 'i' como 'j' para complejos

    if not solution_str:
        return None

    try:
        # Intenta un solo número
        if is_valid_float(solution_str):
            return (float(solution_str),)
        
        # Intenta parsear como número complejo directamente
        if 'j' in solution_str:
             return (complex(solution_str),)

        # Intenta parsear múltiples valores separados por coma
        if ',' in solution_str:
            parts = solution_str.split(',')
            parsed_solutions = []
            for part in parts:
                if is_valid_float(part):
                    parsed_solutions.append(float(part))
                elif 'j' in part:
                    parsed_solutions.append(complex(part))
                else:
                    return None # No se pudo parsear
            if parsed_solutions:
                return tuple(parsed_solutions)
            return None

    except ValueError:
        return None
    except Exception: # Captura cualquier otro error de parsing
        return None
    
    return None # Si no coincide con ningún patrón conocido

def compare_solutions(user_solutions, correct_solutions, tolerance=1e-4):
    """
    Compara las soluciones del usuario con las soluciones correctas,
    considerando una tolerancia para números flotantes/complejos.
    Retorna True si son similares, False en caso contrario.
    """
    if user_solutions is None or correct_solutions is None:
        return False

    if isinstance(correct_solutions, str): # Casos especiales como "infinitas" o "sin_solucion"
        return user_solutions == correct_solutions

    # Aseguramos que ambas sean tuplas para la comparación
    user_solutions = tuple(sorted(user_solutions, key=lambda x: (x.real, x.imag) if isinstance(x, complex) else x))
    correct_solutions = tuple(sorted(correct_solutions, key=lambda x: (x.real, x.imag) if isinstance(x, complex) else x))

    if len(user_solutions) != len(correct_solutions):
        return False

    for u_sol, c_sol in zip(user_solutions, correct_solutions):
        if isinstance(u_sol, complex) and isinstance(c_sol, complex):
            if abs(u_sol.real - c_sol.real) > tolerance or abs(u_sol.imag - c_sol.imag) > tolerance:
                return False
        elif isinstance(u_sol, (float, int)) and isinstance(c_sol, (float, int)):
            if abs(u_sol - c_sol) > tolerance:
                return False
        else: # Tipo de dato incompatible
            return False
            
    return True

if __name__ == "__main__":
    # Pruebas de validación
    print(f"Es 10.5 válido float? {is_valid_float('10.5')}") # True
    print(f"Es 'abc' válido float? {is_valid_float('abc')}") # False

    print(f"Parsear '5': {parse_user_solution('5')}") # (5.0,)
    print(f"Parsear '-2.5, 3': {parse_user_solution('-2.5, 3')}") # (-2.5, 3.0)
    print(f"Parsear '1+2j': {parse_user_solution('1+2j')}") # (1+2j,)
    print(f"Parsear '1+2i': {parse_user_solution('1+2i')}") # (1+2j,)
    print(f"Parsear 'no valido': {parse_user_solution('no valido')}") # None

    print("\nComparación de soluciones:")
    print(f"Comparar (1.0, 2.0) con (2.0, 1.0): {compare_solutions((1.0, 2.0), (2.0, 1.0))}") # True
    print(f"Comparar (1.0,) con (1.0, 2.0): {compare_solutions((1.0,), (1.0, 2.0))}") # False
    print(f"Comparar (1.0+2j,) con (1.0+2j,): {compare_solutions((1.0+2j,), (1.0+2j,))}") # True
    print(f"Comparar (1.0+2j,) con (1.0+2.0000001j,): {compare_solutions((1.0+2j,), (1.0+2.0000001j,))}") # True
    print(f"Comparar 'infinitas' con 'infinitas': {compare_solutions('infinitas', 'infinitas')}") # True