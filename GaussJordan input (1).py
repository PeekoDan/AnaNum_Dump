def mostrar_sistema(matriz, resultados):
    n = len(matriz)
    print("\nSistema de ecuaciones:")
    for i in range(n):
        ecuacion = " + ".join([f"{matriz[i][j]}*x{j+1}" for j in range(n)])
        print(f"{ecuacion} = {resultados[i]}")
    print()


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


n = int(input("Ingresa el tamaño de la matriz (nxn): "))
matriz = []
resultados = []

for i in range(n):
    fila = []
    for j in range(n):
        valor = float(input(f"Coeficiente de x_{j+1} en ecuación {i+1}: "))
        fila.append(valor)
    matriz.append(fila)

for i in range(n):
    res = float(input(f"Resultado de ecuación {i+1}: "))
    resultados.append(res)

mostrar_sistema(matriz, resultados)

confirmar = input("¿Es correcto el sistema? (s/n): ").lower()
if confirmar == "n":
    accion = input("¿Quieres editar (e) o borrar (b) la matriz?: ").lower()
    if accion == "e":
        matriz, resultados = editar_matriz(matriz, resultados)
    elif accion == "b":
        print("Matriz eliminada. Fin del programa.")
        exit()
input("Presione enter para terminar")