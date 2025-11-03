"""
Módulo graficar.py
Utiliza matplotlib.animation para generar una visualización dinámica
del movimiento de las partículas del gas ideal. 
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import simulacion 
from particula import Particula 
from typing import List


def obtener_parametro(prompt: str, tipo: type, valor_defecto: float, min_val: float = 0.0):
    """
    Función auxiliar para interactuar con el usuario en la consola, pedir un 
    parámetro, y validar que la entrada sea del tipo correcto y cumpla con un valor
    mínimo.

    Args:
        prompt (str): La pregunta que se muestra al usuario.
        tipo (type): El tipo de dato esperado (int o float).
        valor_defecto (float): El valor a usar si el usuario presiona ENTER.
        min_val (float): El valor mínimo aceptado para el parámetro.

    Returns:
        float/int: El valor validado introducido por el usuario o el valor por defecto.
    """
    while True:
        entrada = input(f"{prompt} (Defecto: {valor_defecto}, Mínimo: {min_val}): ")
        if not entrada:
            return valor_defecto # Retorna el valor por defecto si la entrada es vacía
        try:
            valor = tipo(entrada)
            if valor >= min_val:
                return valor
            else:
                print(f"⚠️ El valor debe ser mayor o igual a {min_val}.")
        except ValueError:
            print("⚠️ Entrada inválida. Asegúrate de ingresar un número válido.")

def inicializar_animacion(N_PARTICULAS: int, ANCHO_CAJA: float, ALTO_CAJA: float, V_MEDIA_INI: float) -> tuple:
    """
    Configura la figura y los ejes de matplotlib para la animación.
    Crea el gas inicial con los parámetros definidos y el objeto de puntos (plot) 
    que se actualizará.

    Args:
        N_PARTICULAS (int): Número de partículas.
        ANCHO_CAJA (float): Límite en X de la caja de simulación.
        ALTO_CAJA (float): Límite en Y de la caja de simulación.
        V_MEDIA_INI (float): Velocidad media inicial de las partículas.

    Returns:
        Tuple: (fig, ax, puntos, particulas), con la figura, los ejes, el objeto
               de la gráfica y la lista de partículas iniciales.
    """
    # 1. Crear el gas usando los parámetros del menú
    particulas = simulacion.crear_gas(N_PARTICULAS, ANCHO_CAJA, ALTO_CAJA, V_MEDIA_INI)
    
    # 2. Configurar la figura y los ejes 
    fig, ax = plt.subplots()
    ax.set_xlim(0, ANCHO_CAJA)
    ax.set_ylim(0, ALTO_CAJA)
    # Título que refleja los parámetros de la simulación
    ax.set_title(f"Simulación de Gas Ideal (N={N_PARTICULAS}, Vm={V_MEDIA_INI:.1f} m/s)")
    ax.set_xlabel("Posición X (m)")
    ax.set_ylabel("Posición Y (m)")
    ax.set_aspect('equal') # Asegura que la caja se vea cuadrada si ancho=alto
    
    # 3. Crear el objeto de gráfico (puntos) 
    # Extraemos posiciones iniciales
    pos_inicial = np.array([p.posicion for p in particulas])
    puntos, = ax.plot(pos_inicial[:, 0], pos_inicial[:, 1], 'o', markersize=3, color='blue')
    
    return fig, ax, puntos, particulas

def actualizar_cuadro(frame: int, particulas: List[Particula], puntos, DT: float, ANCHO_CAJA: float, ALTO_CAJA: float) -> tuple:
    """
    Función que se llama en cada cuadro (frame) de la animación.
    Ejecuta un paso de simulación (`DT`) y actualiza la posición de los puntos
    en la gráfica, aplicando las colisiones con los límites de la caja.

    Args:
        frame (int): Número de cuadro (requerido por FuncAnimation).
        particulas (List[Particula]): La lista de partículas a simular.
        puntos (matplotlib.lines.Line2D): El objeto de la gráfica a actualizar.
        DT (float): El paso de tiempo para el avance de la simulación.
        ANCHO_CAJA (float): El límite horizontal de la caja.
        ALTO_CAJA (float): El límite vertical de la caja.

    Returns:
        tuple: Una tupla con los artistas de matplotlib actualizados (solo 'puntos').
    """
    # 1. Avanzar la simulación un paso
    simulacion.paso(particulas, DT, ANCHO_CAJA, ALTO_CAJA)
    
    # 2. Obtener las nuevas posiciones
    # Usamos un generador y np.array para eficiencia
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
    Función principal para solicitar los parámetros al usuario y ejecutar la visualización
    del gas ideal.
    """
    # --- Parámetros por Defecto de la Simulación ---
    DEFAULT_N = 100         # Número de partículas
    DEFAULT_ANCHO = 200.0   # Límite en X
    DEFAULT_ALTO = 100.0    # Límite en Y
    DEFAULT_V_MEDIA = 5.0   # Velocidad media inicial
    DEFAULT_DT = 0.1        # Paso de tiempo
    # -----------------------------------------------

    print("╔════════════════════════════════════════╗")
    print("║   ⚙️ Configuración de la Simulación ⚙️   ║")
    print("╚════════════════════════════════════════╝")
    print("Consejo: Presiona ENTER para usar el valor por defecto en cada pregunta.")

    # 1. Recolección de parámetros del usuario usando la función auxiliar
    N_PARTICULAS = int(obtener_parametro("Número de partículas (N)", int, DEFAULT_N, 1))
    ANCHO_CAJA = obtener_parametro("Ancho de la caja (m)", float, DEFAULT_ANCHO, 10.0)
    ALTO_CAJA = obtener_parametro("Alto de la caja (m)", float, DEFAULT_ALTO, 10.0)
    V_MEDIA_INI = obtener_parametro("Velocidad media inicial (m/s)", float, DEFAULT_V_MEDIA, 0.1)
    DT = obtener_parametro("Paso de tiempo (DT)", float, DEFAULT_DT, 0.001)

    print("\n✅ Parámetros listos. Iniciando simulación gráfica...")
    print("Cierre la ventana de matplotlib para terminar.")
    
    # 2. Inicializar la animación con los parámetros definidos
    fig, ax, puntos, particulas = inicializar_animacion(N_PARTICULAS, ANCHO_CAJA, ALTO_CAJA, V_MEDIA_INI)
    
    # 3. Crear la animación
    # fargs: argumentos adicionales que se pasan a la función 'actualizar_cuadro' en cada frame.
    ani = animation.FuncAnimation(
        fig=fig, 
        func=actualizar_cuadro, 
        fargs=(particulas, puntos, DT, ANCHO_CAJA, ALTO_CAJA), 
        frames=None, # Corre indefinidamente
        interval=20, # Aprox 50 FPS (1000ms / 20ms)
        blit=True, # Optimización que solo redibuja lo que cambió
        cache_frame_data=False 
    )
    
    # 4. Mostrar la animación
    plt.show() # 

if __name__ == "__main__":
    main()
