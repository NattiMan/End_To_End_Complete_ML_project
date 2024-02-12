
import os
import sys
import pandas as pd
import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from dataclasses import dataclass
from src.utils import save_object
from src.logger import logging as log
from src.exception import CustomException

@dataclass
class DataTransformationConfig:
    transformationProcessorPath = os.path.join('Artifacts', 'transformationProcessor.pkl')


class DataTransformation:
    
       
    def __init__(self, testing_data_path, numerical_columns = None, categorical_columns = None, is_testing = False,training_data_path = None):
        try:
            if (is_testing or training_data_path):
                self.dataTransformationConfig = DataTransformationConfig()
                self.numerical_columns = numerical_columns
                self.categorical_columns = categorical_columns
                self.training_data_path = training_data_path
                self.testing_data_path = testing_data_path
                self.is_testing = is_testing

            else:
                log.warn("Please enter training data path, you are not carrying out a prediction.")

        except Exception as e:
            raise CustomException(e, sys)


    def get_data_transform_object(self):
        try:            

            num_pipeline = Pipeline(
                steps = [
                    ("imputer",SimpleImputer(strategy="median")),
                    ("Scaler",StandardScaler(with_mean=False))
                    ],
                memory = './cache_directory'
            )

            cat_pipeline = Pipeline(
                steps = [
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder",OneHotEncoder()),
                    ("Scaler",StandardScaler(with_mean=False))
                    ],
                memory = './cache_directory'
            )

            preprocessor = ColumnTransformer([
                ("num_pipeline", num_pipeline, self.numerical_columns),
                ("cat_pipeline", cat_pipeline, self.categorical_columns)
            ]
            )

            return preprocessor


        except Exception as e:
            raise CustomException(e, sys)



    def initiate_data_transformation(self, target_column):
        log.info("Data transformation is initiated.")
        try:
            log.info("Creating data transformer object.")   
            preprocesing_obj = self.get_data_transform_object()
            log.info("Done creating data transformer object.")   

            log.info("Starting reading the training and testing datasets.")
            train_df = pd.read_csv(self.training_data_path)
            test_df = pd.read_csv(self.testing_data_path)            
            log.info("Successfully done reading the training and testing datasets into their respective dataframes.")

            log.info("Creating feature columns and target column.")
            input_features_training = train_df.drop(columns=target_column, axis=1)
            target_feature_training = train_df[target_column]

            input_features_testing = test_df.drop(columns=target_column, axis=1)
            target_feature_testing = test_df[target_column]

            log.info("Transforming feature columns of training and test dataframes.")
            input_feature_train_arr = preprocesing_obj.fit_transform(input_features_training)
            input_feature_test_arr = preprocesing_obj.transform(input_features_testing)

            log.info("Concatenating feature and target columns of training and test dataframes.")
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_training)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_testing)]

            log.info("Saving the transformer object preprocessing_obj.pkl")
            save_object(
                file_path=self.dataTransformationConfig.transformationProcessorPath,
                obj=preprocesing_obj
            )
            log.info("Saved the transformer object preprocessing_obj.pkl")
            log.info("Returning train_arr,test_arr and the transformer object path.")

            return (
                train_arr,
                test_arr,
                self.dataTransformationConfig.transformationProcessorPath
            )

        except Exception as e:
            raise CustomException(e, sys)





