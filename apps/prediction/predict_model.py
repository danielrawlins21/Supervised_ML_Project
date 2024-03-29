import pandas as pd
from apps.core.logger import Logger
from apps.ingestion.load_validate import LoadValidate
from apps.preprocess.preprocessor import Preprocessor
from apps.core.file_operation import FileOperation

class PredictModel:
    """_summary_
    **************************************************************************
    *
    *filename:       predict_model.py
    *version:        1.0
    *author:         Daniel Rawlins
    *creation date:  19-Jan-2024
    *
    *change history:
    *
    *who           when           version    change(include bug# if apply)
    *----------    -----------    -------    -----------------------------
    *D. Rawlins    19-JAN-2024       1.0     initial creation
    *
    *
    *description: Class to prediction the result
    *
    **************************************************************************
    """
    def __init__(self, run_id, data_path):
        self.run_id = run_id
        self.data_path = data_path
        self.logger = Logger(self.run_id, 'PredictModel','prediction')
        self.loadValidate = LoadValidate(self.run_id, self.data_path,'prediction')
        self.preProcess = Preprocessor(self.run_id, self.data_path,'prediction')
        self.fileOperation = FileOperation(self.run_id, self.data_path,'prediction')
    
    def batch_predict_from_model(self):
        """
        *method: batch_predict_from_model
        *description: method to predict the results
        *return: none
        *
        *who           when           version   change (include bug# if apply)
        *---------     -----------    -------   ------------------------------
        *D. Rawlins    19-JAN-2024       1.0     initial creation
        *
        *Parameters
        *   none:
        """
        try:
            self.logger.info('Start of Prediction')
            self.logger.info('run_id:'+ str(self.run_id) )
            #validations and transformation
            self.loadValidate.validate_predictset()
            #preprocessing activities
            self.X = self.preProcess.preprocess_predictset()
            #load model
            kmeans = self.fileOperation.load_model('KMeans')
            #cluster selection
            clusters = kmeans.predict(self.X.drop(['empid'],axis=1))
            self.X['clusters'] = clusters
            clusters = self.X['clusters'].unique()
            y_predicted = []
            for i in clusters:
                self.logger.info('clusters loop started')
                cluster_data = self.X[self.X['clusters']==i]
                cluster_data_new = cluster_data.drop(['empid','clusters'], axis=1)
                model_name = self.fileOperation.correct_model(i)
                model = self.fileOperation.load_model(model_name)
                y_predicted = model.predict(cluster_data_new)
                
                result = pd.DataFrame({"EmpId":cluster_data['empid'],"Prediction":y_predicted})
                result.to_csv(self.data_path+'_results/'+'Predictions.csv', header=True, mode='a+', index=False)
            self.logger.info('End of Prediction')
        except Exception:
            self.logger.exception('Unsuccessful End of Prediction')
            raise Exception
    
    def single_predict_from_model(self,data):
        """
        *method: single_predict_from_model
        *description: method to predict single results
        *return: y_predicted
        *
        *who           when           version   change (include bug# if apply)
        *---------     -----------    -------   ------------------------------
        *D. Rawlins    19-JAN-2024       1.0     initial creation
        *D. Rawlins    19-JAN-2024      1.0.1    editing return function
        *
        *Parameters
        *   data:
        """
        try:
            self.logger.info('Start of Prediction')
            self.logger.info('run_id:'+ str(self.run_id) )
            
            #preprocessing activities
            self.X = self.preProcess.preprocess_predict(data)
            #load model
            kmeans = self.fileOperation.load_model('KMeans')
            #cluster selection
            clusters = kmeans.predict(self.X.drop(['empid'], axis=1))
            self.X['clusters'] = clusters
            y_predicted = []
            for i in clusters:
                self.logger.info('clusters loop started')
                cluster_data = self.X[self.X['clusters']==i]
                cluster_data_new = cluster_data.drop(['empid','clusters'], axis=1)
                model_name = self.fileOperation.correct_model(i)
                model = self.fileOperation.load_model(model_name)
                self.logger.info('Shape of Data '+str(cluster_data_new.shape))
                self.logger.info('Info of Data '+str(cluster_data_new.info()))
                y_predicted = model.predict(cluster_data_new)
                                               
                #result = pd.DataFrame({"EmpId":cluster_data['empid'],"Prediction":y_predicted})
                #result.to_csv(self.data_path+'_results/'+'Predictions.csv', header=True, mode='a+', index=False)
                self.logger.info('Output : '+str(y_predicted))
                return int(y_predicted[0])
            self.logger.info('End of Prediction')
        except Exception:
            self.logger.exception('Unsuccessful End of Prediction')
            raise Exception
    