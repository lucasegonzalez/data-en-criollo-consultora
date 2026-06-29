# Plan Estratégico — Sistema Autónomo Data en Criollo

> De la idea al sistema autónomo: toda la historia, dónde estamos y hacia dónde vamos.

---

## 1. La Historia — Cómo llegamos hasta acá

### El origen (Mayo 2026)

Lucas necesita un sistema que le permita hacer **videos para YouTube** mientras la parte operativa de la consultoría funciona sola: captar leads, responder consultas, gestionar clientes, publicar en redes sociales.

La idea es clara: **un sistema autónomo que gestione el negocio mientras él se centra en crear contenido**.

### Fase 1: SDD + Código (Junio 2026)

Arrancamos con SDD (Spec-Driven Development) para planificar todo antes de escribir código:

1. **Proposal** → Definimos el alcance: VPS + FastAPI + n8n + Hermes + Traefik
2. **Spec** → Especificamos cada componente con detalle
3. **Design** → Arquitectura técnica, modelos de datos, flujos
4. **Tasks** → Dividimos en 37 tareas en 7 fases, 3 bloques

**Código completado (100%):**

| Bloque | Componentes | Archivos |
| ------ | ----------- | -------- |
| 1 | VPS + Docker + Traefik + UFW | docker-compose.yml, traefik/, SETUP.md |
| 2 | FastAPI + SQLite + JWT + Hermes | backend/, hermes/ |
| 3 | n8n + CI/CD + Backups + Cloudflare | .github/, backup.sh, website/, DEPLOY_CHECKLIST.md |

**37 archivos, ~1239 líneas de código, todo commiteado en GitHub.**

### Fase 2: La búsqueda del VPS (Junio 2026 — actualidad)

El código está listo, falta el VPS donde deployarlo. Arranca la novela:

| Proveedor | Resultado | Motivo |
| --------- | --------- | ------ |
| **Hetzner** (€4,49) | ❌ | Rechazó el registro |
| **Hostinger KVM 2** ($7,99/mes) | ❌ | Pedía $215 upfront |
| **Contabo Cloud VPS S** (€5,50/mes) | ❌ | Tarjeta no pasó el CVC |
| **Argencloud** (~$20.000/mes) | ❌ | +$36.000 con setup e IVA |
| **Neolo** (~$15.000/mes) | ❌ | Sitio no funcionaba |
| **Baires Host VPS Basic** ($20.280/mes) | ✅ **Pendiente** | Mercado Pago, Buenos Aires |

### Lecciones aprendidas

- **Pagar en USD desde Argentina es un calvario.** Las tarjetas rebotan, los CVC no pasan, los bancos bloquean.
- **Los "precios gancho" no existen.** Hostinger pide $215 upfront, Contabo no toma tarjetas argentinas.
- **Los proveedores locales en ARS son la solución real.** Baires Host opera en Buenos Aires y toma Mercado Pago.
- **Más caro ≠ peor.** Baires Host cuesta ~$13 USD/mes vs ~$6 de Contabo, pero se paga en ARS sin drama.

---

## 2. La Visión — Sistema Autónomo

### Filosofía

> "Vos hacés videos. El sistema labura solo."

### Lo que el sistema hace (sin que toques nada)

#### 📬 Clasificación de leads por email
- Llega un mail a `consultoria@tudominio.com`
- Cloudflare lo redirige a la API
- Hermes (IA) analiza el contenido:
  - **Lead calificado** → responde automáticamente con presupuesto + agenda reunión
  - **Consulta general** → responde con info automática
  - **Spam** → lo ignora
- Todo queda registrado en SQLite como cliente potencial

#### 📱 Auto-posting en redes sociales
- Via n8n, programás contenido para Instagram y LinkedIn
- Se publica automáticamente en los horarios que definas
- Sin estar pegado al celu, sin apps externas

#### 🤖 Hermes — El agente IA
- Responde consultas de clientes (WhatsApp + Telegram)
- Revisa tareas vencidas cada 15 minutos
- Envía recordatorios de reuniones
- Coordina todo el sistema

#### 📊 Panel de gestión
- Clientes, contratos, reuniones y tareas
- API REST desde FastAPI + SQLite
- Acceso seguro con JWT

