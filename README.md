# Data en Criollo — Consultoría de Datos

> **Decisiones de negocio con datos, en criollo.**

Landing page + pipeline de leads para la consultoría de Data en Criollo.

## Stack actual

| Capa | Herramienta | Costo |
| ---- | ----------- | ----- |
| Landing | Cloudflare Pages | $0 |
| Lead Pipeline | Cloudflare Pages Functions → Airtable | $0 |
| Email transaccional | Resend (3.000 emails/mes) | $0 |
| Automación | n8n (self-hosted) | incluido |
| Dominio | dataencriollo.com | ~$1 USD/mes |

## Cómo funciona

```
Lead llena el form
       ↓
Cloudflare Pages Function (/api/lead)
       ↓
Airtable → Lead guardado en tabla "Leads"
       ↓
Resend → Mail de confirmación al lead (opcional)
       ↓
Lucas abre Airtable → vista "🔥 A llamar" → lee mensaje → pone Calor 1-3 → llama
```

## Estructura del repo

```
consultora/
├── functions/
│   └── api/
│       └── lead.js          # Serverless: form → Airtable + Resend
├── website/
│   └── index.html           # Landing page (estilo VOX)
├── n8n-workflows/           # Workflows de n8n
├── .env.example             # Variables de entorno
├── AIRTABLE-SETUP.md        # Esquema de Airtable (campos, vistas, fórmulas)
├── PLAN.md                  # Visión estratégica completa
└── README.md                # Este archivo
```

## Deploy

1. Conectá el repo a **Cloudflare Pages**
2. Build output directory: `website`
3. Agregá las variables de entorno en Settings → Variables and Secrets:
   - `AIRTABLE_TOKEN` = tu Personal Access Token
   - `AIRTABLE_BASE_ID` = ID de tu base (empieza con `app`)
4. Deploy

## Documentación

| Documento | Qué contiene |
| --------- | ------------ |
| [`AIRTABLE-SETUP.md`](AIRTABLE-SETUP.md) | Esquema completo de Airtable: campos, vistas, flujo |
| [`PLAN.md`](PLAN.md) | Visión estratégica, roadmap, stack, costos |

---

**Sitio:** [dataencriollo.com](https://dataencriollo.com)
**Repo:** [github.com/lucasegonzalez/data-en-criollo-consultora](https://github.com/lucasegonzalez/data-en-criollo-consultora)
