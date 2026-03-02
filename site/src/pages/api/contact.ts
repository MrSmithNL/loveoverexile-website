import type { APIRoute } from 'astro';

const MAILERLITE_API_KEY = import.meta.env.MAILERLITE_API_KEY;
const CONTACT_GROUP_ID = '180832854326904301';

export const prerender = false;

export const POST: APIRoute = async ({ request }) => {
  if (!MAILERLITE_API_KEY) {
    return new Response(JSON.stringify({ error: 'Server configuration error' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  let body: { email?: string; name?: string; subject?: string; message?: string };
  try {
    body = await request.json();
  } catch {
    return new Response(JSON.stringify({ error: 'Invalid request' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  const { email, name, subject, message } = body;

  if (!email || !name || !subject || !message) {
    return new Response(JSON.stringify({ error: 'All fields are required' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  // Add to MailerLite "Contact Messages" group with subject and message in fields
  const payload = {
    email,
    groups: [CONTACT_GROUP_ID],
    fields: {
      name,
      last_name: `[CONTACT] ${subject}`,
      company: message.slice(0, 255),
    },
  };

  const res = await fetch('https://connect.mailerlite.com/api/subscribers', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${MAILERLITE_API_KEY}`,
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    const msg =
      res.status === 422
        ? 'Please check your email address and try again.'
        : 'Something went wrong. Please try again.';
    return new Response(JSON.stringify({ error: msg, detail: err }), {
      status: res.status,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  return new Response(JSON.stringify({ ok: true }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  });
};
