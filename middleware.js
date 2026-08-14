// Password gate for private client proposals under /proposal/*.
//
// Why not encrypt the page like the old build did: encrypted-in-JS pages cannot
// be edited in myaieditor, because there is no HTML for the editor to bind to.
// Gating at the edge keeps the markup plain, so click-to-edit works.
//
// Two hard-won constraints from the myaieditor preview pane (do not regress):
//
// 1. NEVER return 4xx for the gate. The editor probes the page server-side
//    (myaiediter app/api/preview-check/route.ts) and any status >= 400 makes
//    the pane show "Preview can't load here" instead of the iframe. The lock
//    screen is returned as a normal 200 page; it leaks nothing and is
//    Cache-Control: no-store, so the status code is doing no real work.
//
// 2. The editor iframes this site CROSS-SITE (myaieditor.com framing
//    entertainment-pros.com), and SameSite=Lax cookies are not sent in that
//    context. So the unlock sets two cookies: a Lax one for normal top-level
//    visits (the client), and a SameSite=None; Partitioned one that survives
//    inside the editor's iframe. Either one passes the gate.
//
// Scope: only the public custom domain is gated. Vercel preview and
// *.vercel.app hosts stay open — the editor swaps its iframe to those while
// editing, they are unguessable, and the page itself sends noindex.

export const config = { matcher: '/proposal/:path*' }

const GATED_HOSTS = new Set([
  'www.entertainment-pros.com',
  'entertainment-pros.com',
])

const COOKIE = 'ep_proposal'          // top-level visits (SameSite=Lax)
const COOKIE_IFRAME = 'ep_proposal_e' // cross-site iframe visits (editor pane)
const MAX_AGE = 2592000               // 30 days

function loginPage(wrong) {
  return `<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>Private Proposal | Entertainment Pros</title>
<style>
*{box-sizing:border-box}
body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;
     background:#1a1a1a;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;padding:24px}
.card{background:#fff;border-radius:14px;padding:40px 34px;max-width:400px;width:100%;text-align:center;
      box-shadow:0 10px 40px rgba(0,0,0,.4)}
h1{font-size:1.15rem;margin:0 0 6px;color:#1a1a1a;letter-spacing:.2px}
p{font-size:.9rem;color:#646464;margin:0 0 22px;line-height:1.6}
input{width:100%;padding:13px 15px;border:2px solid #e2e2e2;border-radius:8px;font-size:1rem;
      margin-bottom:12px;outline:none}
input:focus{border-color:#F38929}
button{width:100%;padding:13px;background:#F38929;color:#fff;border:0;border-radius:8px;
       font-size:.95rem;font-weight:700;cursor:pointer;letter-spacing:.3px}
button:hover{background:#C66000}
.rule{height:4px;border-radius:2px;margin:0 0 22px;
      background:linear-gradient(90deg,#F5C518 0%,#F38929 45%,#C1272D 100%)}
.err{background:#fdecec;color:#b0201f;font-size:.85rem;padding:9px 12px;border-radius:6px;margin-bottom:14px}
.foot{margin-top:20px;font-size:.78rem;color:#a0a0a0}
.foot a{color:#F38929;text-decoration:none}
</style></head><body>
<div class="card">
  <div class="rule"></div>
  <h1>This proposal is private</h1>
  <p>Enter the access code from your email to view it.</p>
  ${wrong ? '<div class="err">That code did not match. Please try again.</div>' : ''}
  <form method="GET">
    <input type="password" name="key" placeholder="Access code" autofocus autocomplete="current-password">
    <button type="submit">View proposal</button>
  </form>
  <div class="foot">Entertainment Pros &middot; <a href="tel:727-804-2277">(727) 804-2277</a></div>
</div></body></html>`
}

function gateResponse(wrong) {
  // 200 on purpose — see constraint 1 above.
  return new Response(loginPage(wrong), {
    status: 200,
    headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' },
  })
}

export default function middleware(request) {
  const url = new URL(request.url)
  const host = (request.headers.get('host') || '').toLowerCase()

  // Preview and deployment hosts stay open so the editor iframe can load.
  if (!GATED_HOSTS.has(host)) return

  const password = process.env.PROPOSAL_PASSWORD
  // Fail open rather than locking a client out of a live proposal if the env
  // var is ever missing. The page is noindex either way.
  if (!password) return

  // Already unlocked (either cookie counts)
  const cookies = request.headers.get('cookie') || ''
  const has = (name) => cookies.split(';').some(c => c.trim() === `${name}=${password}`)
  if (has(COOKIE) || has(COOKIE_IFRAME)) return

  // Submitted a code (also how an emailed ?key= link auto-unlocks)
  const key = url.searchParams.get('key')
  if (key !== null) {
    if (key === password) {
      const headers = new Headers({ Location: url.pathname })
      headers.append('Set-Cookie',
        `${COOKIE}=${password}; Path=/proposal; Max-Age=${MAX_AGE}; Secure; HttpOnly; SameSite=Lax`)
      headers.append('Set-Cookie',
        `${COOKIE_IFRAME}=${password}; Path=/; Max-Age=${MAX_AGE}; Secure; HttpOnly; SameSite=None; Partitioned`)
      return new Response(null, { status: 302, headers })
    }
    return gateResponse(true)
  }

  return gateResponse(false)
}
