FROM base:latest

# Set working directory to /app
WORKDIR /app

# Copy your application files into the container
#COPY . /app

# Expose port 8000 (FastAPI default port)
EXPOSE 8000

# Command to run the application using Uvicorn (FastAPI)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
