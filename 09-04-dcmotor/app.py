import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from gpiozero import PWMOutputDevice

app = FastAPI()
app.mount(path="/9-4/static", app=StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

out1 = PWMOutputDevice(25)
out2 = PWMOutputDevice(24)
out1.value = 0
out2.value = 0

@app.get('/9-4/get/{rate1}/{rate2}')
async def get(rate1: str, rate2: str):
    rate1_f = float(rate1)
    rate2_f = float(rate2)

    out1.value = rate1_f
    out2.value = rate2_f

    return rate1_f

@app.get('/9-4', response_class=HTMLResponse)
async def index(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)

try:
    uvicorn.run(app, host='0.0.0.0', port=8000)
except KeyboardInterrupt:
    pass

out1.close()
out2.close()
