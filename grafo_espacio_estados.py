from modelo_rompecabezas_o_rutas import crear_problema


def construir_grafo(problema, profundidad_maxima=2):
    visitados = set()
    arcos = []
    cola = [(problema.estado_inicial, 0, [problema.estado_inicial])]

    while cola:
        estado, profundidad, camino = cola.pop(0)

        if estado in visitados:
            continue

        visitados.add(estado)

        if profundidad >= profundidad_maxima:
            continue

        for destino in problema.acciones_validas(estado):
            costo = problema.costo(estado, destino)

            arcos.append((estado, destino, costo))

            nuevo_camino = camino + [destino]

            if destino not in camino and destino not in visitados:
                cola.append(
                    (destino, profundidad + 1, nuevo_camino)
                )

    return visitados, arcos


def mostrar_grafo(problema):
    estados, arcos = construir_grafo(problema)

    print("=== ESPACIO DE ESTADOS ===")
    print(f"Estados encontrados: {len(estados)}")
    print(f"Arcos encontrados: {len(arcos)}")

    print("\nEstados:")
    for estado in sorted(estados):
        print(f"- {estado}")

    print("\nArcos:")
    for origen, destino, costo in arcos:
        print(f"- {origen} -> {destino} ({costo} min)")


if __name__ == "__main__":
    problema = crear_problema()
    mostrar_grafo(problema)
