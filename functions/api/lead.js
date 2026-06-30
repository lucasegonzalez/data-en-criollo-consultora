// /functions/api/lead.js
// Cloudflare Pages Function — receives form data, writes to Airtable

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};

const FACT = {
  lt_5m: "Menos de $5M / mes",
  "5m_15m": "$5M a $15M / mes",
  "15m_30m": "$15M a $30M / mes",
  gt_30m: "Más de $30M / mes",
  prefiero_no: "Prefiero no decirlo",
};

const FUENTE = {
  youtube: "YouTube",
  linkedin: "LinkedIn",
  instagram: "Instagram",
  directo: "Directo",
  otro: "Otro",
};

const TIPO = { email: "Email", whatsapp: "WhatsApp" };

export async function onRequestPost(context) {
  const { request, env } = context;

  // Parse body
  let body;
  try {
    body = await request.json();
  } catch {
    return new Response(JSON.stringify({ error: "JSON inválido" }), {
      status: 400,
      headers: { "Content-Type": "application/json", ...CORS },
    });
  }

  // Extract and validate
  const nombre = (body.nombre || "").trim();
  const contacto = (body.contacto || "").trim();
  const tipo = (body.tipo || "email").toLowerCase();
  const facturacion = (body.facturacion || "").trim();
  const mensaje = (body.mensaje || "").trim();
  const fuente = (body.fuente || "directo").toLowerCase();

  if (!nombre || !contacto || !mensaje) {
    return new Response(
      JSON.stringify({ error: "Faltan campos obligatorios: nombre, contacto, mensaje" }),
      { status: 400, headers: { "Content-Type": "application/json", ...CORS } }
    );
  }

  // Map to Airtable labels
  const airtablePayload = {
    fields: {
      Nombre: nombre,
      Contacto: contacto,
      Tipo: TIPO[tipo] || "Email",
      Mensaje: mensaje,
      Fuente: FUENTE[fuente] || "Directo",
      Estado: "Nuevo",
    },
  };

  // Only add Facturación if provided and valid
  if (facturacion && FACT[facturacion]) {
    airtablePayload.fields["Facturación"] = FACT[facturacion];
  }

  // Write to Airtable
  try {
    const atRes = await fetch(
      `https://api.airtable.com/v0/${env.AIRTABLE_BASE_ID}/Leads`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${env.AIRTABLE_TOKEN}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(airtablePayload),
      }
    );

    if (!atRes.ok) {
      const err = await atRes.text();
      console.error("Airtable error:", err);
      return new Response(
        JSON.stringify({ error: "Error guardando en Airtable", detail: err }),
        { status: 502, headers: { "Content-Type": "application/json", ...CORS } }
      );
    }
  } catch (e) {
    console.error("Airtable fetch failed:", e);
    return new Response(
      JSON.stringify({ error: "No se pudo conectar con Airtable" }),
      { status: 502, headers: { "Content-Type": "application/json", ...CORS } }
    );
  }

  // Optional: send confirmation email via Resend
  if (env.RESEND_API_KEY) {
    try {
      await fetch("https://api.resend.com/emails", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${env.RESEND_API_KEY}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          from: env.FROM_EMAIL || "hola@dataencriollo.com",
          to: contacto.includes("@") ? contacto : "tu-email@ejemplo.com",
          subject: "Recibimos tu consulta — Data en Criollo",
          html: `<p>Hola ${nombre},</p><p>Recibimos tu mensaje. Te escribimos dentro de las próximas 48 hs hábiles para coordinar la llamada.</p><p>Mientras tanto, podés pasar por el canal de YouTube: <a href="https://www.youtube.com/@Dataencriollo">Data en Criollo</a></p><p>— Lucas</p>`,
        }),
      });
    } catch (e) {
      console.error("Resend error (non-fatal):", e);
    }
  }

  return new Response(JSON.stringify({ ok: true }), {
    status: 200,
    headers: { "Content-Type": "application/json", ...CORS },
  });
}

export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS });
}