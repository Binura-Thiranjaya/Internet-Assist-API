from __future__ import annotations

import hashlib
import re
from datetime import datetime, timedelta, timezone

import sqlalchemy as sa
from flask import g, request
from flask_smorest import Blueprint
from sqlalchemy import cast, func

from app.extensions import db, limiter
from app.models.page_view import PageView
from app.utils.decorators import roles_required
from app.utils.response import envelope

blp = Blueprint('analytics', __name__, description='Analytics')

# ── UA parsing ────────────────────────────────────────────────────────────────

_MOBILE_RE  = re.compile(r'Mobile|Android|iPhone|iPod|BlackBerry|IEMobile|Opera Mini', re.I)
_TABLET_RE  = re.compile(r'iPad|Android(?!.*Mobile)|Tablet', re.I)
_BROWSER_MAP = [
    ('Edge',    re.compile(r'Edg/', re.I)),
    ('Chrome',  re.compile(r'Chrome/', re.I)),
    ('Firefox', re.compile(r'Firefox/', re.I)),
    ('Safari',  re.compile(r'Safari/', re.I)),
    ('Opera',   re.compile(r'OPR/|Opera', re.I)),
    ('IE',      re.compile(r'MSIE|Trident/', re.I)),
]
_OS_MAP = [
    ('Windows', re.compile(r'Windows NT', re.I)),
    ('macOS',   re.compile(r'Mac OS X', re.I)),
    ('iOS',     re.compile(r'iPhone|iPad|iPod', re.I)),
    ('Android', re.compile(r'Android', re.I)),
    ('Linux',   re.compile(r'Linux', re.I)),
]


def _parse_ua(ua: str) -> tuple[str, str, str]:
    """Returns (device_type, browser, os)."""
    if _TABLET_RE.search(ua):
        device = 'tablet'
    elif _MOBILE_RE.search(ua):
        device = 'mobile'
    else:
        device = 'desktop'

    browser = 'Other'
    for name, pat in _BROWSER_MAP:
        if pat.search(ua):
            browser = name
            break

    os_name = 'Other'
    for name, pat in _OS_MAP:
        if pat.search(ua):
            os_name = name
            break

    return device, browser, os_name


def _hash_ip(ip: str) -> str:
    return hashlib.sha256(ip.encode()).hexdigest()


def _clean_referrer(ref: str | None) -> str | None:
    if not ref:
        return None
    try:
        from urllib.parse import urlparse
        parsed = urlparse(ref)
        return parsed.netloc or None
    except Exception:
        return None


# ── Public tracking endpoint ──────────────────────────────────────────────────

@blp.route('/analytics/track', methods=['POST'])
@limiter.limit('120/minute')
def track():
    data = request.get_json(silent=True) or {}
    path       = (data.get('path') or '/')[:1024]
    referrer   = _clean_referrer(data.get('referrer'))
    session_id = str(data.get('session_id') or '')[:64] or None

    ua = request.headers.get('User-Agent', '')
    device_type, browser, os_name = _parse_ua(ua)
    ip_hash = _hash_ip(request.remote_addr or '')

    pv = PageView(
        path=path,
        referrer=referrer,
        device_type=device_type,
        browser=browser,
        os=os_name,
        session_id=session_id,
        ip_hash=ip_hash,
    )
    db.session.add(pv)
    db.session.commit()
    return envelope(data={'ok': True}, status=201)


# ── Admin analytics ───────────────────────────────────────────────────────────

@blp.route('/admin/analytics')
@roles_required('admin')
def analytics_summary():
    now     = datetime.now(timezone.utc)
    today   = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_ago  = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)

    total_views   = PageView.query.count()
    today_views   = PageView.query.filter(PageView.created_at >= today).count()
    week_views    = PageView.query.filter(PageView.created_at >= week_ago).count()
    unique_sessions = db.session.query(func.count(func.distinct(PageView.session_id))).scalar() or 0

    # Daily trend — last 30 days
    date_col = cast(PageView.created_at, sa.Date)
    daily_rows = (
        db.session.query(date_col.label('date'), func.count(PageView.id).label('views'))
        .filter(PageView.created_at >= month_ago)
        .group_by(date_col)
        .order_by(date_col)
        .all()
    )
    daily = [{'date': str(r.date), 'views': r.views} for r in daily_rows]

    # Top pages
    top_pages_rows = (
        db.session.query(PageView.path, func.count(PageView.id).label('views'))
        .filter(PageView.created_at >= month_ago)
        .group_by(PageView.path)
        .order_by(func.count(PageView.id).desc())
        .limit(10)
        .all()
    )
    top_pages = [{'path': r.path, 'views': r.views} for r in top_pages_rows]

    # Devices
    device_rows = (
        db.session.query(PageView.device_type, func.count(PageView.id).label('count'))
        .filter(PageView.created_at >= month_ago)
        .group_by(PageView.device_type)
        .all()
    )
    devices = {r.device_type or 'unknown': r.count for r in device_rows}

    # Browsers
    browser_rows = (
        db.session.query(PageView.browser, func.count(PageView.id).label('count'))
        .filter(PageView.created_at >= month_ago)
        .group_by(PageView.browser)
        .order_by(func.count(PageView.id).desc())
        .limit(6)
        .all()
    )
    browsers = [{'name': r.browser or 'Other', 'count': r.count} for r in browser_rows]

    # Top referrers
    ref_rows = (
        db.session.query(PageView.referrer, func.count(PageView.id).label('views'))
        .filter(PageView.created_at >= month_ago, PageView.referrer.isnot(None))
        .group_by(PageView.referrer)
        .order_by(func.count(PageView.id).desc())
        .limit(8)
        .all()
    )
    referrers = [{'referrer': r.referrer, 'views': r.views} for r in ref_rows]

    return envelope(data={
        'totals': {
            'total_views':      total_views,
            'today_views':      today_views,
            'week_views':       week_views,
            'unique_sessions':  unique_sessions,
        },
        'daily':     daily,
        'top_pages': top_pages,
        'devices':   devices,
        'browsers':  browsers,
        'referrers': referrers,
    }, status=200)
