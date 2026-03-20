"""
server.py — Serves the custom UI and proxies /api/* → ADK backend (port 8000)
"""
import os
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

ADK_BASE = os.getenv("ADK_BASE_URL", "http://localhost:8000")

app = FastAPI(title="Vertex AI RAG Agent UI", docs_url=None, redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Proxy all /api/* requests to the ADK backend ──
@app.api_route("/api/{path:path}", methods=["GET","POST","PUT","DELETE","PATCH","OPTIONS"])
async def proxy(path: str, request: Request):
    url = f"{ADK_BASE}/{path}"
    body = await request.body()
    params = dict(request.query_params)
    headers = {k: v for k, v in request.headers.items()
               if k.lower() not in ("host", "content-length")}
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.request(
                method=request.method,
                url=url,
                content=body,
                params=params,
                headers=headers,
            )
        return Response(
            content=resp.content,
            status_code=resp.status_code,
            headers=dict(resp.headers),
        )
    except httpx.ConnectError:
        return Response(
            content=b'{"error":"ADK backend not running. Start it with: python run.py"}',
            status_code=502,
            media_type="application/json",
        )

# ── Serve static files & index.html ──
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    with open(os.path.join(static_dir, "index.html"), encoding="utf-8") as f:
        return HTMLResponse(f.read())