#### 🔐 Seguridad y respaldo
- Traefik con SSL automático (Let's Encrypt)
- UFW firewall (solo puertos 22, 80, 443)
- Backups diarios a Backblaze B2
- Watchtower actualiza los contenedores automáticamente

---

## 3. El Stack Actual

```
                     ┌──────────────┐
                     │  Cloudflare  │
                     │   (DNS +     │
                     │    Proxy)    │
                     └──────┬───────┘
                            │
                     ┌──────┴───────┐
                     │   Traefik    │
                     │  (SSL +      │
                     │   Reverse    │
                     │   Proxy)     │
                     └──────┬───────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
       ┌──────┴──────┐ ┌───┴────┐ ┌──────┴──────┐
       │   FastAPI   │ │  n8n   │ │   Hermes    │
       │ + SQLite    │ │  Auto- │ │  Agente IA  │
       │ Clientes,   │ │ posts  │ │  WhatsApp,  │
       │ Contratos,  │ │ IG+LI  │ │  Telegram,  │
       │ Tareas      │ │ Emails │ │  Scheduler  │
       └─────────────┘ └────────┘ └─────────────┘
              │
       ┌──────┴──────┐
       │  Watchtower │
       │ (Auto-update│
       │  imágenes)  │
       └─────────────┘
```

**Todo corre en un solo VPS de 4 GB RAM con Docker Compose.**

---

## 4. ¿Dónde Estamos?

### ✅ Logrado

- [x] Código del stack completo (37 archivos, 3 bloques)
- [x] SDD completo (Proposal → Spec → Design → Tasks)
- [x] GitHub repo: `github.com/lucasegonzalez/data-en-criollo-consultora`
- [x] SETUP.md + DEPLOY_CHECKLIST.md
- [x] Sitio estático listo para Cloudflare Pages
- [x] CI/CD listo (GHCR + Watchtower)
- [x] backup.sh a Backblaze B2

### 🔄 En proceso

- [ ] **Comprar VPS en Baires Host** — VPS Basic, $20.280/mes, Mercado Pago
- [ ] Tener dominio propio configurado en Cloudflare

### ❌ Pendiente (post-deploy)

- [ ] Deployar todo el stack en el VPS
- [ ] Configurar Cloudflare DNS (records A)
- [ ] Configurar email routing (Cloudflare → API)
- [ ] Crear workflows de n8n (IG, LinkedIn)
- [ ] Conectar WhatsApp Business API para Hermes
- [ ] Subir landing page a Cloudflare Pages
- [ ] Configurar backups (cron + B2)
- [ ] Verificación E2E

---

## 5. Costos Estimados

| Item | Costo/mes | Pago |
| ---- | --------- | ---- |
| **Baires Host VPS Basic** (2 vCPU, 4 GB, 40 GB NVMe) | **$20.280 ARS** (~$13 USD) | Mercado Pago ✅ |
| Dominio (.com) | ~$10 USD/año (~$0,83/mes) | Donde lo compres |
| Cloudflare (DNS + proxy) | **$0** | ✅ |
| Cloudflare Pages (landing) | **$0** | ✅ |
| Backblaze B2 (backups) | ~$0,50 USD/mes | Tarjeta o saldo |
| **Total mensual** | **~$21.000 ARS (~$14 USD)** | ✅ |

---

## 6. Próximos Pasos Concretos

### Ahora mismo
1. **[Baires Host](https://baires.host/es/cloud-vps)** → Comprar VPS Basic
2. Pagar con **Mercado Pago** (~$20.280)
3. Pasarme la **IP del VPS**

### Apenas tenés el VPS
4. Yo deployo todo el stack (30 min)
5. Configuramos Cloudflare DNS (15 min)
6. Verificamos SSL + servicios (10 min)

### Timeline realista
- **Día 1**: VPS comprado + stack deployado + SSL funcionando
- **Día 2**: Cloudflare email routing + Hermes clasificando leads
- **Día 3**: n8n con auto-posting a IG + LinkedIn
- **Semana 2**: WhatsApp Business API conectada
- **Semana 3**: Landing page en Cloudflare Pages

---

## 7. El Futuro (Cuando el negocio crezca)

| Hito | Cuando | Qué cambia |
| ---- | ------ | ---------- |
| Más clientes | 20+ leads/mes | Migrar a Postgres (más escalable) |
| Más carga | VPS al 70%+ | Escalar a 6 GB RAM en Baires Host |
| WhatsApp masivo | Muchos mensajes | Agregar worker de Hermes dedicado |
| Multi-idioma | Clientes internacionales | Cloudflare + traducción automática |
| Dashboard público | Web para clientes | Agregar frontend (Next.js) en el VPS |

---

*Documento actualizado: 29 de Junio, 2026*
*Próxima revisión: post-deploy*
