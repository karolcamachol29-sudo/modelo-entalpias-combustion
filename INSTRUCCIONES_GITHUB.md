# 🛠️ Guía Paso a Paso de Comandos de Git y GitHub
**Para:** Karol Paola Camacho López  
**Proyecto:** Predicción de Entalpías de Combustión Mediante Machine Learning

---

## 📋 ¿Cómo Inicializar y Vincular este Proyecto a GitHub?

Sigue estos pasos en la pestaña **Terminal** de PyCharm (o en cualquier terminal abierta en la carpeta `github/`):

### 1. Configurar tu identidad en Git (solo si es una computadora nueva)
```bash
git config --global user.name "Karol Paola Camacho Lopez"
git config --global user.email "tu_correo@alumno.buap.mx"
```

### 2. Inicializar el Repositorio Local
```bash
git init
```

### 3. Verificar los archivos rastreados
```bash
git status
```
*Verás la lista de archivos que acabamos de crear en color rojo (archivos sin seguimiento).*

### 4. Añadir todos los archivos al área de preparación (Staging)
```bash
git add .
```
*Si vuelves a escribir `git status`, verás que todos los archivos aparecen en color verde.*

### 5. Realizar el Primer Commit Oficial
```bash
git commit -m "feat: estructura inicial del proyecto, configuracion de entorno, chempy y cuaderno 01"
```

### 6. Vincular con tu Repositorio Remoto en GitHub
1. Ve a [github.com](https://github.com/) e inicia sesión con tu cuenta.
2. Haz clic en el botón verde **New** para crear un nuevo repositorio.
3. Asigna el nombre: `modelo-entalpias-combustion`.
4. **IMPORTANTE:** Déjalo en modo **Public** y **NO marques** ninguna casilla de "Add a README file", "Add .gitignore" ni "Choose a license" (porque ya los creamos nosotros localmente).
5. Haz clic en **Create repository**.
6. Copia la URL de tu repositorio (por ejemplo: `https://github.com/tu-usuario/modelo-entalpias-combustion.git`).
7. En la terminal de PyCharm, ejecuta:
```bash
git branch -M main
git remote add origin https://github.com/tu-usuario/modelo-entalpias-combustion.git
git push -u origin main
```

---

## 🔄 El Flujo de Trabajo Diario (Los 3 Comandos Mágicos)

Cada vez que termines de trabajar en tu cuaderno o hagas mejoras:
```bash
# 1. Ver qué modificaste
git status

# 2. Preparar los cambios
git add .

# 3. Guardar la fotografía del cambio con un mensaje descriptivo
git commit -m "docs: actualizacion de analisis exploratorio y graficas de residuales"

# 4. Enviar a GitHub
git push
```
