import pygame
import sys
import math
import time

pygame.init()
NOMBRE_IMAGEN_OCULTA = "ocultar.png"
MEDIDA_CUADRADO = 200
SEGUNDOS_MOSTRAR_PIEZA = 1

imagen_oculta = pygame.image.load(NOMBRE_IMAGEN_OCULTA)
imagen_oculta = pygame.transform.scale(imagen_oculta, (MEDIDA_CUADRADO, MEDIDA_CUADRADO))


class Cuadro:
    def __init__(self, fuente_imagen):
        self.mostrar = False
        self.descubierta = False
        self.fuente_imagen = fuente_imagen
        imagen_real = pygame.image.load(fuente_imagen)
        self.imagen_real = pygame.transform.scale(imagen_real, (MEDIDA_CUADRADO, MEDIDA_CUADRADO))


cuadros = [
    [Cuadro("conejo.jpg"), Cuadro("conejo.jpg"), Cuadro("leon.jpg"), Cuadro("leon.jpg")],
    [Cuadro("oveja.jpg"), Cuadro("oveja.jpg"), Cuadro("perro.jpg"), Cuadro("perro.jpg")],
    [Cuadro("gato.jpg"), Cuadro("gato.jpg"), Cuadro("cabra.jpg"), Cuadro("cabra.jpg")],
    [Cuadro("cocodrilo.jpg"), Cuadro("cocodrilo.jpg"), Cuadro("huron.jpg"), Cuadro("huron.jpg")],
]

ALTURA_BOTON = 50
anchura_pantalla = (len(cuadros[0]) * MEDIDA_CUADRADO) + ALTURA_BOTON
altura_pantalla = len(cuadros) * MEDIDA_CUADRADO

ANCHURA_BOTON = anchura_pantalla
pantalla_juego = pygame.display.set_mode((anchura_pantalla, altura_pantalla))
pygame.display.set_caption('Memoria')

boton = pygame.Rect(0, altura_pantalla - ALTURA_BOTON, ANCHURA_BOTON, altura_pantalla)

cuadro_actual = None
deberia_ocultar = False
ultimos_segundos = None
puede_jugar = True
x1 = None
y1 = None
x2 = None
y2 = None
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and puede_jugar:
            xx, yy = event.pos
            x = math.floor(xx / MEDIDA_CUADRADO)
            y = math.floor(yy / MEDIDA_CUADRADO)
            # Primero lo primero. Si  ya está mostrada o descubierta, no hacemos nada
            cuadro = cuadros[y][x]
            if cuadro.mostrar or cuadro.descubierta:
                continue
            # Si es la primera vez que tocan la imagen (es decir, no están buscando el par de otra, sino apenas están
            # descubriendo la primera)
            if x1 is None and y1 is None:
                # Entonces la actual es en la que acaban de dar clic, la mostramos
                x1 = x
                y1 = y
                cuadros[y1][x1].mostrar = True
                print("OK tienes una, busca su par")
            else:
                # En caso de que ya hubiera una clickeada anteriormente y estemos buscando el par, comparamos...
                # Si coinciden, entonces a ambas las ponemos en descubiertas:
                x2 = x
                y2 = y
                cuadros[y2][x2].mostrar = True
                cuadro1 = cuadros[y1][x1]
                cuadro2 = cuadros[y2][x2]
                if cuadro1.fuente_imagen == cuadro2.fuente_imagen:
                    print("Sí era! le diste")
                    cuadros[y1][x1].descubierta = True
                    cuadros[y2][x2].descubierta = True
                    x1 = None
                    x2 = None
                    y1 = None
                    y2 = None
                else:
                    # Si no, tenemos que ocultarlas en el plazo de 1 segundo. Así que establecemos la bandera
                    ultimos_segundos = int(time.time())
                    print("No era, vamos a ocultarlas en 3 segundos")
                    print(ultimos_segundos)
                    puede_jugar = False

    ahora = int(time.time())
    if ultimos_segundos is not None and ahora - ultimos_segundos >= 2:
        print("Se oculta")
        print(ahora)
        cuadros[y1][x1].mostrar = False
        cuadros[y2][x2].mostrar = False
        # cuadros[indiceY][indiceX].mostrar = False
        x1 = None
        y1 = None
        x2 = None
        y2 = None
        ultimos_segundos = None
        puede_jugar = True

    pantalla_juego.fill((255, 255, 255,))
    x = 0
    y = 0
    for fila in cuadros:
        x = 0
        for cuadro in fila:
            if cuadro.descubierta or cuadro.mostrar:
                pantalla_juego.blit(cuadro.imagen_real, (x, y))
            else:
                pantalla_juego.blit(imagen_oculta, (x, y))
            x += MEDIDA_CUADRADO
        y += MEDIDA_CUADRADO

    # También dibujamos el botón
    pygame.draw.rect(pantalla_juego, [255, 0, 0], boton)

    pygame.display.update()