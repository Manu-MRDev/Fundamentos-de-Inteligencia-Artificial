# -*- coding: utf-8 -*-
"""
ACTIVIDAD 5. BÚSQUEDA LOCAL Y ANÁLISIS DEL PAISAJE DE SOLUCIONES
PROGRAMA 1. ASCENSO DE COLINA

Material de apoyo para el curso del Dr. Jaime Aguilar Ortiz.
Base: ACTIVIDAD_05_Busqueda_Local_Ilustrada.docx, secciones 2 a 9.

QUÉ CONSTRUYE ESTE ARCHIVO
Evalúa vecinos, elige el de menor costo y acepta solo mejoras estrictas.
Reproduce los ejemplos de solución y estancamiento del documento.

CÓMO EMPEZAR EN SPYDER
1. Extraiga el ZIP en una carpeta donde pueda guardar archivos.
2. Abra este archivo .py completo y pulse F5 (Ejecutar archivo).
3. Lea la consola. Al final aparece la carpeta de resultados.
4. Abra los CSV para ver los datos y los SVG para ver las curvas.
5. Cambie primero UNA variable de CONFIGURACIÓN y vuelva a ejecutar.

Cada programa funciona solo: no importa archivos de los otros programas.
No necesita Internet ni instalar bibliotecas. Requiere Python 3.9 o posterior.
La exportación gráfica usa SVG con biblioteca estándar, no un optimizador.

GUÍA PARA LEER EL CÓDIGO
Primero lea CONFIGURACIÓN, contar_conflictos y generar_vecinos. Después siga
ejecutar_intento_colina y ascenso_colina. Lea main al final para ver cómo se unen las tareas.
Las funciones de exportación pueden estudiarse después de entender la búsqueda.

IDEAS DE PYTHON QUE APARECEN EN EL PROGRAMA
- Una lista, como [1, 4, 1, 3], guarda varios valores en orden.
- estado[0] es la primera posición; len(estado) devuelve la cantidad de valores.
- = asigna un valor; == compara si dos valores son iguales; != compara diferencia.
- if ejecuta un bloque cuando su condición se cumple; else cubre la alternativa.
- for recorre elementos; while repite mientras su condición sea verdadera.
- break termina el ciclo más cercano. La sangría determina qué pertenece a cada bloque.
- def define una función; return devuelve un resultado sin imprimirlo necesariamente.
- Un diccionario guarda pares clave-valor: resultado['mejor_costo'] consulta un dato.
- Las líneas que empiezan con # son comentarios, no instrucciones ejecutables.

Conviene conservar los parámetros originales hasta reproducir los ejemplos.
Los cambios numéricos y el tiempo de ejecución se registran, no se inventan.
"""

# Todas estas herramientas vienen incluidas con Python.
import csv          # Escribir tablas que también puede abrir una hoja de cálculo.
import hashlib      # Identificar el archivo ejecutado mediante una huella SHA-256.
import html         # Escapar texto al escribir las etiquetas de una figura SVG.
import json         # Guardar estados y parámetros de forma estructurada.
import math         # Exponencial, infinito y comprobaciones numéricas.
import platform     # Registrar el sistema donde se ejecutó el programa.
import random       # Generadores de números pseudoaleatorios con semilla.
import statistics   # Promedio y desviación estándar muestral.
import sys          # Registrar la versión de Python.
import time         # Medir la duración de la búsqueda.
from datetime import datetime  # Nombrar cada carpeta con fecha y hora.
from pathlib import Path       # Trabajar con rutas en Windows, Linux y macOS.
from typing import Optional    # Indicar que un argumento también admite None.

__author__ = "Jaime Aguilar Ortiz"
__version__ = "1.0"

# =============================================================================
# CONFIGURACIÓN: ESTAS SON LAS PRIMERAS VARIABLES QUE PUEDE MODIFICAR
# =============================================================================
ESTADO_INICIAL = [1, 1, 1, 1]  # Ejemplo de la Tabla 5; cada valor es una fila.
PRESUPUESTO = 3000             # Máximo de cálculos de C(q) por corrida.
EJECUTAR_PRUEBAS = True        # True comprueba los ejemplos antes de trabajar.

# =============================================================================
# 1. HERRAMIENTAS BÁSICAS: VALIDAR, CONTAR CONFLICTOS Y CREAR VECINOS
# =============================================================================
# Una función agrupa instrucciones para una tarea concreta. La palabra def la
# define; return entrega su resultado a la parte del programa que la llamó.
# Las anotaciones : int, : list y -> dict orientan al lector sobre los tipos.
# No hacen la validación por sí mismas: para eso escribimos comprobaciones.


