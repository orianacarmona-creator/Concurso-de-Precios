import random
import tkinter as tk

from algoritmos import quickselect_inplace, bfprt, mergesort_referencia


PRODUCTOS_BASE = [
    "Cafetera", "Audífonos", "Teclado", "Mouse", "Monitor",
    "Silla", "Lámpara", "Mochila", "Termo", "Reloj",
    "Parlante", "Cámara", "Micrófono", "Disco Duro", "Tableta"
]


def generar_catalogo(n):
    nombres = random.sample(PRODUCTOS_BASE, min(n, len(PRODUCTOS_BASE)))
    return [(nombres[i], random.randint(10, 500) * 1000) for i in range(n)]


def evaluar_metodos(precios, k):
    """Ejecuta los 3 métodos sobre copias del arreglo y devuelve el resultado y comparaciones."""
    c_qs = {"comparaciones": 0}
    quickselect_inplace(precios.copy(), 0, len(precios) - 1, k, c_qs)

    c_bfprt = {"comparaciones": 0}
    bfprt(precios.copy(), 0, len(precios) - 1, k, c_bfprt)

    c_ref = {"comparaciones": 0}
    ordenado = mergesort_referencia(precios.copy(), c_ref)
    return ordenado[k], c_qs["comparaciones"], c_bfprt["comparaciones"], c_ref["comparaciones"]


def calcular_puntos(estimacion, real):
    """Gana más puntos quien más se acerque sin pasarse."""
    if estimacion > real:
        return 0
    diferencia_pct = (real - estimacion) / real
    return max(0, int(100 * (1 - diferencia_pct)))


