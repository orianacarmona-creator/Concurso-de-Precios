import random

def _particionar(A, izq, der, indice_pivote, cont):
    """Particiona el subarreglo A[izq..der] alrededor de A[indice_pivote] in-place."""
    valor_pivote = A[indice_pivote]
    # Mover pivote al final
    A[indice_pivote], A[der] = A[der], A[indice_pivote]
    almacen = izq
    
    for i in range(izq, der):
        cont["comparaciones"] += 1
        if A[i] < valor_pivote:
            A[almacen], A[i] = A[i], A[almacen]
            almacen += 1
            
    # Mover pivote a su posición final
    A[der], A[almacen] = A[almacen], A[der]
    return almacen

def quickselect_inplace(A, izq, der, k, cont):
    """Devuelve el k-ésimo menor (k desde 0) modificando A in-place. Tiempo esperado O(n)."""
    if izq == der:
        return A[izq]
    
    indice_pivote = random.randint(izq, der)
    indice_pivote = _particionar(A, izq, der, indice_pivote, cont)
    
    if k == indice_pivote:
        return A[k]
    elif k < indice_pivote:
        return quickselect_inplace(A, izq, indice_pivote - 1, k, cont)
    else:
        return quickselect_inplace(A, indice_pivote + 1, der, k, cont)

def _insertion_sort_subarreglo(A, izq, der, cont):
    """Ordena grupos pequeños (<= 5) in-place para cumplir con no usar sorted()."""
    for i in range(izq + 1, der + 1):
        clave = A[i]
        j = i - 1
        while j >= izq:
            cont["comparaciones"] += 1
            if A[j] > clave:
                A[j + 1] = A[j]
                j -= 1
            else:
                break
        A[j + 1] = clave

def _seleccionar_pivote_bfprt(A, izq, der, cont):
    """Encuentra el índice de la mediana de medianas en A[izq..der]."""
    if der - izq < 5:
        _insertion_sort_subarreglo(A, izq, der, cont)
        return (izq + der) // 2
    
    # Mover las medianas de cada grupo de 5 al inicio del subarreglo
    for i in range(izq, der + 1, 5):
        sub_der = min(i + 4, der)
        _insertion_sort_subarreglo(A, i, sub_der, cont)
        mediana_idx = (i + sub_der) // 2
        destino = izq + (i - izq) // 5
        A[destino], A[mediana_idx] = A[mediana_idx], A[destino]
        
    num_medianas = (der - izq) // 5 + 1
    mid = izq + (num_medianas - 1) // 2
    # Llamada recursiva para encontrar la mediana de las medianas
    bfprt(A, izq, izq + num_medianas - 1, mid, cont)
    return mid

def bfprt(A, izq, der, k, cont):
    """Algoritmo Mediana de Medianas completo (peor caso O(n) garantizado)."""
    if izq == der:
        return A[izq]
    
    indice_pivote = _seleccionar_pivote_bfprt(A, izq, der, cont)
    indice_pivote = _particionar(A, izq, der, indice_pivote, cont)
    
    if k == indice_pivote:
        return A[k]
    elif k < indice_pivote:
        return bfprt(A, izq, indice_pivote - 1, k, cont)
    else:
        return bfprt(A, indice_pivote + 1, der, k, cont)

def mergesort_referencia(A, cont):
    """Solución de referencia O(n log n) propia para comparar comparaciones."""
    if len(A) <= 1:
        return A
    medio = len(A) // 2
    izq = mergesort_referencia(A[:medio], cont)
    der = mergesort_referencia(A[medio:], cont)
    
    resultado = []
    i = j = 0
    while i < len(izq) and j < len(der):
        cont["comparaciones"] += 1
        if izq[i] <= der[j]:
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1
    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    return resultado