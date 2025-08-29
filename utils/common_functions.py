import os
import pandas as pd
import yaml
from src.logger import get_logger
from src.custom_exception import CustomException

logger = get_logger(__name__)

def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found at path: {file_path}")
        
        with open(file_path, "r") as yaml_file:
            config = yaml.safe_load(yaml_file)
            logger.info("Successfully read the YAML file")
            return config

    except Exception as e:
        logger.error(f"Error while reading YAML file: {e}")
        raise CustomException("Failed to read YAML file", e)

def load_data(path):
    try:
        logger.info(f"Loading data from {path}")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Data file not found at path: {path}")
        return pd.read_csv(path)
    except Exception as e:
        logger.error(f"Error loading the data from {path}: {e}")
        raise CustomException("Failed to load data", e)

if __name__ == "__main__":
    config = read_yaml("config.yaml")
    print(config)