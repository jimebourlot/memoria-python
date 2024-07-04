
import pygame
import sys
import math
import time
import random

"""
Iniciamos todo lo de Pygame para poder usar sonido, pantalla, etcétera
"""
pygame.init()
pygame.font.init()
pygame.mixer.init()

"""
Variables y configuraciones que vamos a usar a lo largo del programa
"""

altura_boton = 30  # El botón de abajo, para iniciar juego
medida_cuadro = 200  # Medida de la imagen en pixeles
# La parte trasera de cada tarjeta
nombre_imagen_oculta = "assets/oculta.png"
imagen_oculta = pygame.image.load(nombre_imagen_oculta)
segundos_mostrar_pieza = 2  # Segundos para ocultar la pieza si no es la correcta
"""
Una clase que representa el cuadro. El mismo tiene una imagen y puede estar
descubierto (cuando ya lo han descubierto anteriormente y no es la tarjeta buscada actualmente)
o puede estar mostrado (cuando se voltea la imagen)
También tiene una fuente o nombre de imagen que servirá para compararlo más tarde
"""


class Cuadro:
    def __init__(self, fuente_imagen):
        self.mostrar = True
        self.descubierto = False
        """
        Una cosa es la fuente de la imagen (es decir, el nombre del archivo) y otra
        la imagen lista para ser pintada por PyGame
        La fuente la necesitamos para más tarde, comparar las tarjetas
        """
        self.fuente_imagen = fuente_imagen
        self.imagen_real = pygame.image.load(fuente_imagen)


"""
Todo el juego; que al final es un arreglo de objetos
"""
cuadros = [
    [Cuadro(f"assets/image1.png"), Cuadro(f"assets/image1.png"),
     Cuadro(f"assets/image2.png"), Cuadro(f"assets/image2.png")],
    [Cuadro(f"assets/image3.png"), Cuadro(f"assets/image3.png"),
     Cuadro(f"assets/image4.png"), Cuadro(f"assets/image4.png")],
    [Cuadro(f"assets/image5.png"), Cuadro(f"assets/image5.png"),
     Cuadro(f"assets/image6.png"), Cuadro(f"assets/image6.png")],
    [Cuadro(f"assets/image7.png"), Cuadro(f"assets/image7.png"),
     Cuadro(f"assets/image8.png"), Cuadro(f"assets/image8.png")],
]
logo = pygame.image.load("assets/logo.png")  # Reemplaza con el nombre de tu archivo de imagen
ruta_fuente = "assets/MrEavesXLModNarOT-Heavy.ttf" 

# Obtener las dimensiones originales de la imagen
ancho_original, alto_original = logo.get_size()

# Redimensionar la imagen al 20% de su tamaño original
nuevo_ancho = int(ancho_original * 0.03)
nuevo_alto = int(alto_original * 0.03)
logo = pygame.transform.scale(logo, (nuevo_ancho, nuevo_alto))
ancho_logo, alto_logo = logo.get_size()

# Colores
color_blanco = (255, 255, 255)
color_negro = (0, 0, 0)
color_gris = (75,77,78)
color_rosa = (214, 14, 65)

# Los sonidos
sonido_fondo = pygame.mixer.Sound("assets/fondo.wav")
sonido_clic = pygame.mixer.Sound("assets/clic.wav")
sonido_exito = pygame.mixer.Sound("assets/ganador.wav")
sonido_fracaso = pygame.mixer.Sound("assets/equivocado.wav")
sonido_voltear = pygame.mixer.Sound("assets/voltear.wav")

# Calculamos el tamaño de la pantalla en base al tamaño de los cuadrados

# Obtener información sobre la pantalla
info_pantalla = pygame.display.Info()

# Usar el ancho de la pantalla actual
anchura_pantalla = info_pantalla.current_w
altura_pantalla = info_pantalla.current_h

# La fuente que estará sobre el botón
tamanio_fuente = 72
fuente = pygame.font.Font(ruta_fuente, tamanio_fuente)

