from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from utils.jsonUtils import loadConfig

app = FastAPI()

verifyToken = loadConfig()['VERIFY_TOKEN']

@app.get("/webhook")
def verify(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == verifyToken:
        return PlainTextResponse(content=challenge)
    return PlainTextResponse(status_code=403, content="Forbidden")

@app.post("/webhook")
async def receive(request: Request):
    body = await request.json()
    print(body)
    return {"status": "received"}
