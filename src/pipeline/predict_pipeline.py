
        
    
        

import shutil
import os,sys
import pandas as pd
import pickle
from src.logger import logging

from src.exception import CustomException
import sys
from flask import request
from src.constants import *
from src.utils.main_utils import MainUtils

from dataclasses import dataclass
@dataclass
class PredictPipelineConfig:
    prediction_output_dirname :str="predictions_output"
    pred_file_input_dir="prediction_input"
    prediction_file_name :str="prediction_file.csv"
    model_file_path :str=os.path.join("artifacts","model.pkl")
    preprocessor_file_path :str=os.path.join("artifacts","preprocessor.pkl")
    op_file_path=os.path.join(prediction_output_dirname , prediction_file_name )
class PredictPipeline:
    def __init__(self,request):
        self.request=request
        self.config=PredictPipelineConfig()
        self.utils=MainUtils()
    def save_input_files(self):
        try:
            
            os.makedirs(self.config.pred_file_input_dir, exist_ok=True)
            input_csv_file=self.request.files['file']
            pred_file_path=os.path.join(self.config.pred_file_input_dir,input_csv_file.filename)
            input_csv_file.save(pred_file_path)
            return pred_file_path
        except Exception as e:
            raise CustomException(e, sys)
    def predict(self,df :pd.DataFrame):
        try:
            model=self.utils.load_object(self.config.model_file_path) 
            pp=self.utils.load_object(self.config.preprocessor_file_path)
            trans_x=pp.transform(df)#nump arr
            pred_y=model.predict(trans_x)#np arr
            return pred_y
        
        except Exception as e:
            raise CustomException(e, sys)
    def get_predicted_dataframe(self,csv_path):
        try:
            logging.info("loading data from csv file")
            df=pd.read_csv(csv_path)
            df=df.drop(columns=["Unnamed: 0"]) if "Unnamed: 0" in df.columns else df
            pred_y=self.predict(df)
            df["pred_y"]=pred_y
            maping_dict={0:"bad",1:"good"}
            df["pred_y"]=df["pred_y"].map(maping_dict) #mapping 0 to bad and 1 to good
        #Series.where(condition, other) df["pred_y"]-> series df hai but with oe  row 
        #df["pred_y"]=df["pred_y"].where(df["pred_y"]==0, "bad") #if pred_y is null then replace it with bad
        # df["pred_y"]=df["pred_y"].where(df["pred_y"]==1, "good") #if pred_y is null then replace it with good
            os.makedirs(self.config.prediction_output_dirname, exist_ok=True)
            df.to_csv(self.config.op_file_path, index=False)
            logging.info("predictions completed")
        except Exception as e:
            raise CustomException(e, sys)
    
    
    
    
    def run_pipeline(self):
        try:
            input_csv_path = self.save_input_files()
            self.get_predicted_dataframe(input_csv_path)

            return self.config


        except Exception as e:
            raise CustomException(e,sys)
            
        
    
        
        

 
        

        
   