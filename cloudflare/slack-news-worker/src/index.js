/**
 * Slack slash command endpoint: verifies the request came from Slack,
 * then triggers the "Slack Career News" GitHub Actions workflow on demand.
 */
export default {
  async fetch(request, env, ctx) {
    if (request.method !== "POST") {
      return new Response("Method not allowed", { status: 405 });
    }

    const rawBody = await request.text();

    const validSignature = await verifySlackSignature(request, rawBody, env.SLACK_SIGNING_SECRET);
    if (!validSignature) {
      return new Response("Invalid signature", { status: 401 });
    }

    ctx.waitUntil(triggerGithubWorkflow(env));

    return new Response(
      JSON.stringify({
        response_type: "ephemeral",
        text: ":mag: Hole die neuesten Career News, kommt gleich in den Kanal!",
      }),
      { headers: { "Content-Type": "application/json" } }
    );
  },
};

async function verifySlackSignature(request, rawBody, signingSecret) {
  const timestamp = request.headers.get("X-Slack-Request-Timestamp");
  const signature = request.headers.get("X-Slack-Signature");
  if (!timestamp || !signature) return false;

  // Reject requests older than 5 minutes to prevent replay attacks.
  const fiveMinutes = 60 * 5;
  if (Math.abs(Date.now() / 1000 - Number(timestamp)) > fiveMinutes) return false;

  const base = `v0:${timestamp}:${rawBody}`;
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(signingSecret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );
  const mac = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(base));
  const computed = "v0=" + [...new Uint8Array(mac)].map((b) => b.toString(16).padStart(2, "0")).join("");

  return timingSafeEqual(computed, signature);
}

function timingSafeEqual(a, b) {
  if (a.length !== b.length) return false;
  let result = 0;
  for (let i = 0; i < a.length; i++) {
    result |= a.charCodeAt(i) ^ b.charCodeAt(i);
  }
  return result === 0;
}

async function triggerGithubWorkflow(env) {
  const url = `https://api.github.com/repos/${env.GITHUB_OWNER}/${env.GITHUB_REPO}/actions/workflows/slack-news.yml/dispatches`;
  const resp = await fetch(url, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${env.GITHUB_TOKEN}`,
      Accept: "application/vnd.github+json",
      "Content-Type": "application/json",
      "User-Agent": "slack-news-trigger-worker",
    },
    body: JSON.stringify({ ref: env.GITHUB_REF }),
  });

  if (!resp.ok) {
    console.error("GitHub dispatch failed", resp.status, await resp.text());
  }
}
