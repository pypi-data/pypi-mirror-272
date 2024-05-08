import os
import sys

from ...source.Exception import CustomException
from ...source.Logger import logging



from sklearn.model_selection import train_test_split
from dataclasses import dataclass


@dataclass
class DataIngestionConfig:
    """
    This Class is to save file locations to artifact folder it will save train , test and raw data into it
    """

    train_data_path: str = os.path.join('artifact','train.csv')
    test_data_path: str = os.path.join('artifact','test.csv')
    raw_data_path: str = os.path.join('artifact','data.csv')

class DataIngestion:
    """
    Here we are starting with Data Ingestion and will read dataset making dir structures doing train test splits

    """

    def __init__(self):
        self.ingestion_config =DataIngestionConfig()

    def initate_data_ingestion(self,df):

        """
        To Initate Data Ingestion use this Function.
        """

        logging.info("Entering the Data Ingestion Method or Components")

        try:
            
            #df = Data_df
            logging.info("Read the Data Set as Pandas Dataframe")
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path,index=False, header=True)
            logging.info("Train Test Split will Start, Raw Data Exported")
            train_set, test_set = train_test_split(df,test_size=0.2,random_state=14)

            train_set.to_csv(self.ingestion_config.train_data_path,index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False, header=True) 

            logging.info("Train Test Split is Done , Data in Artifact Folder")
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,     
            )

        except Exception as e:
            raise CustomException(e,sys)