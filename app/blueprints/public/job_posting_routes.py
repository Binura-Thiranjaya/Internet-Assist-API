from __future__ import annotations

from flask_smorest import Blueprint

from app.models.job_posting import JobPosting
from app.utils.response import envelope

blp = Blueprint('public-job-postings', __name__, description='Public job postings')


def _serialize(p: JobPosting) -> dict:
    return {
        'id': p.id,
        'title': p.title,
        'team': p.team,
        'location': p.location,
        'type': p.employment_type,
        'summary': p.summary,
        'responsibilities': p.responsibilities or [],
        'requirements': p.requirements or [],
        'status': p.status,
        'created_at': p.created_at.isoformat(),
    }


@blp.route('/job-postings', methods=['GET'])
def list_job_postings():
    postings = JobPosting.query.filter_by(status='active').order_by(JobPosting.created_at.desc()).all()
    return envelope(data=[_serialize(p) for p in postings], status=200)
