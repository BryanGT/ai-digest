#!/usr/bin/env python3
"""
AI Daily Digest - Genera un resumen diario de noticias de IA y lo envía a Slack
"""

import anthropic
import json
import os
import sys
from datetime import datetime
import urllib.request
import urllib.error

# ── Configuración ──────────────────────────────────────────────────────────────
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL", "")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

TOPICS = [
    "nuevos modelos de IA: GPT, Claude, Gemini, Llama, Mistral y otros LLMs",
    "herramientas y productos de IA para desarrolladores: APIs, frameworks, IDEs con IA, agentes",
    "tendencias del mercado de IA: funding, startups, adquisiciones, lanzamientos de empresas tech",
]

SYSTEM_PROMPT = """Eres un curador experto de noticias de IA para un equipo de desarrollo y automatización.
Tu tarea es generar un digest diario conciso, técnico y útil en español.

Formato OBLIGATORIO del mensaje (usa exactamente estos bloques de Slack markdown):

*🤖 AI Daily Digest — {fecha}*
_Lectura estimada: ~10 min_

━━━━━━━━━━━━━━━━━━━━━━

*📡 MODELOS & RELEASES*
[3-4 items con • bullet, título en negrita, 2-3 líneas de contexto técnico relevante, fuente entre paréntesis]

*🛠️ HERRAMIENTAS & PRODUCTOS*
[3-4 items con • bullet, enfocado en utilidad práctica para devs]

*💰 MERCADO & TENDENCIAS*
[2-3 items con • bullet, funding, movimientos estratégicos, lo que viene]

*💡 TAKE DEL DÍA*
[1 párrafo corto: la implicación más importante de todo esto para un equipo que construye con IA]

━━━━━━━━━━━━━━━━━━━━━━
_Generado con Claude + web search_ 🔍

Reglas:
- Sé específico y técnico, no genérico
- Incluye números/datos cuando estén disponibles (parámetros, precios, benchmarks)
- Prioriza novedades de los últimos 7 días
- Si no tienes info reciente de algo, omítelo, no inventes
- El "Take del día" debe ser una opinión fundamentada y útil, no una frase vacía"""


def generate_digest() -> str:
    """Genera el digest usando Claude con web search."""
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    today = datetime.now().strftime("%d %b %Y")
    topics_str = "\n".join(f"- {t}" for t in TOPICS)

    user_prompt = f"""Fecha de hoy: {today}

Busca las noticias más relevantes y recientes sobre:
{topics_str}

Genera el AI Daily Digest siguiendo exactamente el formato del sistema.
Busca información actualizada sobre cada categoría antes de escribir."""

    print("🔍 Buscando noticias con web search...")

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2000,
        system=SYSTEM_PROMPT.format(fecha=today),
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": user_prompt}],
    )

    # Extraer el texto final de la respuesta
    digest_text = ""
    for block in response.content:
        if block.type == "text":
            digest_text += block.text

    if not digest_text:
        raise ValueError("No se generó contenido en el digest")

    print("✅ Digest generado correctamente")
    return digest_text


def send_to_slack(message: str) -> bool:
    """Envía el mensaje al webhook de Slack."""
    if not SLACK_WEBHOOK_URL:
        raise ValueError("SLACK_WEBHOOK_URL no está configurada")

    payload = {
        "text": message,
        "unfurl_links": False,
        "unfurl_media": False,
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        SLACK_WEBHOOK_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = resp.read().decode("utf-8")
            if result == "ok":
                print("✅ Mensaje enviado a Slack exitosamente")
                return True
            else:
                print(f"⚠️ Respuesta inesperada de Slack: {result}")
                return False
    except urllib.error.HTTPError as e:
        print(f"❌ Error HTTP al enviar a Slack: {e.code} - {e.read().decode()}")
        return False


def main():
    print(f"🚀 Iniciando AI Daily Digest — {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # Validaciones
    if not ANTHROPIC_API_KEY:
        print("❌ Error: ANTHROPIC_API_KEY no está configurada")
        sys.exit(1)

    if not SLACK_WEBHOOK_URL:
        print("❌ Error: SLACK_WEBHOOK_URL no está configurada")
        sys.exit(1)

    # Generar digest
    digest = generate_digest()

    # Preview en consola
    print("\n" + "─" * 60)
    print("PREVIEW DEL DIGEST:")
    print("─" * 60)
    print(digest)
    print("─" * 60 + "\n")

    # Enviar a Slack
    success = send_to_slack(digest)

    if not success:
        print("❌ Falló el envío a Slack")
        sys.exit(1)

    print("🎉 ¡Digest completado y enviado!")


if __name__ == "__main__":
    main()