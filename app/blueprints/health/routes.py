from __future__ import annotations

from flask import Blueprint, current_app, render_template_string
from sqlalchemy import text

from app.extensions import db
from app.utils.response import envelope

blp = Blueprint('health', __name__)

_INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Internet Assist API</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: #0f172a;
      color: #e2e8f0;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 2rem;
    }
    .card {
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 16px;
      padding: 2.5rem 3rem;
      max-width: 560px;
      width: 100%;
      box-shadow: 0 25px 50px -12px rgba(0,0,0,.5);
    }
    .badge {
      display: inline-flex;
      align-items: center;
      gap: .4rem;
      background: #10b981;
      color: #fff;
      font-size: .7rem;
      font-weight: 700;
      letter-spacing: .08em;
      text-transform: uppercase;
      border-radius: 999px;
      padding: .25rem .75rem;
      margin-bottom: 1.25rem;
    }
    .dot { width: 7px; height: 7px; background: #fff; border-radius: 50%; animation: pulse 2s infinite; }
    @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.4} }
    h1 { font-size: 1.75rem; font-weight: 700; color: #f8fafc; line-height: 1.25; }
    p  { color: #94a3b8; margin-top: .75rem; line-height: 1.6; font-size: .95rem; }
    .links { margin-top: 2rem; display: flex; flex-wrap: wrap; gap: .75rem; }
    .btn {
      display: inline-flex; align-items: center; gap: .4rem;
      padding: .6rem 1.25rem; border-radius: 8px; font-size: .875rem;
      font-weight: 600; text-decoration: none; transition: opacity .15s;
    }
    .btn:hover { opacity: .85; }
    .btn-primary { background: #2563eb; color: #fff; }
    .btn-outline { background: transparent; color: #94a3b8; border: 1px solid #334155; }
    .endpoints { margin-top: 2rem; }
    .endpoints h2 { font-size: .8rem; font-weight: 600; text-transform: uppercase;
                    letter-spacing: .08em; color: #64748b; margin-bottom: .75rem; }
    .endpoint { display: flex; align-items: center; gap: .6rem;
                padding: .5rem .75rem; border-radius: 6px; background: #0f172a;
                margin-bottom: .4rem; font-family: monospace; font-size: .8rem; }
    .method { font-weight: 700; width: 3rem; flex-shrink: 0; }
    .get    { color: #34d399; }
    .post   { color: #60a5fa; }
    .patch  { color: #f59e0b; }
    .delete { color: #f87171; }
    .path   { color: #e2e8f0; }
    .env-tag { margin-top: 2rem; padding: .5rem .75rem; background: #0f172a;
               border-radius: 6px; font-size: .8rem; color: #64748b; }
    .env-tag span { color: #a78bfa; font-weight: 600; }
  </style>
</head>
<body>
  <div class="card">
    <div class="badge"><div class="dot"></div> Live</div>
    <h1>Internet Assist API</h1>
    <p>Flask REST backend powering the Internet Assist platform. All endpoints require JWT authentication except public submission and chat routes.</p>

    <div class="links">
      <a class="btn btn-primary" href="/docs">Swagger Docs</a>
      <a class="btn btn-outline" href="/healthz">Health Check</a>
      <a class="btn btn-outline" href="/readyz">Readiness</a>
    </div>

    <div class="endpoints">
      <h2>Key Endpoints</h2>
      <div class="endpoint"><span class="method post">POST</span><span class="path">/admin/login</span></div>
      <div class="endpoint"><span class="method post">POST</span><span class="path">/admin/forgot-password</span></div>
      <div class="endpoint"><span class="method post">POST</span><span class="path">/admin/reset-password</span></div>
      <div class="endpoint"><span class="method get">GET</span><span class="path">/admin/contacts</span></div>
      <div class="endpoint"><span class="method get">GET</span><span class="path">/admin/quotes</span></div>
      <div class="endpoint"><span class="method get">GET</span><span class="path">/admin/jobs</span></div>
      <div class="endpoint"><span class="method get">GET</span><span class="path">/admin/job-postings</span></div>
      <div class="endpoint"><span class="method get">GET</span><span class="path">/admin/stats</span></div>
      <div class="endpoint"><span class="method get">GET</span><span class="path">/admin/audit-logs</span></div>
      <div class="endpoint"><span class="method post">POST</span><span class="path">/chat</span></div>
      <div class="endpoint"><span class="method post">POST</span><span class="path">/contact</span></div>
      <div class="endpoint"><span class="method post">POST</span><span class="path">/quotes</span></div>
      <div class="endpoint"><span class="method post">POST</span><span class="path">/job-applications</span></div>
      <div class="endpoint"><span class="method post">POST</span><span class="path">/remote-support-request</span></div>
      <div class="endpoint"><span class="method get">GET</span><span class="path">/job-postings</span></div>
    </div>

    <div class="env-tag">env: <span>{{ env }}</span> &nbsp;|&nbsp; python: <span>{{ python }}</span></div>
  </div>
</body>
</html>"""


@blp.route('/')
def index():
    import sys
    env = current_app.config.get('APP_ENV', 'development')
    if env == 'production':
        # Don't expose stack details in production
        return envelope(data={'status': 'ok'}, status=200)
    python = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    return render_template_string(_INDEX_HTML, env=env, python=python)


@blp.route('/healthz')
def healthz():
    return envelope(data={'status': 'ok'}, status=200)


@blp.route('/readyz')
def readyz():
    db.session.execute(text('SELECT 1'))
    # Don't expose environment name in production responses
    return envelope(data={'status': 'ready'}, status=200)
