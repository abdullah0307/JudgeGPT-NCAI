# FROM python:3.12-slim

# # Set working directory
# WORKDIR /app

# # Install dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy all app files
# COPY . .

# # Streamlit will run on port 8080 for Cloud Run
# EXPOSE 8080

# # Run Streamlit app
# CMD ["streamlit", "run", "main.py", "--server.port=8080", "--server.address=0.0.0.0"]



FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies including Poppler
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app files
COPY . .

# Streamlit will run on port 8080 for Cloud Run
EXPOSE 8080

# Run Streamlit app
CMD ["streamlit", "run", "main.py", "--server.port=8080", "--server.address=0.0.0.0"]
