"""
Módulo simulacion.py
Contiene funciones para crear y simular el colectivo de partículas (gas ideal).
Incluye cálculos de propiedades macroscópicas como energía y temperatura.
"""

import numpy as np
from typing import List
# Importamos la clase Particula del módulo local
from particula import Particula

def crear_gas(N: int, ancho: float, alto: float, v_media: float) -> List[Particula]:
    """
    Crea una lista de N partículas con posiciones y velocidades aleatorias. [cite: 36]

    Las posiciones se distribuyen uniformemente dentro de la caja [0, ancho] x [0, alto].
    Las velocidades se generan aleatoriamente (distribución normal) con una
    magnitud promedio relacionada con v_media.

    Args:
        N (int): Número de partículas a crear.
        ancho (float): Ancho de la caja.
        alto (float): Alto de la caja.
        v_media (float): Valor para escalar las velocidades iniciales.

    Returns:
        List[Particula]: Una lista de N objetos Particula inicializados.
    """
    particulas = []
    for _ in range(N):
        # Posición aleatoria dentro de los límites
        x = np.random.rand() * ancho
        y = np.random.rand() * alto
        
        # Velocidad aleatoria (componentes normalizadas escaladas por v_media)
        # np.random.randn() da una dist. normal (media 0, std 1)
        vx = np.random.randn() * v_media
        vy = np.random.randn() * v_media
        
        # Asumimos masa 1.0 para todas las partículas
        particulas.append(Particula(x, y, vx, vy, masa=1.0))
        
    return particulas

def paso(particulas: List[Particula], dt: float, ancho: float, alto: float):
    """
    Ejecuta un paso de simulación para todas las partículas.
    Actualiza la posición de cada partícula y maneja sus colisiones
    con las paredes. [cite: 37]

    Args:
        particulas (List[Particula]): La lista de partículas a simular.
        dt (float): El incremento de tiempo.
        ancho (float): Ancho de la caja.
        alto (float): Alto de la caja.
    """
    for p in particulas:
        p.mover(dt)
        p.colisionar_pared(ancho, alto)

def energia_total(particulas: List[Particula]) -> float:
    """
    Calcula la energía cinética total del sistema.
    Es la suma de las energías cinéticas de todas las partículas. [cite: 38]

    Args:
        particulas (List[Particula]): La lista de partículas.

    Returns:
        float: La energía cinética total del gas.
    """
    return sum(p.energia_cinetica() for p in particulas)

def temperatura(particulas: List[Particula], k_B: float = 1.0) -> float:
    """
    Calcula la temperatura efectiva del gas.
    Se basa en la energía cinética promedio por partícula. [cite: 39]
    La fórmula es T = E_prom / k_B, donde E_prom = E_total / N. [cite: 40]

    Args:
        particulas (List[Particula]): La lista de partículas.
        k_B (float, optional): Constante de Boltzmann (en unidades 
                                 apropiadas). Por defecto es 1.0.

    Returns:
        float: La temperatura efectiva del gas.
    """
    if not particulas:
        return 0.0
        
    e_total = energia_total(particulas)
    e_prom = e_total / len(particulas)
    
    # Del teorema de equipartición para 2D, <E_k> = k_B * T
    return e_prom / k_B