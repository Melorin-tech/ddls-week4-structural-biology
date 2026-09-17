from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

ROOT = Path(__file__).parent
app = FastAPI(title="p53 Structure Viewer")
app.mount("/results", StaticFiles(directory=ROOT / "results"), name="results")

@app.get("/", response_class=HTMLResponse)
def index():
    return HTMLResponse((ROOT / "templates" / "index.html").read_text())
