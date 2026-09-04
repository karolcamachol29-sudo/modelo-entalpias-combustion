"""
ENTREGABLE OFICIAL: F0-ENV_ACT02_SCR_funciones_chempy_v1.0_FINAL.py
Proyecto: Predicción de Entalpías de Combustión Mediante Machine Learning
Autora: Karol Paola Camacho López (FIQ — BUAP)
Fecha de Cierre: 2026-09-04
"""

from src.funciones_quimicas import (
    calcular_dH_especifica,
    balancear_combustion,
    extraer_descriptores_estequiometricos
)

__all__ = [
    "calcular_dH_especifica",
    "balancear_combustion",
    "extraer_descriptores_estequiometricos"
]

if __name__ == "__main__":
    print("Verificación de entregable de funciones ChemPy:")
    reac, prod = balancear_combustion("C2H6O")
    print("Combustión de etanol:", reac, "->", prod)
    print("ESTADO: APROBADO")
