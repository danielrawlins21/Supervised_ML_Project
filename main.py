from wsgiref import simple_server
from flask import Flask, render_template, request
from flask import Response
from flask_cors import CORS, cross_origin
import flask_monitoringdashboard as dashboard
import pandas as pd
import os 

from apps.core.config import Config
from apps.training.train_model import TrainModel
from apps.prediction.predict_model import PredictModel

app = Flask(__name__)

CORS(app)

@app.route('/', methods=['POST','GET'])
def index_page():
    """
    *method: index_page
    *description: method to call index html page
    *return: index.html
    *
    *who           when           version   change (include bug# if apply)
    *---------     -----------    -------   ------------------------------
    *D. Rawlins    12-JAN-2024       1.0     initial creation
    *
    *Parameters
    *   none:
    """
    return render_template('index.html')

@app.route('/training', methods = ['POST'])
@cross_origin()
def training_route_client():
    """
    *method: training_route_client
    *description: method to call training route
    *return: none
    *
    *who           when           version   change (include bug# if apply)
    *---------     -----------    -------   ------------------------------
    *D. Rawlins    12-JAN-2024       1.0     initial creation
    *
    *Parameters
    *   none:
    """
    try:
        config = Config()
        #get run id and data path
        run_id = config.get_run_id()
        data_path = config.training_data_path
        #train model object initialization
        trainModel = TrainModel(run_id, data_path)
        #training the model
        trainModel.training_model()
                
        return Response("Training successfull! and its RunID is: "+str(run_id))
    except ValueError:
        return Response("Error Occurred! %s" % ValueError)
    except KeyError:
        return Response("Error Occurred! %s" % KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" % e)

@app.route('/batchprediction', methods = ['POST'])
@cross_origin()
def batch_prediction_route_client():
    """
    *method: batch_prediction_route_client
    *description: method to call batch prediction route
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
        config = Config()
        #get run id and data path
        run_id = config.get_run_id()
        data_path = config.prediction_data_path
        #prediction object initialization
        predictModel = PredictModel(run_id, data_path)
        #prediction the model
        predictModel.batch_predict_from_model()
                
        return Response("Prediction successfull! and its RunID is: "+str(run_id))
    except ValueError:
        return Response("Error Occurred! %s" % ValueError)
    except KeyError:
        return Response("Error Occurred! %s" % KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" % e)

@app.route('/prediction', methods = ['POST'])
@cross_origin()
def single_prediction_route_client():
    """
    *method: single_prediction_route_client
    *description: method to call single prediction route
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
        config = Config()
        #get run id and data path
        run_id = config.get_run_id()
        data_path = config.prediction_data_path
        
        if request.method == 'POST':
            satisfaction_level = request.form['satisfaction_level']
            last_evaluation = request.form["last_evaluation"]
            number_project = request.form["number_project"]
            average_montly_hours = request.form["average_montly_hours"]
            time_spend_company = request.form["time_spend_company"]
            work_accident = request.form["work_accident"]
            promotion_last_5years = request.form["promotion_last_5years"]
            salary = request.form["salary"]
            
            data = pd.DataFrame(data=[[
                0,
                satisfaction_level,
                last_evaluation,
                number_project,
                average_montly_hours,
                time_spend_company,
                work_accident,
                promotion_last_5years,
                salary
            ]],
                                columns=[
                                    'empid',
                                    'satisfaction_level',
                                    'last_evaluation',
                                    'number_project',
                                    'average_montly_hours',
                                    'time_spend_company',
                                    'work_accident',
                                    'promotion_last_5years',
                                    'salary'
                                ])
            # usinf dictionary to convert specific columns
            convert_dict = {
                'empid': int,
                'satisfaction_level': float,
                'last_evaluation':float,
                'number_project': int,
                'average_montly_hours': int,
                'time_spend_company': int,
                'work_accident': int,
                'promotion_last_5years': int,
                'salary': object
            }
            data = data.astype(convert_dict)
            
            # object initialization
            predictModel = PredictModel(run_id,data_path)
            # prediction model
            output = predictModel.single_predict_from_model(data)
            return Response("Predicted Output is: "+str(output))
                
        return Response("Prediction successfull! and its RunID is: "+str(run_id))
    except ValueError:
        return Response("Error Occurred! %s" % ValueError)
    except KeyError:
        return Response("Error Occurred! %s" % KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" % e)

dashboard.bind(app)

if __name__ == "__main__":
    #app.run()
    host = '0.0.0.0'
    port = 5000
    httpd = simple_server.make_server(host, port, app)
    httpd.serve_forever()
