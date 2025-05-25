
import random
import Data
from TestClass import Test
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse, StreamingResponse
import uuid, os, io, tempfile
from db import connect_to_db
from auth import create_access_token, verify_token, get_current_user
import Functions as f
from google.cloud import storage


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../key.json"

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

class User(BaseModel):
    id: int
    fname: str
    lname: str
    email: str
    created_at: str

class Answer(BaseModel):
    data: dict[str, str | None]
    user: User
    test: str

class PersonalData(BaseModel):
    name: str
    surname: str
    email: str
    password: str

class LoginData(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    code: int


@app.get("/pdf")
async def root(user_id=Depends(f.get_user_id_from_request)):
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

    test_id = uuid.uuid4()
    bucket_name = "test-gen-pdfs"
    destination_blob_name = f"{user_id}/{test_id}-math-test.pdf"

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file_name = os.path.splitext(temp_file.name)[0]
        temp_file_path = temp_file.name

    # Generate the PDF and save it to the temporary file
    pdf.generate_pdf(temp_file_name, compiler="xelatex", clean_tex=True)

    # Upload the file to cloud storage using the file path
    await f.upload_to_cloud(bucket_name, temp_file_path, destination_blob_name)

    # Clean up the temporary file
    os.remove(temp_file_path)

    return {
        "task-count": pdf.task_counter-1,
        "answer-type-template": pdf.answers_input_template,
        "pdf-path": f"{test_id}-math-test.pdf",
        "test-id": test_id
    }

@app.post("/check")
async def check(user_answer: Answer):
    score = pdf.check_answer(user_answer)

    connection = connect_to_db()
    cursor = connection.cursor()


    try:
    # Insert the new user into the database
        cursor.execute("INSERT INTO test_scores (user_id, test_url, score) VALUES (?, ?, ?)", (user_answer.user.id, user_answer.test, score))
        connection.commit()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

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
        cursor.execute("INSERT INTO users (fname, lname, email, password) VALUES (?, ?, ?, ?)", name, surname, email, f.hash_password(password))
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


@app.post("/login", response_model=Token)
async def login(user_personal_data: LoginData):
    email = user_personal_data.email
    password = user_personal_data.password

    # Connect to the database
    connection = connect_to_db()
    cursor = connection.cursor()

    try:
        # Check if the email exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE email = ?", (email,))
        count = cursor.fetchone()[0]
        if count == 0:
            return {"message": "Email not found",
                    "code": -1}

        cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
        result = cursor.fetchone()[0]

        if f.verify_password(password, result):

            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()

            token = create_access_token(data={"sub": str(user.id), "fname": user.fname, "lname": user.lname}, expires_delta=30)

            return {
                "access_token": token,
                "token_type": "bearer",
                "code": 0
            }

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

@app.get("/testsList")
async def get_user_tests(user_id: int, page: int = 0, page_size: int = 10):
    # Connect to the database
    connection = connect_to_db()
    cursor = connection.cursor()

    try:
        sql_command = """
            SELECT test_url, test_date, score 
            FROM test_scores WHERE user_id = ?
            ORDER BY test_date 
            OFFSET ? ROWS
            FETCH NEXT ? ROWS ONLY
        """

        params = (user_id, page * page_size, page_size)
        cursor.execute(sql_command, params)
        tests = cursor.fetchall()

        # Convert the results to a list of dictionaries
        coloumns = [cols[0] for cols in cursor.description]
        tests = [dict(zip(coloumns, row)) for row in tests]

        cursor.execute("SELECT COUNT(*) FROM test_scores WHERE user_id = ?", (user_id,))
        total_count = cursor.fetchone()[0]



        return {"tests": tests, "totalCount": total_count}

    except Exception as e:
        print(f"Error: {e}")

    finally:
        cursor.close()
        connection.close()

@app.get("/get-test/{file_name:str}")
async def get_test(file_name: str, user_id: int = Depends(get_current_user)):
    try:
        bucket_name = "test-gen-pdfs"
        blob_path = f"{user_id}/{file_name}"  # Adjust path logic as needed

        client = storage.Client()
        bucket = client.bucket(bucket_name)
        print(blob_path)
        blob = bucket.blob(blob_path)

        if not blob.exists():
            raise HTTPException(status_code=404, detail="File not found")

        pdf_bytes = blob.download_as_bytes()
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": "inline; filename=test.pdf"}

        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



