# Use lightweight Python
FROM python:3.10-slim

# Avoid .pyc files, unbuffer output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System dependencies for LightGBM
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy package and setup files
COPY setup.py setup.py
COPY src/ src/
COPY artifacts/models/lgbm_model.pkl artifacts/models/lgbm_model.pkl

# Install your package in editable mode
RUN pip install --no-cache-dir -e .

# Copy Flask app
COPY application.py .

# Expose Cloud Run port
EXPOSE 8080

# Start Flask app
CMD ["python", "application.py"]
