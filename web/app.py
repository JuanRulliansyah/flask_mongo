from flask import Flask
from flask_restful import Api, Resource
from pymongo import MongoClient

from web.auth import Register, Store, Sentence

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://localhost:27017")
db = client.flask_db
db.visitor.insert({
    'num_of_users': 0
})


class Visit(Resource):
    def get(self):
        prev_num = db.visitor.find({})[0]['num_of_users']
        new_num = prev_num + 1
        db.visitor.update({}, {"$set": {'num_of_users': new_num}})
        return str("Hello user" + str(new_num))



@app.route('/')
def hello_world():
    return 'Hello World!'


api.add_resource(Visit, '/visit/')
api.add_resource(Register, '/auth/register/')
api.add_resource(Store, '/auth/store/')
api.add_resource(Sentence, '/auth/sentence/')


if __name__ == '__main__':
    app.run()
