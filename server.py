
from flask import Flask, Response, request
import pymongo
import json
from bson.objectid import ObjectId

app=Flask(__name__)
#######################################
try:
    mongo = pymongo.MongoClient(
        host= "localhost",
        port = 27017,
        serverSelectionTimeoutMS =1000
    )
    db = mongo.company
    mongo.server_info()
except: 
    print("ERROR - Cannot connect to mongodb")
#######################################
@app.route('/users', methods=['POST'])
def create_user():
    try:
        user = {
            "name" : request.form["name"],
            "lastname" : request.form["lastname"]
        }
        dbResponse = db.users.insert_one(user)
        # print(dbResponse.inserted_id)

        return Response(
            response= json.dumps(
                {
                    "massage": "user created",
                    "id": f"{dbResponse.inserted_id}"
                }
            ), status = 200,
            mimetype = "application/json"
        )

    except Exception as e:
        print(e)
#######################################
@app.route('/users', methods=["GET"])
def read_user():
    try:
        data = list(db.users.find())
        for user in data:
            user["_id"] = str(user['_id'])
        return Response(
            response= json.dumps(data),
            status=500,
            mimetype="application/json"
        )
    except Exception as e:
        print(e)
        return Response(
            response= json.dumps(
                {"massage": "cannot read users"})
                , status = 500,
                mimetype = "application/json"
        )


#######################################


if __name__ == "__main__":
    app.run(port=80, debug=True)