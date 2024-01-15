from wsgiref import simple_server
from flask import Flask, request, render_template
from flask import Response
from flask_cors import CORS, cross_origin

from apps.core.config import Config

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
        #
        
        return Response("Training successfull!")
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
