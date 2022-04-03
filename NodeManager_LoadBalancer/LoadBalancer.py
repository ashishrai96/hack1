from flask import Flask, request
import requests
import pymongo
import sys

session = requests.Session()
app = Flask(__name__)
myclient=pymongo.MongoClient("mongodb+srv://hackathon:hackathon@hackathon.wgs03.mongodb.net/Hackathon?retryWrites=true&w=majority")
mydb=myclient["Hackathon"]
mycollection=mydb["Node_db"]

SENSOR_PORT = 9100
MODEL_PORT = 9200
LOAD_PORT = 9300
APP_PORT = 9400
DEPLOYER_PORT = 9500
NODE_PORT = 9500
SCH_PORT = 9600


endpoint = {
    "sensor_manager": {
        "base_url": "http://localhost:"+str(SENSOR_PORT), 
        "uri": {
            "sensorinfo": "/sensorinfo",
            "getsensordata": "/getsensordata"
        }
    },
    "app_manager": {
        "base_url": "http://localhost:" + str(APP_PORT),
        "uri": {
            "get_all_models_sensos": "/get_models_sensors",
            "get_all_apps": "/get_all_applications",
            "get_sensor_by_app_id": "/get_sensor_by_app_id",
            "deploy_app": "/deploy"
        }
    },
    "load_balancer": {
        "base_url": "http://localhost:" + str(LOAD_PORT),
        "uri": {
            "get_node_id": "/get_node_id"
        }
    },
    "deployer": {
        "base_url": "http://localhost:" + str(DEPLOYER_PORT),
        "uri": {
            "send_to_deployer": "/send_to_deployer",
        }
    },
}


@app.route("/get_node_id", methods=["POST"])
def get_node_id():
    req = request.get_json()
    """
    req={
        'stand_alone': bool
    }

    we will ignore stand_alone for now
    and do load balancing on basis of num of apps running
    """

    min_load=sys.maxint
    resultant_node=""
    for x in mycollection.find():
        if x['list_of_appInst']<min_load:
            min_load=x['list_of_appInst']
            resultant_node=x['node_id']
    reply={
        'node_id':resultant_node,
        'message':"Node Assigned.."
    }
    return reply


if __name__=="__main__":
    app.run(port=LOAD_PORT, debug=True)