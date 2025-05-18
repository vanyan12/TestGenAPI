
import random
import Data
from TestClass import Test
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
import uuid
from db import connect_to_db
from Functions import hash_password, verify_password


app = FastAPI()
pdf = None


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

class PersonalData(BaseModel):
    name: str
    surname: str
    email: str
    password: str

class LoginData(BaseModel):
    email: str
    password: str

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

@app.post("/signup")
async def signup(user_personal_data: PersonalData):
    name = user_personal_data.name
    surname = user_personal_data.surname
    email = user_personal_data.email
    password = user_personal_data.password

    # Connect to the database
    connection = connect_to_db()
    cursor = connection.cursor()

    # Check if the email already exists
    cursor.execute("SELECT COUNT(*) FROM users WHERE email = ?", email)
    count = cursor.fetchone()[0]
    if count > 0:
        print("Email already exists")
        return {"message": "Email already exists",
                "code": 1}

    try:

        # Insert the new user into the database
        cursor.execute("INSERT INTO users (fname, lname, email, password) VALUES (?, ?, ?, ?)", name, surname, email, hash_password(password))
        connection.commit()

        if cursor.rowcount > 0:
            return {"message": "User registered successfully",
                    "code": 0}
        else :
            return {"message": "User registration failed",
                    "code": -1}

    except Exception as e:
        print(f"Error: {e}")

    finally:
        cursor.close()
        connection.close()

@app.post("/login")
async def login(user_personal_data: LoginData):
    email = user_personal_data.email
    password = user_personal_data.password

    # Connect to the database
    connection = connect_to_db()
    cursor = connection.cursor()

    try:
        # Check if the email exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE email = ?", email)
        count = cursor.fetchone()[0]
        if count == 0:
            return {"message": "Email not found",
                    "code": -1}

        cursor.execute("SELECT password FROM users WHERE email = ?", email)
        result = cursor.fetchone()[0]

        if verify_password(password, result):

            cursor.execute("SELECT fname, lname FROM users WHERE email = ?", email)
            user = cursor.fetchone()

            print(f"{user[0]} {user[1]}")

            return {"message": f"{user[0]} {user[1]}",
                    "code": 0}
        else:
            return {"message": "Invalid password",
                    "code": -1}

    except Exception as e:
        print(f"Error: {e}")
        return {"message": "An error occurred",
                "code": -1}
    finally:
        cursor.close()
        connection.close()