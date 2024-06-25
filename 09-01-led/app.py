import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from gpiozero import LED

app = FastAPI()
app.mount(path="/9-1/static", app=StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

led = LED(25)

@app.get('/9-1/get/{gpio}')
async def get(gpio: int):
    if gpio == 25:
        led.toggle()
    return led.value

@app.get('/9-1', response_class=HTMLResponse)
async def index(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)

uvicorn.run(app, host='0.0.0.0', port=8000)
