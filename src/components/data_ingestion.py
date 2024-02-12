import pandas as pd
import sys
import os
from src.logger import logging as log
from src.exception import CustomException
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
# Import the csv files and store it as a dataframe

@dataclass
class DataIngestionConfig:
    train_data_path = os.path.join('Artifacts', 'train.csv')
    test_data_path = os.path.join('Artifacts', 'test.csv')
    raw_data_path = os.path.join('Artifacts', 'raw.csv')


class DataIngestion:

    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    # function to read a csv file
    def initiate_data_ingestion (self,file_path):
        log.info("Starting data ingestion method.")
        try:
            log.info("Now reading input csv files into a dataframe.")
            data_source = pd.read_csv(file_path)
            log.info("csv file SUCCESSFULLY read as a df.")

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)
            log.info("Directory creation was SUCCESSFUL.")

            train_data, test_data = train_test_split(data_source, random_state=42, test_size=0.3)

            train_data.to_csv(self.ingestion_config.train_data_path)
            test_data.to_csv(self.ingestion_config.test_data_path)
            # log.info("Directory creation was SUCCESSFUL.")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            log.info(CustomException(e, sys))
            raise CustomException(e, sys)
        


