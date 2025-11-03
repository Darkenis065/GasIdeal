"""
Módulo particula.py
Define la clase 'Particula' para representar una partícula en un gas ideal.
"""

import numpy as np

class Particula:
    """
    Representa una partícula puntual con propiedades físicas.

    El modelo asume que las partículas no interactúan entre sí, solo
    colisionan elásticamente con las paredes del contenedor.

    Atributos:
        posicion (np.ndarray): Arreglo de numpy de 2D [x, y] con la posición.
        velocidad (np.ndarray): Arreglo de numpy de 2D [vx, vy] con la velocidad.
        masa (float): La masa de la partícula.
    """

    def __init__(self, x: float, y: float, vx: float, vy: float, masa: float = 1.0):
        """
        Inicializa una nueva partícula.

        Args:
            x (float): Posición inicial en el eje x.
            y (float): Posición inicial en el eje y.
            vx (float): Velocidad inicial en el eje x.
            vy (float): Velocidad inicial en el eje y.
            masa (float, optional): Masa de la partícula. Por defecto es 1.0.
        """
        self.posicion = np.array([x, y], dtype=float)
        self.velocidad = np.array([vx, vy], dtype=float)
        self.masa = float(masa)

    def mover(self, dt: float):
        """
        Actualiza la posición de la partícula usando un paso de tiempo dt.
        Utiliza la ecuación de movimiento libre: r(t+dt) = r(t) + v(t)*dt.

        Args:
            dt (float): El incremento de tiempo para la actualización.
        """
        self.posicion += self.velocidad * dt

    def colisionar_pared(self, ancho: float, alto: float):
        """
        Verifica y maneja colisiones elásticas con las paredes del contenedor.
        Si la partícula colisiona, invierte la componente de velocidad
        correspondiente.

        Args:
            ancho (float): El ancho (límite en x) del contenedor.
            alto (float): El alto (límite en y) del contenedor.
        """
        # Colisión con paredes verticales (izquierda: x=0, derecha: x=ancho)
        if self.posicion[0] < 0:
            self.posicion[0] = 0
            self.velocidad[0] = -self.velocidad[0]
        elif self.posicion[0] > ancho:
            self.posicion[0] = ancho
            self.velocidad[0] = -self.velocidad[0]

        # Colisión con paredes horizontales (abajo: y=0, arriba: y=alto)
        if self.posicion[1] < 0:
            self.posicion[1] = 0
            self.velocidad[1] = -self.velocidad[1]
        elif self.posicion[1] > alto:
            self.posicion[1] = alto
            self.velocidad[1] = -self.velocidad[1]

    def energia_cinetica(self) -> float:
        """
        Calcula y retorna la energía cinética de la partícula.
        La fórmula es E_k = 0.5 * m * |v|^2.

        Returns:
            float: La energía cinética (0.5 * m * (vx^2 + vy^2)).
        """
        return 0.5 * self.masa * np.dot(self.velocidad, self.velocidad)
