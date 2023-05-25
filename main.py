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

userIdData = {"admin":"1234","user1":"2345"}

# userType = admin or user / id = nickname / email = email address / profilePicture = user profile picture 
userInfo = {"admin":{"userType":"admin", "id":"admin", "email":"email1111@aaaaaa.com", "profilePicture":"admin.png"},
            "user1":{"userType":"user", "id":"user1", "email":"email2222@bbbbbb.com", "profilePicture":"user1.png"}
        }
#------#


#---backend server---#

@app.get("/", response_class=HTMLResponse) #main page
def index(request:Request):
    return templets.TemplateResponse("index.html", {"request":request})

#@app.post("/login.php", response_class=HTMLResponse)
@app.post("/login.php") #temp code for test
#def loginIndex(request:Request, id: str=Form(...), password: str=Form(...)):
def loginIndex(username: str=Form(...), password: str=Form(...)): #temp code for test
    if password == userIdData[username]:
        print(f"{username} login sucsess")
        #return templets.TemplateResponse("", {"request":request})
        return userInfo[username] #temp code for test
    else:
        print(f"{username} login failed")
        return "login failed" #temp code for test

@app.post("/", response_class=HTMLResponse) #logined main page
def login_index(request:Request, id:str=Form(...)):
    return templets.TemplateResponse("", {"request":request, "id":id})




#404 page
@app.get("/{item_id}", response_class=HTMLResponse)
def error(request:Request):
    return templets.TemplateResponse("", {"request":request})
#------#


