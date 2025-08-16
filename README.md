# TestGenAPI

**TestGenAPI** is a robust backend solution for automated mathematical test generation, user management, and results processing. Built using modern Python tools, it delivers configurable Armenian-language PDF tests, secure authentication, and cloud storage integration.

---

## Key Technologies & Skills

- **Python 3.12+** – Core backend language
- **FastAPI** – High-performance API framework
- **Pydantic** – Data validation
- **SQL Server (pyodbc)** – Relational database integration
- **Google Cloud Storage** – Scalable file storage for generated PDFs
- **PyLaTeX & XeLaTeX** – Dynamic PDF generation with Unicode/font support
- **JWT, OAuth2, Passlib** – Secure authentication and password hashing
- **Starlette** – Async web toolkit for scalable applications
- **CI/CD (GitHub Actions)** – Automated deployment to Azure

---

## Features

- **Automated test generation** from configurable question banks
- **PDF export** with Armenian Unicode support
- **JWT-secured user registration and login**
- **Cloud-based file management** for PDFs
- **Automated answer checking and scoring**
- **User test history and analytics**
- **Multiple academic program support (IMA, KFM, manual)**
- **Frontend-ready CORS configuration**

---

## Example API Endpoints

- `POST /signup` – Register user
- `POST /login` – Obtain JWT token
- `GET /pdf` – Generate new test PDF
- `POST /check` – Submit answers for scoring
- `GET /testsList` – Retrieve test history

---

## Project Highlights

- Designed and implemented a secure, scalable backend in modern Python
- Integrated cloud storage and automated PDF generation
- Applied best practices in authentication, validation, and API design
- Automated deployment pipeline for Azure cloud

---

## Setup

1. **Install Python 3.12+ and dependencies:**  
   `pip install -r requirements.txt`
2. **Configure SQL Server** and update connection string in `db.py`
3. **Set up Google Cloud Storage** and service account credentials
4. **Install XeLaTeX** and Armenian fonts for PDF generation
5. **Run server:**  
   `uvicorn main:app --reload`

---

## Professional Impact

This project demonstrates expertise in backend Python development, REST API design, authentication, cloud integration, and modern deployment. It reflects practical skills ready for real-world backend engineering roles.