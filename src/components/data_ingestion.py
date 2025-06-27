import sys 
import os
import numpy as np
import pandas as pd
from pymongo import MongoClient
from src.constants import *
from src.exception import CustomException
from src.utils.main_utils import MainUtils
from dataclasses import dataclass
from src.logger import logging

@dataclass
class DataIngestionConfig:
    artifact_folder: str=os.path.join(artifact_folder)
    
class DataIngestion:
    def __init__(self):
        self.data_ingestion_congif= DataIngestionConfig()
        self.utils= MainUtils()
    def export_collection_as_dataframe(self, collection_name: str,db_name) -> pd.DataFrame:
        try:
            mongo_client= MongoClient(MONGO_DB_URL)
            collections= mongo_client[db_name][collection_name]#fetch all the data and store it in collection 
            df= pd.DataFrame(list(collections.find())) 
            #convert the data into dataframe
            if "_id" in df.columns:
                df.drop("_id",axis=1,inplace=True)
            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise CustomException(e, sys)
    def export_data_into_feature_store_file_path(self):
        try:
            logging.info("Exporting data from MongoDB to feature store")
            raw_file_path=self.data_ingestion_congif.artifact_folder 
            os.makedirs(raw_file_path,exist_ok=True)
            sensor_data=self.export_collection_as_dataframe(MONGO_COLLECTION_NAME,DATABASE_NAME)
            
            logging.info(f"Exported data from MongoDB to feature store at {raw_file_path}")
            feature_store_file_path=os.path.join(raw_file_path,"wafers_fault.csv")
            sensor_data.to_csv(feature_store_file_path,index=False)
            return feature_store_file_path
        except Exception as e:
            raise CustomException(e, sys)
    def initiate_data_ingestion(self):
        logging.info("Initiating data ingestion")
        try:
            feature_store_file_path=self.export_data_into_feature_store_file_path()
            logging.info(f"Data ingestion completed. Feature store file path: {feature_store_file_path}")
            return feature_store_file_path
        except Exception as e:
            logging.error(f"Error during data ingestion: {e}")
            raise CustomException(e, sys)
        
            