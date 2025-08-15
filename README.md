# TestGenAPI

A Python FastAPI application for automated mathematical test generation, user authentication, and result management. The system generates customized PDF tests with Armenian language support, manages user authentication through JWT tokens, and stores files using Google Cloud Storage.

## Project Overview

TestGenAPI is designed for educational institutions to automatically generate mathematical tests in PDF format. The application supports multiple test sections covering various mathematical topics, provides user authentication and authorization, and maintains test history with scoring capabilities.

### Key Features

- **Automated Test Generation**: Creates randomized mathematical tests from predefined question banks
- **PDF Generation**: Uses PyLaTeX to generate professionally formatted PDF tests with Armenian font support
- **User Authentication**: JWT-based authentication system with secure password hashing
- **Cloud Storage**: Integration with Google Cloud Storage for PDF file management
- **Answer Checking**: Automated scoring system for submitted test answers
- **Test Management**: Track test history and scores for individual users
- **Multi-Faculty Support**: Different test configurations for various academic programs (IMA, KFM, manual)
- **CORS Support**: Frontend integration ready with configurable CORS settings

## Technology Stack

### Backend Framework
- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation and settings management using Python type annotations
- **Starlette**: ASGI framework for high-performance async applications

### Authentication & Security
- **JWT (JSON Web Tokens)**: Token-based authentication using `python-jose`
- **Passlib**: Password hashing with bcrypt
- **OAuth2**: Standard authentication flow implementation

### PDF Generation
- **PyLaTeX**: Python library for generating LaTeX documents and PDFs
- **XeLaTeX**: LaTeX engine for proper Unicode and Armenian font rendering

### Database & Storage
- **SQL Server**: Primary database using `pyodbc` driver
- **Google Cloud Storage**: Cloud-based file storage for generated PDFs

### Additional Libraries
- **Requests**: HTTP library for external API calls
- **PyTZ**: Timezone handling for date/time operations

## Setup Instructions

### Prerequisites

