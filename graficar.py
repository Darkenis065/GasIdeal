"""
Módulo graficar.py
Utiliza matplotlib.animation para generar una visualización dinámica
del movimiento de las partículas del gas ideal. 
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import simulacion
from particula import Particula # Necesario si se usa type hinting
from typing import List

# --- Parámetros de la Simulación ---
N_PARTICULAS = 100       # Número de partículas
ANCHO_CAJA = 200.0     # Límite en X
ALTO_CAJA = 100.0      # Límite en Y
V_MEDIA_INI = 5.0      # Velocidad media inicial
DT = 0.1               # Paso de tiempo
# -----------------------------------

def inicializar_animacion():
    """
    Configura la figura y los ejes de matplotlib para la animación.
    Crea el gas inicial y el objeto de puntos (plot) que se actualizará.

    Returns:
        Tuple: (fig, ax, puntos, particulas)
    """
    # 1. Crear el gas
    particulas = simulacion.crear_gas(N_PARTICULAS, ANCHO_CAJA, ALTO_CAJA, V_MEDIA_INI)
    
    # 2. Configurar la figura y los ejes [cite: 68]
    fig, ax = plt.subplots()
    ax.set_xlim(0, ANCHO_CAJA)
    ax.set_ylim(0, ALTO_CAJA)
    ax.set_title("Simulación de Gas Ideal (N={})".format(N_PARTICULAS))
    ax.set_xlabel("Posición X (m)")
    ax.set_ylabel("Posición Y (m)")
    ax.set_aspect('equal') # Asegura que la caja se vea cuadrada si ancho=alto
    
    # 3. Crear el objeto de gráfico (puntos) [cite: 64]
    # Extraemos posiciones iniciales
    pos_inicial = np.array([p.posicion for p in particulas])
    puntos, = ax.plot(pos_inicial[:, 0], pos_inicial[:, 1], 'o', markersize=3, color='blue')
    
    return fig, ax, puntos, particulas

def actualizar_cuadro(frame: int, particulas: List[Particula], puntos) -> tuple:
    """
    Función que se llama en cada cuadro (frame) de la animación.
    Ejecuta un paso de simulación y actualiza la posición de los puntos
    en la gráfica.

    Args:
        frame (int): Número de cuadro (no se usa directamente, pero es requerido
                     por FuncAnimation).
        particulas (List[Particula]): La lista de partículas a simular.
        puntos (matplotlib.lines.Line2D): El objeto de la gráfica a actualizar.

    Returns:
        tuple: Una tupla con los artistas de matplotlib actualizados (solo 'puntos').
    """
    # 1. Avanzar la simulación un paso
    simulacion.paso(particulas, DT, ANCHO_CAJA, ALTO_CAJA)
    
    # 2. Obtener las nuevas posiciones
    # (Usamos un generador y np.array para eficiencia)
    nuevas_pos = np.array([p.posicion for p in particulas])
    
    # 3. Actualizar los datos del gráfico
    # .set_data() espera X e Y por separado
    if nuevas_pos.size > 0:
        puntos.set_data(nuevas_pos[:, 0], nuevas_pos[:, 1])
    else:
        puntos.set_data([], [])
        
    return puntos,

def main():
    """
    Función principal para ejecutar la visualización.
    """
    print("Iniciando simulación gráfica...")
    print("Cierre la ventana de matplotlib para terminar.")
    
    fig, ax, puntos, particulas = inicializar_animacion()
    
    # Crear la animación
    # interval: milisegundos entre cuadros
    # blit=True: optimización que solo redibuja lo que cambió
    ani = animation.FuncAnimation(
        fig=fig, 
        func=actualizar_cuadro, 
        fargs=(particulas, puntos),
        frames=None, # Corre indefinidamente
        interval=20, # Aprox 50 FPS (1000ms / 20ms)
        blit=True,
        cache_frame_data=False # Evita consumo excesivo de memoria
    )
    
    # Mostrar la animación
    plt.show()

if __name__ == "__main__":
    main()