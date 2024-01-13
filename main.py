from flask import Flask, request, render_template
from flask import Response
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route('/training', methods = ['POST'])
@cross_origin()
def training_route_client():
    try:
        return Response("Training successfull!")
    except ValueError:
        return Response("Error Occurred! %s" % ValueError)
    except KeyError:
        return Response("Error Occurred! %s" % KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" % e)


if __name__ == "__main__":
    app.run()
