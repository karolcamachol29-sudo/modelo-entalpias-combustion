# Predicción de Entalpías de Combustión Mediante Machine Learning

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/Licencia-Uso%20Exclusivo%20Acad%C3%A9mico-red.svg)](LICENSE)
[![Framework](https://img.shields.io/badge/Framework-Scikit--Learn%20%7C%20ChemPy-orange.svg)](https://scikit-learn.org/)
[![Institution](https://img.shields.io/badge/BUAP-Facultad%20de%20Ingenier%C3%ADa%20Qu%C3%ADmica-navy.svg)](https://www.buap.mx/)

---

## 📌 Descripción del Proyecto

Este repositorio contiene el desarrollo, reproducción, auditoría y validación de modelos de **Machine Learning** aplicados a la predicción precisa de la **entalpía estándar de combustión** ($\Delta H_c^\circ$) de compuestos orgánicos a partir de descriptores moleculares y propiedades fisicoquímicas.

El proyecto forma parte de la formación práctica y científica de **Karol Paola Camacho López** en la Facultad de Ingeniería Química de la **Benemérita Universidad Autónoma de Puebla (BUAP)**, integrando principios de termodinámica clásica, calorimetría experimental y ciencia de datos predictiva, como plataforma de preparación para el modelado de sistemas en **equilibrio químico** (con fecha de inicio el 10 de diciembre de 2026).

---

## 🎯 Objetivos Principales

1. **Comprensión Físico-Química:** Relacionar el origen experimental calorimétrico de la entalpía (bomba de Mahler a volumen constante, $Q_v = \Delta U_c$, correcciones de Washburn y conversión a $\Delta H_c^\circ$) con la representación computacional de las moléculas.
2. **Representación Molecular:** Mapear cadenas de texto **SMILES** y fórmulas químicas a descriptores moleculares y propiedades fisicoquímicas cuantitativas (masa molar, conteos de heteroátomos, enlaces y balance estequiométrico).
3. **Optimización de Modelos Predictivos:** Entrenar y evaluar modelos de regresión supervisada (Random Forest Regressor, Gradient Boosting y modelos lineales regularizados) para optimizar la precisión de estimación ($\text{MAE}$, $\text{RMSE}$, $R^2$).
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
git clone https://github.com/karolcamachol29-sudo/modelo-entalpias-combustion.git
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

$$\text{Molécula (SMILES / Fórmula)} \longrightarrow \text{Vector de Descriptores Moleculares } \mathbf{x} \longrightarrow \text{Pipeline Scikit-Learn} \longrightarrow \widehat{\Delta H_c^\circ}$$

### Descriptores Moleculares y Fisicoquímicos Principales:
* **Propiedades Constitutivas:** Masa molar ($M$), número de átomos de carbono ($n_C$), hidrógeno ($n_H$), oxígeno ($n_O$), nitrógeno ($n_N$) y demás heteroátomos.
* **Propiedades Estructurales y Termoquímicas:** Enlaces rotables, conteo de enlaces simples/dobles/aromáticos, área superficial polar topológica (TPSA) y coeficientes de combustión estequiométrica ($n_{\text{O}_2}$).

---

## 📚 Referencias y Fuentes Termodinámicas
 
1. **NIST Chemistry WebBook:** SRD 69, National Institute of Standards and Technology (NIST), Gaithersburg MD.
2. **CRC Handbook of Chemistry and Physics:** Standard Thermodynamic Properties of Chemical Substances, CRC Press / Taylor & Francis.
3. **Smith, J. M., Van Ness, H. C., Abbott, M. M., & Swihart, M. T.:** *Introduction to Chemical Engineering Thermodynamics*, 9th Edition, McGraw-Hill.
4. **Pedregosa, F. et al. (2011):** *Scikit-learn: Machine Learning in Python*, Journal of Machine Learning Research, 12, pp. 2825–2830.

---

## 👩‍🔬 Autora

* **Karol Paola Camacho López**  
  Estudiante de Ingeniería Química  
  *Facultad de Ingeniería Química — Benemérita Universidad Autónoma de Puebla (BUAP)*  
  Heroica Puebla de Zaragoza, México.

---

## ⚖️ Licencia y Términos de Uso

**Copyright © 2026 Karol Paola Camacho López. Todos los derechos reservados.**

Este repositorio es de **acceso público únicamente para fines de visualización académica, revisión por pares y verificación científica**. 

> **AVISO DE RESTRICCIÓN DE USO:**  
> La disponibilidad pública de este repositorio **NO otorga una licencia de software libre ni permiso de libre uso, modificación o explotación**. Queda estrictamente prohibido el uso comercial, industrial o lucrativo, así como la redistribución, republicación o creación de obras derivadas sin la autorización expresa, previa y por escrito de la autora. Para consultas o colaboraciones académicas, contactar directamente a través de los canales institucionales de la BUAP. Consulta los términos completos en el archivo [LICENSE](LICENSE).

