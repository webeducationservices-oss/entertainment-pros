// Password gate for private client proposals under /proposal/*.
//
// Why not encrypt the page like the old build did: encrypted-in-JS pages cannot
// be edited in myaieditor, because there is no HTML for the editor to bind to.
// Gating at the edge keeps the markup plain, so click-to-edit works.
//
// Scope: only the public custom domain is gated. Vercel preview and *.vercel.app
// hosts are left open on purpose, because that is what the myaieditor preview
// iframe loads while editing. Those hosts are unguessable and the page itself
// sends noindex, so it stays out of search either way.

export const config = { matcher: '/proposal/:path*' }

const GATED_HOSTS = new Set([
  'www.entertainment-pros.com',
  'entertainment-pros.com',
])

const COOKIE = 'ep_proposal'

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

export default function middleware(request) {
  const url = new URL(request.url)
  const host = (request.headers.get('host') || '').toLowerCase()

  // Preview and deployment hosts stay open so the editor iframe can load.
  if (!GATED_HOSTS.has(host)) return

  const password = process.env.PROPOSAL_PASSWORD
  // Fail open rather than locking a client out of a live proposal if the env
  // var is ever missing. The page is noindex either way.
  if (!password) return

  // Already unlocked
  const cookies = request.headers.get('cookie') || ''
  if (cookies.split(';').some(c => c.trim() === `${COOKIE}=${password}`)) return

  // Submitted a code
  const key = url.searchParams.get('key')
  if (key !== null) {
    if (key === password) {
      return new Response(null, {
        status: 302,
        headers: {
          Location: url.pathname,
          'Set-Cookie': `${COOKIE}=${password}; Path=/proposal; Max-Age=2592000; Secure; HttpOnly; SameSite=Lax`,
        },
      })
    }
    return new Response(loginPage(true), {
      status: 401,
      headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' },
    })
  }

  return new Response(loginPage(false), {
    status: 401,
    headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' },
  })
}
