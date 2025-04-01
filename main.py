
import random
from Functions import *
import Data
from TestClass import Test
from fastapi import FastAPI, Depends, HTTPException, Request, Response
from pydantic import BaseModel
from pylatex import Command, Document, Section, Subsection
from pylatex.utils import NoEscape, italic
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from itsdangerous import URLSafeTimedSerializer
from typing import Optional
import hashlib
import uuid
from db import cursor


app = FastAPI()
pdf = None

SECRET_KEY = "van40k"
serializer = URLSafeTimedSerializer(SECRET_KEY)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

fake_db = {
    "testuser": {
        "username": "testuser",
        "password": hash_password("password123"),
        "user_id": str(uuid.uuid4())
    }
}




def get_current_user(request: Request):
    session_token = request.cookies.get("session")

    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        session_data = serializer.loads(session_token, max_age=3600)  # max_age = 1 hour
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid session")

    user_id =  session_data["user_id"]

    user = next((u for u in fake_db.values() if u["user_id"] == user_id), None)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid session")

    return user


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/pdfs", StaticFiles(directory="./Tests"), name="pdfs")


class Answer(BaseModel):
    data: dict[str, str | None]

@app.post("/signup")
async def signup(form_data: OAuth2PasswordRequestForm = Depends()):


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Find the user in the fake database
    # user = fake_db.get()
    user = cursor.execute(
        "SELECT * FROM users WHERE username = ?", (f"{form_data.username}",)
    )


    if not user or user["password"] != hash_password(form_data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # If authentication is successful, create a session cookie
    session_data = {"user_id": user["user_id"]}
    session_token = serializer.dumps(session_data)

    # Set the session cookie (with HttpOnly, Secure, and SameSite flags for security)
    response = HTMLResponse(content="Login successful")
    response.set_cookie(key="session", value=session_token, httponly=True, secure=True, samesite="strict")



    return response


@app.get("/profile")
async def profile(current_user: str = Depends(get_current_user)):
    return {"message": f"Welcome {current_user}!"}

@app.post("/logout")
async def logout(response: Response):
    # Remove the session cookie
    response.delete_cookie("session")
    return {"message": "Logged out successfully"}


@app.get("/pdf")
async def root():
    Sections = Data.Faculties["manual"]

    Count = [Data.Database[sec] for sec in Sections]

    Randoms = [random.randint(1, Count[Sections.index(sec)]) for sec in Sections]

    Tasks = list(zip(Sections, Randoms))
    print(Tasks)

    global pdf
    pdf = Test()

    for section, task_n in Tasks:
        file = f"./Texts/{section}/{section}-{task_n}.json"

        pdf.define_task_type(file)(file)

        pdf.get_answer(section, task_n)

    print(pdf.answers)



    path_for_test = f"./Tests/{uuid.uuid4()}-math_test"

    pdf.generate_pdf(path_for_test, compiler="xelatex", clean_tex=True)

    # # Convert relative path to absolute
    # pdf_path = os.path.abspath(path_for_test)

    return {
        "task-count": pdf.task_counter-1,
        "answer-type-template": pdf.answers_input_template,
        "pdf-path": f"{path_for_test}.pdf"
    }

    #return FileResponse(path=pdf_path, media_type="application/pdf", filename="Math_test.pdf")

@app.get("/pdf/{filename:path}")
async def pdf(filename: str):
    return FileResponse(path=filename, media_type="application/pdf")

@app.post("/check")
async def check(user_answer: Answer):
    score = pdf.check_answer(user_answer)
    return {"score": score}