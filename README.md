# Data en Criollo — Consultoría

Infraestructura autogestionada para la consultoría de Data en Criollo.
Cliente, contratos, reuniones, tareas, automatizaciones n8n y un agente IA (Hermes) para WhatsApp y Telegram.

## Stack

| Capa       | Herramienta                         |
| ---------- | ----------------------------------- |
| VPS        | Hetzner CX22 (2 vCPU, 4 GB RAM)     |
| SO         | Ubuntu 24.04 LTS                    |
| Proxy      | Traefik v3.1 (Let's Encrypt, HTTP/3) |
| Backend    | FastAPI + SQLite (SQLAlchemy)       |
| Agente IA  | Hermes (Python, APScheduler)        |
| Automación | n8n                                 |
| Backup     | Backblaze B2 via restic             |
| CD         | Watchtower + GHCR                   |

## Deploy rápido

```bash
# 1. Clonar
git clone <repo-url> consultora
cd consultora

# 2. Configurar variables
cp .env.example .env
# Editar .env con tus dominios y credenciales

# 3. Levantar
docker compose up -d

# 4. Verificar
docker compose logs traefik
```

## Bloques

Este proyecto se despliega por bloques para mantener PRs revisables (<400 líneas):

| Bloque | Qué incluye                        | Estado     |
| ------ | ---------------------------------- | ---------- |
| 1      | VPS + Docker + Traefik             | ✅ Hecho   |
| 2      | FastAPI + Hermes                   | ✅ Hecho   |
| 3      | n8n + CI/CD + Cloudflare + Backups | ✅ Hecho   |