# Definir dimensiones y posición del botón
anchura_boton = 450
altura_boton = 100
xFuente = int(anchura_pantalla / 2 - anchura_boton / 2)
yFuente = int(altura_pantalla / 2 - altura_boton / 2)

# Renderizar texto en el botón
texto_boton_iniciar = fuente.render("Iniciar Juego", True, color_blanco)
texto_boton_iniciar_rect = texto_boton_iniciar.get_rect()
texto_boton_iniciar_rect.center = (xFuente + anchura_boton / 2, yFuente + altura_boton / 2)
boton = pygame.Rect(xFuente, yFuente, anchura_boton, altura_boton)


# Banderas
# Bandera para saber si se debe ocultar la tarjeta dentro de N segundos
ultimos_segundos = None
puede_jugar = True  # Bandera para saber si reaccionar a los eventos del usuario
# Saber si el juego está iniciado; así sabemos si ocultar o mostrar piezas, además del botón
juego_iniciado = False
# Banderas de las tarjetas cuando se busca una pareja. Las necesitamos como índices para el arreglo de cuadros
# x1 con y1 sirven para la primer tarjeta
x1 = None
y1 = None
# Y las siguientes para la segunda tarjeta
x2 = None
y2 = None

"""
Funciones útiles
"""


# Ocultar todos los cuadros
def ocultar_todos_los_cuadros():
    for fila in cuadros:
        for cuadro in fila:
            cuadro.mostrar = False
            cuadro.descubierto = False


def aleatorizar_cuadros():
    # Elegir X e Y aleatorios, intercambiar
    cantidad_filas = len(cuadros)
    cantidad_columnas = len(cuadros[0])
    for y in range(cantidad_filas):
        for x in range(cantidad_columnas):
            x_aleatorio = random.randint(0, cantidad_columnas - 1)
            y_aleatorio = random.randint(0, cantidad_filas - 1)
            cuadro_temporal = cuadros[y][x]
            cuadros[y][x] = cuadros[y_aleatorio][x_aleatorio]
            cuadros[y_aleatorio][x_aleatorio] = cuadro_temporal


