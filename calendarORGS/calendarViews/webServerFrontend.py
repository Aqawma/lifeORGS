from pathlib import Path
from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, RedirectResponse, FileResponse

from utils.timeUtilitities.timeDataClasses import UnixTimePeriods
from whatsappSecrets.initSecrets import SecretCreator
from whatsappSecrets.TwofaKeyGenerator import TwoFAKey
from utils.projRoot import getProjRoot


app = FastAPI()

PRIVATE_KEY = SecretCreator().loadSecrets()['SITE_PRIVATE_KEY']
app.add_middleware(SessionMiddleware, secret_key=PRIVATE_KEY)

siteDir = Path(getProjRoot()) / "calendarORGS" / "calendarViews" / "calendarSite"

@app.get("/", response_class=HTMLResponse)
async def loginPage():
    return """
    <form method="post">
      <input type="password" name="tfaKey" placeholder="Enter Two Factor Authentication Key">
      <input type="submit" value="Verify Key">
    </form>
    """

@app.post("/", response_class=HTMLResponse)
async def login(tfaKey: str = Form(...)):
    if TwoFAKey().check2faKey(tfaKey):
        response = RedirectResponse(url="/calendar", status_code=302)
        response.set_cookie("auth", "ok", max_age=UnixTimePeriods.week * 2)
        return response
    return HTMLResponse("Incorrect or Expired Key. Please Request a New Key.")

@app.get("/calendar")
async def calendarPage(request: Request):
    if request.cookies.get("auth") == "ok":
        return FileResponse(siteDir / "index.html")
    return RedirectResponse("/")

# Serve static HTML from ./static directory
app.mount("/", StaticFiles(directory=siteDir, html=True), name="calendarSite")