def validar_entero(nombre: str, valor: int, minimo: int = 1) -> None:
    """Exigir un entero no menor que 'minimo', con un mensaje comprensible.

    True y False son valores lógicos. Python los relaciona con 1 y 0, pero aquí
    no deben admitirse como tamaños, presupuestos ni semillas. Por eso se usa
    type(valor) is int, en vez de convertir cualquier entrada con int(valor).
    """
    if type(valor) is not int or valor < minimo:
        raise ValueError(f"{nombre} debe ser un entero mayor o igual que {minimo}.")


def validar_estado(estado: list, n: Optional[int] = None) -> None:
    """Comprobar la representación de n-reinas, no que ya sea una solución.

    Ejemplo válido: [1, 4, 1, 3]. Tiene cuatro posiciones y filas entre 1 y 4.
    Ejemplo inválido: [1, 5, 1, 3]. La fila 5 no existe en un tablero de 4 filas.
    Se permiten filas repetidas: sus conflictos son lo que intentamos corregir.
    Si se proporciona n, también se comprueba que la longitud sea exactamente n.
    La función no modifica la lista recibida.
    """
    if not isinstance(estado, list) or len(estado) == 0:
        raise ValueError("El estado debe ser una lista no vacía, por ejemplo [1, 4, 1, 3].")
    if n is None:
        n = len(estado)
    validar_entero("Número de reinas", n)
    if len(estado) != n:
        raise ValueError(f"Se esperaban {n} reinas, pero la lista contiene {len(estado)}.")
    for columna, fila in enumerate(estado):
        if type(fila) is not int or not 1 <= fila <= n:
            raise ValueError(f"Columna {columna + 1}: la fila debe ser un entero entre 1 y {n}.")


def contar_conflictos(estado: list) -> int:
    """Calcular C(q), la función objetivo de la ecuación (2) de la actividad.

    La posición i de la lista representa una columna; estado[i] es su fila.
    En Python las posiciones empiezan en 0, pero las filas se guardan desde 1.
    Dos reinas se atacan cuando están en la misma fila o en la misma diagonal.
    Hay diagonal cuando la diferencia absoluta de filas coincide con la de
    columnas. abs(-3), por ejemplo, devuelve 3.

    El segundo ciclo empieza en i + 1: cada pareja se cuenta una sola vez.
    C([1, 4, 1, 3]) = 1; C([2, 4, 1, 3]) = 0; C([1, 1, 1, 1]) = 6.
    No hay ataques por columna porque la representación ya coloca una reina
    en cada una. Menos conflictos significa mejor candidato.
    """
    validar_estado(estado)
    conflictos = 0
    n = len(estado)
    for i in range(n - 1):
        for j in range(i + 1, n):
            misma_fila = estado[i] == estado[j]
            misma_diagonal = abs(estado[i] - estado[j]) == j - i
            if misma_fila or misma_diagonal:
                conflictos += 1
    return conflictos


def generar_vecinos(estado: list) -> list:
    """Crear los n(n-1) vecinos de la ecuación (4), sin alterar el estado.

    Se mueve UNA reina a OTRA fila de su misma columna. No se intercambian dos
    reinas ni se cambian dos posiciones. Para n = 4 se obtienen 12 vecinos.
    Se recorren columnas de izquierda a derecha y filas de menor a mayor:
    este orden permite reproducir el desempate de la sección 4.

    vecino = estado.copy() crea una lista independiente. Escribir únicamente
    vecino = estado daría otro nombre a la misma lista y dañaría el original.
    append agrega un elemento al final de una lista; no lo reemplaza.
    """
    validar_estado(estado)
    vecinos = []
    n = len(estado)
    for columna in range(n):
        for fila_nueva in range(1, n + 1):
            if fila_nueva != estado[columna]:
                vecino = estado.copy()
                vecino[columna] = fila_nueva
                vecinos.append(vecino)
    return vecinos


def generar_estado_inicial(n: int, semilla: int) -> list:
    """Crear un inicio reproducible, con cada fila uniforme entre 1 y n.

    Random(semilla) crea un generador local: no cambia el azar de otros programas.
    randint(1, n) incluye los dos extremos. No exigimos filas distintas: hacerlo
    cambiaría la distribución inicial acordada en la actividad.
    """
    validar_entero("Número de reinas", n)
    validar_entero("Semilla", semilla, 0)
    generador = random.Random(semilla)
    estado = []
    for _ in range(n):
        estado.append(generador.randint(1, n))
    return estado


