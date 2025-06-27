import sys
from typing import Dict,Tuple
import os
import pandas as pd
import pickle
import  yaml 
import boto3

from src.constants import *
from src.exception import CustomException
from src.logger import logging

class MainUtils:
    def __init__(self):
        pass
    def read_yaml_file(self,filename)->dict:
        try:
            with open(filename,"rb") as yaml_file:
                return yaml.safe_load(yaml_file)
        except Exception as e:
            raise CustomException(e,sys)
        """
        A file object is what you get from open("file.yaml").
    A string containing YAML is just a variable with YAML-formatted text.
    yaml.safe_load() can parse both and return a Python dictionary.

    """
    def read_schema_config_file(self) ->dict:
        try:
            schema_config=self.read_yaml_file(os.path.join("config","schema.yaml"))
            return schema_config
        except Exception as e:
            raise CustomException(e,sys)
    @staticmethod 
    def save_object(file_path:str , obj: object):
        logging.info("entered the save_object method of Main utils class")
        try:
            with open(file_path,"wb") as file_obj:
                pickle.dump(obj,file_obj)
            logging.info(f"object saved at {file_path}")
        except Exception as e:
            raise CustomException (e,sys)    
    
    """
    save_object and load_object are static methods because
    they only work with the arguments you pass, not with the class
    or instance itself.
    """
    @staticmethod
    def load_object(file_path:str):
        logging.info("entered the load_obje t method ")
        try:
            with open(file_path,"rb") as file_obj:
                logging.info("the object is loaded")
                return pickle.load(file_obj)
            
        except Exception as e:
            raise CustomException(e,sys)
            
        
            
    
       
        


