"""
Date : 2023.05.15
Autor : 서하민

Fashion app

"""

# uvicorn main:app --reload
# run web page  ^^^^

from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Annotated
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta, datetime
from pydantic import BaseModel
import json

app = FastAPI()

templets = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")



#--- JWT setting ---#
# to get a string like this run:
# openssl rand -hex 32
#must change befor live service
SECRET_KEY = "0646f05d474f2960e94e05e3df90193221bf600a250172a4b9d5b062127cd3e0" #must change befor live service
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    userType: str
    username: str
    email: str
    profilePicture: str | None = None


class UserInDB(User):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    
def authenticate_user(userInfo, username: str, password: str):
    user = get_user(userInfo, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(userInfo, username=token_data.username)#changed
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



#------#





#---database---#

# user1 is test account
# user1:2345

# userType = admin or user / username = nickname / hashed_password / email = email address / profilePicture = user profile picture 
userInfo = {"admin":{"userType":"admin", "username":"admin", "hashed_password":"$2b$12$t5758WWPnKsrn.7tprpGnub5qdBhoCvcyzcHOYGQRo6JjLWcnTwLy","email":"email1111@aaaaaa.com", "profilePicture":"admin.png"},
            "user1":{"userType":"user", "username":"user1",  "hashed_password":"$2b$12$zHb1jmxdbpt5P3OTH1fMdOYhwxVav1tluFeNyCDeCURWV/QA.hAU2","email":"email2222@bbbbbb.com", "profilePicture":"user1.png"}
        }
#------#





#---backend server---#


#token
@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(userInfo, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



#main page
@app.get("/") #must read header and check user
async def index():
    return "main page"


#login page html show
@app.get("/login", response_class=HTMLResponse) #login page
async def login(request:Request):
    return templets.TemplateResponse("index.html", {"request":request})

"""
#string login processing page [not secured] [Do not use.]
@app.post("/loginProcess") 
def loginProcess(username: str=Form(...), password: str=Form(...)):
    if username in userIdData: #must be change to hash!!!!!!!!!!!
        if password == userIdData[username]:
            print(f"{username} login sucess.")
            return f"{username} login sucess." #should input jwt to header
        else:
            print(f"{username} login failed. (password incorrect)")
            return f"{username} login failed. (password incorrect)" #just alert in page
    else:
        print(f"{username} dose not exist in DB.")
        return f"{username} dose not exist in DB." #just alert in page
"""

#token login processing, return token
@app.post("/loginProcess", response_model=Token)
async def login_to_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(userInfo, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    print(f"[{datetime.utcnow()}] {form_data.username} logined")
    return {"access_token": access_token, "token_type": "bearer"} #acces_token must input to header



@app.get("/register", response_class=HTMLResponse)
async def register(request:Request):
    return templets.TemplateResponse("register.html", {"request":request})

@app.post("/registerProcess")
async def registerPrecess(username:str = Form(...), password:str = Form(...), email:str = Form(...)):
    userInfo[username] = {"userType":"user", "username":username,  "hashed_password":get_password_hash(password),"email":email, "profilePicture":username+".png"}
    print(f"[{datetime.utcnow()}] {username} register sucess")
    return f"{username} register sucess"






#404 page
@app.get("/{item_id}") 
async def error():
    return "404 not found"
#------#