class InterfazJuego:
    ANCHO = 900
    ALTO = 700

    def __init__(self, turtle):
        self.turtle = turtle
        self.pantalla = turtle.Screen()
        self.pantalla.setup(self.ANCHO, self.ALTO)
        self.pantalla.title("El Precio Justo")
        self.pantalla.bgcolor("#f4f7fb")
        self.pantalla.tracer(False)

        self.lapiz = turtle.Turtle(visible=False)
        self.lapiz.speed(0)
        self.lapiz.penup()
        self.botones = []
        self.canvas = self.pantalla.getcanvas()._canvas
        validar_entrada = self.canvas.register(self._validar_entrada)
        self.campo_entrada = tk.Entry(
            self.canvas,
            font=("Arial", 16),
            justify="center",
            validate="key",
            validatecommand=(validar_entrada, "%P"),
        )
        self.campo_entrada.bind("<Return>", self._al_confirmar_tecla)
        self.ventana_entrada = self.canvas.create_window(
            self.ANCHO // 2,
            self.ALTO // 2,
            window=self.campo_entrada,
            width=360,
            height=34,
            state="hidden",
        )
        self.pantalla.onclick(self._al_hacer_clic)

        self.estado = "inicio"
        self.jugadores = []
        self.puntajes = {}
        self.ronda = 0
        self.catalogo = []
        self.precios = []
        self.jugador_actual = 0
        self.entrada = ""
        self.mensaje = ""
        self.ofertas = []
        self.ofertas_jugadores = {}

        self._dibujar_inicio()
        self.pantalla.mainloop()

    def _validar_entrada(self, valor):
        if self.estado == "nombre":
            return len(valor) <= 24
        if self.estado in ("apuesta", "oferta"):
            return len(valor) <= 10 and (not valor or valor.isdigit())
        return True

    def _mostrar_campo_entrada(self, coordenada_y):
        self.canvas.itemconfigure(self.ventana_entrada, state="normal")
        self.canvas.coords(
            self.ventana_entrada,
            self.ANCHO // 2,
            self.ALTO // 2 - coordenada_y,
        )
        self.campo_entrada.delete(0, tk.END)
        self.campo_entrada.insert(0, self.entrada)
        self.canvas.after_idle(self.campo_entrada.focus_set)

    def _al_confirmar_tecla(self, evento):
        if evento.keysym != "Return":
            return
        self.entrada = self.campo_entrada.get()
        self._confirmar_entrada()
        return "break"

    def _texto(self, x, y, contenido, tamano=16, color="#243247", alineacion="center", negrita=False):
        self.lapiz.goto(x, y)
        self.lapiz.color(color)
        estilo = "bold" if negrita else "normal"
        self.lapiz.write(contenido, align=alineacion, font=("Arial", tamano, estilo))

    def _boton(self, texto, x, y, ancho, alto, accion):
        izquierda = x - ancho / 2
        abajo = y - alto / 2
        self.lapiz.goto(izquierda, abajo)
        self.lapiz.color("#2563eb")
        self.lapiz.fillcolor("#2563eb")
        self.lapiz.pensize(1)
        self.lapiz.pendown()
        self.lapiz.begin_fill()
        for _ in range(2):
            self.lapiz.forward(ancho)
            self.lapiz.left(90)
            self.lapiz.forward(alto)
            self.lapiz.left(90)
        self.lapiz.end_fill()
        self.lapiz.penup()
        self._texto(x, y - 9, texto, 15, "white", negrita=True)
        self.botones.append((izquierda, abajo, izquierda + ancho, abajo + alto, accion))

    def _preparar_dibujo(self):
        self.pantalla.tracer(False)
        self.lapiz.clear()
        self.canvas.itemconfigure(self.ventana_entrada, state="hidden")
        self.botones = []
        self._texto(0, 285, "EL PRECIO JUSTO", 28, "#12305a", negrita=True)
        self.lapiz.goto(-400, 260)
        self.lapiz.color("#d8e1ee")
        self.lapiz.pensize(2)
        self.lapiz.pendown()
        self.lapiz.forward(800)
        self.lapiz.penup()

    def _actualizar(self):
        self.pantalla.update()

    def _al_hacer_clic(self, x, y):
        for izquierda, abajo, derecha, arriba, accion in reversed(self.botones):
            if izquierda <= x <= derecha and abajo <= y <= arriba:
                if self.estado in ("nombre", "apuesta", "oferta"):
                    self.entrada = self.campo_entrada.get()
                accion()
                return

    def _dibujar_inicio(self):
        self.estado = "inicio"
        self._preparar_dibujo()
        self._texto(0, 125, "¡Un juego de precios y estrategia!", 20)
        self._texto(0, 80, "Memoriza los precios, calcula tus apuestas", 16)
        self._texto(0, 52, "y compite contra tus amigos.", 16)
        self._boton("JUGAR", 0, -40, 220, 54, self._elegir_jugadores)
        self._actualizar()

    def _elegir_jugadores(self):
        self.estado = "seleccion_jugadores"
        self._preparar_dibujo()
        self._texto(0, 150, "¿Cuántas personas van a jugar?", 20)
        for cantidad in range(1, 4):
            self._boton(str(cantidad), (cantidad - 2) * 150, 40, 100, 60,
                        lambda cantidad=cantidad: self._iniciar_nombres(cantidad))
        self._texto(0, -30, "Haz clic en una opción para continuar.", 14, "#58677c")
        self._actualizar()

    def _iniciar_nombres(self, cantidad):
        self.cantidad_jugadores = cantidad
        self.jugadores = []
        self.puntajes = {}
        self._pedir_nombre()

    def _reiniciar_juego(self):
        self.jugadores = []
        self.puntajes = {}
        self.ronda = 0
        self.catalogo = []
        self.precios = []
        self.jugador_actual = 0
        self.entrada = ""
        self.mensaje = ""
        self.ofertas = []
        self.ofertas_jugadores = {}
        self._dibujar_inicio()

    def _pedir_nombre(self):
        self.estado = "nombre"
        self.entrada = ""
        self._dibujar_nombre()

    def _dibujar_nombre(self):
        self._preparar_dibujo()
        numero = len(self.jugadores) + 1
        self._texto(0, 140, f"Nombre de la persona {numero} de {self.cantidad_jugadores}", 19)
        self._mostrar_campo_entrada(55)
        self._texto(0, 5, "Haz clic en el campo, escribe el nombre y presiona Enter.", 14, "#58677c")
        self._boton("CONTINUAR", 0, -80, 190, 48, self._confirmar_entrada)
        self._actualizar()

    def _confirmar_entrada(self):
        if self.estado == "nombre":
            nombre = self.entrada.strip()
            if not nombre:
                self.mensaje = "Escribe un nombre antes de continuar."
                self._dibujar_nombre()
                self._texto(0, -145, self.mensaje, 14, "#b42318")
                self._actualizar()
                return
            self.jugadores.append(nombre)
            self.puntajes[nombre] = 0
            if len(self.jugadores) < self.cantidad_jugadores:
                self._pedir_nombre()
            else:
                self.ronda = 1
                self._iniciar_ronda()
        elif self.estado == "apuesta":
            self._guardar_apuesta()
        elif self.estado == "oferta":
            self._guardar_oferta()

    def _iniciar_ronda(self):
        self.estado = "memoria"
        self.catalogo = generar_catalogo(7)
        self.precios = [precio for _, precio in self.catalogo]
        self.reloj = 5
        self._dibujar_catalogo()
        self.pantalla.ontimer(self._tic_memoria, 1000)

    def _dibujar_catalogo(self):
        self._preparar_dibujo()
        self._texto(0, 215, f"RONDA {self.ronda} · MEMORIZA LOS PRECIOS", 18, negrita=True)
        for indice, (producto, precio) in enumerate(self.catalogo):
            self._texto(0, 165 - indice * 42, f"{producto}:  ${precio:,}", 17)
        self._texto(0, -180, f"El catálogo se ocultará en {self.reloj} segundos", 16, "#2563eb")
        self._actualizar()

    def _tic_memoria(self):
        if self.estado != "memoria":
            return
        self.reloj -= 1
        if self.reloj <= 0:
            self._mostrar_pregunta()
        else:
            self._dibujar_catalogo()
            self.pantalla.ontimer(self._tic_memoria, 1000)

    def _mostrar_pregunta(self):
        self.estado = "apuesta"
        self.jugador_actual = 0
        if self.ronda == 1:
            self.pregunta = "¿Cuál es el precio mediano del catálogo?"
            self.k = 3
        else:
            self.k = random.randint(0, 6)
            self.pregunta = f"¿Cuál es el {self.k + 1}º producto más barato?"
        self.resultado = evaluar_metodos(self.precios, self.k)
        self.entrada = ""
        self._dibujar_entrada_precio()

    def _dibujar_entrada_precio(self):
        self._preparar_dibujo()
        titulo = "RONDA FINAL · OFERTA SECRETA" if self.estado == "oferta" else f"RONDA {self.ronda}"
        self._texto(0, 205, titulo, 18, negrita=True)
        if self.estado == "oferta":
            self._texto(0, 145, "Producto: Consola Retro", 18)
            self._texto(0, 105, "¿Cuál es tu oferta?", 18)
        else:
            self._texto(0, 145, self.pregunta, 18)
            self._texto(0, 95, "Gana puntos quien más se acerque sin pasarse.", 14, "#58677c")
        self._texto(0, 15, f"Turno de {self.jugadores[self.jugador_actual]}", 19, "#12305a", negrita=True)
        self._mostrar_campo_entrada(-35)
        self._texto(0, -85, "Haz clic en el campo, escribe solo números y presiona Enter.", 14, "#58677c")
        if self.mensaje:
            self._texto(0, -130, self.mensaje, 14, "#b42318")
        self._boton("CONFIRMAR", 0, -190, 200, 48, self._confirmar_entrada)
        self._actualizar()

    def _guardar_apuesta(self):
        if not self.entrada:
            self.mensaje = "Escribe un precio antes de confirmar."
            self._dibujar_entrada_precio()
            return
        apuesta = int(self.entrada)
        nombre = self.jugadores[self.jugador_actual]
        precio_real = self.resultado[0]
        self.puntajes[nombre] += calcular_puntos(apuesta, precio_real)
        self.jugador_actual += 1
        self.entrada = ""
        self.mensaje = ""
        if self.jugador_actual < len(self.jugadores):
            self._dibujar_entrada_precio()
        else:
            self._mostrar_resultado_ronda()

    def _mostrar_resultado_ronda(self):
        self.estado = "resultado_ronda"
        real, comp_qs, comp_bfprt, comp_ref = self.resultado
        self._preparar_dibujo()
        self._texto(0, 175, f"RESULTADO DE LA RONDA {self.ronda}", 21, negrita=True)
        self._texto(0, 110, f"Precio correcto:  ${real:,}", 20, "#12305a")
        self._texto(0, 55, f"Quickselect: {comp_qs} comparaciones", 15)
        self._texto(0, 20, f"Mediana de Medianas: {comp_bfprt} comparaciones", 15)
        self._texto(0, -15, f"MergeSort: {comp_ref} comparaciones", 15)
        self._mostrar_puntajes()
        self._boton("CONTINUAR", 0, -215, 200, 48, self._continuar_despues_ronda)
        self._actualizar()

    def _mostrar_puntajes(self):
        y = -85
        for nombre, puntos in sorted(self.puntajes.items(), key=lambda fila: fila[1], reverse=True):
            self._texto(0, y, f"{nombre}: {puntos} puntos", 15)
            y -= 28

    def _continuar_despues_ronda(self):
        if self.ronda < 2:
            self.ronda += 1
            self._iniciar_ronda()
        else:
            self._iniciar_subasta()

    def _iniciar_subasta(self):
        self.estado = "oferta"
        self.jugador_actual = 0
        self.ofertas = []
        self.ofertas_jugadores = {}
        self.entrada = ""
        self.mensaje = ""
        self._dibujar_entrada_precio()

    def _guardar_oferta(self):
        if not self.entrada:
            self.mensaje = "Escribe una oferta antes de confirmar."
            self._dibujar_entrada_precio()
            return
        oferta = int(self.entrada)
        nombre = self.jugadores[self.jugador_actual]
        self.ofertas.append(oferta)
        self.ofertas_jugadores[nombre] = oferta
        self.jugador_actual += 1
        self.entrada = ""
        self.mensaje = ""
        if self.jugador_actual < len(self.jugadores):
            self._dibujar_entrada_precio()
        else:
            self._calcular_subasta()

    def _calcular_subasta(self):
        self.ofertas.extend(random.randint(80, 420) * 1000 for _ in range(3))
        self.ofertas.append(9999000)
        precio, comp_qs, comp_bfprt, comp_ref = evaluar_metodos(self.ofertas, len(self.ofertas) // 2)
        for nombre, oferta in self.ofertas_jugadores.items():
            self.puntajes[nombre] += calcular_puntos(oferta, precio)

        self.estado = "final"
        self._preparar_dibujo()
        self._texto(0, 200, "¡FIN DEL CONCURSO!", 24, "#12305a", negrita=True)
        self._texto(0, 145, f"Precio de venta: ${precio:,}", 19)
        self._texto(0, 105, f"Ofertas (humanos y bots): {', '.join(f'${valor:,}' for valor in self.ofertas)}", 13)
        self._texto(0, 55, f"Comparaciones · Quickselect: {comp_qs} | Mediana de Medianas: {comp_bfprt}", 13)
        self._texto(0, 25, f"MergeSort: {comp_ref}", 13)
        self._texto(0, -35, "TABLA DE POSICIONES", 18, negrita=True)
        self._mostrar_puntajes()
        self._boton("JUGAR OTRA VEZ", 0, -235, 230, 48, self._reiniciar_juego)
        self._actualizar()


def jugar():
    import turtle

    InterfazJuego(turtle)


if __name__ == "__main__":
    jugar()
