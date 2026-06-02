<div align="center">

# 🤖 Auto-Commits Bot

**Generador automático de contribuciones GitHub con patrones realistas**

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-Enabled-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)](#)

<br />

<img src="https://github-readme-stats.vercel.app/api?username=YOUR_USERNAME&show_icons=true&theme=radical" alt="GitHub Stats" />

---

</div>

## ✨ Características

| Feature | Descripción |
|---------|-------------|
| 🎯 **Patrones Realistas** | Commits con frecuencias y horarios que simulan actividad humana natural |
| 📅 **Rango Personalizable** | Configura el período de tiempo para generar commits |
| 🔄 **Push Automático** | Los cambios se envían automáticamente al repositorio remoto |
| 📊 **Frecuencia Variable** | Entre 0 y 10 commits por día con distribución ponderada |
| ⏰ **GitHub Actions** | Ejecución automática diaria via CI/CD |
| 🔧 **Configurable** | Archivo `config.json` para personalizar todos los parámetros |
| 🏃 **Modo Dry-Run** | Previsualiza los commits sin ejecutarlos |
| 📝 **Mensajes Convencionales** | Usa [Conventional Commits](https://www.conventionalcommits.org/) para mensajes profesionales |
| 🎨 **CLI Profesional** | Interfaz de terminal con colores, barra de progreso y resumen |

## 🚀 Quick Start

### 1. Clona el repositorio

```bash
git clone https://github.com/YOUR_USERNAME/Auto-Commits.git
cd Auto-Commits
```

### 2. Configura (opcional)

Edita `config.json` para personalizar el comportamiento:

```json
{
  "max_commits_per_day": 10,
  "min_commits_per_day": 0,
  "days_back": 365,
  "branch": "main",
  "commit_hour_start": 9,
  "commit_hour_end": 23,
  "skip_weekends_probability": 0.3,
  "git_username": "Auto-Commits Bot",
  "git_email": "bot@autocommits.dev"
}
```

### 3. Ejecuta el bot

```bash
python scripts/bot.py
```

## 📖 Uso

```bash
# Generar commits para los últimos 365 días
python scripts/bot.py

# Generar commits para los últimos 180 días
python scripts/bot.py --days 180

# Modo preview (sin crear commits reales)
python scripts/bot.py --dry-run

# Limitar a 5 commits por día
python scripts/bot.py --max-commits 5

# Generar sin push automático
python scripts/bot.py --no-push

# Especificar branch
python scripts/bot.py --branch main
```

## ⚙️ Configuración

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `max_commits_per_day` | `int` | `10` | Máximo de commits por día |
| `min_commits_per_day` | `int` | `0` | Mínimo de commits por día |
| `days_back` | `int` | `365` | Días hacia atrás para generar |
| `branch` | `string` | `"main"` | Branch para push |
| `commit_hour_start` | `int` | `9` | Hora de inicio de commits |
| `commit_hour_end` | `int` | `23` | Hora de fin de commits |
| `skip_weekends_probability` | `float` | `0.3` | Probabilidad de saltar fines de semana |
| `git_username` | `string` | `"Auto-Commits Bot"` | Nombre de usuario git |
| `git_email` | `string` | `"bot@autocommits.dev"` | Email de git |

## 🔄 GitHub Actions

El bot incluye un workflow de GitHub Actions que se ejecuta automáticamente:

- **⏰ Schedule**: Diario a medianoche UTC
- **🖱️ Manual**: Se puede ejecutar manualmente desde la pestaña Actions
- **🎛️ Inputs**: Configurable con `days_back` y `max_commits` al ejecutar manualmente

### Activar GitHub Actions

1. Ve a la pestaña **Actions** en tu repositorio
2. Haz clic en **"I understand my workflows, go ahead and enable them"**
3. El bot comenzará a ejecutarse automáticamente

## 📁 Estructura del Proyecto

```
Auto-Commits/
├── 📂 .github/
│   └── 📂 workflows/
│       └── 📄 bot.yml           # GitHub Actions workflow
├── 📂 contributions/
│   └── 📄 data.txt              # Registro de contribuciones
├── 📂 docs/
│   ├── 📄 index.html            # Dashboard web
│   └── 📄 style.css             # Estilos del dashboard
├── 📂 scripts/
│   └── 🐍 bot.py                # Script principal del bot
├── 📄 .gitignore
├── 📄 config.json               # Configuración del bot
├── 📄 LICENSE                   # Licencia MIT
└── 📄 README.md                 # Este archivo
```

## 🌐 Dashboard

El proyecto incluye un dashboard web que puedes desplegar con GitHub Pages:

1. Ve a **Settings** → **Pages**
2. Selecciona **Deploy from a branch**
3. Selecciona la branch `main` y la carpeta `/docs`
4. Tu dashboard estará disponible en `https://YOUR_USERNAME.github.io/Auto-Commits/`

## ⚠️ Disclaimer

> Este bot es solo para fines educativos y de demostración. Úsalo con responsabilidad y de acuerdo con los [Términos de Servicio de GitHub](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service).

## 📄 Licencia

Este proyecto está bajo la [Licencia MIT](LICENSE).

---

<div align="center">

**Hecho con ❤️ y 🤖**

</div>
