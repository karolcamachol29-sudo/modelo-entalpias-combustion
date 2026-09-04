# 📖 MANUAL DE OPERACIÓN: WORKFLOW MODULAR Y AUTOMATIZACIÓN
**Proyecto:** Predicción de Entalpías de Combustión Mediante Machine Learning  
**Autora:** Karol Paola Camacho López (FIQ — BUAP)

---

## 🎯 ¿Cómo Funciona este Sistema?

Este repositorio cuenta con un **motor de gestión técnica y automatización de entregables** (`src/workflow_manager.py`). Permite gestionar el avance del proyecto mediante:

1. **Matriz Maestra de Actividades (`config/matriz_actividades.json`):**  
   Base de datos editable con cada tarea, alcance, fechas límite y archivo de cierre exacto.
2. **Tablero Kanban Dinámico (`KANBAN.md`):**  
   Vista ágil organizada en columnas (`Por Iniciar`, `En Desarrollo`, `Revisión`, `Completado`, `Bloqueado`).
3. **Roadmap Temporal (`ROADMAP.md`):**  
   Cronograma visual con diagrama de Gantt en Mermaid con horizonte al 10 de Diciembre de 2026.
4. **Dashboard Interactivo Local (`dashboard.html`):**  
   Página web standalone que puedes abrir en tu navegador para ver métricas en tiempo real y validar nombres de archivos.
5. **Cierre Automático por Detección de Archivo (Trigger):**  
   Al guardar o subir un archivo cuyo nombre coincida con el requerido para una tarjeta, el sistema la marca automáticamente como `Completado`.

---

## 🛠️ Comandos de Utilidad en Terminal

Abre la terminal en la carpeta `github/` y utiliza estos comandos:

```bash
# 1. Ver el estado y porcentaje de avance actual del proyecto
python src/workflow_manager.py --status

# 2. Escanear el repositorio y cerrar automáticamente las tareas que tengan su archivo listo
python src/workflow_manager.py --scan

# 3. Regenerar y sincronizar todas las vistas (KANBAN.md, ROADMAP.md y dashboard.html)
python src/workflow_manager.py --dashboard

# 4. Validar si el nombre de un archivo cumple con la norma estricta antes de guardarlo
python src/workflow_manager.py --validate-name "F1-DAT_ACT03_DAT_dataset_curado_v1.0_FINAL.csv"
```

---

## 📝 ¿Cómo Modificar Actividades, Fechas o Nombres de Archivo?

Para adaptar el proyecto sin romper ninguna automatización:

1. Abre el archivo `config/matriz_actividades.json` en PyCharm.
2. Localiza la actividad que deseas editar (por ejemplo, `ACT03`).
3. Puedes cambiar:
   * `"fecha_limite"`: Formato `YYYY-MM-DD`.
   * `"archivo_cierre_requerido"`: Asegúrate de que cumpla con la expresión regular.
   * `"descripcion"`: Actualizar alcances o criterios de aceptación.
   * `"dependencias"`: Lista de IDs de tareas requeridas previas.
4. Guarda el archivo y ejecuta:
   ```bash
   python src/workflow_manager.py --sync
   ```
   *El sistema regenerará inmediatamente el tablero Kanban, el Gantt y el Dashboard.*

---

## 🌐 ¿Cómo Abrir el Dashboard Interactivo?
Simplemente haz doble clic sobre el archivo `dashboard.html` en tu explorador de archivos o ábrelo desde PyCharm con clic derecho $\longrightarrow$ **Open in $\longrightarrow$ Browser**.
Verás:
* Porcentaje global completado.
* Tarjetas dinámicas organizadas por columnas.
* Validador interactivo en vivo de nombres de archivo.
