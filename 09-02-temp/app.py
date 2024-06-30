import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import smbus

app = FastAPI()
app.mount(path="/9-2/static", app=StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

bus = smbus.SMBus(1)
address_adt7410 = 0x48
register_adt7410 = 0x00

def read_adt7410():
    word_data = bus.read_word_data(address_adt7410, register_adt7410)
    data = (word_data & 0xff00)>>8 | (word_data & 0xff)<<8
    data = data>>3  # 13ビットデータ
    if data & 0x1000 == 0:  # 温度が正または0の場合
        temperature = data*0.0625
    else:  # 温度が負の場合、絶対値を取ってからマイナスをかける
        temperature = ( (~data&0x1fff) + 1)*-0.0625
    return temperature

@app.get('/9-2/get')
async def get():
    return read_adt7410()

@app.get('/9-2', response_class=HTMLResponse)
async def index(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)

try:
    uvicorn.run(app, host='0.0.0.0', port=8000)
except KeyboardInterrupt:
    pass
