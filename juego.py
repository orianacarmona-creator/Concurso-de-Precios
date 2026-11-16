import random
import time
import os
from algoritmos import quickselect_inplace, bfprt, mergesort_referencia

PRODUCTOS_BASE = [
    "Cafetera", "Audífonos", "Teclado", "Mouse", "Monitor", 
    "Silla", "Lámpara", "Mochila", "Termo", "Reloj", 
    "Parlante", "Cámara", "Micrófono", "Disco Duro", "Tableta"
]

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def generar_catalogo(n):
    nombres = random.sample(PRODUCTOS_BASE, min(n, len(PRODUCTOS_BASE)))
    return [(nombres[i], random.randint(10, 500) * 1000) for i in range(n)]

def evaluar_metodos(precios, k):
    """Ejecuta los 3 métodos sobre copias del arreglo y devuelve el resultado y comparaciones."""
    c_qs = {"comparaciones": 0}
    res_qs = quickselect_inplace(precios.copy(), 0, len(precios) - 1, k, c_qs)
    
    c_bfprt = {"comparaciones": 0}
    res_bfprt = bfprt(precios.copy(), 0, len(precios) - 1, k, c_bfprt)
    
    c_ref = {"comparaciones": 0}
    ordenado = mergesort_referencia(precios.copy(), c_ref)
    res_ref = ordenado[k]
    
    return res_ref, c_qs["comparaciones"], c_bfprt["comparaciones"], c_ref["comparaciones"]

def calcular_puntos(estimacion, real):
    """Gana más puntos quien más se acerque sin pasarse."""
    if estimacion > real:
        return 0
    diferencia_pct = (real - estimacion) / real
    return max(0, int(100 * (1 - diferencia_pct)))

def jugar():
    print("=== EL PRECIO JUSTO: CONCURSO DE PRECIOS ===")
    num_jugadores = int(input("Número de jugadores humanos (1 a 3): "))
    jugadores = [input(f"Nombre del jugador {i+1}: ") for i in range(num_jugadores)]
    puntajes = {j: 0 for j in jugadores}
    
    # 2 rondas normales (1 de mediana, 1 de k-ésimo)
    for ronda in range(1, 3):
        n = 7
        catalogo = generar_catalogo(n)
        precios = [p[1] for p in catalogo]
        
        print(f"\n--- RONDA {ronda} ---")
        print("Memoriza los precios (tienes 5 segundos):")
        for prod, precio in catalogo:
            print(f" - {prod}: ${precio:,}")
        
        time.sleep(5)
        limpiar_pantalla()
        
        if ronda == 1:
            k = n // 2
            pregunta = "¿Cuál es el PRECIO MEDIANO del catálogo?"
        else:
            k = random.randint(0, n - 1)
            pregunta = f"¿Cuál es el {k + 1}º producto MÁS BARATO?"
            
        print(f"\n¡TIEMPO! {pregunta}")
        print("(Gana puntos quien más se acerque SIN PASARSE)")
        
        real, comp_qs, comp_bfprt, comp_ref = evaluar_metodos(precios, k)
        
        for j in jugadores:
            apuesta = int(input(f"{j}, ingresa tu precio: $"))
            pts = calcular_puntos(apuesta, real)
            puntajes[j] += pts
            print(f" -> {j} gana {pts} puntos.")
            
        print(f"\nRespuesta exacta: ${real:,}")
        print(f"Comparaciones -> Quickselect: {comp_qs} | Mediana de Medianas: {comp_bfprt} | Ordenar (MergeSort): {comp_ref}")

    # Ronda final: Subasta silenciosa
    print("\n--- RONDA FINAL: SUBASTA SILENCIOSA ---")
    producto_final = ("Consola Retro", random.randint(100, 400) * 1000)
    print(f"Producto a subastar: {producto_final[0]} (Valor referencial oculto)")
    print("El precio de venta será la MEDIANA de todas las ofertas (humanos + 4 bots).")
    
    ofertas = []
    ofertas_jugadores = {}
    for j in jugadores:
        of = int(input(f"{j}, haz tu oferta secreta: $"))
        ofertas.append(of)
        ofertas_jugadores[j] = of
        
    # Bots hacen ofertas (uno exagera para probar que la mediana protege el precio)
    for b in range(3):
        ofertas.append(random.randint(80, 420) * 1000)
    ofertas.append(9999000) # Bot manipulador con oferta exagerada
    
    k_subasta = len(ofertas) // 2
    precio_venta, comp_qs, comp_bfprt, comp_ref = evaluar_metodos(ofertas, k_subasta)
    
    print(f"\nOfertas totales en la mesa: {[f'${x:,}' for x in ofertas]}")
    print(f"Precio de venta (Mediana): ${precio_venta:,}")
    print(f"Comparaciones -> Quickselect: {comp_qs} | Mediana de Medianas: {comp_bfprt} | Ordenar: {comp_ref}")
    
    for j, of in ofertas_jugadores.items():
        pts = calcular_puntos(of, precio_venta)
        puntajes[j] += pts
        
    print("\n=== TABLA DE POSICIONES FINAL ===")
    for j, pts in sorted(puntajes.items(), key=lambda x: x[1], reverse=True):
        print(f"{j}: {pts} pts")

if __name__ == "__main__":
    jugar()