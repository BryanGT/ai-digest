# 🤖 AI Daily Digest para Slack

Automatización que genera y envía cada mañana un resumen de ~10 min de las últimas novedades de IA directamente a tu canal de Slack, usando **Claude con web search** para buscar contenido actualizado.

## 📋 Contenido del digest

- 📡 **Modelos & Releases** — GPT, Claude, Gemini, Llama y otros LLMs
- 🛠️ **Herramientas & Productos** — APIs, frameworks, agentes, IDEs con IA
- 💰 **Mercado & Tendencias** — Funding, startups, adquisiciones
- 💡 **Take del día** — La implicación más importante para tu equipo

---

## 🚀 Setup en 5 pasos

### 1. Crear el Incoming Webhook en Slack

1. Ve a [api.slack.com/apps](https://api.slack.com/apps) → **Create New App** → **From scratch**
2. Nombre: `AI Digest Bot` | Selecciona tu workspace
3. En el menú lateral: **Incoming Webhooks** → activar el toggle
4. Clic en **Add New Webhook to Workspace**
5. Selecciona el canal donde quieres recibir el digest
6. Copia la URL del webhook (empieza con `https://hooks.slack.com/services/...`)

### 2. Crear el repositorio en GitHub

```bash
git init ai-daily-digest
cd ai-daily-digest

# Copia los archivos:
# - generate_digest.py  (en la raíz)
# - .github/workflows/ai-digest.yml
```

### 3. Agregar los Secrets en GitHub

En tu repo de GitHub: **Settings → Secrets and variables → Actions → New repository secret**

| Secret | Valor |
|--------|-------|
| `ANTHROPIC_API_KEY` | Tu API key de Anthropic (console.anthropic.com) |
| `SLACK_WEBHOOK_URL` | La URL del webhook que copiaste en el paso 1 |

### 4. Push del código

```bash
git add .
git commit -m "feat: AI daily digest automation"
git push origin main
```

### 5. Probar manualmente

En GitHub: **Actions → 🤖 AI Daily Digest → Run workflow → Run workflow**

---

## ⏰ Horario

Por defecto corre **lunes a viernes a las 8:00 AM** (Guatemala / UTC-6).

Para cambiar el horario, edita el cron en `.github/workflows/ai-digest.yml`:

```yaml
# Ejemplos de cron:
"0 14 * * 1-5"   # Lunes-viernes 8am Guatemala (14:00 UTC)
"0 13 * * 1-5"   # Lunes-viernes 7am Guatemala (13:00 UTC)
"0 14 * * *"     # Todos los días 8am Guatemala
```

🔗 Para generar expresiones cron: [crontab.guru](https://crontab.guru)

---

## 💰 Costo estimado

| Servicio | Costo |
|----------|-------|
| GitHub Actions | **Gratis** (2,000 min/mes en repos públicos o privados) |
| Anthropic API (Claude Opus) | ~$0.10–0.20 por digest (con web search) |
| **Total mensual (22 días)** | **~$2–4 USD** |

---

## 🛠️ Personalización

### Cambiar los temas del digest

En `generate_digest.py`, edita la lista `TOPICS`:

```python
TOPICS = [
    "nuevos modelos de IA: GPT, Claude, Gemini, Llama, Mistral",
    "herramientas para desarrolladores: APIs, frameworks, agentes",
    "tendencias del mercado: funding, startups, adquisiciones",
    # Agrega tus propios temas aquí:
    # "noticias de Kubernetes y DevOps con IA",
    # "papers de investigación en NLP",
]
```

### Cambiar el idioma o tono

Modifica el `SYSTEM_PROMPT` en `generate_digest.py` para ajustar el tono, idioma o estructura del digest.

---

## 🐛 Troubleshooting

**El workflow no corre automáticamente:**
- GitHub puede pausar workflows en repos sin actividad. Haz un commit cada tanto o ejecútalo manualmente.

**Error de API key:**
- Verifica que los secrets estén bien escritos (sin espacios extra)

**No llega el mensaje a Slack:**
- Verifica que el webhook esté activo en api.slack.com
- Asegúrate que el bot tenga permisos en el canal

**El digest está desactualizado:**
- El web search busca noticias recientes automáticamente. Si ves info vieja, puede ser un día con poco movimiento en el tema.
