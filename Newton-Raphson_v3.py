# Método de Newton-Raphson para encontrar una raíz de un polinomio

import math
import os

os.system("cls")


# ---------------------------------------------------------
# Funciones auxiliares
# ---------------------------------------------------------

def evaluar_polinomio(coeficientes, x):
    grado = len(coeficientes) - 1
    resultado = 0

    for i, coeficiente in enumerate(coeficientes):
        potencia = grado - i
        resultado += coeficiente * (x ** potencia)

    return resultado



def derivada_coeficientes(coeficientes):
    """Obtiene los coeficientes de la derivada del polinomio."""
    grado = len(coeficientes) - 1

    return [
        coeficientes[i] * (grado - i)
        for i in range(grado)
    ]


def construir_polinomio(coeficientes):
    """Construye una representación legible del polinomio."""
    grado = len(coeficientes) - 1
    polinomio = ""

    for i, coeficiente in enumerate(coeficientes):
        potencia = grado - i

        if coeficiente == 0:
            continue

        # Signo
        if polinomio == "":
            if coeficiente < 0:
                signo = "-"
            else:
                signo = ""
        else:
            signo = " - " if coeficiente < 0 else " + "

        valor = abs(coeficiente)

        # Término
        if potencia == 0:
            termino = f"{valor:g}"

        elif potencia == 1:
            if valor == 1:
                termino = "x"
            else:
                termino = f"{valor:g}x"

        else:
            if valor == 1:
                termino = f"x^{potencia}"
            else:
                termino = f"{valor:g}x^{potencia}"

        polinomio += signo + termino

    if polinomio == "":
        polinomio = "0"

    return polinomio


def criterio_convergencia(coeficientes, derivada, segunda_derivada, x):
    """
    Evalúa el criterio de convergencia de Newton-Raphson:
    |f(x)f''(x) / [f'(x)]^2| < 1
    Devuelve False si no se cumple o si f'(x) = 0 (no evaluable).
    """
    fx = evaluar_polinomio(coeficientes, x)
    fprima_x = evaluar_polinomio(derivada, x)
    fdobprima_x = evaluar_polinomio(segunda_derivada, x)

    if fprima_x == 0:
        return False

    return abs((fx * fdobprima_x) / (fprima_x ** 2)) < 1


def encontrar_valor_inicial_valido(coeficientes, derivada, derivada2, x0, paso=0.1, intentos=1000):
    """
    Busca un valor cercano a x0 que cumpla el criterio de convergencia,
    alternando incrementos hacia la derecha e izquierda de x0.
    Devuelve el nuevo valor, o None si no se encontró ninguno.
    """
    for i in range(1, intentos + 1):
        candidato_der = x0 + i * paso
        candidato_izq = x0 - i * paso

        if criterio_convergencia(coeficientes, derivada, derivada2, candidato_der):
            return candidato_der

        if criterio_convergencia(coeficientes, derivada, derivada2, candidato_izq):
            return candidato_izq

    return None


# ---------------------------------------------------------
# 1. Solicitar coeficientes
# ---------------------------------------------------------
# Se determina automáticamente según la cantidad de coeficientes
# que se ingresen.

print("--- Método Gauss-Jordan ---")
print("\n")

while True:
    entrada = input(
        "Ingrese los coeficientes del polinomio en orden descendente de grado,\n"
        "separados por espacios\n"
        "Por ejemplo, para x^3 + 2 ingrese: 1 0 0 2\n\n> "
    )

    try:
        coeficientes = list(map(float, entrada.split()))

        if len(coeficientes) == 0:
            print("Error: debe ingresar al menos un coeficiente.")
            continue

        # Antes se validaba que el primer coeficiente no fuera 0; ahora se
        # permite y la lista se reduce más adelante, tras confirmarse.
        break

    except ValueError:
        print("Error: ingrese únicamente números separados por espacios.")


# ---------------------------------------------------------
# 2. Mostrar polinomio y permitir cambios
# ---------------------------------------------------------

while True:

    print("\nEl polinomio ingresado es:")
    print(f"f(x) = {construir_polinomio(coeficientes)}")

    if coeficientes[0] == 0:
        print("\nEl coeficiente principal que ingresó usted era 0.")
        print("Por favor verifique que el polinomio sea correcto.")
    
    cambio = input("\n¿Desea hacer algún cambio? (s/n): ").lower()

    if cambio == "n":
        break

    elif cambio == "s":

        # Antes se ofrecían dos opciones ("grado y coeficientes" o "solo
        # coeficientes"); se unifican porque el grado ahora es automático.
        while True:
            try:
                entrada = input(
                    "Ingrese los nuevos coeficientes en orden descendente de grado,\n"
                    "separados por espacios (incluya los "
                    "coeficientes que valgan 0)\n> "
                )

                nuevos_coeficientes = list(map(float, entrada.split()))

                if len(nuevos_coeficientes) == 0:
                    print("\nError: debe ingresar al menos un coeficiente.\n")
                    continue

                coeficientes = nuevos_coeficientes
                break

            except ValueError:
                print("Error: ingrese únicamente números.")

    else:
        print("\nError: responda únicamente con 's' o 'n'.\n")


# ---------------------------------------------------------
# 3. Reducir coeficientes y validar que no sea constante
# ---------------------------------------------------------

# Se elimina cualquier 0 inicial para que el coeficiente principal
# (el de mayor grado) no sea cero.
while len(coeficientes) > 1 and coeficientes[0] == 0:
    coeficientes.pop(0)

