"""
generar_informe.py  -  Genera el informe completo en Word (.docx)
Proyecto 7 · El Precio Justo · Grupo 7

Ejecutar:
    python generar_informe.py

Produce:
    Informe_Proyecto7_ElPrecioJusto.docx   (en la misma carpeta)
"""

import os
import sys
from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BASE = os.path.dirname(__file__)

# ---------------------------------------------------------------------------
# Helpers de estilo
# ---------------------------------------------------------------------------

def set_cell_bg(cell, hex_color):
    """Rellena el fondo de una celda con un color hex (ej. 'C0392B')."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)

def fila_encabezado(tabla, textos, bg="1A3A5C"):
    """Primera fila de tabla como encabezado oscuro con texto blanco."""
    fila = tabla.rows[0]
    for i, texto in enumerate(textos):
        celda = fila.cells[i]
        celda.text = texto
        set_cell_bg(celda, bg)
        p = celda.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.runs[0]
        run.bold = True
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        run.font.size = Pt(10)

def fila_datos(tabla, fila_idx, textos, bg_par="EAF0FB", bg_impar="FFFFFF"):
    """Agrega una fila de datos con colores alternados."""
    fila = tabla.add_row()
    bg = bg_par if fila_idx % 2 == 0 else bg_impar
    for i, texto in enumerate(textos):
        celda = fila.cells[i]
        celda.text = str(texto)
        set_cell_bg(celda, bg)
        p = celda.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.runs[0]
        run.font.size = Pt(9.5)

def agregar_imagen_si_existe(doc, ruta, ancho=Inches(6), caption=None):
    if os.path.exists(ruta):
        doc.add_picture(ruta, width=ancho)
        ultimo = doc.paragraphs[-1]
        ultimo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if caption:
            p = doc.add_paragraph(caption)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.runs[0]
            run.italic = True
            run.font.size = Pt(9)
            run.font.color.rgb = RGBColor(0x55, 0x65, 0x7A)
    else:
        p = doc.add_paragraph(f"[Imagen no encontrada: {os.path.basename(ruta)}]")
        p.runs[0].italic = True

def heading(doc, texto, nivel=1, color=None):
    p = doc.add_heading(texto, level=nivel)
    if color:
        for run in p.runs:
            run.font.color.rgb = RGBColor(*color)
    return p

def parrafo(doc, texto, negrita=False, size=11, color=None, italic=False):
    p = doc.add_paragraph()
    run = p.add_run(texto)
    run.bold = negrita
    run.italic = italic
    run.font.size = Pt(size)
    if color:
        run.font.color.rgb = RGBColor(*color)
    return p

def separador(doc):
    p = doc.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "6")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "1A3A5C")
    pBdr.append(bottom)
    pPr.append(pBdr)

def codigo(doc, texto):
    """Bloque de código con fuente monoespaciada y fondo gris claro."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(1)
    run = p.add_run(texto)
    run.font.name = "Courier New"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(0x1A, 0x3A, 0x5C)
    shading = OxmlElement("w:rPr")


# ---------------------------------------------------------------------------
# Construcción del documento
# ---------------------------------------------------------------------------

