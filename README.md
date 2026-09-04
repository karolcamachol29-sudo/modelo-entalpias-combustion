# Predicción de Entalpías de Combustión Mediante Machine Learning

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Framework](https://img.shields.io/badge/Framework-Scikit--Learn%20%7C%20ChemPy-orange.svg)](https://scikit-learn.org/)
[![Institution](https://img.shields.io/badge/BUAP-Facultad%20de%20Ingenier%C3%ADa%20Qu%C3%ADmica-navy.svg)](https://www.buap.mx/)

---

## 📌 Descripción del Proyecto

Este repositorio contiene el desarrollo, reproducción, auditoría y validación de modelos de **Machine Learning** aplicados a la predicción precisa de la **entalpía estándar de combustión** ($\Delta H_c^\circ$) de compuestos orgánicos a partir de descriptores moleculares y **Teoría de Grafos Químicos**.

El proyecto forma parte de la formación práctica y científica de **Karol Paola Camacho López** en la Facultad de Ingeniería Química de la **Benemérita Universidad Autónoma de Puebla (BUAP)**, integrando principios de termodinámica clásica, calorimetría experimental y ciencia de datos predictiva, como plataforma de preparación para el modelado de sistemas en **equilibrio químico** (con fecha de inicio el 10 de diciembre de 2026).

---

## 🎯 Objetivos Principales

1. **Comprensión Físico-Química:** Relacionar el origen experimental calorimétrico de la entalpía (bomba de Mahler a volumen constante, $Q_v = \Delta U_c$, correcciones de Washburn y conversión a $\Delta H_c^\circ$) con la representación computacional de las moléculas.
2. **Representación Molecular:** Mapear cadenas de texto **SMILES** a grafos químicos para extraer descriptores topológicos (índices de Wiener, Estrada, Gutman y centralidades).
3. **Reproducción de Modelos:** Replicar con rigor y reproducibilidad el modelo ganador reportado en la literatura del grupo de investigación (Random Forest Regressor, $R^2 \approx 0.981$, $\text{MAE} \approx 287.6\text{ kJ/mol}$).
4. **Validación Científica:** Evaluar el sesgo y la varianza mediante validación cruzada ($k$-fold) y análisis detallado de gráficos de residuales ($y_{\text{exp}} - y_{\text{pred}}$) en lugar de depender únicamente de la métrica $R^2$.

---

## 📂 Estructura del Repositorio

El proyecto sigue una arquitectura estandarizada para ciencia de datos reproducibles:

```text
.
├── data/
│   ├── raw/                  # Datos crudos originales entregados por el laboratorio (solo lectura)
│   │   └── base_entalpias.csv
│   └── processed/            # Matrices limpias con features y target listos para entrenar
├── notebooks/
│   ├── 01_exploracion_inicial.ipynb  # Carga inicial, auditoría de tipos y valores nulos
│   └── 02_limpieza_y_eda.ipynb       # Análisis exploratorio, detección de outliers y correlaciones
├── src/                      # Módulos y scripts reutilizables en Python (.py)
│   ├── __init__.py
│   └── funciones_quimicas.py # Utilidades de estequiometría y ChemPy
├── .gitignore                # Reglas de exclusión de Git (ignora .venv, cachés, etc.)
├── INSTRUCCIONES_GITHUB.md   # Guía paso a paso de comandos de terminal
├── LICENSE                   # Licencia de código abierto MIT
├── README.md                 # Este documento
└── requirements.txt          # Lista de librerías y versiones exactas
```

---

## 🚀 Instalación y Configuración del Entorno

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/modelo-entalpias-combustion.git
cd modelo-entalpias-combustion
```

### 2. Crear y Activar el Entorno Virtual (`.venv`)
* **En Linux / macOS:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```
* **En Windows:**
  ```bash
  python -m venv .venv
  .venv\Scripts\activate
  ```

### 3. Instalar las Dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🔬 Metodología y Fundamentos Teóricos

El pipeline de predicción implementado sigue la secuencia:

$$\text{Molécula (SMILES)} \longrightarrow \text{Grafo Químico } G(V,E) \longrightarrow \text{Vector de Descriptores } \mathbf{x} \longrightarrow \text{Pipeline Scikit-Learn} \longrightarrow \widehat{\Delta H_c^\circ}$$

### Descriptores Topológicos Centrales:
* **Índice de Wiener ($W$):** Suma de distancias topológicas mínimas en la matriz de distancias molecular:
  $$W = \frac{1}{2} \sum_{i=1}^n \sum_{j=1}^n D_{ij}$$
* **Índice de Estrada ($EE$):** Basado en los autovalores $\lambda_i$ de la matriz de adyacencia del grafo:
  $$EE = \sum_{i=1}^n e^{\lambda_i}$$

---

## 📚 Referencias Científicas de Respaldo

Este desarrollo está fundamentado en las investigaciones del Dr. Jesús Andrés Arzola Flores y colaboradores:

1. **ACS Omega (2025):** *Prediction of Standard Combustion Enthalpy of Organic Compounds Combining Machine Learning and Chemical Graph Theory: A Strategy*. DOI: [10.1021/acsomega.5c05927](https://doi.org/10.1021/acsomega.5c05927).
2. **The Journal of Physical Chemistry A (2024):** *Experimental Determination of the Standard Enthalpy of Formation of Trimellitic Acid and Its Prediction by Supervised Learning*. DOI: [10.1021/acs.jpca.3c05235](https://doi.org/10.1021/acs.jpca.3c05235).
3. **Thermochimica Acta (2025):** *Tailored group contribution methods designed using machine learning to predict enthalpies in carboxylic acids and anhydrides*. DOI: [10.1016/j.tca.2024.179923](https://doi.org/10.1016/j.tca.2024.179923).
4. **ACS Omega (2023):** *7-Methoxy-4-methylcoumarin: Standard Molar Enthalpy of Formation Prediction in the Gas Phase Using Machine Learning and Its Comparison to the Experimental Data*. DOI: [10.1021/acsomega.3c06637](https://doi.org/10.1021/acsomega.3c06637).

---

## 👩‍🔬 Autora

* **Karol Paola Camacho López**  
  Estudiante de Ingeniería Química  
  *Facultad de Ingeniería Química — Benemérita Universidad Autónoma de Puebla (BUAP)*  
  Heroica Puebla de Zaragoza, México.
