# Deploy Checklist

## Prerequisitos
- [ ] Cuenta en Hetzner creada y verificada
- [ ] Dominio propio (ej: dataencriollo.com)
- [ ] Cuenta en Cloudflare (gratis)

## Paso a paso
1. [ ] Hetzner: Provisionar CX22 con Ubuntu 24.04 (ver SETUP.md)
2. [ ] SSH al VPS: `ssh root@<IP>`
3. [ ] Instalar Docker (ver SETUP.md)
4. [ ] Configurar UFW (ver SETUP.md)
5. [ ] Cloudflare: Agregar dominio y crear records A → IP del VPS
6. [ ] En el VPS: `mkdir -p /opt/consultora && cd /opt/consultora`
7. [ ] Subir el repo: `git clone <repo-url> .`
8. [ ] Crear .env: `cp .env.example .env` y completar
9. [ ] `docker compose up -d`
10. [ ] Verificar SSL: curl -I https://api.tudominio.com
11. [ ] Verificar n8n: https://n8n.tudominio.com
12. [ ] Configurar backup cron: `crontab -e` → `0 3 * * * /opt/consultora/backup.sh`

## Post-deploy
- [ ] Configurar WhatsApp Business API para Hermes
- [ ] Crear workflows en n8n
- [ ] Subir landing page a Cloudflare Pages
- [ ] Configurar monitoreo (opcional)
