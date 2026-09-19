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
    """
    NOTA: coeficientes en orden ASCENDENTE
    """
    resultado = 0
 
    for potencia, coeficiente in enumerate(coeficientes):
        resultado += coeficiente * (x ** potencia)
 
    return resultado


def construir_polinomio(coeficientes):
    """
    Construye una representación legible del polinomio.
    NOTA: coeficientes está en orden ASCENDENTE (cte, lineal, ^2,...)
    """
    grado = len(coeficientes) - 1
    polinomio = ""
 
    for potencia in range(grado, -1, -1):
        coeficiente = coeficientes[potencia]
 
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
    y_int = yi + ((yi1 - yi) / (xi1 - xi)) * (x - xi)

    return y_int


# === POLINOMIO DE INTERPOLACIÓN ÚNICO ===

# Usaremos el método de Gauss Jordan para obtener la solución de los coefs.

def int_pol(datosx, datosxy, x, pol=None):
    matriz = []
    n = len(datosx)

    if pol != None:
        return evaluar_polinomio(pol, x), pol

    # Construyendo la matriz
    for a in datosx:
        fila = [a ** k for k in range(n)] #a^0, a^1, ..., a^n-1
        fila.append(datosxy[a])
        matriz.append(fila)

    # Coeficientes en el orden correcto
    pol = gauss_jordan(matriz)

    return evaluar_polinomio(pol, x), pol


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
            if j == i + 1:  # Si ya pasamos la diagonal principal, es 0 siempre
                fila.extend([0] * (n - j))
                break
            product *= datosx[i] - datosx[j - 1]  # Añadiendo el producto total
            fila.append(product)
        fila.append(datosxy[datosx[i]])  # Se añade el "lado derecho"
        matriz.append(fila)  # Ya tenemos la fila, y se añade

    # Coeficientes en el orden correcto
    C = gauss_jordan(matriz)

    # Evaluando en el polinomio con los coeficientes dados
    product = 1
    tot = 0

    for i in range(n):
        tot += C[i] * product
        product *= (x - datosx[i])

    return tot


# === INTERPOLACIÓN DE LAGRANGE ===

def L(k, datosx, x):  # Polinomio Lk(x)
    n = len(datosx)
    producto = 1
    for i in range(n):
        producto *= (x - datosx[i] if i != k else 1)
        # Multiplica por (x-xi) a menos que i=k
    return producto


def int_lagrange(datosx, datosxy, x):
    suma = 0
    n = len(datosx)

    for i in range(n):
        xi = datosx[i]

        suma += datosxy[xi] * L(i, datosx, x) / L(i, datosx, xi)

    return suma


# ======================================================================
# SECCIÓN 2: Funciones traídas de GaussJordan.py, SIN CAMBIOS.
# ======================================================================

def pedir_coeficientes(mensaje, n):
    """
    Pide al usuario una fila de n numeros separados por espacios.
    Repite la solicitud hasta que el usuario ingrese exactamente
    n valores numericos validos.
    Devuelve una lista de floats.
    """
    while True:
        try:
            valores = list(map(float, input(mensaje).split()))
            if len(valores) != n:
                print(f"  Error: se esperaban {n} valores, se ingresaron {len(valores)}. Intente de nuevo.\n")
                continue
            return valores
        except ValueError:
            print("  Error: ingrese solo numeros separados por espacios. Intente de nuevo.\n")


def pedir_entero(mensaje):
    """
    Pide al usuario un numero entero positivo.
    Repite la solicitud si el valor no es valido.
    """
    while True:
        try:
            valor = int(input(mensaje))
            if valor <= 0:
                print("  Error: debe ser un numero entero positivo. Intente de nuevo.\n")
                continue
            return valor
        except ValueError:
            print("  Error: ingrese un numero entero. Intente de nuevo.\n")


# ======================================================================
# SECCIÓN 3: Funciones nuevas de este archivo, para solicitar los datos
# de la misma forma en que GaussJordan.py solicita las ecuaciones
# (tamaño -> filas -> mostrar -> confirmar -> editar/borrar).
# ======================================================================

def mostrar_datos(datosx, datosxy):
    print("\nPuntos ingresados:")
    for i, x in enumerate(datosx):
        print(f"  Punto {i + 1}: f({x:g}) = {datosxy[x]:g}")
    print()


def editar_datos(datosx, datosxy):
    while True:
        mostrar_datos(datosx, datosxy)
        opcion = input("¿Quieres editar algún punto? (s/n): ").lower()
        if opcion == "n":
            break

        indice = int(input("Ingresa el número de punto a editar: ")) - 1
        x_viejo = datosx[indice]

        nuevo = pedir_coeficientes(
            f"Ingrese el nuevo punto {indice + 1} (x f(x)), separado por un espacio\n> ",
            2,
        )

        del datosxy[x_viejo]
        datosx[indice] = nuevo[0]
        datosxy[nuevo[0]] = nuevo[1]

    return datosx, datosxy


