import math
import os

os.system("cls")


# DEFINIR VARIABLES INICIALES

datosx = []
datosxy = {}


# EJEMPLO
# datosx = [1,2,3,4]
# datosxy = { 1:1, 2:4, 3:9, 4:16}
# Esto define cuatro puntos de la función f(x) = x^2

# Se va a usar de esta forma para poder ordenar los datosx
# y luego poder usar interpolación lineal.






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


# = GAUSS JORDAN = (IMPORTANTE)

def gauss_jordan(matriz_og):
    """
    Aplica el método de Gauss-Jordan como en nuestro proyecto 1.
    """
    matriz = [fila[:] for fila in matriz_og]  # copia de la matriz
    n = len(matriz)

    for i in range(n):
        pivote = matriz[i][i]
        for j in range(len(matriz[i])):
            matriz[i][j] /= pivote

        for k in range(n):
            if k != i:
                factor = matriz[k][i]
                for j in range(len(matriz[k])):
                    matriz[k][j] -= factor * matriz[i][j]

    return tuple(matriz[i][-1] for i in range(n))



# === INTERPOLACIÓN LINEAL ===

# Suposiciones:
# x   not in  datosx
# min(datosx) < x < max(datosx) 

def int_lineal(datosx, datosxy, x):
    n = len(datosx)
    izq = 0
    der = n - 1

    # Encontrando xi consecutivos tal que x esté en xi
    while der - izq > 1:
        nextn = math.floor((izq + der) / 2)
        if datosx[nextn] < x:
            izq = nextn
        else:
            der = nextn

    # Aquí: datosx[izq] < x < datosx[der], con der == izq + 1
    xi, xi1 = datosx[izq], datosx[der]
    yi = datosxy[xi]
    yi1 = datosxy[xi1]

    # Aplicando la fórmula
    y_int = yi + ((yi1 - yi)/(xi1-xi)) * (x - xi)

    return y_int
    

# === POLINOMIO DE INTERPOLACIÓN ÚNICO ===

# Usaremos el método de Gauss Jordan para obtener la solución de los coefs.

def int_pol(datosx, datosxy, x, pol = None):
    matriz = []
    n= len(datosx)

    if pol != None:
        return evaluar_polinomio(pol,x), pol

    # Construyendo la matriz
    for a in datosx:
        fila = [a**k for k in range(n + 1)]
        fila.append(datosxy[a])
        matriz.append(fila)

    #Coeficientes en el orden correcto
    pol = gauss_jordan(matriz)

    return evaluar_polinomio(pol,x), pol

    

# === POLINOMIO DE INTERPOLACIÓN - NEWTON ===

# Este método aplica tanto para diferencias divididas como separadas.

# Usaremos el método de Gauss Jordan para obtener la solución de los coefs.

def int_newton(datosx, datosxy, x):
    matriz = []
    n = len(datosx)

    # Construyendo la matriz
    for i in range(n):  # Fila i
        product = 1
        fila = [product]
        for j in range(1, n):  # Columna i
            if j == i+1: # Si ya pasamos la diagonal principal, es 0 siempre
                fila.extend([0] * (n - j))
                break
            product *= datosx[i] - datosx[j-1] # Añadiendo el producto total
            fila.append(product)
        fila.append(datosxy[datosx[i]]) # Se añade el "lado derecho"
        matriz.append(fila) # Ya tenemos la fila, y se añade
                

    # Coeficientes en el orden correcto
    C = gauss_jordan(matriz)

    # Evaluando en el polinomio con los coeficientes dados
    product = 1
    tot = 0

    for i in range(n):
        tot += C[i]*product
        product *= (x-datosx[i])

    return tot


# === INTERPOLACIÓN DE LAGRANGE ===

def L(k, datosx, x):  # Polinomio Lk(x)
    n = len(datosx)
    producto = 1
    for i in range(n):
        producto *= (x - datosx[i] if i!=k else 1)
        # Multiplica por (x-xi) a menos que i=k
    return producto

def int_lagrange(datosx, datosxy, x):
    suma = 0
    n = len(datosx)

    for i in range(n):
        xi = datosx[i]
        
        suma += datosxy[xi] * L(i, datosx, x) / L(i, datosx, xi)
    return suma





# INICIO DEL PROGRAMA



print("--- Interpolación ---")
print("\n")


# ---------------------------------------------------------
# 1. Solicitar coeficientes
# ---------------------------------------------------------
# Se determina automáticamente según la cantidad de coeficientes
# que se ingresen.



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

        # Solicitar el nuevo coeficiente
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

    input("\n\nPresione Enter para terminar...")
    exit()


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

