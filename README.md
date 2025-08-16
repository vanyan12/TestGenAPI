# TestGenAPI

TestGenAPI is a robust backend service built with FastAPI for automated generation, delivery, and evaluation of mathematics tests. Designed to support educational platforms, it streamlines test creation, secure delivery in PDF format, automated answer checking, and user management. The project demonstrates modern backend engineering practices, integration with cloud services, and secure user authentication.

## Features

- **Automated Test Generation:** Generates randomized math tests based on user criteria and delivers them as PDF files.
- **PDF Delivery & Cloud Storage:** Test PDFs are generated on-the-fly and stored in Google Cloud Storage for secure, scalable access.
- **User Authentication & Management:** Secure signup, login, and session management using JWT tokens and hashed passwords.
- **Automated Answer Checking:** Submissions are checked automatically and scores are stored securely.
- **User Test History:** Retrieves lists of previous user tests along with scores and timestamps.
- **Feedback Handling:** Supports user feedback submission, routed to administrators.
- **Rate Limiting:** Users can generate new tests at controlled intervals.
- **RESTful API Design:** Modern API endpoints for integration with frontend applications or other services.

## Main Endpoints

- `POST /signup` – Register a new user
- `POST /login` – Authenticate user and provide access token
- `GET /auth-check` – Verify authentication status
- `GET /pdf` – Generate a test as PDF
- `GET /get-test/{file_name}` – Stream a specific test PDF
- `POST /check` – Submit answers for automated grading
- `GET /testsList` – Get a user's test history
- `GET /can-generate` – Check if new test generation is allowed
- `POST /send-feedback` – Submit user feedback

## Technologies Used

- **Python 3**
- **FastAPI**
- **Google Cloud Storage**
- **SQL Server**
- **JWT Authentication**
- **Docker**

## Usage

1. **Clone the repository**  
   ```
   git clone https://github.com/vanyan12/TestGenAPI.git
   ```

2. **Install dependencies**  
   ```
   pip install -r requirements.txt
   ```

3. **Configure environment variables**  
   - Set up Google Cloud credentials and other required `.env` variables.

4. **Run the application**  
   ```
   uvicorn main:app --reload
   ```


## Project Highlights

- Secure, token-based authentication for all user operations.
- Randomized test content ensures unique, fair assessments.
- Cloud integration for scalable and secure file storage.
- Extensible and maintainable codebase following modern Python and FastAPI best practices.

## License

This project is private and all rights are reserved by the author.

---

For more details, visit the [repository](https://github.com/vanyan12/TestGenAPI).
