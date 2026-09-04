# 📌 TABLERO KANBAN AUTOMATIZADO
**Proyecto:** Predicción de Entalpías de Combustión Mediante Machine Learning  
**Responsable:** Karol Paola Camacho López (Facultad de Ingeniería Química — BUAP)  
**Última Sincronización:** 2026-09-04 07:45:42  
**Progreso General:** 16.7% (2/12 entregables cerrados)

---

## ⛔ Bloqueado (9)

### [ACT04] Análisis Exploratorio de Datos (EDA) y Detección de Outliers
- **Fase:** `F2-EDA` | **Progreso:** `0%`
- **Descripción:** Generación de histogramas de dH_combustion, diagramas de dispersión respecto a masa molar, matriz de correlación de Pearson y detección de anomalías termodinámicas con IQR.
- **Plazo:** `2026-09-12` al `2026-09-19`<br>**Depende de:** ACT03
- **Archivo de Cierre Requerido:** `F2-EDA_ACT04_NBK_exploracion_distribuciones_v1.0_FINAL.ipynb`
- **Etiquetas:** `#ipynb` `[Backlog]` `@data-engineering`

---
### [ACT05] Cálculo de Descriptores Moleculares y Fisicoquímicos
- **Fase:** `F2-EDA` | **Progreso:** `0%`
- **Descripción:** Extracción sistemática de descriptores moleculares a partir de cadenas SMILES y composición química (masa molar, conteos de heteroátomos, número de enlaces, TPSA y balance estequiométrico).
- **Plazo:** `2026-09-19` al `2026-09-26`<br>**Depende de:** ACT03
- **Archivo de Cierre Requerido:** `F2-EDA_ACT05_SCR_calculo_descriptores_moleculares_v1.0_FINAL.py`
- **Etiquetas:** `#py` `[Backlog]` `@descriptores-moleculares`

---
### [ACT06] Entrenamiento de Modelos Base (OLS, Ridge y Lasso)
- **Fase:** `F3-MLB` | **Progreso:** `0%`
- **Descripción:** Implementación del pipeline de regresión lineal estándar y regularizada con partición 80/20 train/test sin fuga de datos (Data Leakage) como punto de comparación.
- **Plazo:** `2026-09-26` al `2026-10-03`<br>**Depende de:** ACT04, ACT05
- **Archivo de Cierre Requerido:** `F3-MLB_ACT06_NBK_modelos_lineales_baseline_v1.0_FINAL.ipynb`
- **Etiquetas:** `#ipynb` `[Backlog]` `@machine-learning`

---
### [ACT07] Implementación y Ajuste de Random Forest Regressor
- **Fase:** `F3-MLB` | **Progreso:** `0%`
- **Descripción:** Entrenamiento de ensamble de árboles (RandomForestRegressor) sobre descriptores moleculares y fisicoquímicos, controlando max_depth y n_estimators para evitar overfitting.
- **Plazo:** `2026-10-03` al `2026-10-10`<br>**Depende de:** ACT06
- **Archivo de Cierre Requerido:** `F3-MLB_ACT07_SCR_random_forest_regressor_v1.0_FINAL.py`
- **Etiquetas:** `#py` `[Backlog]` `@machine-learning`

---
### [ACT08] Validación Cruzada k-Fold y Análisis Gráfico de Residuales
- **Fase:** `F4-VAL` | **Progreso:** `0%`
- **Descripción:** Evaluación con 10-fold cross validation, análisis de homocedasticidad mediante gráficos de residuales (y_exp - y_pred vs y_pred) y detección de sesgos por familias.
- **Plazo:** `2026-10-10` al `2026-10-17`<br>**Depende de:** ACT07
- **Archivo de Cierre Requerido:** `F4-VAL_ACT08_NBK_diagnostico_residuales_v1.0_FINAL.ipynb`
- **Etiquetas:** `#ipynb` `[Backlog]` `@machine-learning`

---
### [ACT09] Auditoría y Reproducción Exacta del Modelo Rector del Profesor
- **Fase:** `F5-REP` | **Progreso:** `0%`
- **Descripción:** Ejecución del protocolo de 10 pasos de ingeniería inversa para replicar el modelo de 3,477 compuestos reportado en ACS Omega 2025 (Dr. Jesús Andrés Arzola Flores).
- **Plazo:** `2026-10-17` al `2026-10-31`<br>**Depende de:** ACT08
- **Archivo de Cierre Requerido:** `F5-REP_ACT09_REP_informe_reproduccion_modelo_v1.0_FINAL.pdf`
- **Etiquetas:** `#pdf` `#tex` `[Backlog]` `@documentacion`

