from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from utils.projRoot import getProjRoot

app = FastAPI()

siteDir = Path(getProjRoot()) / "calendarORGS" / "calendarViews" / "calendarSite"

# Serve static HTML from ./static directory
app.mount("/", StaticFiles(directory=siteDir, html=True), name="calendarSite")
