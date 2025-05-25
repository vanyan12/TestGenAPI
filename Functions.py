import re, os
from passlib.context import CryptContext
from google.cloud import storage
from fastapi import Request, HTTPException
from jose import JWTError, jwt


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
        print(f"JWTError: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")
def get_user_id_from_request(request: Request):
    auth_header = request.headers.get("authorization")

    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")

    token = auth_header[len("Bearer "):] if auth_header.startswith("Bearer ") else auth_header
    return decode_token(token)

# Function to hash password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Optional: Function to verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)