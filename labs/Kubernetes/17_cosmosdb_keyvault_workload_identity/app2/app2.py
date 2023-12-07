from flask import Flask, render_template
import pymongo
import os

app = Flask(__name__)

CONN_STR = os.getenv('CONNECTION_STRING')
client = pymongo.MongoClient(CONN_STR)
database = client[os.getenv('COSMOS_DATABASE_NAME')]
user_collection = database[os.getenv('USER_COLLECTION_NAME')]
activity_collection = database[os.getenv('ACTIVITY_COLLECTION_NAME')]

@app.route('/')
def index():
    last_two_users = list(user_collection.find().sort([("timestamp", pymongo.DESCENDING)]).limit(2))
    last_two_activities = list(activity_collection.find().sort([("timestamp", pymongo.DESCENDING)]).limit(2))
    
    return render_template('index.html', users=last_two_users, activities=last_two_activities)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8095)
