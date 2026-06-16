from __future__ import annotations

from flask import jsonify


def envelope(data=None, error=None, meta=None, status: int = 200):
    return jsonify({'data': data, 'error': error, 'meta': meta}), status


def error_envelope(code: str, message: str, details=None, status: int = 400):
    return envelope(
        error={'code': code, 'message': message, 'details': details},
        status=status,
    )
