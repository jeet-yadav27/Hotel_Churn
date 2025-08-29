import os

# Get project root (2 levels up from this file)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

########################### DATA INGESTION #########################

RAW_DIR = os.path.join(PROJECT_ROOT, "artifacts", "raw")
RAW_FILE_PATH = os.path.join(RAW_DIR, "raw.csv")
TRAIN_FILE_PATH = os.path.join(RAW_DIR, "train.csv")
TEST_FILE_PATH = os.path.join(RAW_DIR, "test.csv")

CONFIG_PATH = os.path.join(PROJECT_ROOT, "config", "config.yaml")

######################## DATA PROCESSING ########################

PROCESSED_DIR = os.path.join(PROJECT_ROOT, "artifacts", "processed")
PROCESSED_TRAIN_DATA_PATH = os.path.join(PROCESSED_DIR, "processed_train.csv")
PROCESSED_TEST_DATA_PATH = os.path.join(PROCESSED_DIR, "processed_test.csv")

####################### MODEL TRAINING ########################

MODEL_DIR = os.path.join(PROJECT_ROOT, "artifacts", "models")
MODEL_OUTPUT_PATH = os.path.join(MODEL_DIR, "lgbm_model.pkl")

####################### ENSURE DIRECTORIES #####################

# Create all directories safely
for path in [RAW_DIR, PROCESSED_DIR, MODEL_DIR]:
    os.makedirs(path, exist_ok=True)
