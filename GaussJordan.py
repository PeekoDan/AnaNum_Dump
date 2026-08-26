import os

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


def mostrar_sistema(matriz, resultados):
    n = len(matriz)
    print("\nSistema de ecuaciones:")
    for i in range(n):
        ecuacion = " + ".join([f"{matriz[i][j]}*x{j+1}" for j in range(n)])
        print(f"{ecuacion} = {resultados[i]}")
    print()

def formatear_numero(valor, decimales=4):
    """
    Formatea un número usando como máximo 'decimales' posiciones,
    pero quitando los ceros innecesarios al final
    Regresa un texto (para imprimir de forma bonita)
    """
    valor_redondeado = round(valor, decimales)

    # Evitar el caso de "-0"
    if valor_redondeado == 0:
        valor_redondeado = 0

    texto = f"{valor_redondeado:.{decimales}f}"

    if "." in texto:
        texto = texto.rstrip("0").rstrip(".")

    return texto


def imprimir_matriz(matriz, num_vars=None):
    """
    Imprime una matriz con las columnas alineadas (como matriz escrita en papel)
    Cada valor usa como máximo 4 decimales, mostrando solo los decimales necesarios.
    """
    filas_formateadas = [[formatear_numero(valor) for valor in fila] for fila in matriz]
    #^^^^ las filas ahora son textos bonitos
    num_columnas = len(matriz[0])

    anchos = [
        max(len(filas_formateadas[f][c]) for f in range(len(matriz)))
        for c in range(num_columnas)
    ]
    #^^^^ saca la máxima longitud en cada columna para alinear las columnas

    for fila in filas_formateadas:
        partes = []
        for c, valor in enumerate(fila):
            if num_vars is not None and c == num_vars:
                partes.append("|")
            partes.append(valor.rjust(anchos[c]))
        print("[ " + "  ".join(partes) + " ]")
    print()
    #esta ultima parte es nomas la impresion de la matriz


#Esta función se utiliza para revisar si el sistema tiene solución unica.
def calcular_rango(m, tolerancia=1e-9): #tolerancia es por problemas con floats
    """
    Calcula el rango de una matriz m
    llevándola a forma escalonada con eliminación gaussiana y
    pivoteo parcial, sin modificar la matriz original.
    """
    matriz_temp = [fila[:] for fila in m] #copia de la matriz
    filas = len(matriz_temp)
    columnas = len(matriz_temp[0]) if filas > 0 else 0
    rango = 0
    fila_pivote = 0

    for col in range(columnas):
        if fila_pivote >= filas: #si ya nos acabamos las filas
            break

        max_fila = max(
            range(fila_pivote, filas),
            key=lambda r: abs(matriz_temp[r][col])
        )
        #Se encontró la fila con mayor valor abs para usar de pivote.

        if abs(matriz_temp[max_fila][col]) < tolerancia:
            continue
        #si la fila es todo ceros, no se cuenta para el rango y se pasa a la siguiente columna
        

        matriz_temp[fila_pivote], matriz_temp[max_fila] = matriz_temp[max_fila], matriz_temp[fila_pivote]

        for r in range(fila_pivote + 1, filas):
            factor = matriz_temp[r][col] / matriz_temp[fila_pivote][col]
            for c in range(col, columnas):
                matriz_temp[r][c] -= factor * matriz_temp[fila_pivote][c]
        #se hace eliminación gaussiana simple (sin dividir entre el pivote)
        
        fila_pivote += 1
        rango += 1
        #se suma 1 al rango porque la fila es L.I.

    return rango

def editar_matriz(matriz, resultados):
    while True:
        mostrar_sistema(matriz, resultados)
        opcion = input("¿Quieres editar alguna variable? (s/n): ").lower()
        if opcion == "n":
            break
        fila = int(input("Ingresa el número de ecuación (fila): ")) - 1
        col = int(input("Ingresa el número de variable (columna): ")) - 1
        nuevo_valor = float(input("Nuevo valor: "))
        matriz[fila][col] = nuevo_valor
    return matriz, resultados


"""
SOLICITUD DE DATOS
Se pide el tamaño de la matriz y luego, por cada ecuación,
todos sus coeficientes en una sola línea separados por espacios,
y por último el resultado de esa ecuación.
"""

print("--- Método Gauss-Jordan ---")
print("\n")

n = pedir_entero("Ingresa el tamaño del sistema (nxn)\n> ")

matriz = []
resultados = []

