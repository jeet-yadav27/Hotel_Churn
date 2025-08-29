import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml, load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)


class DataProcessor:

    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir

        self.config = read_yaml(config_path)

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)

    def preprocess_data(self, df):
        try:
            logger.info("Starting Data Processing step")

            # Drop unnecessary columns
            df.drop(columns=[c for c in ['Unnamed: 0', 'Booking_ID'] if c in df.columns],
                    inplace=True, errors='ignore')
            df.drop_duplicates(inplace=True)

            cat_cols = self.config["data_processing"]["categorical_columns"]
            num_cols = self.config["data_processing"]["numerical_columns"]

            # Label Encoding
            logger.info("Applying Label Encoding")
            label_encoder = LabelEncoder()
            mappings = {}

            for col in cat_cols:
                if col in df.columns:
                    df[col] = label_encoder.fit_transform(df[col].astype(str))
                    mappings[col] = {label: code for label, code in zip(label_encoder.classes_,
                                                                      label_encoder.transform(label_encoder.classes_))}

            for col, mapping in mappings.items():
                logger.info(f"{col} : {mapping}")

            # Handle skewness
            logger.info("Handling Skewness")
            skew_threshold = self.config["data_processing"]["skewness_threshold"]
            skewness = df[num_cols].apply(lambda x: x.skew())

            for column in skewness[skewness > skew_threshold].index:
                df[column] = np.log1p(df[column])

            return df

        except Exception as e:
            logger.error(f"Error during preprocess step {e}")
            raise CustomException("Error while preprocessing data", e)

    def balance_data(self, df):
        """Apply SMOTE only on training set"""
        try:
            logger.info("Handling Imbalanced Data (SMOTE)")
            X = df.drop(columns='booking_status')
            y = df["booking_status"]

            smote = SMOTE(random_state=42)
            X_resampled, y_resampled = smote.fit_resample(X, y)

            balanced_df = pd.DataFrame(X_resampled, columns=X.columns)
            balanced_df["booking_status"] = y_resampled

            logger.info("Data balanced successfully")
            return balanced_df

        except Exception as e:
            logger.error(f"Error during balancing data step {e}")
            raise CustomException("Error while balancing data", e)

    def select_features(self, df):
        try:
            logger.info("Starting Feature selection step")

            X = df.drop(columns='booking_status')
            y = df["booking_status"]

            model = RandomForestClassifier(random_state=42)
            model.fit(X, y)

            feature_importance = model.feature_importances_
            feature_importance_df = pd.DataFrame({
                'feature': X.columns,
                'importance': feature_importance
            })

            top_features_df = feature_importance_df.sort_values(by="importance", ascending=False)
            num_features_to_select = self.config["data_processing"]["no_of_features"]

            selected_features = top_features_df["feature"].head(num_features_to_select).values
            logger.info(f"Features selected: {selected_features}")

            selected_df = df[list(selected_features) + ["booking_status"]]

            logger.info("Feature selection completed successfully")
            return selected_df

        except Exception as e:
            logger.error(f"Error during feature selection step {e}")
            raise CustomException("Error while feature selection", e)

    def save_data(self, df, file_path):
        try:
            logger.info("Saving processed data")
            df.to_csv(file_path, index=False)
            logger.info(f"Data saved successfully to {file_path}")

        except Exception as e:
            logger.error(f"Error during saving data step {e}")
            raise CustomException("Error while saving data", e)

    def process(self):
        try:
            logger.info("Loading data from RAW directory")

            # Load
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            # Preprocess
            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)

            # Balance ONLY train
            train_df = self.balance_data(train_df)

            # Feature selection on train
            train_df = self.select_features(train_df)

            # Align test features with train
            test_df = test_df.reindex(columns=train_df.columns, fill_value=0)

            # Save
            self.save_data(train_df, PROCESSED_TRAIN_DATA_PATH)
            self.save_data(test_df, PROCESSED_TEST_DATA_PATH)

            logger.info("Data processing pipeline completed successfully")

        except Exception as e:
            logger.error(f"Error during preprocessing pipeline {e}")
            raise CustomException("Error in full data preprocessing pipeline", e)


if __name__ == "__main__":
    processor = DataProcessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    processor.process()
