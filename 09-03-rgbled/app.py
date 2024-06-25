import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from gpiozero import PWMLED

app = FastAPI()
app.mount(path="/9-3/static", app=StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

led1 = PWMLED(25)
led2 = PWMLED(24)
led3 = PWMLED(23)
led1.value = 0
led2.value = 0
led3.value = 0
# 共通アノードの場合、初期デューティ比を 1.0 に
#led1.value = 1
#led2.value = 1
#led3.value = 1

@app.get('/9-3/get/{gpio}/{rate}')
async def get(gpio: int, rate: str):
    rate_f = float(rate)

    if gpio == 25:
        led1.value = rate_f
    elif gpio == 24:
        led2.value = rate_f
    elif gpio == 23:
        led3.value = rate_f

    return rate_f

@app.get('/9-3', response_class=HTMLResponse)
async def index(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)

uvicorn.run(app, host='0.0.0.0', port=8000)
