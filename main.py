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


#---database---#

#must be change to hash!!!!!!!
userIdData = {"admin":"1234","user1":"2345"}

# userType = admin or user / id = nickname / email = email address / profilePicture = user profile picture 
userInfo = {"admin":{"userType":"admin", "id":"admin", "email":"email1111@aaaaaa.com", "profilePicture":"admin.png"},
            "user1":{"userType":"user", "id":"user1", "email":"email2222@bbbbbb.com", "profilePicture":"user1.png"}
        }
#------#


#---backend server---#

#main page
@app.get("/") #must read header and check user
def index():
    return "main page"


#login page
@app.get("/login", response_class=HTMLResponse) #login page
def login(request:Request):
    return templets.TemplateResponse("index.html", {"request":request})


#login processing page
@app.post("/loginProcess") 
def loginProcess(id: str=Form(...), password: str=Form(...)):
    if id in userIdData: #must be change to hash!!!!!!!!!!!
        if password == userIdData[id]:
            print(f"{id} login sucess.")
            return f"{id} login sucess." #should input jwt to header
        else:
            print(f"{id} login failed. (password incorrect)")
            return f"{id} login failed. (password incorrect)" #just alert in page
    else:
        print(f"{id} dose not exist in DB.")
        return f"{id} dose not exist in DB." #just alert in page






#404 page
@app.get("/{item_id}") 
def error():
    return "404 not found"
#------#


