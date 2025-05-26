import re, os
from passlib.context import CryptContext
from google.cloud import storage
from fastapi import Request, HTTPException
from jose import JWTError, jwt
import json
from db import connect_to_db


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Functions for JWT token handling
SECRET_KEY = "van40k"
ALGORITHM = "HS256"

def T_F_to_str(str):
    return "Ճիշտ" if str == "1" else "Սխալ"

def str_for_table(answer):
    if str(type(answer)) == "<class 'int'>":
        answer = str(answer)
        return " ".join(f"{char}," for char in answer)[:-1]
    elif str(type(answer) == "<class 'list'>"):
        answer = re.sub(r"[\[\], ]", '', str(answer)) if len(answer) == 6 else re.sub(r"[\[\]]", '', str(answer))
        return answer

def rename_to_json(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):  # Check if the file is a .txt file
            txt_path = os.path.join(directory, filename)
            json_path = os.path.join(directory, filename[:-4] + ".json")  # Replace .txt with .json
            os.rename(txt_path, json_path)  # Rename file

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Optional: Function to verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

async def upload_to_cloud(bucket_name, file_path, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(file_path, content_type='application/pdf')



def decode_token(token: str) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")


        if user_id is None:
            raise HTTPException(status_code=401, detail="User ID not found in token")
        return int(user_id)

    except JWTError as e:
        print(f"JWTError: {e}") # Remove this in production
        raise HTTPException(status_code=401, detail="Invalid token")

def get_user_id_from_request(request: Request):
    token = request.cookies.get("access_token")
    print(f"Token from request: {token}")  # Debugging line, remove in production

    if not token:
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    return decode_token(token)



def check_answer(user_answers):
    user_answers = json.loads(user_answers.json())
    grade = 0

    answers = user_answers["data"]

    # Get the correct answers from the database
    connection = connect_to_db()
    cursor = connection.cursor()

    # Fetch the correct answers for the test
    cursor.execute("SELECT test_answer FROM test_scores WHERE test_url = ?", user_answers["test"])
    result = cursor.fetchone()[0]
    correct_answers = json.loads(result)

    for variant in answers:
        if answers[variant] == correct_answers[variant]:
            grade += 1

    # Update the score in the database
    cursor.execute("UPDATE test_scores SET score = ? WHERE test_url = ?", (grade, user_answers["test"]))
    cursor.commit()

    cursor.close()
    connection.close()

    return grade