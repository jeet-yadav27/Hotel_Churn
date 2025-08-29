# Hotel Churn Prediction 🚀

A Machine Learning project to predict hotel reservation cancellations. The project uses Python, LightGBM, Flask, and can be deployed on **Google Cloud Run** via **Docker** and **Jenkins CI/CD**.

---

## Features

- Data ingestion from **Google Cloud Storage**
- Data preprocessing:
  - Label encoding
  - Handling skewness
  - Feature selection using Random Forest
  - Balancing dataset using SMOTE
- LightGBM model training
- Flask web app for real-time prediction
- Containerized using **Docker**
- Deployment to **Google Cloud Run**
- Automated pipeline using **Jenkins**

---

## Project Structure

Hotel_Churn/
├── application.py # Flask app
├── pipeline/
│ └── training_pipeline.py # Data ingestion + preprocessing + model training
├── src/
│ ├── data_ingestion.py # Download CSV & split data
│ ├── data_processor.py # Data preprocessing & feature selection
│ ├── custom_exception.py
│ └── logger.py
├── config/
│ └── config.yaml # Configuration file
├── artifacts/ # Raw/processed data, models
├── Dockerfile # Docker setup
├── Jenkinsfile # Jenkins CI/CD pipeline
└── templates/
└── index.html # Flask frontend



---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/jeet-yadav27/Hotel_Churn.git
cd Hotel_Churn


2. Create a virtual environment and install dependencies:

python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -e .


3. Add your GCP service account key (for data ingestion):
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/gcp-key.json"


Configuration

Edit config/config.yaml to update:

GCP bucket name and file path

Train/test split ratio

Columns for preprocessing


Running Locally

1. Run the training pipeline:
