#!/usr/bin/env python3
"""
MÓDULO DE GESTIÓN Y AUTOMATIZACIÓN DE ENTREGABLES TÉCNICOS (WORKFLOW MANAGER)
Proyecto: Predicción de Entalpías de Combustión Mediante Machine Learning
Autora: Karol Paola Camacho López (FIQ — BUAP)

Funcionalidades:
  1. Validación estricta de nomenclatura mediante Expresión Regular (Regex).
  2. Escaneo del repositorio y disparo automático de cierre de tarjetas (Trigger).
  3. Generación automática de KANBAN.md y ROADMAP.md (con diagramas Mermaid de Gantt).
  4. Generación de un Dashboard interactivo HTML/CSS/JS autocontenido.
"""

import os
import re
import json
import argparse
from datetime import datetime
from typing import Dict, List, Any, Optional

# Rutas estándar del proyecto
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONFIG_PATH = os.path.join(ROOT_DIR, "config", "matriz_actividades.json")
KANBAN_MD_PATH = os.path.join(ROOT_DIR, "KANBAN.md")
ROADMAP_MD_PATH = os.path.join(ROOT_DIR, "ROADMAP.md")
DASHBOARD_HTML_PATH = os.path.join(ROOT_DIR, "dashboard.html")

REGEX_NOMENCLATURA = (
    r"^(F[0-7]-[A-Z]{3})_([A-Z]{3}\d{2})_([A-Z]{3})_([a-z0-9_]+)_(v\d+\.\d+)_(DRAFT|REV|FINAL)\.([a-zA-Z0-9]+)$"
)


