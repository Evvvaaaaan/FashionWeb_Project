"""
Date : 2023.05.15
Autor : 서하민

Fashion app

"""


# uvicorn main:app --reload
# run web page  ^^^^

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import json

app = FastAPI()

templets = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def index(request:Request):
    return templets.TemplateResponse("", {"request":request})

@app.get("/login", response_class=HTMLResponse)
def loginIndex(request:Request):
    return templets.TemplateResponse("", {"request":request})



