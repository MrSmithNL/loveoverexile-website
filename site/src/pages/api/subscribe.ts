import type { APIRoute } from 'astro';

const MAILERLITE_API_KEY = import.meta.env.MAILERLITE_API_KEY;

const GROUP_IDS: Record<string, string> = {
  waitlist: '180822675834275748',
  guide: '180822675888801753',
  community: '180822675859441598',
};

export const prerender = false;

export const POST: APIRoute = async ({ request }) => {
  if (!MAILERLITE_API_KEY) {
    return new Response(JSON.stringify({ error: 'Server configuration error' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  let body: { email?: string; name?: string; group?: string };
  try {
    body = await request.json();
  } catch {
    return new Response(JSON.stringify({ error: 'Invalid request' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  const { email, name, group } = body;

  if (!email || !group || !GROUP_IDS[group]) {
    return new Response(JSON.stringify({ error: 'Missing or invalid fields' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  const payload: Record<string, unknown> = {
    email,
    groups: [GROUP_IDS[group]],
  };

  if (name) {
    payload.fields = { name };
  }

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
    const message =
      res.status === 422 ? 'Please check your email address and try again.' : 'Something went wrong. Please try again.';
    return new Response(JSON.stringify({ error: message, detail: err }), {
      status: res.status,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  return new Response(JSON.stringify({ ok: true }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  });
};
