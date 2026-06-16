from __future__ import annotations

import httpx
from flask import current_app

from app.logging import logger

_TICKET_LABELS = {
    'contact':         'Contact Request',
    'quote':           'Quote Request',
    'job_application': 'Job Application',
    'remote_support':  'Remote Support Request',
    'chat':            'Chat Support Request',
}


def _build_content(fields: dict) -> str:
    lines = []
    for key, value in fields.items():
        lines.append(f'{key}: {value if value is not None else "—"}')
    return '\n'.join(lines)


def create_ticket(
    ticket_type: str,
    ticket_id: str,
    fields: dict,
    sender_email: str,
    sender_name: str | None = None,
) -> dict | None:
    """Call the ticket platform and return {'ticket_id': uuid, 'ticket_ref': 'TKT-N'} or None on failure."""
    base_url = current_app.config.get('TICKET_API_URL', '').rstrip('/')

    if not base_url:
        logger.info('ticket_api_skipped_no_url', ticket_type=ticket_type, ticket_id=ticket_id)
        return None

    label   = _TICKET_LABELS.get(ticket_type, 'New Request')
    short   = ticket_id[:8].upper()
    subject = f'[#{short}] {label}'
    content = _build_content(fields)

    payload = {
        'subject':     subject,
        'content':     content,
        'senderEmail': sender_email,
        'senderName':  sender_name,
    }

    try:
        response = httpx.post(f'{base_url}/api/tickets', json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        result = {
            'ticket_id':  data.get('id'),
            'ticket_ref': data.get('displayId'),
        }
        logger.info('ticket_created', ticket_type=ticket_type, ticket_id=ticket_id,
                    sender=sender_email, ref=result['ticket_ref'])
        return result
    except Exception:
        logger.exception('ticket_creation_failed', ticket_type=ticket_type, ticket_id=ticket_id)
        return None
