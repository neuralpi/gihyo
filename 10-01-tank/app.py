import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from gpiozero import PWMOutputDevice

app = FastAPI()
app.mount(path="/10-1/static", app=StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

out1 = PWMOutputDevice(25)
out2 = PWMOutputDevice(24)
out3 = PWMOutputDevice(23)
out4 = PWMOutputDevice(22)
out1.value = 0
out2.value = 0
out3.value = 0
out4.value = 0

@app.get('/10-1/get/{rate1}/{rate2}/{rate3}/{rate4}')
async def get(rate1: str, rate2: str, rate3: str, rate4:str):
    rate1_f = float(rate1)
    rate2_f = float(rate2)
    rate3_f = float(rate3)
    rate4_f = float(rate4)

    out1.value = rate1_f
    out2.value = rate2_f
    out3.value = rate3_f
    out4.value = rate4_f

    return rate1_f

@app.get('/10-1', response_class=HTMLResponse)
async def index(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)

uvicorn.run(app, host='0.0.0.0', port=8000)