#Solicitando el sistema de ecuaciones
for i in range(n):
    print(f"\nEcuación {i + 1}:")
    fila = pedir_coeficientes(
        f"Imprima los {n} coeficientes de la ecuación {i + 1}\n"
        f"en el orden correcto y un espacio entre ellos.\n> ",
        n,
    )
    matriz.append(fila)

    res = pedir_coeficientes(
        f"Imprima el resultado de la ecuación {i + 1}.\n> ",
        1,
    )
    resultados.append(res[0])

mostrar_sistema(matriz, resultados)

confirmar = input("Por favor revise detalladamente. ¿Es correcto el sistema? (s/n)\n> ").lower()
while confirmar not in ("s", "n"):
    print("  Error: responda solo 's' o 'n'. Intente de nuevo.\n")
    confirmar = input("Por favor revise detalladamente. ¿Es correcto el sistema? (s/n)\n> ").lower()

if confirmar == "n":
    accion = input("¿Quieres editar (e) o borrar (b) la matriz?\n> ").lower()
    while accion not in ("e", "b"):
        print("  Error: responda solo 'e' o 'b'. Intente de nuevo.\n")
        accion = input("¿Quieres editar (e) o borrar (b) la matriz?\n> ").lower()

    if accion == "e":
        matriz, resultados = editar_matriz(matriz, resultados)
    elif accion == "b":
        print("Matriz eliminada. Fin del programa.")
        exit()


#VALIDACIÓN!!
#Se valida que el sistema tenga solución (o que no tenga sols. inf.)


rango_coef = calcular_rango(matriz)

#Se determina si el sistema de ecuaciones tiene soluciones por los rangos
# Véase el Teorema de Rouché–Frobenius para saber como se determina.
if rango_coef < n: #Condición suficiente para que el sistema no tenga solucion unica
    matriz_aumentada = [fila[:] + [resultados[i]] for i, fila in enumerate(matriz)]
    rango_aum = calcular_rango(matriz_aumentada)

    if rango_coef == rango_aum: #si el rango de la aumentada es igual a la normal, infinitas
        print("\nEl sistema tiene INFINITAS SOLUCIONES.")
        print("Alguna (o varias) de las ecuaciones es una combinación lineal de las otras")
    else: #si el rango de la normal es menor al de la aumentada, CERO soluciones
        print("\nEl sistema NO TIENE SOLUCIÓN.")
        print("Alguna de las ecuaciones es incompatible con otra.")

    print("\nNo es posible determinar una solución para este sistema de ecuaciones.\nLo lamentamos.\n")
    input("\nPresione enter para terminar...")
    exit()

for i in range(n):
    matriz[i].append(resultados[i])


os.system("cls")
print("\n--- Proceso Gauss-Jordan ---")

print("\nMatriz aumentada inicial:")
imprimir_matriz(matriz, num_vars=n)
print("")
for i in range(n):
    """
    Pivoteo parcial :D
    Se busca, entre la fila i y las de abajo, cuál tiene el mayor valor
    absoluto en la columna i, para usarla como pivote (evita dividir
    entre un pivote 0 o muy pequeño).
    """
    fila_max = max(range(i, n), key=lambda r: abs(matriz[r][i]))
    if fila_max != i:
        print(f"Pivoteo parcial: intercambiando fila {i+1} con fila {fila_max+1} "
              f"(|{matriz[fila_max][i]}| > |{matriz[i][i]}|)")
        matriz[i], matriz[fila_max] = matriz[fila_max], matriz[i]
        imprimir_matriz(matriz, num_vars=n)

    #Ahora se continúa haciendo el ciclo usual de Gauss Jordan

    pivote = matriz[i][i]
    print(f"Dividiendo fila {i+1} entre {round(pivote,5)}") #i+1 porque se empieza en cero
    for j in range(len(matriz[i])):
        matriz[i][j] /= pivote

    for k in range(n):
        if k != i:
            factor = matriz[k][i]
            print(f"Restando {round(factor,5)} * fila {i+1} a fila {k+1}")
            for j in range(len(matriz[k])):
                matriz[k][j] -= factor * matriz[i][j]

    imprimir_matriz(matriz, num_vars=n)

soluciones = [matriz[i][-1] for i in range(n)]
print("\nSoluciones finales:")
for i, sol in enumerate(soluciones):
    print(f"x{i+1} = {round(sol,5)}")
input("\nPresione enter para terminar...")