def mostrar_tablero(estado: list) -> None:
    """Mostrar el tablero en la consola: R es una reina y . una casilla vacía.

    Se recorren las filas de arriba hacia abajo, como en el documento. Esta
    presentación no calcula conflictos ni consume evaluaciones de la búsqueda.
    """
    validar_estado(estado)
    n = len(estado)
    print("      " + " ".join(f"{columna:>2}" for columna in range(1, n + 1)))
    for fila in range(1, n + 1):
        casillas = []
        for columna in range(n):
            casillas.append(" R" if estado[columna] == fila else " .")
        print(f"{fila:>3} | " + " ".join(casillas))


# =============================================================================
# 2. REGISTRO: UN CONTADOR COMÚN PARA TODAS LAS EVALUACIONES
# =============================================================================
# Un diccionario relaciona claves con valores. registro['evaluaciones'] consulta
# el valor asociado a esa clave. La búsqueda usa este registro para no superar
# el presupuesto. No se cuentan como búsqueda los cálculos de las pruebas previas.


def crear_registro(presupuesto: int) -> dict:
    """Preparar el presupuesto, el mejor resultado y sus evidencias.

    None significa que todavía no se ha evaluado ningún candidato. curva_mejor
    guardará un dato por evaluación REAL, sin rellenar artificialmente la traza.
    """
    validar_entero("Presupuesto de evaluaciones", presupuesto)
    return {"presupuesto": presupuesto, "evaluaciones": 0,
            "mejor_estado": None, "mejor_costo": None,
            "curva_mejor": [], "traza_evaluaciones": []}


def evaluar_y_registrar(estado: list, registro: dict, intento: int,
                       iteracion: int, tipo: str) -> int:
    """Evaluar una vez, descontar trabajo y conservar el mejor candidato visto.

    Esta es la ÚNICA puerta al cálculo de C(q) dentro de los algoritmos. Así se
    cuentan la evaluación inicial, los vecinos y los nuevos inicios de B.
    El mejor observado puede ser un vecino aún no adoptado como estado actual.
    Esta distinción importa si el presupuesto termina a mitad de una vecindad.
    La curva implementa b_e = min(c_1, ..., c_e), ecuación (17).
    """
    if registro["evaluaciones"] >= registro["presupuesto"]:
        raise RuntimeError("Se intentó evaluar después de consumir el presupuesto.")
    costo = contar_conflictos(estado)
    registro["evaluaciones"] += 1
    if registro["mejor_costo"] is None or costo < registro["mejor_costo"]:
        registro["mejor_costo"] = costo
        registro["mejor_estado"] = estado.copy()
    registro["curva_mejor"].append(registro["mejor_costo"])
    registro["traza_evaluaciones"].append({
        "evaluacion": registro["evaluaciones"], "intento": intento,
        "iteracion": iteracion, "tipo": tipo, "candidato": estado.copy(),
        "costo_evaluado": costo, "mejor_costo": registro["mejor_costo"]})
    return costo


def cerrar_resultado(inicial: list, actual: list, costo_actual: int,
                     registro: dict, motivo: str, tiempo_s: float,
                     intentos: int, movimientos: list, decisiones: list,
                     resumen_intentos: list) -> dict:
    """Reunir la respuesta sin recalcular la función objetivo.

    Se guardan el último estado actual y el mejor observado por separado.
    'exito' depende de encontrar costo cero, no de que el programa haya terminado.
    Cada lista de evidencia tiene una función diferente: evaluaciones, cambios
    adoptados, decisiones probabilísticas y resumen de los intentos.
    """
    return {"estado_inicial": inicial.copy(), "estado_final": actual.copy(),
            "costo_final": costo_actual, "mejor_estado": registro["mejor_estado"].copy(),
            "mejor_costo": registro["mejor_costo"],
            "exito": registro["mejor_costo"] == 0,
            "evaluaciones": registro["evaluaciones"], "presupuesto": registro["presupuesto"],
            "tiempo_s": tiempo_s, "motivo": motivo, "intentos": intentos,
            "movimientos": movimientos, "decisiones": decisiones,
            "resumen_intentos": resumen_intentos,
            "curva_mejor": registro["curva_mejor"],
            "traza_evaluaciones": registro["traza_evaluaciones"]}




