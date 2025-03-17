# Use the official Python 3.12 slim image as base
FROM python:3.12-slim

## Install LaTeX and necessary dependencies
# Install TeX Live full package (includes all LaTeX packages)
RUN apt-get update && apt-get install -y \
    texlive-xetex \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    texlive-lang-other \
    fontconfig \
    && rm -rf /var/lib/apt/lists/*  # Clean up

# Create directory for custom fonts and copy them into the container
COPY ./Fonts/ /usr/share/fonts/truetype/custom/

# Update font cache
RUN fc-cache -fv

# Set working directory to /app
WORKDIR /app

# Copy your application files into the container
COPY . /app

# Install Python dependencies (make sure you have requirements.txt in your project)
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 (FastAPI default port)
EXPOSE 8000

# Command to run the application using Uvicorn (FastAPI)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