1. **Python 3.12** or higher
2. **SQL Server** instance (local or cloud)
3. **Google Cloud Project** with Storage API enabled
4. **LaTeX distribution** with XeLaTeX support (for PDF generation)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/vanyan12/TestGenAPI.git
   cd TestGenAPI
   ```

2. **Install dependencies**:
   ```bash
   pip install fastapi uvicorn
   pip install pylatex
   pip install google-cloud-storage
   pip install pyodbc
   pip install python-jose[cryptography]
   pip install passlib[bcrypt]
   pip install pydantic[email]
   pip install python-multipart
   pip install requests
   pip install pytz
   ```

3. **Configure Google Cloud Storage**:
   - Create a service account in your Google Cloud Project
   - Download the service account key file
   - Place the key file as `../key.json` relative to the project root
   - Update the `GOOGLE_APPLICATION_CREDENTIALS` environment variable in `main.py`

4. **Configure Database**:
   - Update the connection string in `db.py` with your SQL Server details
   - Ensure the database has the required tables:
     - `users` (for user management)
     - `test_scores` (for test results)

5. **Install LaTeX distribution**:
   - **Ubuntu/Debian**: `sudo apt-get install texlive-xetex`
   - **macOS**: Install MacTeX
   - **Windows**: Install MiKTeX or TeX Live

6. **Add Armenian fonts**:
   - Install the GHEAMariam font family (files in `/Fonts` directory)
   - Ensure fonts are accessible to the LaTeX engine

### Running the Application

1. **Development server**:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Production server**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication

#### POST `/signup`
Register a new user account.

**Request Body**:
```json
{
  "name": "John",
  "surname": "Doe",
  "email": "john.doe@example.com",
  "password": "securepassword"
}
```

#### POST `/login`
Authenticate user and receive access token.

**Request Body**:
```json
{
  "email": "john.doe@example.com",
  "password": "securepassword"
}
```

**Response**: Sets HTTP-only cookie with JWT token.

#### GET `/auth-check`
Verify user authentication status.

**Headers**: Requires authentication cookie.

### Test Generation

#### GET `/pdf`
Generate a new randomized test PDF.

**Headers**: Requires authentication cookie.

**Response**:
```json
{
  "task-count": 15,
  "answer-type-template": {"0": "choose", "1": "input", ...},
  "pdf-path": "uuid-math-test.pdf",
  "test-id": "uuid"
}
```

#### GET `/get-test/{file_name}`
Download a previously generated test PDF.

**Parameters**:
- `file_name`: Name of the PDF file to download

**Headers**: Requires authentication cookie.

### Answer Submission

#### POST `/check`
Submit test answers for scoring.

**Request Body**:
```json
{
  "data": {
    "0": "answer1",
    "1": "answer2",
    ...
  },
  "test": "path/to/test.pdf"
}
```

**Response**:
```json
{
  "score": 12
}
```

### Test History

#### GET `/testsList`
Retrieve user's test history with pagination.

**Query Parameters**:
- `user_id`: User identifier
- `page`: Page number (default: 0)
- `page_size`: Items per page (default: 10)

## Usage Examples

### Basic Test Generation Flow

1. **Register a user**:
   ```bash
   curl -X POST "http://localhost:8000/signup" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Student",
       "surname": "Name",
       "email": "student@example.com",
       "password": "password123"
     }'
   ```

2. **Login**:
   ```bash
   curl -X POST "http://localhost:8000/login" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "student@example.com",
       "password": "password123"
     }' \
     -c cookies.txt
   ```

3. **Generate a test**:
   ```bash
   curl -X GET "http://localhost:8000/pdf" \
     -b cookies.txt
   ```

4. **Download the test**:
   ```bash
   curl -X GET "http://localhost:8000/get-test/uuid-math-test.pdf" \
     -b cookies.txt \
     -o test.pdf
   ```

5. **Submit answers**:
   ```bash
   curl -X POST "http://localhost:8000/check" \
     -H "Content-Type: application/json" \
     -b cookies.txt \
     -d '{
       "data": {"0": "1", "1": "42", "2": "3"},
       "test": "user_id/uuid-math-test.pdf"
     }'
   ```

## Test Structure

### Question Sections

The system supports multiple mathematical sections:

- **Section1-10**: Basic mathematical operations and problems
- **2Section1-8**: Advanced mathematical concepts
- **3Section1,2,4**: True/False mathematical statements

### Faculty Configurations

- **IMA**: Information, Mathematics, and Applications program
- **KFM**: Physical and Mathematical Faculty program  
- **Manual**: Custom test configuration

### Question Types

1. **Multiple Choice** (`choose`): Questions with 4 or 6 options
2. **Input** (`input`): Questions requiring numerical or text answers
3. **True/False**: Binary choice questions (for 3Section* categories)

## Development Notes

### Project Structure

```
TestGenAPI/
├── main.py              # FastAPI application and routes
├── TestClass.py         # PDF generation using PyLaTeX
├── Functions.py         # Utility functions
├── auth.py             # Authentication utilities
├── db.py               # Database connection
├── Data.py             # Test configuration and metadata
├── Answers.py          # Answer keys for all test sections
├── Fonts/              # Armenian font files
├── Texts/              # Question bank JSON files
└── .github/workflows/  # CI/CD configuration
```

### Adding New Questions

1. Create JSON files in the appropriate `Texts/{section}/` directory
2. Follow the existing JSON structure:
   ```json
   {
     "requirement": "Instructions in Armenian",
     "data": {
       "1": "Question 1 text",
       "2": "Question 2 text"
     }
   }
   ```
3. Update corresponding answers in `Answers.py`
4. Update question count in `Data.py` if needed

### Security Considerations

- JWT tokens expire after 60 minutes (configurable in `auth.py`)
- Passwords are hashed using bcrypt
- CORS is configured for `http://localhost:5173` (update for production)
- Google Cloud credentials should be secured and not committed to version control

### Performance Notes

- PDF generation is CPU-intensive and may take several seconds
- Files are temporarily created during PDF generation and cleaned up automatically
- Consider implementing rate limiting for production environments

## Deployment

### Azure Web App

The project includes GitHub Actions workflow for automatic deployment to Azure Web App:

1. Configure Azure Web App service
2. Set up the following GitHub secrets:
   - `AZURE_CREDENTIALS`: Azure service principal credentials
   - `AZURE_WEBAPP_PUBLISH_PROFILE`: Web App publish profile
3. Update `AZURE_WEBAPP_NAME` in `.github/workflows/azure-webapps-python.yml`

### Environment Variables

For production deployment, configure:

- Database connection strings
- Google Cloud Storage credentials
- JWT secret key
- CORS origins
- LaTeX/XeLaTeX binary paths

### Database Schema

Ensure the following tables exist:

```sql
-- Users table
CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100),
    surname NVARCHAR(100),
    email NVARCHAR(255) UNIQUE,
    password_hash NVARCHAR(255),
    created_at DATETIME DEFAULT GETDATE()
);

-- Test scores table  
CREATE TABLE test_scores (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT,
    test_url NVARCHAR(500),
    test_answer NTEXT,
    score INT,
    created_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit a pull request

## License

This project is developed for educational purposes. Please ensure compliance with your institution's policies when using or modifying this software.