"""
Módulo test_gas.py
Pruebas unitarias (unittest) para validar el modelo físico de la simulación.
Verifica la creación de partículas, los límites de la caja y la
conservación de la energía.
"""

import unittest
import numpy as np
import simulacion
from particula import Particula

class TestGasIdeal(unittest.TestCase):
    """
    Suite de pruebas para los módulos particula.py y simulacion.py.
    """

    def setUp(self):
        """
        Configuración inicial que se ejecuta antes de cada método de prueba.
        Crea un escenario de simulación estándar.
        """
        self.N = 50
        self.ancho = 100.0
        self.alto = 100.0
        self.v_media = 5.0
        self.dt = 0.1
        self.particulas = simulacion.crear_gas(self.N, self.ancho, self.alto, self.v_media)

    def test_rf3_1_numero_particulas_correcto(self):
        """
        Verifica (RF3.1): El número de partículas creadas es N.
        """
        self.assertEqual(len(self.particulas), self.N)

    def test_rf3_2_particulas_no_salen_caja(self):
        """
        Verifica (RF3.2): Las partículas permanecen dentro de los límites
        después de varios pasos de simulación.
        """
        for _ in range(100):
            simulacion.paso(self.particulas, self.dt, self.ancho, self.alto)

        for p in self.particulas:
            self.assertGreaterEqual(p.posicion[0], 0, "Partícula salió por la izquierda")
            self.assertLessEqual(p.posicion[0], self.ancho, "Partícula salió por la derecha")
            self.assertGreaterEqual(p.posicion[1], 0, "Partícula salió por abajo")
            self.assertLessEqual(p.posicion[1], self.alto, "Partícula salió por arriba")

    def test_rf3_3_energia_total_positiva(self):
        """
        Verifica (RF3.3): La energía total es siempre positiva (o cero si v=0).
        """
        e_total = simulacion.energia_total(self.particulas)
        self.assertGreaterEqual(e_total, 0.0)

    def test_rf3_4_conservacion_energia(self):
        """
        Verifica (RF3.4): La energía total se conserva (variación < 1%).
        
        Nota: En este modelo simple sin interacciones y colisiones
        elásticas perfectas, la conservación debe ser exacta.
        """
        e_inicial = simulacion.energia_total(self.particulas)
        
        for _ in range(100):
            simulacion.paso(self.particulas, self.dt, self.ancho, self.alto)
            
        e_final = simulacion.energia_total(self.particulas)

        # Criterio de aceptación: variación < 1%
        self.assertAlmostEqual(e_inicial, e_final, 
                               msg="La energía total no se conservó.",
                               delta=e_inicial * 0.01)

    def test_rf3_5_e3_temperatura_velocidad(self):
        """
        Verifica (RF3.5 y E3): La temperatura es proporcional al cuadrado
        de la velocidad media. Si se duplica v_media, T debe
        cuadruplicarse aprox.
        """
        # Gas 1
        gas1 = simulacion.crear_gas(self.N, self.ancho, self.alto, v_media=5.0)
        temp1 = simulacion.temperatura(gas1)
        
        # Gas 2 (doble velocidad media)
        gas2 = simulacion.crear_gas(self.N, self.ancho, self.alto, v_media=10.0)
        temp2 = simulacion.temperatura(gas2)
        
        # T ~ E_prom ~ v^2. Si v -> 2v, entonces T -> 4T.
        ratio = temp2 / temp1 if temp1 > 0 else 0
        
        # Usamos un delta grande (p.ej., 1.5) porque la generación aleatoria
        # de velocidades tiene una varianza estadística alta.
        self.assertAlmostEqual(ratio, 4.0, delta=1.5,
                               msg="La temperatura no escaló con v^2")

if __name__ == '__main__':
    """
    Permite ejecutar las pruebas directamente con: python gas_ideal/test_gas.py
    """
    unittest.main()