# =============================================================================
# 3. ASCENSO DE COLINA: REVISAR LA VECINDAD Y ACEPTAR SOLO MEJORAS
# =============================================================================
# Aunque el nombre diga 'ascenso', aquí minimizamos conflictos. Es equivalente
# a maximizar J(q) = -C(q), como explica la ecuación (7) del documento.
# No se usan derivadas ni un optimizador externo: todas las decisiones están aquí.


def ejecutar_intento_colina(inicial: list, registro: dict, intento: int) -> dict:
    """Realizar un intento de mejor mejora, usando un registro ya existente.

    Este registro puede pertenecer a un solo intento o a varios reinicios. Así
    los reinicios comparten el MISMO presupuesto y no pierden el mejor observado.
    La función se usa internamente: la entrada se valida antes de llamarla.

    Precisión de implementación: la Tabla 5 cuenta 37 evaluaciones porque revisa
    la vecindad completa antes de adoptar la mejor mejora. Se conserva esa regla,
    incluso si aparece un vecino de costo cero antes de acabar la revisión. No se
    inicia otra vecindad después de adoptarlo. Si el presupuesto impide acabar,
    se devuelve el mejor observado; encontrar cero sí certifica éxito, pero una
    revisión parcial sin cero NO permite certificar un mínimo local.
    """
    actual = inicial.copy()
    iteracion = 0
    evaluaciones_antes = registro["evaluaciones"]
    tipo = "inicio" if intento == 1 else "reinicio"
    costo_actual = evaluar_y_registrar(actual, registro, intento, iteracion, tipo)
    movimientos = [{"intento": intento, "paso": 0,
                    "evaluacion": registro["evaluaciones"], "estado": actual.copy(),
                    "costo": costo_actual, "accion": tipo}]
    motivo = "solucion_encontrada" if costo_actual == 0 else "presupuesto_agotado"

    # while repite mientras la condición sea verdadera. Cada vuelta completa
    # intenta elegir una mejora; no significa que siempre consiga moverse.
    while costo_actual > 0:
        if registro["evaluaciones"] >= registro["presupuesto"]:
            motivo = "presupuesto_agotado"
            break
        iteracion += 1
        vecinos = generar_vecinos(actual)
        mejor_vecino = None
        costo_mejor_vecino = math.inf  # Infinito: cualquier costo real será menor.
        vecindad_completa = True

        for vecino in vecinos:
            # Se verifica el presupuesto ANTES de cada cálculo, no al acabar
            # la vuelta. Esto impide excederlo en una vecindad de 56 vecinos.
            if registro["evaluaciones"] >= registro["presupuesto"]:
                vecindad_completa = False
                break
            costo_vecino = evaluar_y_registrar(
                vecino, registro, intento, iteracion, "vecino")
            # '<' conserva el primero en un empate. '<=' lo reemplazaría por
            # el último y cambiaría la traza acordada en el documento.
            if costo_vecino < costo_mejor_vecino:
                mejor_vecino = vecino.copy()
                costo_mejor_vecino = costo_vecino

        if not vecindad_completa:
            motivo = "presupuesto_agotado"
            # El cero es una cota inferior conocida. Si ya se vio, no hace falta
            # completar la vecindad para saber que ese candidato es una solución.
            if registro["mejor_costo"] == 0:
                actual = registro["mejor_estado"].copy()
                costo_actual = 0
                motivo = "solucion_encontrada"
                movimientos.append({"intento": intento, "paso": len(movimientos),
                    "evaluacion": registro["evaluaciones"], "estado": actual.copy(),
                    "costo": 0, "accion": "cero_observado_en_revision_parcial"})
            break

        if mejor_vecino is not None and costo_mejor_vecino < costo_actual:
            # Solo aquí se cambia el candidato ACTUAL. Evaluar un vecino no es
            # adoptarlo. Un empate tampoco se acepta en la variante estricta.
            actual = mejor_vecino.copy()
            costo_actual = costo_mejor_vecino
            movimientos.append({"intento": intento, "paso": len(movimientos),
                "evaluacion": registro["evaluaciones"], "estado": actual.copy(),
                "costo": costo_actual, "accion": "mejora_estricta"})
            if costo_actual == 0:
                motivo = "solucion_encontrada"
                break
        else:
            # Se revisaron TODOS los vecinos y ninguno mejora. Hay evidencia
            # para hablar de mínimo local, que puede ser no estricto por empates.
            motivo = "minimo_local_comprobado"
            break

    return {"estado_final": actual, "costo_final": costo_actual, "motivo": motivo,
            "movimientos": movimientos,
            "evaluaciones_usadas": registro["evaluaciones"] - evaluaciones_antes}


