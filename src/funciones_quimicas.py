"""
Módulo de Utilidades Químicas y Termodinámicas
Proyecto: Predicción de Entalpías de Combustión
Autora: Karol Paola Camacho López (FIQ - BUAP)
"""

from typing import Dict, Any, Tuple
import pandas as pd
from chempy import Substance
from chempy.chemistry import balance_stoichiometry


def calcular_dH_especifica(dH_molar: float, masa_molar: float) -> float:
    """
    Convierte la entalpía molar de combustión (kJ/mol) a entalpía específica (kJ/g).
    
    Parámetros:
        dH_molar (float): Entalpía estándar molar en kJ/mol.
        masa_molar (float): Masa molecular en g/mol.
        
    Retorna:
        float: Entalpía específica o poder calorífico en kJ/g.
    """
    if masa_molar <= 0:
        raise ValueError("La masa molar debe ser estrictamente positiva.")
    return dH_molar / masa_molar


def balancear_combustion(formula_combustible: str) -> Tuple[Dict[str, float], Dict[str, float]]:
    """
    Balancea automáticamente la reacción de combustión completa con oxígeno (O2)
    para formar dióxido de carbono (CO2) y agua líquida (H2O).
    
    Parámetros:
        formula_combustible (str): Fórmula molecular textual (ej. 'C2H5OH', 'CH4').
        
    Retorna:
        Tuple[Dict, Dict]: Diccionarios de coeficientes estequiométricos de reactivos y productos.
    """
    reactivos = {formula_combustible, 'O2'}
    productos = {'CO2', 'H2O'}
    reac_bal, prod_bal = balance_stoichiometry(reactivos, productos)
    return dict(reac_bal), dict(prod_bal)


def extraer_descriptores_estequiometricos(formula: str) -> pd.Series:
    """
    Extrae la masa molar, composición atómica y requerimientos estequiométricos de O2
    para ser utilizados como features numéricas en modelos de Machine Learning.
    
    Parámetros:
        formula (str): Cadena con la fórmula química de la sustancia.
        
    Retorna:
        pd.Series: Serie de Pandas con las variables extraídas.
    """
    try:
        sub = Substance.from_formula(formula)
        reac, prod = balance_stoichiometry({formula, 'O2'}, {'CO2', 'H2O'})
        
        moles_comb = reac[formula]
        moles_o2 = reac.get('O2', 0) / moles_comb
        moles_co2 = prod.get('CO2', 0) / moles_comb
        moles_h2o = prod.get('H2O', 0) / moles_comb
        
        comp = sub.composition
        num_C = comp.get(6, 0)
        num_H = comp.get(1, 0)
        num_O = comp.get(8, 0)
        num_N = comp.get(7, 0)
        
        ratio_C_H = (num_C / num_H) if num_H > 0 else 0.0

        return pd.Series({
            "masa_molar": sub.mass,
            "num_C": num_C,
            "num_H": num_H,
            "num_O": num_O,
            "num_N": num_N,
            "ratio_C_H": ratio_C_H,
            "moles_O2_esteq": moles_o2,
            "moles_CO2_esteq": moles_co2,
            "moles_H2O_esteq": moles_h2o
        })
    except Exception as error:
        return pd.Series({
            "masa_molar": None,
            "num_C": None,
            "num_H": None,
            "num_O": None,
            "num_N": None,
            "ratio_C_H": None,
            "moles_O2_esteq": None,
            "moles_CO2_esteq": None,
            "moles_H2O_esteq": None
        })
