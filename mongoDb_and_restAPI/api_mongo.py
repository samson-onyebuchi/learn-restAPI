from flask import Flask
from flask_restful import Resource, Api
import pymongo
from API_constant import mongodb_url

client = pymongo.MongoClient(mongodb_url())

# Select the database and collection to use
db = client["API"]
users_collection = db["book"]

app = Flask(__name__)
api = Api(app)


class To_create_user(Resource):
    def post(self,name,number):
        data = {"name":name, "number":number}
        users_collection.insert_one(data)
        return "successfuly registered"

api.add_resource(To_create_user, "/info/<string:name>/<int:number>")


class To_get_user(Resource):
    def get(self):
        datas = []
        for data in users_collection.find({},{"_id":0}):
            str_data = str(data)
            datas.append(str_data)

        return datas

api.add_resource(To_get_user, "/info/")


class To_delete_user(Resource):
    def delete(self,name):
        data_to_delete = users_collection.delete_one({"name":name})

        return "Deleted"

api.add_resource(To_delete_user, "/info/<string:name>")


class To_update_user(Resource):
    def put(self, name, new_name):
        old_name = {"name": name}
        updated_name = {"$set": {"name": new_name}}
        users_collection.update_one(old_name, updated_name)

        return "successfuly updated"

api.add_resource(To_update_user, "/info/<string:name>/<string:new_name>")
if __name__ == "__main__":
    app.run(debug=True)