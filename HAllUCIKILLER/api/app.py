"""
FastAPI Server Application for Hallucikiller.
"""

import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from api.routes import router
from core.config import settings

app = FastAPI(
    title="Hallucikiller AI Safety & QA Evaluation Pipeline",
    description="Automated red-teaming, hallucination scoring, adversarial benchmarking, and CI/CD gating for LLMs.",
    version="2027.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# High-performance GZip Compression (compress payloads > 500 bytes)
app.add_middleware(GZipMiddleware, minimum_size=500)

# CORS Policy
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

app.include_router(router)

# Mount 2027 Futuristic Web Frontend
WEB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "web")
if os.path.exists(WEB_DIR):
    app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")
    app.mount("/css", StaticFiles(directory=os.path.join(WEB_DIR, "css")), name="css")
    app.mount("/js", StaticFiles(directory=os.path.join(WEB_DIR, "js")), name="js")

@app.get("/")
async def root():
    index_path = os.path.join(WEB_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "message": "Welcome to Hallucikiller AI Safety Evaluation Pipeline API",
        "docs": "/docs",
        "version": "2027.1.0"
    }

@app.get("/dashboard")
async def dashboard():
    index_path = os.path.join(WEB_DIR, "index.html")
    return FileResponse(index_path)

@app.get("/favicon.ico")
@app.get("/favicon.svg")
async def favicon():
    fav_svg = os.path.join(WEB_DIR, "favicon.svg")
    if os.path.exists(fav_svg):
        return FileResponse(fav_svg, media_type="image/svg+xml", headers={"Cache-Control": "public, max-age=86400"})
    return Response(status_code=404)

@app.get("/robots.txt")
async def robots():
    robots_path = os.path.join(WEB_DIR, "robots.txt")
    if os.path.exists(robots_path):
        return FileResponse(robots_path, media_type="text/plain", headers={"Cache-Control": "public, max-age=86400"})
    return Response(status_code=404)

@app.get("/sitemap.xml")
async def sitemap():
    sitemap_path = os.path.join(WEB_DIR, "sitemap.xml")
    if os.path.exists(sitemap_path):
        return FileResponse(sitemap_path, media_type="application/xml", headers={"Cache-Control": "public, max-age=86400"})
    return Response(status_code=404)

@app.get("/site.webmanifest")
async def webmanifest():
    manifest_path = os.path.join(WEB_DIR, "site.webmanifest")
    if os.path.exists(manifest_path):
        return FileResponse(manifest_path, media_type="application/manifest+json", headers={"Cache-Control": "public, max-age=86400"})
    return Response(status_code=404)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)

