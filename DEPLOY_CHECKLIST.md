# Deploy Checklist

## Prerequisitos
- [ ] VPS contratado en Baires Host (VPS Basic)
- [ ] IP del VPS
- [ ] Dominio propio (ej: dataencriollo.com)
- [ ] Cuenta en Cloudflare (gratis)

## Paso a paso
1. [ ] SSH al VPS: `ssh root@<IP>`
2. [ ] Instalar Docker (ver SETUP.md)
3. [ ] Configurar UFW (ver SETUP.md)
4. [ ] Cloudflare: Agregar dominio y crear records A → IP del VPS
5. [ ] En el VPS: `mkdir -p /opt/consultora && cd /opt/consultora`
6. [ ] Subir el repo: `git clone https://github.com/lucasegonzalez/data-en-criollo-consultora .`
7. [ ] Crear .env: `cp .env.example .env` y completar
8. [ ] `docker compose up -d`
9. [ ] Verificar SSL: curl -I https://api.tudominio.com
10. [ ] Verificar n8n: https://n8n.tudominio.com
11. [ ] Configurar backup cron: `crontab -e` → `0 3 * * * /opt/consultora/backup.sh`

## Post-deploy
- [ ] Configurar Cloudflare Email Routing → API
- [ ] Configurar WhatsApp Business API para Hermes
- [ ] Crear workflows en n8n (IG, LinkedIn, emails)
- [ ] Subir landing page a Cloudflare Pages
- [ ] Configurar monitoreo (opcional)
