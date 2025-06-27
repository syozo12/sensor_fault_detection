import sys
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from sklearn.impute import SimpleImputer , KNNImputer
from sklearn.preprocessing import RobustScaler , FunctionTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import  StandardScaler

from src.constants import *
from src.exception import CustomException
from src.logger import logging
from src.utils.main_utils import MainUtils
from dataclasses import dataclass

@dataclass
class dataTransfomationConfig:
    artifact_dir= os.path.join("artifacts")
    transformed_train_file_path=os.path.join(artifact_dir, 'train.npy')
    transformed_test_file_path=os.path.join(artifact_dir, 'test.npy') 
    transformed_object_file_path=os.path.join( artifact_dir, 'preprocessor.pkl' )
class DataTransformation:
    def __init__(self,feature_store_file_path):
        self.data_transformation_config = dataTransfomationConfig()
        self.feature_store_file_path = feature_store_file_path
        self.utils = MainUtils()
    @staticmethod
    def get_data(feature_store_file_path:str) -> pd.DataFrame:
        try:
            df=pd.read_csv(feature_store_file_path)
            df.rename(columns={"Good/Bad":TARGET_COLUMN},inplace=True)
            return df
        except Exception as e:
            raise CustomException(e,sys)
    def get_data_transformer_object(self):
        try:
            imputer = KNNImputer(n_neighbors=3)
            preprocessing_pipeline = Pipeline(
            steps=[('Imputer',imputer), ('Scaler', RobustScaler())])
            return preprocessing_pipeline
        except Exception as e:
            raise CustomException(e, sys)
    def initiate_data_transformation(self):
        logging.info("initiated data data transformation ")
        try:
            d=self.get_data(self.feature_store_file_path)
            logging.info("data loaded successfully")
            logging.info("splitting data into train and test")
            
            x,y= d.drop(TARGET_COLUMN, axis=1), d[TARGET_COLUMN]#df x y pd seres 
            y=np.where(d[TARGET_COLUMN]==-1,0,1)#array
            x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)
            # here waht we pass that we get in return x_train,x_test are df  ,y_train,y_test seriesd 
            proccessor=self.get_data_transformer_object()
            x_train_transformed=proccessor.fit_transform(x_train)
            x_test_transformed=proccessor.transform(x_test)
            #Transformed X: NumPy array
#            Transformed y: NumPy array

            preprocessor_file_path=self.data_transformation_config.transformed_object_file_path
            self.utils.save_object(file_path=preprocessor_file_path, obj=proccessor)
            logging.info("data transformation completed")
            train_arr=np.c_[x_train_transformed,y_train]
            test_arr=np.c_[x_test_transformed,y_test]
            
            return train_arr, test_arr, preprocessor_file_path
        except Exception as e:
            raise CustomException(e, sys)
            

    