# * ~ * ~ * ~ * ~ * ~ * ~ * ~
# * ~ * ~ * ~ * ~ * ~ * ~ * ~


# ==== ==== ==== ==== ====

# PROGRAMA PRINCIPAL

# ==== ==== ==== ==== ====

print("--- Interpolación ---")
print("\n")

# ---------------------------------------------------------
# 1. Solicitar los puntos (x, f(x))
# ---------------------------------------------------------

n = pedir_entero("Ingresa la cantidad de puntos a interpolar\n> ")

datosx = []
datosxy = {}

for i in range(n):
    print(f"\nPunto {i + 1}:")
    punto = pedir_coeficientes(
        "Ingrese el valor de x y su imagen f(x), separados por un espacio\n"
        "Por ejemplo, para el punto (2, 4) ingrese: 2 4\n> ",
        2,
    )
    x_val, y_val = punto
    datosx.append(x_val)
    datosxy[x_val] = y_val

mostrar_datos(datosx, datosxy)

confirmar = input("Por favor revise detalladamente. ¿Son correctos los puntos? (s/n)\n> ").lower()
while confirmar not in ("s", "n"):
    print("  Error: responda solo 's' o 'n'. Intente de nuevo.\n")
    confirmar = input("Por favor revise detalladamente. ¿Son correctos los puntos? (s/n)\n> ").lower()

if confirmar == "n":
    accion = input("¿Quieres editar (e) o borrar (b) los datos?\n> ").lower()
    while accion not in ("e", "b"):
        print("  Error: responda solo 'e' o 'b'. Intente de nuevo.\n")
        accion = input("¿Quieres editar (e) o borrar (b) los datos?\n> ").lower()

    if accion == "e":
        datosx, datosxy = editar_datos(datosx, datosxy)
    elif accion == "b":
        print("Datos eliminados. Fin del programa.")
        exit()

# Se ordena datosx de forma ascendente: lo requiere int_lineal para la
# búsqueda binaria de los xi consecutivos.
datosx = sorted(datosx)


# ---------------------------------------------------------
# 2. Calcular una sola vez el polinomio de interpolación único
#    (no depende de x, así que se calcula y se guarda para
#    reutilizarse en cada consulta).
# ---------------------------------------------------------

_, polinomio_obtenido = int_pol(datosx, datosxy, datosx[0])


# ---------------------------------------------------------
# 3. Ciclo principal: solicitar x, validar, interpolar,
#    repetir hasta que el usuario ingrese "n".
# ---------------------------------------------------------

os.system("cls")

print("\n" + "=" * 65)
print("INTERPOLACIÓN")
print("=" * 65)
print(f"Puntos: {[(round(x, 4), round(datosxy[x], 4)) for x in datosx]}")
print("=" * 65)

while True:
    entrada_x = input(
        "\nIngrese un valor de x para interpolar (o 'n' para salir)\n> "
    ).strip()

    if entrada_x.lower() == "n":
        print("\nFin del programa.")
        break

    try:
        x = float(entrada_x)
    except ValueError:
        print("Error: ingrese un valor numérico válido, o 'n' para salir.")
        continue

    # Validar dominio: min(datosx) < x < max(datosx)
    if x < datosx[0] or x > datosx[-1]:
        print(
            "Este valor no se puede usar para interpolar porque sale del "
            "dominio. Intente otro valor"
        )
        continue

    # Verificar si x ya es un dato conocido
    if x in datosxy:
        print(f"Este valor no se necesita interpolar, f({x:g}) = {datosxy[x]:g}")
        continue

    # Calculando con los 4 métodos
    resultado_lineal = int_lineal(datosx, datosxy, x)
    resultado_pol, polinomio_obtenido = int_pol(datosx, datosxy, x, pol=polinomio_obtenido)
    resultado_newton = int_newton(datosx, datosxy, x)
    resultado_lagrange = int_lagrange(datosx, datosxy, x)

    print("\n" + "-" * 65)
    print(f"Resultados de interpolación para x = {x:g}")
    print("-" * 65)
    print(f"Interpolación lineal:        f({x:g}) ≈ {resultado_lineal:.6f}")
    print(f"Polinomio único (sistema):   f({x:g}) ≈ {resultado_pol:.6f}")
    print(f"Interpolación de Newton:     f({x:g}) ≈ {resultado_newton:.6f}")
    print(f"Interpolación de Lagrange:   f({x:g}) ≈ {resultado_lagrange:.6f}")
    print("-" * 65)
    print(f"\nPolinomio interpolante utilizado:\nf(x) = {construir_polinomio(polinomio_obtenido)}")