# Función para mostrar el cartel de éxito
def mostrar_cartel_exito():

    pantalla_juego.fill(color_blanco)

    # Crear un fuente para el texto
    fuente = pygame.font.Font(ruta_fuente, 72)
    texto = fuente.render("¡Felicitaciones! Ganaste", True, color_rosa)
    fuente = pygame.font.Font(ruta_fuente, 50)
    texto2 = fuente.render("Reiniciando juego... No cierres la ventana", True, color_rosa)
    
    
    # Centrar el texto en la pantalla
    texto_rect = texto.get_rect(center=(anchura_pantalla // 2, altura_pantalla // 2))
    texto_rect2 = texto2.get_rect(center=(anchura_pantalla // 2, altura_pantalla // 2 + 60))

    # Dibujar el texto en la pantalla
    pantalla_juego.blit(texto, texto_rect)
    pantalla_juego.blit(texto2, texto_rect2)

    
    # Actualizar la pantalla
    pygame.display.update()
    
    # Pausa para mostrar el cartel por 2 segundos
    pygame.time.delay(5000)  # 2000 milisegundos = 2 segundos

    reiniciar_juego()

def comprobar_si_gana():
    if gana():
        pygame.mixer.Sound.play(sonido_exito)
        mostrar_cartel_exito()
        


# Regresa False si al menos un cuadro NO está descubierto. True en caso de que absolutamente todos estén descubiertos
def gana():
    for fila in cuadros:
        for cuadro in fila:
            if not cuadro.descubierto:
                return False
    return True


def reiniciar_juego():
    global juego_iniciado
    juego_iniciado = False


def iniciar_juego():

    pygame.mixer.Sound.play(sonido_clic)
    global juego_iniciado
    # Aleatorizar 3 veces
    for i in range(3):
        aleatorizar_cuadros()
    ocultar_todos_los_cuadros()
    juego_iniciado = True

# Función para detectar clics en el botón de reinicio
def detectar_clic_reiniciar(pos):
    boton_rect = pygame.Rect(anchura_pantalla // 2 - 250, altura_pantalla - 60, 500, 40)
    return boton_rect.collidepoint(pos)

"""
Iniciamos la pantalla con las medidas previamente calculadas, colocamos título y
reproducimos el sonido de fondo
"""
pantalla_juego = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption('Memoria Calchines')
pygame.mixer.Sound.play(sonido_fondo, -1)  # El -1 indica un loop infinito
# Ciclo infinito...
while True:


    # Escuchar eventos, pues estamos en un ciclo infinito que se repite varias veces por segundo
    for event in pygame.event.get():
        
        # Si quitan el juego, salimos
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
        # Si hicieron clic y el usuario puede jugar...



        elif event.type == pygame.MOUSEBUTTONDOWN and puede_jugar:

            """
            xAbsoluto e yAbsoluto son las coordenadas de la pantalla en donde se hizo
            clic. PyGame no ofrece detección de clic en imagen, por ejemplo. Así que
            se deben hacer ciertos trucos
            """
            # Obtener las coordenadas absolutas del evento del ratón
            xAbsoluto, yAbsoluto = event.pos

            # Verificar si el clic fue dentro del botón de inicio del juego
            if boton.collidepoint(event.pos):
                if not juego_iniciado:
                    iniciar_juego()

            else:
                # Si no hay juego iniciado, ignoramos el clic
                if not juego_iniciado:
                    continue
                
                if detectar_clic_reiniciar(event.pos):
                    reiniciar_juego()  # Llamar a la función de reinicio si se hace clic en el botón

                # Calcular los índices x e y en base a las coordenadas del clic
                x = math.floor((xAbsoluto - margen_izquierdo) / medida_cuadro)
                y = math.floor((yAbsoluto - margen_superior) / medida_cuadro)

                # Verificar si los índices están dentro de los límites de las cartas
                if 0 <= x < len(cuadros[0]) and 0 <= y < len(cuadros):
                    # Acceder al cuadro solo si los índices están dentro de los límites
                    cuadro = cuadros[y][x]
                    # Aquí puedes realizar las operaciones necesarias con el cuadro
                else:
                    # Si los índices están fuera de los límites, ignorar el clic o realizar otra acción adecuada
                    print("Clic fuera de los límites del área de las cartas")
                # Verificar si las coordenadas de clic están dentro del área de las cartas
                if 0 <= x < len(cuadros[0]) and 0 <= y < len(cuadros):
                    cuadro = cuadros[y][x]
                    if cuadro.mostrar or cuadro.descubierto:
                        # Si el cuadro ya está mostrado o descubierto, ignorar el clic
                        continue

                    # Manejo de lógica para descubrir las cartas
                    if x1 is None and y1 is None:
                        # Si es la primera vez que se hace clic, guardar las coordenadas y mostrar el cuadro
                        x1 = x
                        y1 = y
                        cuadros[y1][x1].mostrar = True
                        pygame.mixer.Sound.play(sonido_voltear)
                    else:
                        # Si ya hay una carta descubierta y estamos buscando el par
                        x2 = x
                        y2 = y

                        # Verificar si las segundas coordenadas también están dentro de los límites
                        if 0 <= x2 < len(cuadros[0]) and 0 <= y2 < len(cuadros):
                            cuadros[y2][x2].mostrar = True
                            cuadro1 = cuadros[y1][x1]
                            cuadro2 = cuadros[y2][x2]
                            # Comparar las cartas descubiertas
                            if cuadro1.fuente_imagen == cuadro2.fuente_imagen:
                                cuadro1.descubierto = True
                                cuadro2.descubierto = True
                                x1 = None
                                y1 = None
                                x2 = None
                                y2 = None
                                pygame.mixer.Sound.play(sonido_clic)
                            else:
                                pygame.mixer.Sound.play(sonido_fracaso)
                                # Lógica para ocultar las cartas después de un tiempo
                                ultimos_segundos = int(time.time())
                                puede_jugar = False  # Bloquear el juego temporalmente
                        else:
                            # Si las segundas coordenadas están fuera de los límites, ignorar el clic o manejar según sea necesario
                            print("Clic fuera del área de las cartas")
                else:
                    # Si las coordenadas de clic están fuera del área de las cartas, ignorar el clic o manejar según sea necesario
                    print("Clic fuera del área de las cartas")

                comprobar_si_gana()

    ahora = int(time.time())
    # Y aquí usamos la bandera del tiempo, de nuevo. Si los segundos actuales menos los segundos
    # en los que se empezó el ocultamiento son mayores a los segundos en los que se muestra la pieza, entonces
    # se ocultan las dos tarjetas y se reinician las banderas
    if ultimos_segundos is not None and ahora - ultimos_segundos >= segundos_mostrar_pieza:
        cuadros[y1][x1].mostrar = False
        cuadros[y2][x2].mostrar = False
        x1 = None
        y1 = None
        x2 = None
        y2 = None
        ultimos_segundos = None
        # En este momento el usuario ya puede hacer clic de nuevo pues las imágenes ya estarán ocultas
        puede_jugar = True

    # Hacer toda la pantalla blanca
    
    pantalla_juego.fill(color_blanco)

    # Calcular el espacio restante en la pantalla
    espacio_horizontal = anchura_pantalla - (len(cuadros[0]) * medida_cuadro)
    espacio_vertical = altura_pantalla - (len(cuadros) * medida_cuadro)
    # Calcular el margen izquierdo y superior para centrar los cuadros
    margen_izquierdo = espacio_horizontal // 2
    margen_superior = espacio_vertical // 2

    
    # Recorrer los cuadros y dibujar en las coordenadas ajustadas
    y = margen_superior
    for fila in cuadros:
        x = margen_izquierdo
        for cuadro in fila:
            if cuadro.descubierto or cuadro.mostrar:
                pantalla_juego.blit(cuadro.imagen_real, (x, y))
            else:
                pantalla_juego.blit(imagen_oculta, (x, y))
            x += medida_cuadro
        y += medida_cuadro

    # También dibujamos el botón
    if not juego_iniciado:
        pygame.draw.rect(pantalla_juego, color_gris, boton, border_radius=10)

        # Dibujar el texto en el botón
        pantalla_juego.blit(texto_boton_iniciar, texto_boton_iniciar_rect)
        
        pantalla_juego.blit(logo, (anchura_pantalla//2 - ancho_logo //2, 40))  # Dibujar la imagen en la posición (100, 100)

    if juego_iniciado:
        fuente_titulo = pygame.font.Font(ruta_fuente, 50)
        titulo_iniciar = fuente_titulo.render("Juego de la memoria", True, color_rosa)
        titulo_iniciar_rect = titulo_iniciar.get_rect()
        titulo_iniciar_rect.center = (anchura_pantalla//2, 40)
        pantalla_juego.blit(titulo_iniciar, titulo_iniciar_rect)
        texto_iniciar = fuente.render("Encontrá las parejas", True, color_rosa)
        texto_iniciar_rect = texto_iniciar.get_rect()
        texto_iniciar_rect.center = (anchura_pantalla //2, 90)
        pantalla_juego.blit(texto_iniciar, texto_iniciar_rect)

        # Dibujar el botón de reiniciar
        fuente = pygame.font.Font(ruta_fuente, 40)
        pygame.draw.rect(pantalla_juego, color_gris, (anchura_pantalla // 2 - 250, altura_pantalla - 60, 500, 40), border_radius=10)  # Rectángulo del botón
        texto_boton = fuente.render("Reiniciar Juego", True, color_blanco)
        texto_boton_rect = texto_boton.get_rect(center=(anchura_pantalla // 2, altura_pantalla - 40))  # Ajustar posición del texto
        pantalla_juego.blit(texto_boton, texto_boton_rect)

    # Actualizamos la pantalla
    pygame.display.update()
