from fastapi import FastAPI, Request
from typing import Union
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def hello_world(request: Request):
    return templates.TemplateResponse(
        request=request, name="hello-world.html"
    )