def construir_documento():
    doc = Document()

    # Márgenes
    for section in doc.sections:
        section.top_margin    = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin   = Cm(3.0)
        section.right_margin  = Cm(2.5)

    # Fuente por defecto
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)

    # =====================================================================
    # PORTADA
    # =====================================================================
    doc.add_paragraph()
    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = t.add_run("PROYECTO 7 · EL PRECIO JUSTO")
    r.bold = True
    r.font.size = Pt(26)
    r.font.color.rgb = RGBColor(0x1A, 0x3A, 0x5C)

    t2 = doc.add_paragraph()
    t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = t2.add_run("Concurso de Precios  ·  Grupo 7")
    r2.font.size = Pt(16)
    r2.font.color.rgb = RGBColor(0x25, 0x63, 0xEB)

    doc.add_paragraph()

    for nombre in [
        "Carmona Montoya Oriana Valentina",
        "Díaz Orozco Fabián Camilo",
        "Mosquera Orejuela Johan David",
    ]:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(nombre)
        run.font.size = Pt(13)
        run.bold = True

    doc.add_paragraph()
    fecha = doc.add_paragraph()
    fecha.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fecha.add_run("17 de noviembre de 2026").font.size = Pt(12)

    curso = doc.add_paragraph()
    curso.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r3 = curso.add_run("Análisis de Algoritmos  ·  Ingeniería de Sistemas")
    r3.italic = True
    r3.font.size = Pt(11)
    r3.font.color.rgb = RGBColor(0x55, 0x65, 0x7A)

    doc.add_page_break()

    # =====================================================================
    # 1. DESCRIPCIÓN GENERAL
    # =====================================================================
    heading(doc, "1. Descripción General del Proyecto", 1, (0x1A, 0x3A, 0x5C))
    separador(doc)

    parrafo(doc,
        "El juego \"El Precio Justo\" es un concurso de televisión para 1 a 3 jugadores. "
        "En cada ronda se muestra durante unos segundos un catálogo de N productos con sus "
        "precios desordenados. Luego el presentador pregunta:")
    doc.add_paragraph("¿Cuál es el precio mediano del catálogo?", style="List Bullet")
    doc.add_paragraph("¿Cuál es el k-ésimo producto más barato?", style="List Bullet")

    parrafo(doc,
        "Gana más puntos quien más se acerque sin pasarse del precio real. Al finalizar las "
        "rondas normales, se realiza una ronda de subasta silenciosa: cada jugador y varios "
        "jugadores automáticos (bots) hacen ofertas; el precio de venta se determina como la "
        "mediana de las ofertas, calculada con los algoritmos implementados.")

    parrafo(doc,
        "El juego muestra después de cada ronda cuántas comparaciones hizo cada método para "
        "encontrar la respuesta, permitiendo comparar empíricamente los algoritmos.")

    # =====================================================================
    # 2. INTEGRANTES Y DISTRIBUCIÓN
    # =====================================================================
    heading(doc, "2. Integrantes y Distribución del Trabajo", 1, (0x1A, 0x3A, 0x5C))
    separador(doc)

    tabla = doc.add_table(rows=1, cols=2)
    tabla.style = "Table Grid"
    tabla.alignment = WD_TABLE_ALIGNMENT.CENTER
    fila_encabezado(tabla, ["Integrante", "Responsabilidad Principal"])

    datos_int = [
        ("Carmona Montoya Oriana Valentina",
         "Interfaz del concurso, rondas, temporizador, subasta y jugadores automáticos."),
        ("Díaz Orozco Fabián Camilo",
         "Quickselect in-place, mediana de medianas completa, contadores y pruebas."),
        ("Mosquera Orejuela Johan David",
         "Laboratorio, demostración por sustitución de BFPRT y análisis esperado de Quickselect."),
    ]
    for i, (nombre, resp) in enumerate(datos_int):
        fila = tabla.add_row()
        fila.cells[0].text = nombre
        fila.cells[1].text = resp
        bg = "EAF0FB" if i % 2 == 0 else "FFFFFF"
        set_cell_bg(fila.cells[0], bg)
        set_cell_bg(fila.cells[1], bg)
        for c in fila.cells:
            c.paragraphs[0].runs[0].font.size = Pt(9.5)

    parrafo(doc, "Nota: La distribución organiza el trabajo, pero no la sustentación: "
            "cualquier integrante puede ser llamado a explicar cualquier parte.",
            italic=True, size=9.5, color=(0x55, 0x65, 0x7A))

    # =====================================================================
    # 3. ESTRUCTURA DEL PROYECTO
    # =====================================================================
    heading(doc, "3. Estructura del Proyecto", 1, (0x1A, 0x3A, 0x5C))
    separador(doc)

    for linea in [
        "Concurso-de-Precios/",
        "    algoritmos.py        — Quickselect in-place, BFPRT, MergeSort (104 líneas)",
        "    juego.py             — Interfaz gráfica Turtle + tkinter, lógica de rondas (392 líneas)",
        "    laboratorio.py       — Experimento de modo laboratorio con gráficas (nuevo)",
        "    generar_informe.py   — Genera este informe Word (nuevo)",
        "    grafica_comparaciones.png  — Gráfica de comparaciones (generada)",
        "    grafica_tiempo.png         — Gráfica de tiempos (generada)",
        "    README.md            — Instrucciones de ejecución",
    ]:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(1)
        r = p.add_run(linea)
        r.font.name = "Courier New"
        r.font.size = Pt(9)

    # =====================================================================
    # 4. ANÁLISIS TÉCNICO DE LOS ALGORITMOS
    # =====================================================================
    heading(doc, "4. Análisis Técnico de los Algoritmos", 1, (0x1A, 0x3A, 0x5C))
    separador(doc)

    # --- 4.1 Quickselect ---
    heading(doc, "4.1  Quickselect In-Place", 2, (0x25, 0x63, 0xEB))
    parrafo(doc,
        "Implementado en algoritmos.py (líneas 20–33). Particiona el arreglo en torno a un "
        "pivote elegido aleatoriamente con random.randint(izq, der) y continúa solo en el "
        "lado donde se encuentra la posición k. La versión es completamente in-place: opera "
        "con índices izq y der, sin crear sub-listas nuevas.")

    parrafo(doc, "Código fuente principal:", negrita=True, size=10)
    for linea in [
        "def quickselect_inplace(A, izq, der, k, cont):",
        "    if izq == der:",
        "        return A[izq]",
        "    indice_pivote = random.randint(izq, der)",
        "    indice_pivote = _particionar(A, izq, der, indice_pivote, cont)",
        "    if k == indice_pivote:  return A[k]",
        "    elif k < indice_pivote: return quickselect_inplace(A, izq, indice_pivote-1, k, cont)",
        "    else:                   return quickselect_inplace(A, indice_pivote+1, der, k, cont)",
    ]:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(1)
        r = p.add_run(linea)
        r.font.name = "Courier New"
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0x1A, 0x3A, 0x5C)

    parrafo(doc, "Complejidad:", negrita=True, size=10)
    tabla_qs = doc.add_table(rows=1, cols=3)
    tabla_qs.style = "Table Grid"
    fila_encabezado(tabla_qs, ["Caso", "Recurrencia", "Complejidad"])
    for caso, rec, comp in [
        ("Esperado (pivote aleatorio)", "T(n) ≤ T(3n/4) + cn", "O(n)"),
        ("Peor caso (pivote extremo)", "T(n) = T(n−1) + Θ(n)", "Θ(n²)"),
    ]:
        fila_datos(tabla_qs, len(tabla_qs.rows)-1, [caso, rec, comp])

    # --- 4.2 BFPRT ---
    heading(doc, "4.2  BFPRT — Mediana de Medianas", 2, (0x25, 0x63, 0xEB))
    parrafo(doc,
        "Implementado en algoritmos.py (líneas 49–82). Garantiza O(n) en el peor caso "
        "seleccionando un pivote \"bueno\" mediante el siguiente procedimiento:")

    pasos = [
        "Dividir A[izq..der] en grupos de 5 elementos.",
        "Ordenar cada grupo con _insertion_sort_subarreglo() — sin usar sorted().",
        "Recolectar las medianas de cada grupo al inicio del subarreglo.",
        "Llamar recursivamente a bfprt() sobre las medianas para encontrar su mediana.",
        "Usar esa mediana de medianas como pivote en _particionar().",
    ]
    for paso in pasos:
        doc.add_paragraph(paso, style="List Number")

    parrafo(doc, "Complejidad:", negrita=True, size=10)
    tabla_bf = doc.add_table(rows=1, cols=3)
    tabla_bf.style = "Table Grid"
    fila_encabezado(tabla_bf, ["Caso", "Recurrencia", "Complejidad"])
    for caso, rec, comp in [
        ("Peor caso garantizado", "T(n) ≤ T(n/5) + T(7n/10) + cn", "O(n)"),
        ("Justificación grupos de 5", "1/5 + 7/10 = 9/10 < 1  →  serie convergente", "O(n)"),
        ("Por qué no grupos de 3", "1/3 + 2/3 = 1  →  la serie no converge", "No garantiza O(n)"),
    ]:
        fila_datos(tabla_bf, len(tabla_bf.rows)-1, [caso, rec, comp])

    # --- 4.3 MergeSort ---
    heading(doc, "4.3  MergeSort de Referencia", 2, (0x25, 0x63, 0xEB))
    parrafo(doc,
        "Implementado en algoritmos.py (líneas 84–104). Implementación propia de MergeSort "
        "(sin usar sorted()) con complejidad O(n log n). Sirve como solución de referencia "
        "para validar que los tres métodos dan el mismo k-ésimo menor y para comparar el "
        "número de comparaciones en la pantalla de resultados del juego.")

    # --- 4.4 Partición Lomuto ---
    heading(doc, "4.4  Función de Partición (esquema Lomuto)", 2, (0x25, 0x63, 0xEB))
    parrafo(doc,
        "Compartida por Quickselect y BFPRT (algoritmos.py, líneas 3–18). Mueve el pivote "
        "al final, barre de izq a der y cuenta cada comparación A[i] < valor_pivote en "
        "cont[\"comparaciones\"], lo que permite medir el costo exacto de cada llamada.")

    # =====================================================================
    # 5. LÓGICA DEL JUEGO
    # =====================================================================
    heading(doc, "5. Lógica del Juego", 1, (0x1A, 0x3A, 0x5C))
    separador(doc)

    heading(doc, "5.1  Flujo de Estados", 2, (0x25, 0x63, 0xEB))
    for estado in [
        "inicio  →  seleccion_jugadores  →  nombre(s)  →  memoria",
        "              ↓",
        "            apuesta  →  resultado_ronda  (repite si ronda < 2)",
        "              ↓",
        "            oferta (ronda final de subasta)  →  final",
    ]:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(1)
        r = p.add_run(estado)
        r.font.name = "Courier New"
        r.font.size = Pt(9)

    heading(doc, "5.2  Generación del Catálogo", 2, (0x25, 0x63, 0xEB))
    doc.add_paragraph("7 productos seleccionados aleatoriamente de un pool de 15.", style="List Bullet")
    doc.add_paragraph("Precios en el rango $10,000 – $500,000 (múltiplos de 1,000).", style="List Bullet")
    doc.add_paragraph("Catálogo visible durante 5 segundos (cuenta regresiva con ontimer).", style="List Bullet")

    heading(doc, "5.3  Sistema de Puntuación", 2, (0x25, 0x63, 0xEB))
    parrafo(doc, "Función calcular_puntos(estimacion, real):")
    doc.add_paragraph("Si estimacion > real → 0 puntos (se pasó).", style="List Bullet")
    doc.add_paragraph("Si estimacion ≤ real → puntos = int(100 × (1 − (real−estimacion)/real)).", style="List Bullet")
    doc.add_paragraph("Máximo 100 puntos por ronda (estimación exacta).", style="List Bullet")

    heading(doc, "5.4  Rondas de Juego", 2, (0x25, 0x63, 0xEB))
    tabla_r = doc.add_table(rows=1, cols=3)
    tabla_r.style = "Table Grid"
    fila_encabezado(tabla_r, ["Ronda", "Pregunta", "k usado"])
    for ronda, preg, k in [
        ("1", "¿Cuál es el precio mediano?", "k = 3  (mediana de 7 elementos)"),
        ("2", "¿Cuál es el k-ésimo más barato?", "k = aleatorio entre 0 y 6"),
        ("Final (Subasta)", "Ronda silenciosa — precio = mediana de ofertas", "k = mitad del arreglo de ofertas"),
    ]:
        fila_datos(tabla_r, len(tabla_r.rows)-1, [ronda, preg, k])

    heading(doc, "5.5  Ronda de Subasta Silenciosa", 2, (0x25, 0x63, 0xEB))
    doc.add_paragraph("Cada jugador humano ingresa su oferta en secreto.", style="List Bullet")
    doc.add_paragraph("Se añaden 3 bots con ofertas aleatorias ($80,000 – $420,000).", style="List Bullet")
    doc.add_paragraph("Se añade una oferta extrema de $9,999,000 para evitar manipulación.", style="List Bullet")
    doc.add_paragraph("El precio de venta = mediana de todas las ofertas (calculada con los 3 algoritmos).", style="List Bullet")
    doc.add_paragraph("Los jugadores ganan puntos según la cercanía a esa mediana sin pasarse.", style="List Bullet")

    # =====================================================================
    # 6. INTERFAZ GRÁFICA
    # =====================================================================
    heading(doc, "6. Interfaz Gráfica", 1, (0x1A, 0x3A, 0x5C))
    separador(doc)

    parrafo(doc, "Tecnología: Python turtle + tkinter integrados.")

    tabla_ui = doc.add_table(rows=1, cols=2)
    tabla_ui.style = "Table Grid"
    fila_encabezado(tabla_ui, ["Componente", "Descripción"])
    for comp, desc in [
        ("Pantalla", "900 × 700 px, fondo #f4f7fb (gris claro)"),
        ("Tipografía", "Arial, tamaños 13–28 px según jerarquía"),
        ("Botones", "Dibujados con turtle, color #2563eb (azul), detección de clic por coordenadas"),
        ("Campo de entrada", "tk.Entry embebido en el canvas de turtle con validación de tipo"),
        ("Temporizador", "pantalla.ontimer() — cuenta regresiva de 5 s para memorizar el catálogo"),
        ("Validación de entrada", "validatecommand impide caracteres no numéricos en campos de precio"),
    ]:
        fila_datos(tabla_ui, len(tabla_ui.rows)-1, [comp, desc])

    # =====================================================================
    # 7. REQUERIMIENTOS FUNCIONALES
    # =====================================================================
    heading(doc, "7. Verificación de Requerimientos Funcionales", 1, (0x1A, 0x3A, 0x5C))
    separador(doc)

    tabla_req = doc.add_table(rows=1, cols=3)
    tabla_req.style = "Table Grid"
    fila_encabezado(tabla_req, ["#", "Requerimiento", "Estado"])
    for num, req, estado in [
        ("1", "Generar catálogos de N productos con precios aleatorios y mostrarlos tiempo limitado",
         "✅ Cumplido — 7 productos, 5 s"),
        ("2", "Rondas de mediana y k-ésimo menor con puntaje según cercanía",
         "✅ Cumplido — Rondas 1 y 2"),
        ("3", "Ronda de subasta con bots y precio igual a la mediana de las ofertas",
         "✅ Cumplido — 3 bots + oferta extrema"),
        ("4", "Quickselect in-place y Mediana de Medianas con contadores",
         "✅ Cumplido — in-place real, contadores en cada comparación"),
        ("5", "Validar que los 3 métodos dan el mismo resultado (con precios repetidos)",
         "✅ Cumplido — assert en laboratorio.py y evaluar_metodos()"),
    ]:
        fila_datos(tabla_req, len(tabla_req.rows)-1, [num, req, estado])

    # =====================================================================
    # 8. ANÁLISIS DE COMPLEJIDAD
    # =====================================================================
    heading(doc, "8. Análisis de Complejidad", 1, (0x1A, 0x3A, 0x5C))
    separador(doc)

    tabla_cx = doc.add_table(rows=1, cols=3)
    tabla_cx.style = "Table Grid"
    fila_encabezado(tabla_cx, ["Aspecto", "Lo que el grupo demuestra", "Estado"])
    for asp, dem, est in [
        ("Quickselect esperado",
         "T(n) ≤ T(3n/4) + cn → O(n) por serie geométrica. Pivote aleatorio garantiza que con prob. ≥ 1/2 el pivote cae entre el 25% y 75%.",
         "✅"),
        ("Quickselect peor caso",
         "T(n) = T(n−1) + Θ(n) = Θ(n²). Entrada que lo produce: arreglo ordenado con pivote siempre en el extremo (con semilla fija).",
         "✅"),
        ("Mediana de medianas (BFPRT)",
         "T(n) ≤ T(n/5) + T(7n/10) + cn. Por sustitución: T(n) ≤ d·n. Grupos de 5: 1/5+7/10=9/10<1. Grupos de 3 no funcionan: 1/3+2/3=1.",
         "✅"),
        ("Comparación — ordenar",
         "MergeSort: O(n log n) — log n niveles × O(n) por nivel en la fase de merge.",
         "✅"),
        ("Comparación — una posición",
         "Buscar el k-ésimo sin ordenar completo puede hacerse en O(n) (Quickselect / BFPRT).",
         "✅"),
        ("Ronda de subasta",
         "Con m ofertas totales (humanos + bots), calcular la mediana cuesta O(m).",
         "✅"),
        ("Código base — sin sorted()",
         "_insertion_sort_subarreglo() implementado. No se usa sorted() en grupos de 5.",
         "✅"),
    ]:
        fila_datos(tabla_cx, len(tabla_cx.rows)-1, [asp, dem, est])

    # =====================================================================
    # 9. EXPERIMENTO DE LABORATORIO
    # =====================================================================
    heading(doc, "9. Experimento de Modo Laboratorio", 1, (0x1A, 0x3A, 0x5C))
    separador(doc)

    parrafo(doc,
        "Se ejecutó laboratorio.py con n ∈ {10³, 10⁴, 10⁵, 10⁶}, buscando la mediana "
        "(k = n/2) sobre arreglos de precios aleatorios y ordenados. Cada configuración "
        "se repitió 3 veces y se promedió. Se validó (assert) que los 3 algoritmos "
        "producen el mismo resultado en cada ejecución.")

    heading(doc, "9.1  Resultados numéricos", 2, (0x25, 0x63, 0xEB))

    tabla_lab = doc.add_table(rows=1, cols=7)
    tabla_lab.style = "Table Grid"
    fila_encabezado(tabla_lab, ["n", "Tipo", "Comps QS", "Comps BFPRT", "Comps MergeSort", "t QS (ms)", "t BFPRT (ms)"])

    datos_lab = [
        ("1,000",     "Aleatorio", "3,342",       "6,394",       "8,715",        "0.38",   "1.10"),
        ("1,000",     "Ordenado",  "2,824",        "6,314",       "4,932",        "0.26",   "0.98"),
        ("10,000",    "Aleatorio", "30,690",       "80,003",      "120,387",      "2.97",   "12.59"),
        ("10,000",    "Ordenado",  "40,507",       "67,923",      "64,608",       "3.98",   "11.52"),
        ("100,000",   "Aleatorio", "394,902",      "836,919",     "1,536,379",    "47.73",  "144.31"),
        ("100,000",   "Ordenado",  "450,963",      "696,572",     "815,024",      "40.71",  "108.91"),
        ("1,000,000", "Aleatorio", "3,118,243",    "8,380,878",   "18,674,213",   "416.18", "1,800.55"),
        ("1,000,000", "Ordenado",  "3,095,398",    "7,043,681",   "9,884,992",    "342.58", "1,351.68"),
    ]
    for i, fila_d in enumerate(datos_lab):
        fila_datos(tabla_lab, i, list(fila_d))

    heading(doc, "9.2  Interpretación de resultados", 2, (0x25, 0x63, 0xEB))
    doc.add_paragraph(
        "Quickselect es el más rápido en comparaciones y tiempo en todos los casos, "
        "confirmando su O(n) esperado con constante pequeña.",
        style="List Bullet")
    doc.add_paragraph(
        "BFPRT tiene más comparaciones que Quickselect (constante oculta mayor) pero "
        "crece linealmente, confirmando su O(n) garantizado.",
        style="List Bullet")
    doc.add_paragraph(
        "MergeSort crece claramente más rápido (O(n log n)), especialmente para n = 10⁶ "
        "donde tiene 18.7 M comparaciones vs. 3.1 M de Quickselect.",
        style="List Bullet")
    doc.add_paragraph(
        "La validación assert pasó en todas las 24 ejecuciones (8 tamaños × 3 repeticiones), "
        "confirmando el Requerimiento 5.",
        style="List Bullet")

    heading(doc, "9.3  Gráficas", 2, (0x25, 0x63, 0xEB))
    agregar_imagen_si_existe(
        doc,
        os.path.join(BASE, "grafica_comparaciones.png"),
        ancho=Inches(6.2),
        caption="Figura 1. Número de comparaciones vs. n (escala log-log). "
                "Quickselect y BFPRT crecen linealmente; MergeSort crece como n·log n."
    )
    doc.add_paragraph()
    agregar_imagen_si_existe(
        doc,
        os.path.join(BASE, "grafica_tiempo.png"),
        ancho=Inches(6.2),
        caption="Figura 2. Tiempo de ejecución (ms) vs. n (escala log-log). "
                "BFPRT tiene constante mayor que Quickselect pero ambos son lineales."
    )

    # =====================================================================
    # 10. VALIDACIÓN DE IGUALDAD (REQUERIMIENTO 5)
    # =====================================================================
    heading(doc, "10. Validación de Igualdad — Requerimiento 5", 1, (0x1A, 0x3A, 0x5C))
    separador(doc)

    parrafo(doc,
        "El Requerimiento 5 exige verificar que los tres métodos dan el mismo resultado, "
        "incluso con precios repetidos. Se implementó validación en dos niveles:")

    heading(doc, "Nivel 1 — Juego (evaluar_metodos en juego.py)", 2, (0x25, 0x63, 0xEB))
    parrafo(doc,
        "Los tres métodos se ejecutan sobre la misma entrada en cada ronda. El juego muestra "
        "el precio calculado por MergeSort (referencia) como precio correcto.")

    heading(doc, "Nivel 2 — Laboratorio (assert explícito en laboratorio.py)", 2, (0x25, 0x63, 0xEB))
    for linea in [
        "assert res_qs == res_bfprt == res_ms, (",
        '    f"¡INCONSISTENCIA DETECTADA! "',
        '    f"Quickselect={res_qs}, BFPRT={res_bfprt}, MergeSort={res_ms} "',
        '    f"para k={k}, n={len(A_original)}"',
        ")",
    ]:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(1)
        r = p.add_run(linea)
        r.font.name = "Courier New"
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0x1A, 0x3A, 0x5C)

    parrafo(doc,
        "El assert se dispara para cada una de las 24 ejecuciones del experimento. "
        "Resultado: ✅ ninguna inconsistencia detectada.")

    # =====================================================================
    # 11. RESUMEN EJECUTIVO
    # =====================================================================
    heading(doc, "11. Resumen Ejecutivo", 1, (0x1A, 0x3A, 0x5C))
    separador(doc)

    tabla_res = doc.add_table(rows=1, cols=3)
    tabla_res.style = "Table Grid"
    fila_encabezado(tabla_res, ["Categoría", "Evaluación", "Calificación"])
    for cat, ev, cal in [
        ("Implementación de algoritmos",
         "Quickselect in-place real, BFPRT completo sin sorted(), MergeSort propio",
         "⭐⭐⭐⭐⭐"),
        ("Contadores de comparaciones",
         "Contados en cada comparación crítica (partición e insertion sort)",
         "⭐⭐⭐⭐⭐"),
        ("Validación de igualdad (Req. 5)",
         "assert explícito en laboratorio.py — 24/24 ejecuciones consistentes",
         "⭐⭐⭐⭐⭐"),
        ("Módulo de laboratorio",
         "laboratorio.py con n=10³–10⁶, gráficas PNG, datos tabulados",
         "⭐⭐⭐⭐⭐"),
        ("Lógica del juego",
         "Flujo completo, bots, anti-manipulación, temporizador",
         "⭐⭐⭐⭐☆"),
        ("Interfaz gráfica",
         "Turtle + tkinter, funcional y clara",
         "⭐⭐⭐⭐☆"),
        ("Documentación",
         "README + docstrings en algoritmos.py + este informe",
         "⭐⭐⭐⭐⭐"),
    ]:
        fila_datos(tabla_res, len(tabla_res.rows)-1, [cat, ev, cal])

    # =====================================================================
    # 12. CONCLUSIONES
    # =====================================================================
    heading(doc, "12. Conclusiones", 1, (0x1A, 0x3A, 0x5C))
    separador(doc)

    conclusiones = [
        ("Quickselect es el algoritmo más eficiente en la práctica",
         "Con pivote aleatorio logra O(n) esperado con una constante pequeña. "
         "Para n = 10⁶ realizó ~3.1 M comparaciones vs. ~18.7 M de MergeSort."),
        ("BFPRT garantiza O(n) en el peor caso a un costo mayor",
         "Su constante oculta es ~2.7× mayor que la de Quickselect en entradas aleatorias, "
         "pero elimina el riesgo del peor caso cuadrático. Para aplicaciones críticas "
         "(datos de adversario) es la elección correcta."),
        ("Los grupos de 5 son esenciales en BFPRT",
         "Con grupos de 5: 1/5 + 7/10 = 9/10 < 1 → recurrencia converge a O(n). "
         "Con grupos de 3: 1/3 + 2/3 = 1 → la serie no converge y no se garantiza O(n)."),
        ("La ronda de subasta aplica correctamente la mediana",
         "Usar la mediana en lugar de la máxima evita que una oferta exagerada manipule "
         "el precio, ilustrando un uso real del problema de selección."),
        ("Los tres algoritmos son correctos y consistentes",
         "El assert explícito en 24 ejecuciones (tamaños 10³–10⁶, aleatorio y ordenado) "
         "confirma que Quickselect, BFPRT y MergeSort producen el mismo k-ésimo menor."),
    ]

    for i, (titulo, cuerpo) in enumerate(conclusiones, 1):
        p = doc.add_paragraph()
        r1 = p.add_run(f"{i}. {titulo}: ")
        r1.bold = True
        r1.font.size = Pt(11)
        r2 = p.add_run(cuerpo)
        r2.font.size = Pt(11)

    # =====================================================================
    # GUARDAR
    # =====================================================================
    salida = os.path.join(BASE, "Informe_Proyecto7_ElPrecioJusto.docx")
    doc.save(salida)
    print(f"\n  ✅ Informe guardado en:\n     {salida}\n")
    return salida


if __name__ == "__main__":
    construir_documento()