def ascenso_colina(estado_inicial: list, presupuesto: int = 3000) -> dict:
    """Resolver desde un solo inicio: sección 4 y ecuaciones (7) y (8).

    Uso desde una consola: resultado = ascenso_colina([1, 1, 1, 1], 3000).
    El reloj mide búsqueda y registro de trazas en memoria. No mide las pruebas,
    la impresión ni la escritura de archivos. perf_counter usa un reloj apropiado
    para medir duraciones; restar final - inicio implementa la ecuación (16).
    """
    validar_estado(estado_inicial)
    registro = crear_registro(presupuesto)
    inicio_reloj = time.perf_counter()
    intento = ejecutar_intento_colina(estado_inicial, registro, 1)
    tiempo_s = time.perf_counter() - inicio_reloj
    return cerrar_resultado(estado_inicial, intento["estado_final"],
        intento["costo_final"], registro, intento["motivo"], tiempo_s, 1,
        intento["movimientos"], [], [])


def pruebas_colina() -> None:
    """Reproducir las Tablas 4 y 5, el estancamiento y varios presupuestos."""
    pruebas_comunes()
    inicial = [1, 1, 1, 1]
    costos_vecinos = [contar_conflictos(v) for v in generar_vecinos(inicial)]
    comprobar(costos_vecinos == [4, 4, 4, 5, 4, 3, 5, 4, 3, 4, 4, 4],
              "Los doce costos deben coincidir con la Tabla 4.")
    resultado = ascenso_colina(inicial)
    estados = [fila["estado"] for fila in resultado["movimientos"]]
    comprobar(estados == [[1, 1, 1, 1], [1, 4, 1, 1], [2, 4, 1, 1], [2, 4, 1, 3]],
              "La secuencia debe coincidir con la Tabla 5.")
    comprobar(resultado["evaluaciones"] == 37, "La Tabla 5 requiere 37 evaluaciones.")
    comprobar(inicial == [1, 1, 1, 1], "La función no debe modificar la entrada.")
    detenido = ascenso_colina([1, 4, 2, 3])
    comprobar(detenido["mejor_costo"] == 1 and detenido["motivo"] == "minimo_local_comprobado",
              "El ejemplo de la sección 5 debe detenerse en un conflicto.")
    resuelto = ascenso_colina([2, 4, 1, 3])
    comprobar(resuelto["exito"] and resuelto["evaluaciones"] == 1,
              "Un inicio resuelto solo necesita su evaluación inicial.")
    parcial = ascenso_colina([1, 4, 2, 3], 5)
    comprobar(parcial["evaluaciones"] == 5 and parcial["motivo"] == "presupuesto_agotado",
              "Una vecindad parcial no demuestra que exista un mínimo local.")
    comprobar(ascenso_colina([1], 1)["exito"], "Una sola reina ya resuelve su tablero.")
    for limite in [1, 2, 12, 13, 14, 25, 36, 37, 50]:
        r = ascenso_colina([1, 1, 1, 1], limite)
        comprobar(r["evaluaciones"] <= limite, "Nunca se debe superar el presupuesto.")
        comprobar(len(r["curva_mejor"]) == r["evaluaciones"], "Una entrada de curva por evaluación real.")
        comprobar(all(a >= b for a, b in zip(r["curva_mejor"], r["curva_mejor"][1:])),
                  "La curva de mejor costo nunca debe subir.")


# =============================================================================
# 4. SALIDAS: TABLAS CSV, CURVAS Y ARCHIVOS PARA REVISAR LA EJECUCIÓN
# =============================================================================
# Estas funciones NO eligen movimientos. Pueden leerse después del algoritmo.
# Solo usan la biblioteca estándar. Las curvas se guardan en SVG, un formato
# gráfico que se abre en un navegador, sin instalar matplotlib ni usar Internet.
# Es una decisión de presentación de esta implementación; las fórmulas y el
# protocolo del documento no cambian.


def preparar_carpeta(nombre: str) -> Path:
    """Crear una carpeta de resultados junto al archivo .py.

    __file__ identifica el programa ejecutado. En una consola sin esa variable
    se usa la carpeta actual. La fecha evita sobrescribir ejecuciones anteriores.
    """
    if "__file__" in globals():
        base = Path(__file__).resolve().parent
    else:
        base = Path.cwd()
    marca = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    carpeta = base / "resultados_actividad5" / nombre / marca
    carpeta.mkdir(parents=True, exist_ok=False)
    return carpeta


