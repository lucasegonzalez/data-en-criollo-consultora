# Setup — Hetzner VPS + Despliegue Inicial

Guía paso a paso para poner en producción la infraestructura de consultoría.

---

## 1. Crear cuenta en Hetzner

1. Andá a [hetzner.com](https://www.hetzner.com) y registrate.
2. Verificá tu identidad (documento + dirección).
3. Agregá método de pago (tarjeta o transferencia).
4. Esperá la aprobación (suele ser instantánea o <24h).

## 2. Provisionar VPS (CX22)

1. Entrá al [Cloud Console](https://console.hetzner.cloud).
2. Creá un proyecto nuevo (ej: `data-en-criollo`).
3. Click **Add Server**:
   - **Location**: Falkenstein o Nuremberg (los más baratos)
   - **Image**: Ubuntu 24.04 LTS
   - **Type**: CX22 (2 vCPU, 4 GB RAM, 40 GB SSD)
   - **SSH Keys**: Agregá tu clave pública (`~/.ssh/id_ed25519.pub`)
   - **Name**: `consultora-vps`
   - **Firewall**: Creá uno nuevo (solo puertos 22, 80, 443)
4. Click **Create & Buy now**.
5. Anotá la **IP pública** que te asignan.

> 💡 Si querés IPv4 + IPv6, activalo antes de crear. Totalmente gratis.

## 3. Conectar por SSH

```bash
ssh root@<IP_DEL_VPS>
```

> Si usaste un nombre de host en vez de IP, podés configurarlo en `~/.ssh/config`:
> ```
> Host consultora
>   HostName <IP_DEL_VPS>
>   User root
>   IdentityFile ~/.ssh/id_ed25519
> ```
> Y después conectás con `ssh consultora`.

## 4. Instalar Docker + Compose

```bash
# Actualizar sistema
apt update && apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com | sh

# Permitir usuario root usar Docker (ya sos root, pero por las dudas)
systemctl enable docker

# Verificar
docker --version
docker compose version
```

## 5. Configurar UFW (Firewall)

```bash
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp comment 'SSH'
ufw allow 80/tcp  comment 'HTTP'
ufw allow 443/tcp comment 'HTTPS'
ufw enable

# Verificar
ufw status verbose
```

> ⚠️ NO abras ningún otro puerto. Todos los servicios internos (FastAPI, n8n) se comunican por la red interna de Docker `consultora-net`.

## 6. Clonar el repositorio

```bash
mkdir -p /opt/consultora
cd /opt/consultora

# Si usás deploy key o HTTPS con token
git clone <repo-url> .

# Crear .env y configurar
cp .env.example .env
nano .env
# Completá: DOMAIN, TRAEFIK_PASS_HASH, etc.
```

### Generar password hash para Traefik

```bash
# Desde tu máquina local (no el VPS):
openssl passwd -apr1 mi_password_seguro
# Copiá el hash completo en TRAEFIK_PASS_HASH del .env
```

## 7. Levantar servicios

```bash
cd /opt/consultora

# Crear directorio para certificados
mkdir -p data/letsencrypt

# Levantar Traefik
docker compose up -d

# Verificar que arrancó
docker compose logs traefik

# Ver estado
docker compose ps
```

Si todo funciona, deberías poder acceder a `https://traefik.<TU_DOMINIO>` con las credenciales que configuraste.

## 8. Configurar Cloudflare DNS

1. Andá a [Cloudflare Dashboard](https://dash.cloudflare.com).
2. Agregá tu dominio (si no está en Cloudflare, transferí los nameservers).
3. En **DNS → Records**, creá:

| Tipo | Nombre                | Contenido  | Proxy |
| ---- | --------------------- | ---------- | ----- |
| A    | @ (o `consultora`)    | `<VPS_IP>` | ✅    |
| A    | `api`                 | `<VPS_IP>` | ✅    |
| A    | `n8n`                 | `<VPS_IP>` | ✅    |
| A    | `traefik` (opcional)  | `<VPS_IP>` | ✅    |

> ⚠️ IMPORTANTE: Dejá el proxy de Cloudflare (nube naranja) activado. Así ocultás tu IP real y Cloudflare filtra tráfico malicioso antes de que llegue al VPS.

4. En **SSL/TLS → Overview**, poné **Full (strict)**.
5. Si querés DNS-01 challenge para wildcard certs, generá un **API Token** con permiso `DNS:Edit` en `Zona: <tu-dominio>` y ponelo en `CF_DNS_API_TOKEN` del `.env`.

## Verificación final

```bash
# Desde tu máquina local:
curl -I https://traefik.<TU_DOMINIO>
# Deberías ver HTTP/2 401 (pide auth — significa que Traefik responde)

# También revisá los logs:
ssh root@<VPS_IP> "cd /opt/consultora && docker compose logs traefik"
```

Si ves `acme: certificate obtained` en los logs, felicitaciones — Tenés SSL funcionando 🎉

---

## Próximos pasos

Una vez que Traefik esté funcionando con certificados válidos, pasá al **Bloque 2**: FastAPI + Hermes.
