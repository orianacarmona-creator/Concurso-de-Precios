"""
laboratorio.py  -  Experimento de Modo Laboratorio
Proyecto 7 · El Precio Justo · Grupo 7

Ejecutar:
    python laboratorio.py

Genera dos gráficas en la carpeta del proyecto:
    grafica_comparaciones.png   —  número de comparaciones vs n
    grafica_tiempo.png          —  tiempo de ejecución vs n

Tamaños evaluados: n = 1_000, 10_000, 100_000, 1_000_000
Para cada n se prueba con:
    - Precios ALEATORIOS
    - Precios ORDENADOS (peor caso para Quickselect aleatorio)
"""

import random
import time
import sys
import os
import math

# ---------------------------------------------------------------------------
# Importar algoritmos del proyecto
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.dirname(__file__))
from algoritmos import quickselect_inplace, bfprt, mergesort_referencia


# ---------------------------------------------------------------------------
# Función de medición
# ---------------------------------------------------------------------------
def medir(A_original, k):
    """
    Ejecuta los 3 algoritmos sobre copias de A_original para buscar el k-ésimo menor.
    Devuelve (comp_qs, comp_bfprt, comp_ms, t_qs, t_bfprt, t_ms, resultado).
    Lanza AssertionError si los 3 métodos no coinciden (Requerimiento 5).
    """
    # --- Quickselect in-place ---
    copia_qs = A_original[:]
    cont_qs = {"comparaciones": 0}
    t0 = time.perf_counter()
    res_qs = quickselect_inplace(copia_qs, 0, len(copia_qs) - 1, k, cont_qs)
    t_qs = time.perf_counter() - t0

    # --- BFPRT (Mediana de Medianas) ---
    copia_bfprt = A_original[:]
    cont_bfprt = {"comparaciones": 0}
    t0 = time.perf_counter()
    res_bfprt = bfprt(copia_bfprt, 0, len(copia_bfprt) - 1, k, cont_bfprt)
    t_bfprt = time.perf_counter() - t0

    # --- MergeSort de referencia ---
    copia_ms = A_original[:]
    cont_ms = {"comparaciones": 0}
    t0 = time.perf_counter()
    ordenado = mergesort_referencia(copia_ms, cont_ms)
    t_ms = time.perf_counter() - t0
    res_ms = ordenado[k]

    # -----------------------------------------------------------------------
    # REQUERIMIENTO 5: Validar que los 3 métodos dan el mismo resultado
    # -----------------------------------------------------------------------
    assert res_qs == res_bfprt == res_ms, (
        f"¡INCONSISTENCIA DETECTADA! "
        f"Quickselect={res_qs}, BFPRT={res_bfprt}, MergeSort={res_ms} "
        f"para k={k}, n={len(A_original)}"
    )

    return (
        cont_qs["comparaciones"],
        cont_bfprt["comparaciones"],
        cont_ms["comparaciones"],
        t_qs,
        t_bfprt,
        t_ms,
        res_ms,
    )


# ---------------------------------------------------------------------------
# Experimento principal
# ---------------------------------------------------------------------------
TAMAÑOS = [1_000, 10_000, 100_000, 1_000_000]
REPETICIONES = 3   # promediamos varias corridas para reducir ruido


def ejecutar_experimento():
    print("=" * 70)
    print("  LABORATORIO — Comparación de Algoritmos de Selección")
    print("  Proyecto 7 · El Precio Justo · Grupo 7")
    print("=" * 70)

    resultados = {
        "aleatorio": {"comp_qs": [], "comp_bfprt": [], "comp_ms": [],
                      "t_qs": [], "t_bfprt": [], "t_ms": []},
        "ordenado":  {"comp_qs": [], "comp_bfprt": [], "comp_ms": [],
                      "t_qs": [], "t_bfprt": [], "t_ms": []},
    }

    for n in TAMAÑOS:
        k = n // 2  # buscamos la mediana

        for tipo in ("aleatorio", "ordenado"):
            acum = {c: 0 for c in ("comp_qs", "comp_bfprt", "comp_ms",
                                   "t_qs", "t_bfprt", "t_ms")}

            for _ in range(REPETICIONES):
                if tipo == "aleatorio":
                    A = [random.randint(1, 10 * n) for _ in range(n)]
                else:
                    A = list(range(n))   # peor caso para Quickselect aleatorio

                cqs, cbfprt, cms, tqs, tbfprt, tms, _ = medir(A, k)
                acum["comp_qs"]    += cqs
                acum["comp_bfprt"] += cbfprt
                acum["comp_ms"]    += cms
                acum["t_qs"]       += tqs
                acum["t_bfprt"]    += tbfprt
                acum["t_ms"]       += tms

            for clave in acum:
                acum[clave] /= REPETICIONES
                resultados[tipo][clave].append(acum[clave])

            print(f"\n  n={n:>9,}  [{tipo:>9}]")
            print(f"    Quickselect   → {acum['comp_qs']:>12,.0f} comps  |  {acum['t_qs']*1000:>8.2f} ms")
            print(f"    BFPRT         → {acum['comp_bfprt']:>12,.0f} comps  |  {acum['t_bfprt']*1000:>8.2f} ms")
            print(f"    MergeSort     → {acum['comp_ms']:>12,.0f} comps  |  {acum['t_ms']*1000:>8.2f} ms")

    print("\n  ✅ Validación (Req. 5): todos los resultados son consistentes.")
    return resultados


