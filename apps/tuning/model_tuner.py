from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score, accuracy_score
from apps.core.logger import Logger
from sklearn.metrics import r2_score

class ModelTuner:
    """_summary_
    **************************************************************************
    *
    *filename:       model_tuner.py
    *version:        1.0
    *author:         Daniel Rawlins
    *creation date:  12-Jan-2024
    *
    *change history:
    *
    *who           when           version    change(include bug# if apply)
    *----------    -----------    -------    -----------------------------
    *D. Rawlins    12-JAN-2024       1.0     initial creation
    *
    *
    *description: Class to tune and select best model
    *
    **************************************************************************
    """
    def __init__(self, run_id, data_path, mode):
        self.run_id = run_id
        self.data_path = data_path
        self.logger = Logger(self.run_id, 'ModelTuner', mode)
        self.rfc = RandomForestClassifier()
        self.xgb = XGBClassifier(objective='binary:logistic')
        
    def best_params_randomforest(self, train_x, train_y):
        """
        *method: best_params_randomforest
        *description: method to get the parameters for Random forest Algorithm which give the best accuracy.
        *             Use Hyper Parameter Tuning.
        *return: The model with the best parameters
        *
        *who           when           version   change (include bug# if apply)
        *---------     -----------    -------   ------------------------------
        *D. Rawlins    12-JAN-2024       1.0     initial creation
        *
        *Parameters
        *   train_x:
        *   train_y:
        """
        try:
            self.logger.info('Start of finding best params for randomforest algo...')
            #initializing with different combination of parameters
            self.param_grid = {"n_estimators":[10,50,100,130], "criterion":['gini','entropy'],
                               "max_depth":range(2,4,1),"max_features":['auto','log2']}
            
            #creating an object of the Grid Search class
            self.grid = GridSearchCV(estimator=self.rfc, param_grid=self.param_grid, cv=5)
            #finding the best parameters
            self.grid.fit(train_x, train_y)
            
            #extracting the best parameters
            self.criterion = self.grid.best_params_['criterion']
            self.max_depth = self.grid.best_params_['max_depth']
            self.max_features = self.grid.best_params_['max_features']
            self.n_estimators = self.grid.best_params_['n_estimators']
            
            #crating a new model with the best parameters
            self.rfc = RandomForestClassifier(n_estimators=self.n_estimators, criterion=self.criterion,
                                              max_depth=self.max_depth, max_features=self.max_features)
            
            #training the new model
            self.rfc.fit(train_x,train_y)
            self.logger.info('Random Forest best params: '+str(self.grid.best_params_))
            
            self.logger.info('End of finding best params for randomforest algo...')
            return self.rfc
        except Exception as e:
            self.logger.exception('Exception raised while finding best params for randomforest algo:'+str(e))
            raise Exception()
    
    def best_params_xgboost(self, train_x, train_y):
        """
        *method: best_params_xgboost
        *description: method to get the parameters for XGBoost Algorithm which give the best accuracy.
        *             Use Hyper Parameter Tuning.
        *return: The model with the best parameters
        *
        *who           when           version   change (include bug# if apply)
        *---------     -----------    -------   ------------------------------
        *D. Rawlins    12-JAN-2024       1.0     initial creation
        *
        *Parameters
        *   train_x:
        *   train_y:
        """ 
        try:
            self.logger.info('Start of finding best params for XGBoost algo...')
            #initializing with different combination of parameters
            self.param_grid_xgboost = {
                'learning_rate':[0.5,0.1,0.01,0.001],
                'max_depth':[3,5,10,20],
                'n_estimators':[10,50,100,200]
            }
            
            #creating an object of the Grid Search class
            self.grid = GridSearchCV(estimator=self.xgb, param_grid=self.param_grid_xgboost, cv=5)
            #finding the best parameters
            self.grid.fit(train_x, train_y)
            
            #extracting the best parameters
            self.learning_rate = self.grid.best_params_['learning_rate']
            self.max_depth = self.grid.best_params_['max_depth']
            self.n_estimators = self.grid.best_params_['n_estimators']
            #creating a new model with the best parameters
            self.xgb = XGBClassifier(objective='binary:logistic', learning_rate=self.learning_rate, max_depth=self.max_depth, n_estimators=self.n_estimators)
            #training the new model
            self.xgb.fit(train_x,train_y)
            self.logger.info('XGBoost best params: '+str(self.grid.best_params_))
            
            
            self.logger.info('End of finding best params for XGBoost algo...')   
            return self.xgb
        except Exception as e:
            self.logger.exception('Exception raised while finding best params for XGBoost algo:'+str(e))
            raise Exception()
        
        
    def get_best_model(self, train_x, train_y, test_x, test_y):
        """
        *method: get_best_model
        *description: method to get the best model.
        *return: The best model between the models
        *
        *who           when           version   change (include bug# if apply)
        *---------     -----------    -------   ------------------------------
        *D. Rawlins    12-JAN-2024       1.0     initial creation
        *
        *Parameters
        *   train_x:
        *   train_y:
        *   test_x:
        *   test_y:
        """
        try:
            self.logger.info('Start of finding best model...')
            #create best model for XGBoost
            self.xgboost = self.best_params_xgboost(train_x, train_y)
            self.prediction_xgboost = self.xgboost.predict(test_x) #Prediction using the XGBoost Model
            
            if len(test_y.unique())== 1: # if there's only one label in y, then roc_auc_score returns error. we will use accuracy in that case
                self.xgboost_score = accuracy_score(test_y, self.prediction_xgboost)
                self.logger.info('Accuracy for XGBoost:'+str(self.xgboost_score))
            else:
                self.xgboost_score = roc_auc_score(test_y, self.prediction_xgboost) #AUC for XGBoost
                self.logger.info('AUC for XGBoost:'+str(self.xgboost_score))
            
            #create best model for Random forest
            self.random_forest = self.best_params_randomforest(train_x, train_y)
            self.prediction_random_forest = self.random_forest.predict(test_x) #Prediction using the Random Forest Algo
            
            if len(test_y.unique())== 1: # if there's only one label in y, then roc_auc_score returns error. we will use accuracy in that case
                self.random_forest_score = accuracy_score(test_y, self.prediction_random_forest)
                self.logger.info('Accuracy for Random Forest:'+str(self.random_forest_score))
            else:
                self.random_forest_score = roc_auc_score(test_y, self.prediction_random_forest) #AUC for Random Forest
                self.logger.info('AUC for Random Forest:'+str(self.random_forest_score))
            
            #Comparing the models
            self.logger.info('End of finding best model...')
            if (self.random_forest_score < self.xgboost_score):
                return 'XGBoost', self.xgboost
            else:
                return 'RandomForest', self.random_forest
        except Exception as e:
            self.logger.exception('Exception raised while finding best model:'+str(e))
            raise Exception()
        
         
            