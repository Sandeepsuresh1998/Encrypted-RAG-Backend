from sanic import Blueprint
from sanic import json

bp = Blueprint("k8s")

@bp.get("/healthz")
async def healthz(request):
    return json({"status": "ok"})