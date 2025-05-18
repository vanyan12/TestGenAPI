import re, os
from passlib.context import CryptContext

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


# Create a context with bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Optional: Function to verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)