---
### [SIM01] Simulación Termodinámica de Combustión en DWSIM
- **Fase:** `F6-SIM` | **Progreso:** `0%`
- **Descripción:** Modelado de una cámara de combustión adiabática e isoperibólica en DWSIM utilizando el paquete de propiedades termodinámicas de Peng-Robinson o NRTL, comparando calor liberado con predicciones de ML.
- **Plazo:** `2026-10-31` al `2026-11-14`<br>**Depende de:** ACT02, ACT09
- **Archivo de Cierre Requerido:** `F6-SIM_SIM01_SIM_reactor_combustion_dwsim_v1.0_FINAL.dwsim`
- **Etiquetas:** `#dwsim` `[Backlog]` `@simulacion`

---
### [ACT10] Puente Termodinámico al Equilibrio: Modelado de Gibbs y Keq
- **Fase:** `F7-EQK` | **Progreso:** `0%`
- **Descripción:** Integración de las entalpías predichas por el modelo con cálculos de entropía estándar para calcular delta_G = delta_H - T*delta_S y constantes de equilibrio Keq = exp(-delta_G / RT).
- **Plazo:** `2026-11-14` al `2026-11-28`<br>**Depende de:** ACT09, SIM01
- **Archivo de Cierre Requerido:** `F7-EQK_ACT10_SCR_calculador_gibbs_keq_v1.0_FINAL.py`
- **Etiquetas:** `#py` `[Backlog]` `@termoquimica`

---
### [DOC01] Entrega de Manuscrito Técnico y Propuesta para el Proyecto de Equilibrio
- **Fase:** `F7-EQK` | **Progreso:** `0%`
- **Descripción:** Redacción y compilación en LaTeX del informe final consolidado de la formación en entalpías de combustión y planteamiento formal del proyecto de equilibrio químico del 10 de diciembre.
- **Plazo:** `2026-11-28` al `2026-12-10`<br>**Depende de:** ACT10
- **Archivo de Cierre Requerido:** `F7-EQK_DOC01_REP_manuscrito_final_propuesta_v1.0_FINAL.pdf`
- **Etiquetas:** `#pdf` `#tex` `[Backlog]` `@documentacion`

---
## 📋 Por Iniciar (Backlog) (0)

_Sin actividades en esta columna._

## ⏳ En Desarrollo (1)

### [ACT03] Adquisición, Normalización y Auditoría del Dataset Crudo
- **Fase:** `F1-DAT` | **Progreso:** `35%`
- **Descripción:** Recepción de la base de datos de entalpías en data/raw/, verificación de unidades (kJ/mol), auditoría de duplicados basados en SMILES canónicos e identificación de valores nulos (NaN).
- **Plazo:** `2026-09-05` al `2026-09-12`<br>**Depende de:** ACT01
- **Archivo de Cierre Requerido:** `F1-DAT_ACT03_DAT_dataset_curado_v1.0_FINAL.csv`
- **Etiquetas:** `#csv` `[En Proceso]` `@data-engineering`

---
## 🔍 Revisión Técnica (0)

_Sin actividades en esta columna._

## ✅ Cerrado / Completado (2)

### [ACT01] Configuración del Entorno Virtual e Intérprete PyCharm
- **Fase:** `F0-ENV` | **Progreso:** `100%`
- **Descripción:** Instalación del entorno virtual .venv, configuración del kernel de Jupyter en PyCharm, instalación de dependencias base (numpy, pandas, chempy, scikit-learn) y verificación de versiones.
- **Plazo:** `2026-09-04` al `2026-09-05`
- **Archivo de Cierre Requerido:** `F0-ENV_ACT01_CFG_entorno_pycharm_v1.0_FINAL.txt`<br>**Cierre:** `2026-09-04T01:06:00Z`
- **Etiquetas:** `#py` `#ipynb` `[Completado]` `@control-versiones`

---
### [ACT02] Implementación de Utilidades Estequiométricas con ChemPy
- **Fase:** `F0-ENV` | **Progreso:** `100%`
- **Descripción:** Desarrollo del módulo de funciones químicas en src/ para balanceo automático de combustión completa (CO2 + H2O) y extracción de masa molar y composición atómica.
- **Plazo:** `2026-09-04` al `2026-09-05`<br>**Depende de:** ACT01
- **Archivo de Cierre Requerido:** `F0-ENV_ACT02_SCR_funciones_chempy_v1.0_FINAL.py`<br>**Cierre:** `2026-09-04T01:06:36Z`
- **Etiquetas:** `#py` `[Completado]` `@termoquimica`

---