# ---------------------------------------------------------------------------
# Gráficas
# ---------------------------------------------------------------------------
def graficar(resultados):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.ticker as ticker
    except ImportError:
        print("\n  ⚠ matplotlib no está instalado. No se generarán gráficas.")
        print("     Instálalo con:  pip install matplotlib")
        return

    etiquetas_n = [f"10³" if n == 1_000 else
                   f"10⁴" if n == 10_000 else
                   f"10⁵" if n == 100_000 else
                   f"10⁶" for n in TAMAÑOS]

    colores = {"Quickselect": "#2563eb", "BFPRT": "#16a34a", "MergeSort (ref)": "#dc2626"}
    estilos = {"aleatorio": "-o", "ordenado": "--s"}

    # ---- Gráfica 1: Comparaciones ----------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=False)
    fig.suptitle("Número de comparaciones vs. n  —  Grupo 7: El Precio Justo",
                 fontsize=14, fontweight="bold")

    for idx, tipo in enumerate(("aleatorio", "ordenado")):
        ax = axes[idx]
        ax.plot(TAMAÑOS, resultados[tipo]["comp_qs"],
                estilos[tipo], color=colores["Quickselect"],
                label="Quickselect (esperado O(n))", linewidth=2, markersize=6)
        ax.plot(TAMAÑOS, resultados[tipo]["comp_bfprt"],
                estilos[tipo], color=colores["BFPRT"],
                label="BFPRT (peor caso O(n))", linewidth=2, markersize=6,
                linestyle="--")
        ax.plot(TAMAÑOS, resultados[tipo]["comp_ms"],
                estilos[tipo], color=colores["MergeSort (ref)"],
                label="MergeSort ref. O(n log n)", linewidth=2, markersize=6,
                linestyle=":")
        ax.set_title(f"Precios {'aleatorios' if tipo == 'aleatorio' else 'ordenados (peor caso)'}")
        ax.set_xlabel("n (tamaño del arreglo)", fontsize=11)
        ax.set_ylabel("Comparaciones promedio", fontsize=11)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xticks(TAMAÑOS)
        ax.set_xticklabels(etiquetas_n)
        ax.legend(fontsize=9)
        ax.grid(True, which="both", linestyle=":", alpha=0.5)

    plt.tight_layout()
    ruta_comp = os.path.join(os.path.dirname(__file__), "grafica_comparaciones.png")
    plt.savefig(ruta_comp, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"\n  📊 Gráfica guardada: {ruta_comp}")

    # ---- Gráfica 2: Tiempo -----------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=False)
    fig.suptitle("Tiempo de ejecución (ms) vs. n  —  Grupo 7: El Precio Justo",
                 fontsize=14, fontweight="bold")

    for idx, tipo in enumerate(("aleatorio", "ordenado")):
        ax = axes[idx]
        ax.plot(TAMAÑOS, [t * 1000 for t in resultados[tipo]["t_qs"]],
                estilos[tipo], color=colores["Quickselect"],
                label="Quickselect", linewidth=2, markersize=6)
        ax.plot(TAMAÑOS, [t * 1000 for t in resultados[tipo]["t_bfprt"]],
                estilos[tipo], color=colores["BFPRT"],
                label="BFPRT", linewidth=2, markersize=6, linestyle="--")
        ax.plot(TAMAÑOS, [t * 1000 for t in resultados[tipo]["t_ms"]],
                estilos[tipo], color=colores["MergeSort (ref)"],
                label="MergeSort ref.", linewidth=2, markersize=6, linestyle=":")
        ax.set_title(f"Precios {'aleatorios' if tipo == 'aleatorio' else 'ordenados (peor caso)'}")
        ax.set_xlabel("n (tamaño del arreglo)", fontsize=11)
        ax.set_ylabel("Tiempo (ms)", fontsize=11)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xticks(TAMAÑOS)
        ax.set_xticklabels(etiquetas_n)
        ax.legend(fontsize=9)
        ax.grid(True, which="both", linestyle=":", alpha=0.5)

    plt.tight_layout()
    ruta_tiempo = os.path.join(os.path.dirname(__file__), "grafica_tiempo.png")
    plt.savefig(ruta_tiempo, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  📊 Gráfica guardada: {ruta_tiempo}")

    return ruta_comp, ruta_tiempo


# ---------------------------------------------------------------------------
# Punto de entrada
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    resultados = ejecutar_experimento()
    graficar(resultados)
    print("\n  Experimento finalizado.\n")
