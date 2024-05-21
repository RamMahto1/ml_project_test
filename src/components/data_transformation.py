import pandas as pd 
import numpy as np 
import os
import sys
from src.logger import logging
from src.exception import CustomException
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from src.utils import save_object
from dataclasses import dataclass




@dataclass
class DataTransformationConfig:
    preprocessor_file_path_object = os.path.join('artifacts',"preprocessor.pkl")
    
    
class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
        
        
    def get_data_transformation_object(self):
        '''
        this function is responsible for data transforamtion
        '''
        
        try:
            numerical_column_name = ["reading_score","writing_score"]
            categorical_column_name = ["gender","race_ethnicity","parental_level_of_education","lunch","test_preparation_course"]
            
            num_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )
            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hotencoder",OneHotEncoder(handle_unknown="ignore")),
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )
            
            logging.info(f"numerical columns{numerical_column_name}")
            logging.info(f"categorical columns{categorical_column_name}")
            
            preprocessor = ColumnTransformer(
                [
                    ("numerical_pipeline",num_pipeline,numerical_column_name),
                    ("categorical_pipeline",cat_pipeline,categorical_column_name)
                ]
            )
            
            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
            
            
    def initiate_data_transformation(self,train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info("read the data as data frame")
            logging.info(f"obtaining preprocessor object")
            preprocessing_obj = self.get_data_transformation_object()
            
            target_columns_name = "math_score"
            numerical_column_name=["reading_score","writing_score"]
            
            input_feature_train_df = train_df.drop(columns=[target_columns_name], axis=1)
            target_feature_train_df = train_df[target_columns_name]
            
            input_feature_test_df = test_df.drop(columns=[target_columns_name],axis=1)
            target_feature_test_df = test_df[target_columns_name]
            
            logging.info(f"applying preprocessor object on training and testing dataset")
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)
            
            train_arr = np.c_[
                input_feature_train_arr,np.array(target_feature_train_df)
            ]
            test_arr = np.c_[
                input_feature_test_arr,np.array(target_feature_test_df)
            ]
            
            logging.info(f"saved preprocessor")
            
            save_object(
                file_path=self.data_transformation_config.preprocessor_file_path_object,
                obj=preprocessing_obj
            )
            
            return(
                train_arr, 
                test_arr,
                self.data_transformation_config.preprocessor_file_path_object
            )
            
            
        except Exception as e:
            raise CustomException(e,sys)
            