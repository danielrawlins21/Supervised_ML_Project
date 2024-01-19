from wsgiref import simple_server
from flask import Flask, request, render_template
from flask import Response
from flask_cors import CORS, cross_origin

from apps.core.config import Config
from apps.training.train_model import TrainModel
from apps.prediction.predict_model import PredictModel

app = Flask(__name__)
CORS(app)

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

if __name__ == "__main__":
    #app.run()
    host = '0.0.0.0'
    port = 5000
    httpd = simple_server.make_server(host, port, app)
    httpd.serve_forever()
