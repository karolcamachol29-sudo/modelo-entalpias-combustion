#!/usr/bin/env python3
"""
SINCRONIZADOR DE ISSUES Y HITOS (ROADMAP) CON GITHUB
Proyecto: Predicción de Entalpías de Combustión Mediante Machine Learning
Autora: Karol Paola Camacho López (FIQ — BUAP)
"""

import json
import subprocess
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONFIG_PATH = os.path.join(ROOT_DIR, "config", "matriz_actividades.json")

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    return result.stdout.strip(), result.stderr.strip(), result.returncode

def main():
    print("🚀 Iniciando sincronización de Etiquetas, Hitos e Issues en GitHub...")

    # 1. Crear Etiquetas (Labels)
    labels = [
        ("fase:F0-ENV", "003b70", "Fase 0: Setup y Entorno"),
        ("fase:F1-DAT", "1f77b4", "Fase 1: Datos y Curaduría"),
        ("fase:F2-EDA", "ff7f0e", "Fase 2: Análisis Exploratorio y Grafos"),
        ("fase:F3-MLB", "2ca02c", "Fase 3: Machine Learning Base"),
        ("fase:F4-VAL", "d62728", "Fase 4: Validación y Residuales"),
        ("fase:F5-REP", "9467bd", "Fase 5: Reproducción Modelo Rector"),
        ("fase:F6-SIM", "8c564b", "Fase 6: Simulación en DWSIM"),
        ("fase:F7-EQK", "e377c2", "Fase 7: Transición al Equilibrio"),
        ("format:py", "79c0ff", "Código Python"),
        ("format:ipynb", "d29922", "Cuaderno Jupyter Notebook"),
        ("format:csv", "7ee787", "Dataset CSV"),
        ("format:dwsim", "ffa657", "Simulación DWSIM"),
        ("format:tex-pdf", "ff7b72", "Documentación LaTeX / PDF"),
        ("format:txt", "c9d1d9", "Archivo de texto plano"),
        ("area:termoquimica", "b60205", "Termodinámica y Calorimetría"),
        ("area:data-engineering", "0e8a16", "Ingeniería y Curaduría de Datos"),
        ("area:grafos-moleculares", "5319e7", "Teoría de Grafos Químicos"),
        ("area:machine-learning", "1d76db", "Algoritmos de Machine Learning"),
        ("area:simulacion", "d93f0b", "Simulación de Procesos Químicos"),
        ("area:documentacion", "0052cc", "Reportes y Manuscritos"),
        ("area:control-versiones", "fbca04", "Git, GitHub y Entornos"),
        ("estado:Completado", "0e8a16", "Actividad Completada"),
        ("estado:En-Proceso", "fbca04", "Actividad en Desarrollo Activo"),
        ("estado:Backlog", "cfd3d7", "Actividad por Iniciar"),
        ("estado:Bloqueado", "b60205", "Actividad Bloqueada")
    ]

    for name, color, desc in labels:
        cmd = f'gh label create "{name}" --color "{color}" --description "{desc}" --force'
        run_cmd(cmd)
    print("✅ Etiquetas taxonómicas configuradas.")

    # 2. Crear Hitos (Milestones) que representan el Roadmap nativo en GitHub
    milestones = [
        ("Hito F0: Setup y Fundamentos Termoquímicos", "2026-09-05T23:59:59Z", "Configuración del entorno digital, Git, ChemPy y checklist del viernes"),
        ("Hito F1-F2: Curaduría de Datos y Grafos Químicos", "2026-09-26T23:59:59Z", "Depuración de base de datos, outliers e índices de Wiener/Estrada"),
        ("Hito F3-F4: Modelado Machine Learning y Validación", "2026-10-17T23:59:59Z", "Modelos lineales OLS/Ridge, Random Forest y análisis de residuales"),
        ("Hito F5-F6: Reproducción Modelo Rector y DWSIM", "2026-11-14T23:59:59Z", "Replicación de ACS Omega 2025 y simulación de combustión en DWSIM"),
        ("Hito F7: Transición al Proyecto de Equilibrio Químico", "2026-12-10T23:59:59Z", "Cálculo de Gibbs, Keq y manuscrito para el 10 de diciembre de 2026")
    ]

    milestone_map = {}
    for title, due, desc in milestones:
        # Consultar si ya existe
        stdout, _, _ = run_cmd(f'gh api /repos/karolcamachol29-sudo/modelo-entalpias-combustion/milestones -q ".[] | select(.title == \\"{title}\\") | .number"')
        if stdout:
            milestone_map[title] = int(stdout)
        else:
            create_cmd = f'gh api /repos/karolcamachol29-sudo/modelo-entalpias-combustion/milestones -f title="{title}" -f due_on="{due}" -f description="{desc}" -q ".number"'
            out, _, rc = run_cmd(create_cmd)
            if rc == 0 and out:
                milestone_map[title] = int(out)

    print(f"✅ Hitos del Roadmap registrados en GitHub: {milestone_map}")

    # Función para asociar actividad con hito
    def obtener_hito_por_fase(fase):
        if fase == "F0-ENV":
            return "Hito F0: Setup y Fundamentos Termoquímicos"
        elif fase in ["F1-DAT", "F2-EDA"]:
            return "Hito F1-F2: Curaduría de Datos y Grafos Químicos"
        elif fase in ["F3-MLB", "F4-VAL"]:
            return "Hito F3-F4: Modelado Machine Learning y Validación"
        elif fase in ["F5-REP", "F6-SIM"]:
            return "Hito F5-F6: Reproducción Modelo Rector y DWSIM"
        else:
            return "Hito F7: Transición al Proyecto de Equilibrio Químico"

    # 3. Leer actividades y crear Issues en GitHub
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Verificar issues existentes para evitar duplicados
    stdout, _, _ = run_cmd('gh issue list --state all --json number,title --limit 100')
    existing_issues = json.loads(stdout) if stdout else []
    existing_titles = {iss["title"]: iss["number"] for iss in existing_issues}

    for act in data["actividades"]:
        act_id = act["id"]
        full_title = f"[{act_id}] {act['titulo']}"
        
        # Mapear tags a labels de GitHub
        labels_to_apply = [f"fase:{act['fase']}", f"estado:{act['estado'].replace(' ', '-')}"]
        for tag in act.get("tags", []):
            if tag.startswith("#"):
                fmt = tag[1:]
                if fmt in ["tex", "pdf"]:
                    fmt = "tex-pdf"
                labels_to_apply.append(f"format:{fmt}")
            elif tag.startswith("@"):
                area = tag[1:]
                labels_to_apply.append(f"area:{area}")

        # Cuerpo markdown completo
        inputs_str = "\n".join([f"- {inp}" for inp in act.get("inputs_requeridos", [])])
        deps_str = ", ".join(act.get("dependencias", [])) if act.get("dependencias") else "Ninguna (Actividad raíz)"

        body = f"""## 🎯 Alcance de la Actividad
{act['descripcion']}

## 📥 Inputs Requeridos
{inputs_str}

## 🏁 Criterios de Aceptación
{act.get('criterios_aceptacion', 'Verificación por el mentor')}

## 📄 Archivo de Cierre Exacto Requerido
`{act['archivo_cierre_requerido']}`

## 📅 Fechas Planificadas en el Roadmap
- **Fecha de Asignación:** `{act['fecha_asignacion']}`
- **Fecha Límite Sugerida:** `{act['fecha_limite']}`
- **Fase de Ejecución:** `{act['fase']}`
- **Dependencias Previas:** {deps_str}

---
*Esta tarjeta está vinculada a la matriz maestra y al motor de automatización en `src/workflow_manager.py`.*
"""
        
        milestone_title = obtener_hito_por_fase(act["fase"])
        milestone_num = milestone_map.get(milestone_title)

        if full_title in existing_titles:
            issue_num = existing_titles[full_title]
            print(f"ℹ️ Issue #{issue_num} '{full_title}' ya existe.")
        else:
            labels_flag = ",".join(labels_to_apply)
            milestone_flag = f'--milestone "{milestone_title}"' if milestone_num else ''
            
            # Crear archivo temporal para el body para evitar problemas de escape en bash
            tmp_body_file = os.path.join(ROOT_DIR, "src", "tmp_body.md")
            with open(tmp_body_file, "w", encoding="utf-8") as tmp_f:
                tmp_f.write(body)

            cmd_create = f'gh issue create --title "{full_title}" --body-file "{tmp_body_file}" --label "{labels_flag}" {milestone_flag}'
            out_iss, err_iss, rc_iss = run_cmd(cmd_create)
            if os.path.exists(tmp_body_file):
                os.remove(tmp_body_file)

            if rc_iss == 0:
                print(f"🎉 Creado Issue en GitHub: {out_iss}")
                # Extraer número del issue creado
                try:
                    issue_num = int(out_iss.split("/")[-1])
                except Exception:
                    issue_num = None
            else:
                print(f"❌ Error al crear issue para {act_id}: {err_iss}")
                continue

        # Si el estado es "Completado", cerrar el issue en GitHub
        if act["estado"] == "Completado" and issue_num:
            archivo_cierre = act.get("archivo_cierre_requerido", "")
            close_cmd = f'gh issue close {issue_num} --comment "✅ Tarjeta cerrada automáticamente por detección y validación del archivo oficial de cierre: `{archivo_cierre}`."'
            run_cmd(close_cmd)
            print(f"  └─ Issue #{issue_num} cerrado formalmente en GitHub.")

    print("\n🎉 Sincronización completa con GitHub finalizada exitosamente.")

if __name__ == "__main__":
    main()
