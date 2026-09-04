# 📊 MATRIZ MAESTRA DE ACTIVIDADES Y ENTREGABLES TÉCNICOS
**Proyecto:** Predicción de Entalpías de Combustión Mediante Machine Learning  
**Responsable:** Karol Paola Camacho López (FIQ — BUAP)  
**Horizonte Temporal:** 2026-09-04 al 2026-12-10

---

## ⚙️ Reglas de Modificación y Flexibilidad
1. **Edición Manual de Parámetros:** Esta tabla refleja directamente el archivo `config/matriz_actividades.json`. Puedes modificar fechas límites (`YYYY-MM-DD`), descripciones o añadir dependencias.
2. **Disparador de Cierre Automático:** Para cerrar una tarea, el sistema busca en el repositorio un archivo cuyo nombre coincida exactamente con la columna **Archivo de Cierre Requerido**.
3. **Validación de Nomenclatura:** Todo archivo debe validar contra la expresión regular:  
   `^(F[0-7]-[A-Z]{3})_([A-Z]{3}\d{2})_([A-Z]{3})_([a-z0-9_]+)_(v\d+\.\d+)_(DRAFT|REV|FINAL)\.([a-zA-Z0-9]+)$`

---

## 📋 Matriz Detallada de Actividades

| ID | Fase | Título de la Actividad | Alcance / Inputs / Criterios de Aceptación | Asignación | Límite Sugerido | Archivo de Cierre Exacto Requerido | Estado | Tags Asignados |
| :---: | :---: | :--- | :--- | :---: | :---: | :--- | :---: | :--- |
| **ACT01** | `F0-ENV` | **Configuración del Entorno PyCharm** | **Alcance:** .venv, kernel Jupyter, paquetes base.<br>**Input:** `requirements.txt`<br>**Criterio:** Intérprete funcional sin errores de importación. | `2026-09-04` | `2026-09-05` | `F0-ENV_ACT01_CFG_entorno_pycharm_v1.0_FINAL.txt` | `Completado` | `#py`, `#ipynb`, `@control-versiones` |
| **ACT02** | `F0-ENV` | **Utilidades Estequiométricas con ChemPy** | **Alcance:** Funciones de balance y masas molares en `src/`.<br>**Input:** ChemPy 0.8+<br>**Criterio:** Balance automático probado con alcanos y alcoholes. | `2026-09-04` | `2026-09-05` | `F0-ENV_ACT02_SCR_funciones_chempy_v1.0_FINAL.py` | `Completado` | `#py`, `@termoquimica` |
| **ACT03** | `F1-DAT` | **Curaduría y Auditoría del Dataset Crudo** | **Alcance:** Carga a `data/raw/`, auditoría de unidades y nulos.<br>**Input:** `base_entalpias.csv`<br>**Criterio:** >3,000 compuestos depurados con target a 298.15 K. | `2026-09-05` | `2026-09-12` | `F1-DAT_ACT03_DAT_dataset_curado_v1.0_FINAL.csv` | `En Proceso` | `#csv`, `@data-engineering` |
| **ACT04** | `F2-EDA` | **Análisis Exploratorio y Outliers** | **Alcance:** Histogramas de $\Delta H_c^\circ$, correlación Pearson, IQR.<br>**Input:** Dataset curado ACT03<br>**Criterio:** Cuaderno reproducible con gráficos de distribución. | `2026-09-12` | `2026-09-19` | `F2-EDA_ACT04_NBK_exploracion_distribuciones_v1.0_FINAL.ipynb` | `Backlog` | `#ipynb`, `@data-engineering` |
| **ACT05** | `F2-EDA` | **Descriptores de Grafos Químicos** | **Alcance:** SMILES a matrices de adyacencia y distancias topológicas.<br>**Input:** SMILES canónicos<br>**Criterio:** Índices de Wiener, Estrada y Gutman calculados en $X$. | `2026-09-19` | `2026-09-26` | `F2-EDA_ACT05_SCR_calculo_indices_grafos_v1.0_FINAL.py` | `Backlog` | `#py`, `@grafos-moleculares` |
| **ACT06** | `F3-MLB` | **Entrenamiento de Modelos Base (OLS, Ridge)** | **Alcance:** Regresión lineal aditiva con `Pipeline` sin fuga de datos.<br>**Input:** Matriz $X$ e $y$<br>**Criterio:** Baseline documentado con MAE, RMSE y $R^2$. | `2026-09-26` | `2026-10-03` | `F3-MLB_ACT06_NBK_modelos_lineales_baseline_v1.0_FINAL.ipynb` | `Backlog` | `#ipynb`, `@machine-learning` |
| **ACT07** | `F3-MLB` | **Ajuste de Random Forest Regressor** | **Alcance:** Ensamble de 200 árboles sobre descriptores topológicos.<br>**Input:** Matriz de features<br>**Criterio:** $R^2 > 0.95$ en test set con control de sobreajuste. | `2026-10-03` | `2026-10-10` | `F3-MLB_ACT07_SCR_random_forest_regressor_v1.0_FINAL.py` | `Backlog` | `#py`, `@machine-learning` |
| **ACT08** | `F4-VAL` | **Validación Cruzada y Gráfico de Residuales** | **Alcance:** 10-fold CV y diagnóstico de homocedasticidad ($y - \hat{y}$).<br>**Input:** Random Forest ajustado<br>**Criterio:** Nube de residuales sin sesgo sistemático en aromáticos. | `2026-10-10` | `2026-10-17` | `F4-VAL_ACT08_NBK_diagnostico_residuales_v1.0_FINAL.ipynb` | `Backlog` | `#ipynb`, `@machine-learning` |
| **ACT09** | `F5-REP` | **Reproducción del Modelo Oficial del Profesor** | **Alcance:** Protocolo de 10 pasos para reproducir ACS Omega 2025.<br>**Input:** Código oficial y 3,477 compuestos<br>**Criterio:** Replicar $R^2=0.9810$ y $\text{MAE}=287.6\text{ kJ/mol}$. | `2026-10-17` | `2026-10-31` | `F5-REP_ACT09_REP_informe_reproduccion_modelo_v1.0_FINAL.pdf` | `Backlog` | `#pdf`, `#tex`, `@documentacion` |
| **SIM01** | `F6-SIM` | **Simulación de Combustión en DWSIM** | **Alcance:** Hoja de flujo de cámara de combustión con Peng-Robinson.<br>**Input:** DWSIM 8+, composiciones<br>**Criterio:** Balance de materia y calor liberado verificado con ML. | `2026-10-31` | `2026-11-14` | `F6-SIM_SIM01_SIM_reactor_combustion_dwsim_v1.0_FINAL.dwsim` | `Backlog` | `#dwsim`, `@simulacion` |
| **ACT10** | `F7-EQK` | **Puente Termodinámico: Gibbs y $K_{eq}$** | **Alcance:** $\Delta G^\circ = \Delta H^\circ - T\Delta S^\circ$ y $K_{eq}(T)$ dependiente de temperatura.<br>**Input:** Modelos validados y NIST<br>**Criterio:** Módulo funcional de equilibrio termoquímico. | `2026-11-14` | `2026-11-28` | `F7-EQK_ACT10_SCR_calculador_gibbs_keq_v1.0_FINAL.py` | `Backlog` | `#py`, `@termoquimica` |
| **DOC01** | `F7-EQK` | **Manuscrito Final y Propuesta de Equilibrio** | **Alcance:** Informe consolidado en LaTeX para el hito del 10 de diciembre.<br>**Input:** Todos los entregables F0--F7<br>**Criterio:** Documento PDF aprobado y repositorio versionado al 100%. | `2026-11-28` | `2026-12-10` | `F7-EQK_DOC01_REP_manuscrito_final_propuesta_v1.0_FINAL.pdf` | `Backlog` | `#pdf`, `#tex`, `@documentacion` |

---

*Para sincronizar cambios realizados en esta tabla o en el JSON, ejecuta: `python src/workflow_manager.py --sync`*
