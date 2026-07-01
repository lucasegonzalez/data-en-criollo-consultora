# Airtable — Sistema de calificación de leads

> Objetivo único: saber **a quién llamar primero**.
> Score **manual** (sin fórmula): el orden lo da `Calor` (1–3, lo pone Lucas al leer) + `Facturación`.
> El form manda 6 datos; Airtable agrega 4 que no se le piden a nadie.

---

## Base y tabla

- **Base:** `Data en Criollo`
- **Tabla:** `Leads`

---

## Campos

| # | Campo | Tipo Airtable | Origen | Notas |
|---|-------|---------------|--------|-------|
| 1 | `Nombre` | Single line text | del form | nombre + negocio |
| 2 | `Contacto` | Single line text | del form | email o teléfono |
| 3 | `Tipo` | Single select | del form | opciones: `Email`, `WhatsApp` |
| 4 | `Facturación` | Single select | del form (mapeado) | opciones abajo ↓ |
| 5 | `Mensaje` | Long text | del form | lo que escribió el lead |
| 6 | `Fuente` | Single select | del form (mapeado) | opciones abajo ↓ |
| 7 | `Recibido` | **Created time** | automático | no se envía nada, Airtable lo sella |
| 8 | `Calor` | **Rating** (máx 3) | **manual (Lucas)** | el score: 1 tibio · 2 bien · 3 caliente |
| 9 | `Estado` | Single select | default `Nuevo` | pipeline, opciones abajo ↓ |
| 10 | `Notas` | Long text | manual (Lucas) | notas de la llamada / seguimiento |

**Opciones de `Facturación`** (en este orden): `Menos de $5M / mes` · `$5M a $15M / mes` · `$15M a $30M / mes` · `Más de $30M / mes` · `Prefiero no decirlo`

**Opciones de `Fuente`:** `YouTube` · `LinkedIn` · `Instagram` · `Directo` · `Otro`

**Opciones de `Estado`:** `Nuevo` · `Calificado` · `Llamada` · `Propuesta` · `Cliente` · `Descartado`
(poné `Nuevo` como opción por defecto del campo)

---

## Vistas

**1. `🔥 A llamar`** (la vista de trabajo, ponela primera)
- Filtro: `Estado` es alguno de [`Nuevo`, `Calificado`]
- Orden: `Calor` ↓ (mayor primero), luego `Recibido` ↑ (más viejo primero, para no dejar a nadie colgado)
- Es la cola: abrís, leés el `Mensaje`, ponés `Calor`, y llamás de arriba para abajo.

**2. `Pipeline`** (Kanban)
- Agrupada por `Estado`. Arrastrás la tarjeta a medida que avanza: Nuevo → Calificado → Llamada → Propuesta → Cliente (o Descartado).

**3. `Todos`** (Grid, default) — el respaldo completo.

---

## El flujo, en una línea

Entra un lead → cae en `Nuevo` con `Calor` vacío → en la vista **A llamar** leés el mensaje, le ponés `Calor` 1–3 y movés el `Estado` → llamás a los de `Calor` 3 primero. Listo, eso es todo el sistema.

---

## Lo que la función (Cloudflare Pages Function) debe escribir

`POST https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/Leads`
Headers: `Authorization: Bearer {AIRTABLE_TOKEN}` · `Content-Type: application/json`

Body — **los nombres de campo tienen que coincidir EXACTO** (incluida la tilde de `Facturación`):

```json
{
  "fields": {
    "Nombre": "Juan · Almacén Don Pepe",
    "Contacto": "juan@correo.com",
    "Tipo": "Email",
    "Facturación": "$5M a $15M / mes",
    "Mensaje": "No sé si me conviene sumar repartos…",
    "Fuente": "YouTube",
    "Estado": "Nuevo"
  }
}
```

La función **no** manda `Calor` (manual), `Recibido` (automático) ni `Notas` (manual).

**Mapas de value → opción de Airtable** (el form manda el `value`, Airtable guarda la etiqueta):

```js
const FACT = {
  lt_5m:   "Menos de $5M / mes",
  "5m_15m":"$5M a $15M / mes",
  "15m_30m":"$15M a $30M / mes",
  gt_30m:  "Más de $30M / mes",
  prefiero_no:"Prefiero no decirlo"
};
const FUENTE = {
  youtube:"YouTube", linkedin:"LinkedIn", instagram:"Instagram",
  directo:"Directo", otro:"Otro"
};
const TIPO = { email:"Email", whatsapp:"WhatsApp" };
```

**Token:** Personal Access Token de Airtable con scope `data.records:write` sobre la base `Data en Criollo`.

**Variables de entorno de la función:** `AIRTABLE_TOKEN`, `AIRTABLE_BASE_ID`. (La tabla se llama `Leads`; podés dejarla fija o como `AIRTABLE_TABLE`.)

---

*Esto reemplaza el §4 del contrato de datos: la `Facturación` y la `Fuente` se guardan como etiquetas legibles (no como `value` crudo), porque la triage es manual y conviene que Lucas lea claro. El `value` sigue viajando estable desde el form; la función traduce.*