class WorkflowManager:
    def __init__(self, config_path: str = CONFIG_PATH):
        self.config_path = config_path
        self.data = self._cargar_configuracion()
        self.actividades = self.data.get("actividades", [])
        self.regex = re.compile(self.data.get("regex_validacion", REGEX_NOMENCLATURA))

    def _cargar_configuracion(self) -> Dict[str, Any]:
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"No se encontró el archivo maestro de configuración en: {self.config_path}")
        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def guardar_configuracion(self) -> None:
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        print(f"✅ Configuración actualizada en: {self.config_path}")

    def validar_nombre_archivo(self, nombre_archivo: str) -> bool:
        """Verifica si un nombre de archivo cumple estrictamente con la norma de nomenclatura."""
        nombre_base = os.path.basename(nombre_archivo)
        return bool(self.regex.match(nombre_base))

    def escanear_archivos_en_repositorio(self) -> List[str]:
        """Recorre las carpetas del proyecto y recopila todos los archivos existentes."""
        archivos_encontrados = []
        carpetas_a_escanear = ["data", "notebooks", "src", "simulaciones", "reportes", "config"]
        for carpeta in carpetas_a_escanear:
            ruta_carpeta = os.path.join(ROOT_DIR, carpeta)
            if os.path.exists(ruta_carpeta):
                for raiz, _, archivos in os.walk(ruta_carpeta):
                    for archivo in archivos:
                        if not archivo.startswith(".git") and archivo != "__pycache__":
                            archivos_encontrados.append(archivo)
        return archivos_encontrados

    def ejecutar_trigger_de_cierre(self) -> List[str]:
        """
        Condición: Al detectar un archivo cuyo nombre coincida con el requerido.
        Acción: Mueve la tarjeta a Completado, registra timestamp y recalcula el progreso.
        """
        archivos_repo = self.escanear_archivos_en_repositorio()
        cambios_realizados = []

        for act in self.actividades:
            archivo_esperado = act.get("archivo_cierre_requerido")
            if not archivo_esperado:
                continue

            # Comprobar si existe el archivo de cierre oficial _FINAL
            if archivo_esperado in archivos_repo:
                if act["estado"] != "Completado":
                    act["estado"] = "Completado"
                    act["progreso_pct"] = 100
                    if not act.get("timestamp_cierre"):
                        act["timestamp_cierre"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                    cambios_realizados.append(f"🎉 Tarea [{act['id']}] '{act['titulo']}' CERRADA por detección de: {archivo_esperado}")
            else:
                # Buscar si existe una versión preliminar en revisión (_REV) o borrador (_DRAFT)
                prefijo_esperado = archivo_esperado.split("_v")[0]
                for archivo_real in archivos_repo:
                    if archivo_real.startswith(prefijo_esperado):
                        if "_REV." in archivo_real and act["estado"] not in ["Completado", "Revisión"]:
                            act["estado"] = "Revisión"
                            act["progreso_pct"] = max(act.get("progreso_pct", 0), 80)
                            cambios_realizados.append(f"🔍 Tarea [{act['id']}] movida a REVISIÓN por detección de: {archivo_real}")
                        elif "_DRAFT." in archivo_real and act["estado"] == "Backlog":
                            act["estado"] = "En Proceso"
                            act["progreso_pct"] = max(act.get("progreso_pct", 0), 40)
                            cambios_realizados.append(f"⏳ Tarea [{act['id']}] iniciada (EN PROCESO) por detección de: {archivo_real}")

        # Comprobar dependencias bloqueantes
        for act in self.actividades:
            if act["estado"] == "Backlog":
                deps = act.get("dependencias", [])
                deps_incompletas = [
                    d for d in deps if any(a["id"] == d and a["estado"] != "Completado" for a in self.actividades)
                ]
                if deps_incompletas:
                    # Tarea bloqueada por dependencias
                    if act["estado"] != "Bloqueado":
                        act["estado"] = "Bloqueado"

        if cambios_realizados:
            self.guardar_configuracion()
            self.generar_kanban_markdown()
            self.generar_roadmap_markdown()
            self.generar_dashboard_html()
        return cambios_realizados

    def generar_kanban_markdown(self) -> None:
        """Genera el archivo KANBAN.md sincronizado."""
        columnas = {
            "Bloqueado": ("⛔ Bloqueado", []),
            "Backlog": ("📋 Por Iniciar (Backlog)", []),
            "En Proceso": ("⏳ En Desarrollo", []),
            "Revisión": ("🔍 Revisión Técnica", []),
            "Completado": ("✅ Cerrado / Completado", [])
        }

        for act in self.actividades:
            estado = act.get("estado", "Backlog")
            if estado in columnas:
                columnas[estado][1].append(act)
            else:
                columnas["Backlog"][1].append(act)

        total = len(self.actividades)
        completadas = len(columnas["Completado"][1])
        pct_global = round((completadas / total) * 100, 1) if total > 0 else 0

        md = f"""# 📌 TABLERO KANBAN AUTOMATIZADO
**Proyecto:** {self.data.get('proyecto')}  
**Responsable:** {self.data.get('responsable')} ({self.data.get('institucion')})  
**Última Sincronización:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Progreso General:** {pct_global}% ({completadas}/{total} entregables cerrados)

---

"""
        for clave, (titulo_col, items) in columnas.items():
            md += f"## {titulo_col} ({len(items)})\n\n"
            if not items:
                md += "_Sin actividades en esta columna._\n\n"
            else:
                for a in items:
                    tags_str = " ".join([f"`{t}`" for t in a.get("tags", [])])
                    cierre = a.get("archivo_cierre_requerido", "N/A")
                    ts = a.get("timestamp_cierre")
                    ts_info = f"<br>**Cierre:** `{ts}`" if ts else ""
                    deps_str = f"<br>**Depende de:** {', '.join(a.get('dependencias', []))}" if a.get("dependencias") else ""
                    
                    md += f"""### [{a['id']}] {a['titulo']}
- **Fase:** `{a['fase']}` | **Progreso:** `{a.get('progreso_pct', 0)}%`
- **Descripción:** {a['descripcion']}
- **Plazo:** `{a.get('fecha_asignacion')}` al `{a.get('fecha_limite')}`{deps_str}
- **Archivo de Cierre Requerido:** `{cierre}`{ts_info}
- **Etiquetas:** {tags_str}

---
"""
        with open(KANBAN_MD_PATH, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"📋 Tablero Kanban actualizado en: {KANBAN_MD_PATH}")

    def generar_roadmap_markdown(self) -> None:
        """Genera el archivo ROADMAP.md con cronograma y diagrama de Gantt en Mermaid."""
        md = f"""# 🗺️ ROADMAP Y LÍNEA TEMPORAL DE ENTREGABLES
**Proyecto:** {self.data.get('proyecto')}  
**Responsable:** {self.data.get('responsable')}  
**Hito Final Crítico:** 10 de Diciembre de 2026 (Inicio Proyecto de Equilibrio Químico)

---

## 📈 Diagrama de Gantt del Proyecto (Mermaid)

```mermaid
gantt
    title Cronograma de Entregables Termoquímicos y ML (2026)
    dateFormat  YYYY-MM-DD
    axisFormat  %d-%b
"""
        fases_ordenadas = {}
        for act in self.actividades:
            f = act.get("fase", "General")
            fases_ordenadas.setdefault(f, []).append(act)

        for fase, acts in fases_ordenadas.items():
            md += f"\n    section {fase}\n"
            for a in acts:
                estado_mermaid = ""
                if a["estado"] == "Completado":
                    estado_mermaid = "done, "
                elif a["estado"] in ["En Proceso", "Revisión"]:
                    estado_mermaid = "active, "
                
                titulo_safe = a["titulo"].replace(":", "-").replace('"', "'")
                f_asig = a.get("fecha_asignacion", "2026-09-04")
                f_lim = a.get("fecha_limite", "2026-09-10")
                md += f"    {titulo_safe} ({a['id']}) :{estado_mermaid}{a['id']}, {f_asig}, {f_lim}\n"

        md += """```

---

## 🎯 Resumen de Hitos y Entregables por Fase

| Fase | Actividad | Título del Entregable | Fecha Límite | Estado Actual | Archivo de Cierre |
| :---: | :---: | :--- | :---: | :---: | :--- |
"""
        for a in self.actividades:
            estado_badge = "✅ Completado" if a["estado"] == "Completado" else ("⏳ En Proceso" if a["estado"] == "En Proceso" else ("🔍 Revisión" if a["estado"] == "Revisión" else ("⛔ Bloqueado" if a["estado"] == "Bloqueado" else "📋 Backlog")))
            md += f"| `{a['fase']}` | **{a['id']}** | {a['titulo']} | `{a['fecha_limite']}` | {estado_badge} | `{a['archivo_cierre_requerido']}` |\n"

        with open(ROADMAP_MD_PATH, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"🗺️ Roadmap actualizado en: {ROADMAP_MD_PATH}")

    def generar_dashboard_html(self) -> None:
        """Genera una interfaz moderna, responsiva e interactiva en HTML/CSS/JS standalone."""
        total = len(self.actividades)
        completadas = sum(1 for a in self.actividades if a["estado"] == "Completado")
        en_proceso = sum(1 for a in self.actividades if a["estado"] in ["En Proceso", "Revisión"])
        pct = round((completadas / total) * 100, 1) if total > 0 else 0

        actividades_json = json.dumps(self.actividades, ensure_ascii=False)

        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dashboard Técnico — {self.data.get('responsable')}</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #0d1117;
      --card-bg: #161b22;
      --border: #30363d;
      --text: #c9d1d9;
      --text-bright: #f0f6fc;
      --primary: #0070f3;
      --buap: #003b70;
      --success: #238636;
      --warning: #d29922;
      --danger: #da3633;
      --purple: #8957e5;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Inter', sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.5;
      padding: 24px;
    }}
    header {{
      background: linear-gradient(135deg, #001f3f, #003b70);
      padding: 24px 32px;
      border-radius: 12px;
      margin-bottom: 24px;
      border: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }}
    h1 {{ font-size: 1.6rem; color: #fff; font-weight: 700; }}
    .subtitle {{ color: #8b949e; font-size: 0.9rem; margin-top: 4px; }}
    .stats-row {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }}
    .stat-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 16px;
      display: flex;
      flex-direction: column;
    }}
    .stat-val {{ font-size: 1.8rem; font-weight: 700; color: var(--text-bright); }}
    .stat-label {{ color: #8b949e; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.5px; }}
    .progress-bar-bg {{
      background: #21262d;
      height: 8px;
      border-radius: 4px;
      overflow: hidden;
      margin-top: 8px;
    }}
    .progress-bar-fill {{
      background: linear-gradient(90deg, #238636, #2ea043);
      height: 100%;
      width: {pct}%;
      transition: width 0.5s ease;
    }}
    .kanban-board {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px;
      align-items: start;
    }}
    .kanban-col {{
      background: #12161c;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 14px;
    }}
    .col-header {{
      font-size: 0.95rem;
      font-weight: 600;
      color: var(--text-bright);
      margin-bottom: 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 8px;
      border-bottom: 1px solid var(--border);
    }}
    .col-badge {{
      background: #21262d;
      padding: 2px 8px;
      border-radius: 12px;
      font-size: 0.75rem;
    }}
    .kanban-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 12px;
      margin-bottom: 12px;
      transition: transform 0.2s, border-color 0.2s;
    }}
    .kanban-card:hover {{
      transform: translateY(-2px);
      border-color: #58a6ff;
    }}
    .card-id {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.75rem;
      color: #58a6ff;
      font-weight: 600;
    }}
    .card-title {{
      font-size: 0.9rem;
      font-weight: 600;
      color: var(--text-bright);
      margin: 4px 0 6px 0;
    }}
    .card-desc {{
      font-size: 0.78rem;
      color: #8b949e;
      margin-bottom: 8px;
      line-height: 1.4;
    }}
    .card-file {{
      background: #0d1117;
      border: 1px solid #21262d;
      border-radius: 4px;
      padding: 4px 6px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.7rem;
      color: #7ee787;
      word-break: break-all;
      margin-bottom: 8px;
    }}
    .card-tags {{
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
    }}
    .tag {{
      font-size: 0.68rem;
      padding: 2px 6px;
      border-radius: 4px;
      background: #21262d;
      color: #8b949e;
    }}
    .tag-py {{ color: #79c0ff; }}
    .tag-dwsim {{ color: #ffa657; }}
    .tag-pdf {{ color: #ff7b72; }}
    .tag-csv {{ color: #7ee787; }}
    .validator-box {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 20px;
      margin-top: 24px;
    }}
    .validator-input {{
      width: 100%;
      padding: 10px 12px;
      background: #0d1117;
      border: 1px solid var(--border);
      border-radius: 6px;
      color: #fff;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.9rem;
      margin-top: 8px;
    }}
    .validator-res {{
      margin-top: 10px;
      font-size: 0.85rem;
      font-family: 'JetBrains Mono', monospace;
    }}
  </style>
</head>
<body>

  <header>
    <div>
      <h1>⚡ Sistema de Gestión y Automatización de Entregables</h1>
      <div class="subtitle">Proyecto: {self.data.get('proyecto')} | Responsable: {self.data.get('responsable')} (FIQ — BUAP)</div>
    </div>
    <div style="text-align: right;">
      <div style="font-size: 0.8rem; color: #8b949e;">HITO CRÍTICO DE CIERRE</div>
      <div style="font-size: 1.1rem; font-weight: 700; color: #79c0ff;">10 de Diciembre de 2026</div>
    </div>
  </header>

  <div class="stats-row">
    <div class="stat-card">
      <span class="stat-label">Progreso Global</span>
      <span class="stat-val">{pct}%</span>
      <div class="progress-bar-bg"><div class="progress-bar-fill"></div></div>
    </div>
    <div class="stat-card">
      <span class="stat-label">Entregables Completados</span>
      <span class="stat-val" style="color: #3fb950;">{completadas} / {total}</span>
    </div>
    <div class="stat-card">
      <span class="stat-label">En Desarrollo Activo</span>
      <span class="stat-val" style="color: #d29922;">{en_proceso}</span>
    </div>
    <div class="stat-card">
      <span class="stat-label">Por Iniciar (Backlog)</span>
      <span class="stat-val" style="color: #58a6ff;">{total - completadas - en_proceso}</span>
    </div>
  </div>

  <div class="kanban-board" id="board"></div>

  <div class="validator-box">
    <h3 style="font-size: 1rem; color: var(--text-bright);">🧪 Validador Interactivo de Nomenclatura Estricta</h3>
    <p style="font-size: 0.8rem; color: #8b949e;">Comprueba si un nombre de archivo cumple con la norma antes de adjuntarlo para el cierre automático.</p>
    <input type="text" class="validator-input" id="fileNameInput" placeholder="Ej: F1-DAT_ACT03_DAT_dataset_curado_v1.0_FINAL.csv" oninput="validarEnVivo()">
    <div class="validator-res" id="validatorOutput"></div>
  </div>

  <script>
    const actividades = {actividades_json};
    const regexVal = new RegExp("{self.data.get('regex_validacion', REGEX_NOMENCLATURA)}");

    const estados = [
      {{ id: 'Bloqueado', title: '⛔ Bloqueado' }},
      {{ id: 'Backlog', title: '📋 Por Iniciar' }},
      {{ id: 'En Proceso', title: '⏳ En Desarrollo' }},
      {{ id: 'Revisión', title: '🔍 Revisión Técnica' }},
      {{ id: 'Completado', title: '✅ Completado' }}
    ];

    function renderBoard() {{
      const container = document.getElementById('board');
      container.innerHTML = '';

      estados.forEach(col => {{
        const colDiv = document.createElement('div');
        colDiv.className = 'kanban-col';
        
        const cards = actividades.filter(a => a.estado === col.id);
        
        colDiv.innerHTML = `
          <div class="col-header">
            <span>${{col.title}}</span>
            <span class="col-badge">${{cards.length}}</span>
          </div>
        `;

        cards.forEach(a => {{
          const card = document.createElement('div');
          card.className = 'kanban-card';
          
          let tagsHtml = (a.tags || []).map(t => {{
            let cls = 'tag';
            if (t.includes('py')) cls += ' tag-py';
            if (t.includes('dwsim')) cls += ' tag-dwsim';
            if (t.includes('pdf') || t.includes('tex')) cls += ' tag-pdf';
            if (t.includes('csv')) cls += ' tag-csv';
            return `<span class="${{cls}}">${{t}}</span>`;
          }}).join('');

          card.innerHTML = `
            <div class="card-id">${{a.id}} · ${{a.fase}}</div>
            <div class="card-title">${{a.titulo}}</div>
            <div class="card-desc">${{a.descripcion}}</div>
            <div class="card-file">📄 ${{a.archivo_cierre_requerido}}</div>
            <div class="card-tags">${{tagsHtml}}</div>
          `;
          colDiv.appendChild(card);
        }});

        container.appendChild(colDiv);
      }});
    }}

    function validarEnVivo() {{
      const val = document.getElementById('fileNameInput').value.trim();
      const out = document.getElementById('validatorOutput');
      if (!val) {{
        out.innerHTML = '';
        return;
      }}
      if (regexVal.test(val)) {{
        out.innerHTML = '<span style="color: #3fb950;">✅ VÁLIDO: El nombre cumple perfectamente con la norma oficial.</span>';
      }} else {{
        out.innerHTML = '<span style="color: #f85149;">❌ INVÁLIDO: Debe respetar [CÓDIGO_FASE]_[ID_ACTIVIDAD]_[TIPO]_[DESCRIPTOR]_[VERSION]_[ESTADO].[ext]</span>';
      }}
    }}

    renderBoard();
  </script>

</body>
</html>
"""
        with open(DASHBOARD_HTML_PATH, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"📊 Dashboard interactivo generado en: {DASHBOARD_HTML_PATH}")


def main():
    parser = argparse.ArgumentParser(description="Workflow Manager & Automation Engine")
    parser.add_argument("--scan", action="store_true", help="Escanea el repo y dispara el cierre automático por archivo.")
    parser.add_argument("--dashboard", action="store_true", help="Regenera KANBAN.md, ROADMAP.md y dashboard.html.")
    parser.add_argument("--status", action="store_true", help="Muestra el estado general del proyecto.")
    parser.add_argument("--validate-name", type=str, help="Valida un nombre de archivo contra la expresión regular.")
    parser.add_argument("--sync", action="store_true", help="Sincroniza todas las vistas a partir del archivo JSON maestro.")

    args = parser.parse_args()
    wm = WorkflowManager()

    if args.validate_name:
        valido = wm.validar_nombre_archivo(args.validate_name)
        if valido:
            print(f"✅ '{args.validate_name}' es VÁLIDO.")
        else:
            print(f"❌ '{args.validate_name}' es INVÁLIDO según la norma.")
        return

    if args.scan or args.sync:
        print("🔍 Escaneando repositorio en busca de archivos de cierre...")
        cambios = wm.ejecutar_trigger_de_cierre()
        if cambios:
            for c in cambios:
                print(c)
        else:
            print("ℹ️ No se detectaron nuevos archivos de cierre en este ciclo.")

    if args.dashboard or args.sync or args.scan:
        wm.generar_kanban_markdown()
        wm.generar_roadmap_markdown()
        wm.generar_dashboard_html()

    if args.status:
        total = len(wm.actividades)
        completadas = sum(1 for a in wm.actividades if a["estado"] == "Completado")
        pct = round((completadas / total) * 100, 1) if total > 0 else 0
        print(f"\n📊 ESTADO DEL PROYECTO: {pct}% completado ({completadas}/{total} entregables)")
        for a in wm.actividades:
            print(f"  [{a['id']}] {a['fase']} | {a['estado']:<12} | {a['titulo']}")


if __name__ == "__main__":
    main()
