# Comparación experimental: ascenso de colina vs. ascenso de colina con reinicios aleatorios
# Requiere ascenso_colina.py en la misma carpeta. Solo usa bibliotecas estándar.
import csv, random, time, statistics, platform, sys, hashlib, json
from pathlib import Path
import ascenso_colina as base

N = 8
PRESUPUESTO = 3000
CORRIDAS = 30
SEMILLA_BASE = 20261018


def ascenso_con_reinicios(estado_inicial, presupuesto=3000, semilla=0):
    """Versión modificada: reinicia aleatoriamente al alcanzar un mínimo local.
    Mantiene la misma representación, función de conflictos y vecindad.
    Todos los intentos comparten un único presupuesto de evaluaciones.
    """
    base.validar_estado(estado_inicial)
    rng = random.Random(semilla)
    registro = base.crear_registro(presupuesto)
    inicio = time.perf_counter()
    actual_inicio = estado_inicial.copy()
    actual_final = estado_inicial.copy()
    costo_actual = None
    movimientos = []
    resumen_intentos = []
    intentos = 0
    motivo = "presupuesto_agotado"
    while registro['evaluaciones'] < presupuesto:
        intentos += 1
        if intentos == 1:
            inicio_intento = actual_inicio
        else:
            inicio_intento = [rng.randint(1, N) for _ in range(N)]
        resultado_intento = base.ejecutar_intento_colina(inicio_intento, registro, intentos)
        actual_final = resultado_intento['estado_final']
        costo_actual = resultado_intento['costo_final']
        resumen_intentos.append({
            'intento': intentos,
            'estado_inicial': inicio_intento.copy(),
            'costo_final': costo_actual,
            'motivo': resultado_intento['motivo'],
            'evaluaciones_acumuladas': registro['evaluaciones']
        })
        movimientos.extend(resultado_intento['movimientos'])
        if registro['mejor_costo'] == 0:
            motivo = 'solucion_encontrada'
            break
        if resultado_intento['motivo'] == 'presupuesto_agotado':
            motivo = 'presupuesto_agotado'
            break
        # Si llegó a un mínimo local sin solución, comienza otro intento.
        motivo = 'presupuesto_agotado'
    tiempo_s = time.perf_counter() - inicio
    return base.cerrar_resultado(actual_inicio, actual_final, costo_actual, registro,
        motivo, tiempo_s, intentos, movimientos, [], resumen_intentos)


def estado_aleatorio(semilla):
    return base.generar_estado_inicial(N, semilla)


def resumen(nombre, filas):
    n = len(filas)
    exitos = sum(1 for r in filas if r['exito'])
    costos = [int(r['mejor_costo']) for r in filas]
    evaluaciones = [int(r['evaluaciones']) for r in filas]
    tiempos = [float(r['tiempo_s']) for r in filas]
    return {
        'version': nombre, 'corridas': n, 'exitos': exitos,
        'tasa_exito_pct': 100*exitos/n,
        'mejor_costo_minimo': min(costos), 'costo_media': statistics.mean(costos),
        'costo_desviacion_estandar': statistics.stdev(costos) if n > 1 else 0.0,
        'evaluaciones_media': statistics.mean(evaluaciones),
        'evaluaciones_desviacion_estandar': statistics.stdev(evaluaciones) if n > 1 else 0.0,
        'tiempo_medio_s': statistics.mean(tiempos),
        'tiempo_desviacion_estandar_s': statistics.stdev(tiempos) if n > 1 else 0.0,
    }


