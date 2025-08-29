# Use a lightweight Python image
FROM python:3.10-slim

# Prevent Python from writing .pyc files & Ensure output is not buffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (required by LightGBM)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Ensure trained model is copied (adjust path if needed)
COPY artifacts/models/lgbm_model.pkl artifacts/models/lgbm_model.pkl

# Expose Cloud Run port
EXPOSE 8080

# Start Flask app
CMD ["python", "application.py"]
