import re, os, random
from passlib.context import CryptContext
from google.cloud import storage
from fastapi import Request, HTTPException
from jose import JWTError, jwt
import json
from db import connect_to_db
from collections import defaultdict
from TestClass import Test
from Data import Database as Data


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


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = payload.get("user")


        if user is None:
            raise HTTPException(status_code=401, detail="User ID not found in token")
        return user

    except JWTError as e:
        print(f"JWTError: {e}") # Remove this in production
        raise HTTPException(status_code=401, detail="Invalid token")

def get_user_id_from_request(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")

    return decode_token(token)



def check_answer(user_answers, test_max_score, test_template):
    user_answers = json.loads(user_answers.json())
    grade = 0
    true_false_score = 0
    TF_remaining_questions = 6

    answers = user_answers["data"]

    # Get the correct answers from the database
    connection = connect_to_db()
    cursor = connection.cursor()


    # Fetch the correct answers for the test
    cursor.execute("SELECT test_answer FROM test_scores WHERE test_url = ?", (user_answers["test"],))
    result = cursor.fetchone()


    if not result:
        raise HTTPException(status_code=404, detail="Test not found")
    correct_answers = json.loads(result[0])

    for variant in answers:
        user_answer = answers[variant]
        correct_answer = correct_answers[variant]
        question_type = test_template[variant]

        if test_max_score == 120:
            if user_answer == correct_answer: # Correct answer
                if question_type == "tf":
                    true_false_score += 1.5
                    TF_remaining_questions -= 1
                elif question_type in ["choose", "input"]:
                    grade += 1.5
            elif question_type == "tf":
                if user_answer == "-1": # Unanswered question
                    TF_remaining_questions -= 1
                else: # Wrong answer for true/false question
                    true_false_score -= 1.5
                    TF_remaining_questions -= 1

        else: # For tests with max score 100
            question_num = int(variant)
            if user_answer == correct_answer: # Correct answer
                if question_num <= 10:
                    if question_type == "tf":
                        true_false_score += 1
                        TF_remaining_questions -= 1
                    else:
                        grade += 1
                else:
                    if question_type == "tf":
                        true_false_score += 1.5
                        TF_remaining_questions -= 1
                    else:
                        grade += 1.5
            elif question_type == "tf": # Wrong answer for true/false question
                if user_answer == "-1": # Unanswered question
                    TF_remaining_questions -= 1
                else:
                    true_false_score -= (1 if question_num <= 10 else 1.5)
                    TF_remaining_questions -= 1

        # After finishing the true/false block
        if TF_remaining_questions == 0:
            if true_false_score > 0:
                grade += true_false_score
            true_false_score = 0
            TF_remaining_questions = 6




    # Update the score in the database
    cursor.execute("UPDATE test_scores SET score = ? WHERE test_url = ?", (grade, user_answers["test"]))
    cursor.commit()

    cursor.close()
    connection.close()

    return grade


def generate_unique_randoms(sections, counts):
    used_values = defaultdict(set)
    randoms = []

    for section, count in zip(sections, counts):
        # Try to generate a unique random number for this section
        while True:
            r = random.randint(1, count)
            if r not in used_values[section]:
                used_values[section].add(r)
                randoms.append(r)
                break


    return randoms


def add_section_to_pdf_and_log_errors(section_name):

    log_file = 'error_log.txt'
    base_path = './Texts'
    pdf = Test()

    # Clear or create the log file
    if os.path.exists(log_file):
        os.remove(log_file)

    # Ensure the section exists in our database
    if section_name not in Data:
        raise ValueError(f"Section '{section_name}' not found in Data.")

    task_count = Data[section_name]
    error_files = []

    # Loop over the tasks in the section
    for task_num in range(1, task_count + 1):
        file_path = f'{base_path}/{section_name}/{section_name}-{task_num}.json'
        try:
            if os.path.exists(file_path):
                pdf.define_task_type(file_path)(file_path)
            else:
                raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            error_files.append(file_path)
            with open(log_file, 'a', encoding='utf-8') as log:
                log.write(f"Error in file: {file_path}\nError: {str(e)}\n\n")

    # Generate the PDF
    try:
        pdf.generate_pdf('./test', compiler='xelatex', clean_tex=True)
    except Exception as e:
        with open(log_file, 'a', encoding='utf-8') as log:
            log.write("Error during PDF generation:\n")
            log.write(f"Error: {str(e)}\n")
            if error_files:
                log.write("Files that caused errors:\n")
                for file in error_files:
                    log.write(f"- {file}\n")
            log.write("\n")


add_section_to_pdf_and_log_errors("Section8")