def main():
    # Verificaciones de cuatro reinas exigidas por el material.
    base.pruebas_colina()
    assert base.contar_conflictos([1,4,1,3]) == 1
    assert base.contar_conflictos([2,4,1,3]) == 0
    assert base.contar_conflictos([1,1,1,1]) == 6
    assert len(base.generar_vecinos([1,1,1,1])) == 12

    out = Path(__file__).resolve().parent / 'resultados_mejora'
    out.mkdir(exist_ok=True)
    filas = []
    curvas = {'Inicial': [], 'Mejorada': []}
    for i in range(CORRIDAS):
        semilla = SEMILLA_BASE + i
        inicial = estado_aleatorio(semilla)
        r = base.ascenso_colina(inicial, PRESUPUESTO)
        filas.append({
            'version':'Inicial', 'corrida':i+1, 'semilla':semilla,
            'estado_inicial':str(inicial), 'estado_final':str(r['mejor_estado']),
            'mejor_costo':r['mejor_costo'], 'exito':int(r['exito']),
            'evaluaciones':r['evaluaciones'], 'tiempo_s':f"{r['tiempo_s']:.8f}",
            'motivo':r['motivo'], 'intentos':r['intentos'],
            'presupuesto':PRESUPUESTO
        })
        curvas['Inicial'].append(r['curva_mejor'])
        rm = ascenso_con_reinicios(inicial, PRESUPUESTO, semilla + 100000)
        filas.append({
            'version':'Mejorada', 'corrida':i+1, 'semilla':semilla,
            'estado_inicial':str(inicial), 'estado_final':str(rm['mejor_estado']),
            'mejor_costo':rm['mejor_costo'], 'exito':int(rm['exito']),
            'evaluaciones':rm['evaluaciones'], 'tiempo_s':f"{rm['tiempo_s']:.8f}",
            'motivo':rm['motivo'], 'intentos':rm['intentos'],
            'presupuesto':PRESUPUESTO
        })
        curvas['Mejorada'].append(rm['curva_mejor'])

    with open(out/'resultados_por_corrida.csv','w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(filas[0].keys())); w.writeheader(); w.writerows(filas)
    sums=[resumen(n,[r for r in filas if r['version']==n]) for n in ['Inicial','Mejorada']]
    with open(out/'resumen_estadistico.csv','w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(sums[0].keys())); w.writeheader(); w.writerows(sums)
    env={
        'n_reinas':N,'corridas_por_version':CORRIDAS,'presupuesto_por_corrida':PRESUPUESTO,
        'semillas_iniciales':[SEMILLA_BASE+i for i in range(CORRIDAS)],
        'python':sys.version,'plataforma':platform.platform(),
        'archivo_base_sha256':hashlib.sha256(Path(base.__file__).read_bytes()).hexdigest(),
        'nota_tiempo':'Los tiempos dependen del equipo y de la carga del sistema; las ejecuciones se midieron en este entorno.'
    }
    (out/'parametros_y_entorno.json').write_text(json.dumps(env,indent=2,ensure_ascii=False),encoding='utf-8')
    # SVG simple: curvas promedio, comparadas por evaluación, con relleno al último valor observado solo para visualizar.
    def svg_curva(path, title, series):
        W,H=900,500; left,right,top,bottom=75,25,55,65; pw=W-left-right; ph=H-top-bottom
        maxx=PRESUPUESTO; maxy=28
        colors=['#2563eb','#dc2626']
        lines=[]
        lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
        lines.append('<rect width="100%" height="100%" fill="white"/>')
        lines.append(f'<text x="{W/2}" y="28" text-anchor="middle" font-size="20" font-family="sans-serif">{title}</text>')
        for tick in range(0,maxy+1,4):
            y=top+ph-(tick/maxy)*ph
            lines.append(f'<line x1="{left}" y1="{y:.1f}" x2="{W-right}" y2="{y:.1f}" stroke="#dddddd"/>')
            lines.append(f'<text x="{left-12}" y="{y+5:.1f}" text-anchor="end" font-size="12" font-family="sans-serif">{tick}</text>')
        for tick in [0,500,1000,1500,2000,2500,3000]:
            x=left+(tick/maxx)*pw
            lines.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{top+ph}" stroke="#eeeeee"/>')
            lines.append(f'<text x="{x:.1f}" y="{top+ph+22}" text-anchor="middle" font-size="12" font-family="sans-serif">{tick}</text>')
        lines.append(f'<line x1="{left}" y1="{top+ph}" x2="{W-right}" y2="{top+ph}" stroke="#222"/>')
        lines.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top+ph}" stroke="#222"/>')
        for idx,(name, curveset) in enumerate(series.items()):
            avg=[]
            for e in range(PRESUPUESTO):
                vals=[]
                for curve in curveset:
                    vals.append(curve[e] if e<len(curve) else curve[-1])
                avg.append(sum(vals)/len(vals))
            pts=[]
            step= max(1, PRESUPUESTO//500)
            for e in range(0,len(avg),step):
                x=left+(e/maxx)*pw; y=top+ph-(avg[e]/maxy)*ph
                pts.append(f'{x:.1f},{y:.1f}')
            lines.append(f'<polyline fill="none" stroke="{colors[idx]}" stroke-width="2.5" points="{" ".join(pts)}"/>')
            lx=left+idx*180
            lines.append(f'<line x1="{lx}" y1="{H-20}" x2="{lx+28}" y2="{H-20}" stroke="{colors[idx]}" stroke-width="3"/>')
            lines.append(f'<text x="{lx+35}" y="{H-15}" font-size="13" font-family="sans-serif">{name}</text>')
        lines.append(f'<text x="{W/2}" y="{H-2}" text-anchor="middle" font-size="12" font-family="sans-serif">Evaluaciones (promedio; curvas detenidas se prolongan visualmente)</text>')
        lines.append(f'<text x="18" y="{H/2}" transform="rotate(-90 18 {H/2})" text-anchor="middle" font-size="12" font-family="sans-serif">Mejor costo C(q)</text>')
        lines.append('</svg>')
        path.write_text('\n'.join(lines),encoding='utf-8')
    svg_curva(out/'figura1_curva_promedio.svg','Figura 1. Convergencia promedio (30 corridas)',curvas)
    print('VERIFICACIONES 4 REINAS: OK')
    print('RESUMEN')
    for s in sums: print(s)
    print('SALIDA',out)

if __name__=='__main__': main()
