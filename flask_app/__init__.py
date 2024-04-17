from flask import Flask
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = 'mongodb+srv://mongodb:mongodb@cluster0.gy12rxn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.trackers

def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_pyfile('config.py', silent=False)
    if test_config is not None:
        app.config.update(test_config)
    
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    
    return app