def guardar_csv(ruta: Path, filas: list) -> None:
    """Guardar una tabla con encabezados; cada diccionario es una fila.

    Se usa punto y coma como separador y UTF-8 con marca inicial para facilitar
    la lectura de acentos en Excel. newline='' evita renglones vacíos en Windows.
    Las listas se escriben como texto JSON, por ejemplo [2, 4, 1, 3].
    Una lista de filas vacía no crea un archivo: puede no haber movimientos.
    """
    if not filas:
        return
    ruta = Path(ruta)
    with ruta.open("w", encoding="utf-8-sig", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=list(filas[0].keys()), delimiter=";")
        escritor.writeheader()
        for fila in filas:
            preparada = {}
            for clave, valor in fila.items():
                if isinstance(valor, (list, dict)):
                    valor = json.dumps(valor, ensure_ascii=False)
                preparada[clave] = valor
            escritor.writerow(preparada)


def guardar_curvas_svg(ruta: Path, series: dict, titulo: str,
                       eje_x: str = "Evaluaciones de la función objetivo",
                       eje_y: str = "Mejor costo observado") -> None:
    """Dibujar curvas con datos reales, sin paquetes externos.

    series relaciona una etiqueta con sus valores: {'A': [6, 4, 3, 0]}.
    El primer dato corresponde a x = 1. La conversión de coordenadas solo adapta
    los números al espacio de dibujo; no suaviza ni cambia los datos. Las líneas
    son escalonadas: el nuevo valor se aplica en la evaluación correspondiente.
    Las series se distinguen por trazos y por su leyenda, no solo por un color.
    """
    if not series or any(len(valores) == 0 for valores in series.values()):
        raise ValueError("Se necesita al menos una serie no vacía para graficar.")
    for valores in series.values():
        if any(not math.isfinite(float(v)) or v < 0 for v in valores):
            raise ValueError("Los datos de la gráfica deben ser finitos y no negativos.")
    if len(series) > 4:
        raise ValueError("Esta figura admite hasta cuatro series para mantener legible la leyenda.")
    ancho, alto = 1000, 630
    izquierda, derecha, arriba, abajo = 90, 35, 75, 130
    ancho_dibujo = ancho - izquierda - derecha
    alto_dibujo = alto - arriba - abajo
    max_x = max(2, max(len(valores) for valores in series.values()))
    max_y = max(1.0, max(max(valores) for valores in series.values())) * 1.08
    def posicion_x(x):
        """Pasar del número de evaluación a su posición horizontal."""
        return izquierda + (x - 1) * ancho_dibujo / (max_x - 1)
    def posicion_y(y):
        """Invertir la altura: en SVG el eje vertical crece hacia abajo."""
        return arriba + alto_dibujo * (1 - y / max_y)
    texto = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ancho} {alto}">',
             f'<title>{html.escape(titulo)}</title>',
             '<rect width="100%" height="100%" fill="white"/>',
             '<g font-family="Arial, sans-serif" font-size="15" fill="black">',
             f'<text x="500" y="32" text-anchor="middle" font-size="21">{html.escape(titulo)}</text>']
    for k in range(6):
        y = max_y * k / 5
        py = posicion_y(y)
        x = 1 + (max_x - 1) * k / 5
        px = posicion_x(x)
        texto.append(f'<path d="M {izquierda} {py} H {ancho-derecha}" stroke="black" opacity="0.13"/>')
        texto.append(f'<text x="{izquierda-12}" y="{py+5}" text-anchor="end">{y:.2g}</text>')
        texto.append(f'<text x="{px}" y="{alto-abajo+26}" text-anchor="middle">{x:.0f}</text>')
    texto.append(f'<path d="M {izquierda} {arriba} V {alto-abajo} H {ancho-derecha}" fill="none" stroke="black"/>')
    patrones = ["none", "10 5", "3 4", "12 4 3 4"]
    for numero, (nombre, valores) in enumerate(series.items()):
        puntos = [f"{posicion_x(1):.2f},{posicion_y(valores[0]):.2f}"]
        for indice in range(1, len(valores)):
            px = posicion_x(indice + 1)
            puntos.append(f"{px:.2f},{posicion_y(valores[indice-1]):.2f}")
            puntos.append(f"{px:.2f},{posicion_y(valores[indice]):.2f}")
        patron = patrones[numero % len(patrones)]
        texto.append(f'<polyline points="{" ".join(puntos)}" fill="none" stroke="black" stroke-width="2" stroke-dasharray="{patron}"/>')
        texto.append(f'<circle cx="{posicion_x(1):.2f}" cy="{posicion_y(valores[0]):.2f}" r="2.5"/>')
        lx = 100 + (numero % 2) * 455
        ly = 567 + (numero // 2) * 26
        texto.append(f'<path d="M {lx} {ly-5} h 42" stroke="black" stroke-width="2" stroke-dasharray="{patron}"/>')
        texto.append(f'<text x="{lx+52}" y="{ly}">{html.escape(nombre)}</text>')
    texto.append(f'<text x="520" y="542" text-anchor="middle">{html.escape(eje_x)}</text>')
    texto.append(f'<text transform="translate(24,290) rotate(-90)" text-anchor="middle">{html.escape(eje_y)}</text>')
    texto.append('</g></svg>')
    Path(ruta).write_text("\n".join(texto), encoding="utf-8")


def mostrar_resultado(resultado: dict, titulo: str) -> None:
    """Explicar el resultado en consola sin asumir que detenerse significa éxito."""
    print("\n" + "=" * 72 + "\n" + titulo + "\n" + "=" * 72)
    print("Inicio:", resultado["estado_inicial"])
    print("Último estado actual:", resultado["estado_final"])
    print("Mejor candidato observado:", resultado["mejor_estado"])
    print("Mejor costo:", resultado["mejor_costo"])
    print("Solución sin conflictos:", "sí" if resultado["exito"] else "no encontrada")
    print("Motivo de terminación:", resultado["motivo"])
    print("Evaluaciones:", resultado["evaluaciones"], "/", resultado["presupuesto"])
    print("Intentos:", resultado["intentos"])
    print(f"Tiempo de búsqueda y registro: {resultado['tiempo_s']:.6f} s")
    mostrar_tablero(resultado["mejor_estado"])
    if not resultado["exito"]:
        print("No encontrar una solución en esta corrida no demuestra que no exista.")


def registrar_resultado(carpeta: Path, nombre: str, resultado: dict,
                       parametros: dict) -> dict:
    """Exportar una corrida y devolver su fila para la tabla comparativa.

    Se registran todas las evaluaciones, no solo los movimientos aceptados.
    Los parámetros se guardan junto al resultado para no perder sus condiciones.
    La escritura sucede DESPUÉS de detener el reloj de la búsqueda.
    """
    fila = dict(parametros)
    for clave in ["estado_inicial", "estado_final", "costo_final", "mejor_estado",
                  "mejor_costo", "exito", "evaluaciones", "presupuesto", "tiempo_s",
                  "motivo", "intentos"]:
        fila[clave] = resultado[clave]
    guardar_csv(carpeta / f"{nombre}_resultado.csv", [fila])
    guardar_csv(carpeta / f"{nombre}_evaluaciones.csv", resultado["traza_evaluaciones"])
    guardar_csv(carpeta / f"{nombre}_movimientos.csv", resultado["movimientos"])
    guardar_csv(carpeta / f"{nombre}_decisiones.csv", resultado["decisiones"])
    guardar_csv(carpeta / f"{nombre}_intentos.csv", resultado["resumen_intentos"])
    return fila


def guardar_entorno(carpeta: Path, parametros: dict) -> None:
    """Conservar versión, sistema, parámetros y huella del código ejecutado.

    Una semilla no basta para repetir un experimento: también deben conservarse
    código, parámetros y entorno. SHA-256 es una huella para reconocer el archivo;
    no interviene en la búsqueda. Los tiempos varían incluso con la misma semilla.
    """
    datos = {"fecha_local": datetime.now().isoformat(), "python": sys.version,
             "sistema": platform.platform(), "parametros": parametros,
             "dependencias_externas": [],
             "medicion": "Incluye búsqueda y trazas en memoria; excluye pruebas, impresión, CSV y dibujo."}
    if "__file__" in globals():
        ruta = Path(__file__).resolve()
        datos["archivo"] = ruta.name
        datos["sha256"] = hashlib.sha256(ruta.read_bytes()).hexdigest()
    (carpeta / "entorno_y_parametros.json").write_text(
        json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")


def comprobar(condicion: bool, mensaje: str) -> None:
    """Detener las pruebas con un mensaje concreto cuando algo no coincide.

    No usamos assert para que las pruebas también funcionen al ejecutar Python
    con optimización. Un error no se ignora ni se convierte en un resultado.
    """
    if not condicion:
        raise RuntimeError("Prueba no superada: " + mensaje)


def comprobar_error(funcion, *argumentos) -> None:
    """Comprobar que una entrada inválida genera ValueError.

    *argumentos reúne las entradas en una secuencia y las entrega a la función.
    Esta pequeña función sirve solo para probar errores; no forma parte del
    algoritmo de búsqueda y puede estudiarse al final.
    """
    try:
        funcion(*argumentos)
    except ValueError:
        return
    raise RuntimeError("Una entrada inválida no fue rechazada como se esperaba.")


def pruebas_comunes() -> None:
    """Revisar la Tabla 2 y las funciones básicas antes de resolver un problema."""
    comprobar(contar_conflictos([1, 4, 1, 3]) == 1, "La Tabla 2 debe dar un conflicto.")
    comprobar(contar_conflictos([2, 4, 1, 3]) == 0, "El tablero conocido debe tener costo cero.")
    comprobar(contar_conflictos([1, 1, 1, 1]) == 6, "Cuatro reinas en una fila forman seis pares.")
    original = [1, 4, 1, 3]
    vecinos = generar_vecinos(original)
    comprobar(len(vecinos) == 12, "Deben existir doce vecinos.")
    comprobar(len({tuple(v) for v in vecinos}) == 12, "No debe haber vecinos repetidos.")
    comprobar(original == [1, 4, 1, 3], "El original no debe modificarse.")
    for vecino in vecinos:
        cambios = sum(a != b for a, b in zip(original, vecino))
        comprobar(cambios == 1, "Cada vecino debe cambiar exactamente una posición.")
    comprobar_error(validar_estado, [1, 5, 1, 3])
    comprobar_error(validar_estado, [True, 2])
    comprobar_error(validar_estado, [], 4)
    comprobar_error(validar_estado, [1, 2], 4)
    comprobar_error(crear_registro, 0)


# =============================================================================
# 5. EJECUCIÓN: EJEMPLO EDITABLE, ESTANCAMIENTO Y SOLUCIÓN YA CONOCIDA
# =============================================================================


def main() -> None:
    """Ejecutar una práctica completa sin pedir datos por teclado.

    Para empezar, deje los valores de la sección CONFIGURACIÓN como están.
    Después cambie solo ESTADO_INICIAL, ejecute de nuevo y compare las trazas.
    Las dos comprobaciones adicionales usan los ejemplos fijos del documento.
    """
    validar_estado(ESTADO_INICIAL)
    validar_entero("Presupuesto", PRESUPUESTO)
    if EJECUTAR_PRUEBAS:
        pruebas_colina()
        print("Pruebas superadas: conflictos, vecinos, Tablas 4 y 5, parada y presupuesto.")
    carpeta = preparar_carpeta("01_ascenso_colina")
    guardar_entorno(carpeta, {"estado_editable": ESTADO_INICIAL, "presupuesto": PRESUPUESTO})
    ejemplos = [("ejemplo_editable", ESTADO_INICIAL),
                ("estancamiento_documento", [1, 4, 2, 3]),
                ("inicio_ya_resuelto", [2, 4, 1, 3])]
    for nombre, estado in ejemplos:
        resultado = ascenso_colina(estado, PRESUPUESTO)
        mostrar_resultado(resultado, nombre.replace("_", " ").upper())
        print("\nCambios adoptados; evaluar un vecino no equivale a adoptarlo:")
        for fila in resultado["movimientos"]:
            print(f"Paso {fila['paso']}: {fila['estado']} | C = {fila['costo']} | "
                  f"evaluaciones acumuladas = {fila['evaluacion']}")
        registrar_resultado(carpeta, nombre, resultado, {"ejemplo": nombre})
        guardar_curvas_svg(carpeta / f"{nombre}_curva.svg",
                           {"Mejor costo observado": resultado["curva_mejor"]},
                           "Ascenso de colina: " + nombre.replace("_", " "))
    print("\nRESULTADOS GUARDADOS EN:\n", carpeta)
    print("Abra los CSV para revisar cada evaluación y los SVG para ver las curvas.")
    print("Pregunta: ¿por qué [1, 4, 2, 3] se detiene aunque se conoce una solución?")


# Esta condición ejecuta main solo al abrir/ejecutar el archivo, no al importarlo.
# Eso permite al docente llamar funciones individuales sin lanzar el experimento.
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nEjecución interrumpida. Los archivos ya escritos pueden estar incompletos.")
    except (ValueError, OSError) as error:
        print("\nNo se completó la ejecución:", error)
        print("Revise los valores de CONFIGURACIÓN y los permisos de la carpeta extraída.")
        # Se conserva el error para que Spyder muestre la línea exacta. No se
        # informa éxito ni se ocultan fallos de entrada, permisos o almacenamiento.
        raise