grado = len(coeficientes) - 1

if grado == 0:
    if coeficientes[0] == 0:
        print("\nEl polinomio se reduce a f(x) = 0 (función nula).")
        print("Todo valor de x es raíz.")
    else:
        print(f"\nEl polinomio se reduce a una constante: f(x) = {coeficientes[0]:g}.")
        print("Ningún valor de x es raíz.")

    exit


# ---------------------------------------------------------
# 4. Calcular derivadas
# ---------------------------------------------------------

derivada = derivada_coeficientes(coeficientes)
segunda_derivada = derivada_coeficientes(derivada)


# ---------------------------------------------------------
# 5. Solicitar valor inicial
# ---------------------------------------------------------

while True:
    try:
        xi = float(input("\nIngrese el valor inicial x0\n> "))
        break

    except ValueError:
        print("Error: ingrese un valor numérico.")

# Se valida el criterio de convergencia |f(x)f''(x) / [f'(x)]^2| < 1
if not criterio_convergencia(coeficientes, derivada, segunda_derivada, xi):
    print(
        "\nEl valor inicial ingresado no cumple el criterio de "
        "convergencia."
    )

    xi_alternativo = encontrar_valor_inicial_valido(
        coeficientes, derivada, segunda_derivada, xi
    )

    if xi_alternativo is None:
        print(
            "No se encontró, cerca de x0, ningún valor que cumpla el criterio.\n"
            "Se continuará con el valor original, pero el método podría\n"
            "no converger."
        )
    else:
        print(f"Se encontró un valor cercano que sí cumple: x0 = {xi_alternativo:.6f}")
        xi = xi_alternativo


# ---------------------------------------------------------
# 6. Solicitar error deseado
# ---------------------------------------------------------

while True:
    try:
        error_deseado = float(
            input("\nIngrese el error deseado (%)\n> ")
        )

        if 0 < error_deseado < 100:
            break
        else:
            print(
                "\nError: el error debe ser mayor que 0 y menor que 100.\n"
            )

    except ValueError:
        print("\nError: ingrese un valor numérico.\n")


# ---------------------------------------------------------
# Método de Newton-Raphson
# ---------------------------------------------------------

os.system('cls')

# La derivada ya se calculó en el paso 4, no es necesario volver a hacerlo.

flag = 0
iteracion = 0
error_aproximado = float("inf")

resultados = []

print("\n" + "=" * 65)
print("MÉTODO DE NEWTON-RAPHSON")
print("=" * 65)

print(f"Polinomio: f(x) = {construir_polinomio(coeficientes)}")
print(f"Valor inicial: x0 = {xi}")
print(f"Error deseado: {error_deseado}%")
print("=" * 65)

while error_aproximado > error_deseado:

    iteracion += 1

    fxi = evaluar_polinomio(coeficientes, xi)
    fprima_xi = evaluar_polinomio(derivada, xi)

    # Evitar división entre cero
    if fprima_xi == 0:
        print("\nError: la derivada es cero.")
        print("Newton-Raphson no puede continuar con este valor.")
        break

    # Fórmula de Newton-Raphson
    xi_nuevo = xi - (fxi / fprima_xi)

    # Error aproximado porcentual
    if xi_nuevo != 0:
        error_aproximado = abs(
            (xi_nuevo - xi) / xi_nuevo
        ) * 100
    else:
        error_aproximado = abs(xi_nuevo - xi) * 100

    resultados.append(
        (iteracion, xi_nuevo, error_aproximado)
    )


    xi = xi_nuevo

    # Evitar que el programa se quede ejecutándose indefinidamente
    if iteracion >= 5000:
        flag = 1
        print("\nSe alcanzó el máximo de 5000 iteraciones.")
        break


# ---------------------------------------------------------
# 7. Tabla final
# ---------------------------------------------------------

print("\n")
print("=" * 65)
print("TABLA DE ITERACIONES")
print("=" * 65)
print("")

print(
    f"{'Iteración':^12}"
    f"{'Valor de xi actual':^25}"
    f"{'Error aproximado (%)':^25}"
)

print("-" * 65)

if not flag:  # Se halló raíz, se imprime toda la tabla
    for iteracion, xi, error in resultados:
        print(
            f"{iteracion:^12}"
            f"{xi:^25.8f}"
            f"{error:^25.8f}"
        )

else:  # No se halló una raíz, se resume la tabla
    
    # Primeras 10 filas
    for iteracion, xi, error in resultados[:10]:
        print(
            f"{iteracion:^12}"
            f"{xi:^25.8f}"
            f"{error:^25.8f}"
        )

    # Puntos suspensivos, uno por columna, en 3 líneas
    for _ in range(3):
        print(
            f"{'.':^12}"
            f"{'.':^25}"
            f"{'.':^25}"
        )

    # Últimas 10 filas
    for iteracion, xi, error in resultados[-10:]:
        print(
            f"{iteracion:^12}"
            f"{xi:^25.8f}"
            f"{error:^25.8f}"
        )
            

print("-" * 65)

if resultados:
    print(f"\nRaíz aproximada:    x = {resultados[-1][1]:.10f}")
    print(f"Error aproximado:       {resultados[-1][2]:.10f}%")
    print(f"Iteraciones realizadas: {len(resultados)}")

if flag:
    print("\nNo se pudo hallar una raíz para el polinomio...")
    print("Lo lamentamos.")

input("\n\nPresione Enter para terminar...")

