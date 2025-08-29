import os
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self,config):
        self.config = config["data_ingestion"]
        print(self.config)
        self.bucket_name = self.config["bucket_name"]
        self.file_name = self.config["bucket_file_name"]
        self.train_test_ratio = self.config["train_ratio"]

        os.makedirs(RAW_DIR , exist_ok=True)

        logger.info(f"Data Ingestion started with {self.bucket_name} and file is  {self.file_name}")

    def download_csv_from_gcp(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)

            blob.download_to_filename(RAW_FILE_PATH)

            logger.info(f"CSV file is sucesfully downloaded to {RAW_FILE_PATH}")

        except Exception as e:
            logger.error("Error while downloading the csv file")
            raise CustomException("Failed to downlaod csv file ", e)
        
    def split_data(self):
        try:
            logger.info("Starting the splitting process")
            if not os.path.exists(RAW_FILE_PATH):
                raise FileNotFoundError(f"Raw file not found at {os.path.abspath(RAW_FILE_PATH)}")

            data = pd.read_csv(RAW_FILE_PATH)
            train_data, test_data = train_test_split(
                data, test_size=1 - self.train_test_ratio, random_state=42
            )

            os.makedirs(os.path.dirname(TRAIN_FILE_PATH), exist_ok=True)
            os.makedirs(os.path.dirname(TEST_FILE_PATH), exist_ok=True)

            train_data.to_csv(TRAIN_FILE_PATH, index=False)
            test_data.to_csv(TEST_FILE_PATH, index=False)

            logger.info(f"Train data saved to {os.path.abspath(TRAIN_FILE_PATH)}")
            logger.info(f"Test data saved to {os.path.abspath(TEST_FILE_PATH)}")

        except Exception as e:
            logger.error("Error while splitting data")
            import sys
            raise CustomException("Failed to split data into training and test sets", sys)
            
    def run(self):

        try:
            logger.info("Starting data ingestion process")

            self.download_csv_from_gcp()
            self.split_data()

            logger.info("Data ingestion completed sucesfully")
        
        except CustomException as ce:
            logger.error(f"CustomException : {str(ce)}")
        
        finally:
            logger.info("Data ingestion completed")

if __name__ == "__main__":
    print(CONFIG_PATH)
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()





