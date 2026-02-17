from datetime import datetime, timezone
from pathlib import Path
import re

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

APP_NAME = "openoa-interview"
METHODS = [
    "MonteCarloAEP",
    "WakeLosses",
    "EYAGapAnalysis",
    "ElectricalLosses",
    "StaticYawMisalignment",
    "TurbineLongTermGrossEnergy",
]

app = FastAPI(title=APP_NAME)

STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
OPENOA_INIT = Path(__file__).resolve().parents[2] / "openoa" / "__init__.py"
VERSION_REGEX = re.compile(r"^__version__\s*=\s*['\"]([^'\"]+)['\"]", re.MULTILINE)


def read_openoa_version() -> str:
    try:
        content = OPENOA_INIT.read_text(encoding="utf-8")
    except OSError:
        return "unknown"
    match = VERSION_REGEX.search(content)
    return match.group(1) if match else "unknown"


@app.get("/api/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": APP_NAME,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/api/version")
def version() -> dict[str, str]:
    return {"package": "openoa", "version": read_openoa_version()}


@app.get("/api/methods")
def methods() -> dict[str, list[str]]:
    return {"methods": METHODS}


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")
