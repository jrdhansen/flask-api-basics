"""
User requirements:
- Allow users to register, costs 0 credits
- Each user gets 10 credits (credit = unit of purchase) for free at registration
- Store a sentence on our database, one sentence costs one credit
- Retrieve a user's stored sentence from our db at a price of one credit
"""

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://db:27017')
db = client.SentencesDB
Users = db['Users']  # rather than having Sentences as separate collection, store sentences as embedded doc w/in user doc


class Register(Resource):
    def post(self):
        # STEP 1.1: get user's posted data
        posted_data = request.get_json()
        # STEP 1.2
        # Could/should validate user's submission for their username and password,
        # e.g. sufficiently-strong password, no unallowed chars, etc.
        # However, that gets us away from the point of learning about and
        # implementing the API and is more detail than needed for that purpose at the moment.
        # STEP 2: 
        username = posted_data['username']
        password = posted_data['password']
        # STEP 3: hash(password, salt) to get hashed password. Don't store password as plaint text!




"""
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app=app)

client = MongoClient('mongodb://db:27017')  # tell mongo client to use 'db' service defined in docker-compose using (default) mongo port 27017
db = client.aNewDB
UserNum = db['UserNum']
UserNum.insert_one({
    'num_of_users': 0
})

class Visit(Resource):
    def get (self):
        prev_num = UserNum.find({})[0]['num_of_users']
        updated_num = prev_num + 1
        UserNum.update_one({}, {"$set":{'num_of_users':updated_num}})
        return 'hello user: {}'.format(updated_num)

def input_validation(posted_data, function_name):
    if function_name in ["add", "subtract", "multiply"]:
        if "x" not in posted_data or "y" not in posted_data:
            return 301  # status code we defined in Resource Method Chart for missing an operand
        else:
            return 200  # status code for all inputs being available and valid
    elif function_name == "divide": 
        if "x" not in posted_data or "y" not in posted_data:
            return 301  # status code we defined in Resource Method Chart for missing an operand
        elif posted_data["y"] == 0:
            return 302  # dstatus code defined in Resource method chart for divide-by-zero error
        else:
            return 200  # status code for all inputs being available and valid
    else:
        return 307  # status code for an unexpected function_name


class Add(Resource):
    def post(self):
        """
        Obtain posted data for addition, validate operands, sum inputs,
        return {sum, status code}.
        """
        posted_data = request.get_json()

        status_code = input_validation(posted_data=posted_data, function_name="add")
        if status_code == 200:
            x = posted_data["x"]
            y = posted_data["y"]
            return_value = x+y
        else:
            return_value = "At least one of operand inputs {x, y} is missing"

        return_map = {
            "Message":  return_value,
            "Status Code": status_code 
        }
        return jsonify(return_map)


class Subtract(Resource):
    def post(self):
        """
        Obtain posted data for subtraction, validate operands, calc diff inputs,
        return {difference_btwn_nums, status code}.
        """
        posted_data = request.get_json()

        status_code = input_validation(posted_data=posted_data, function_name="subtract")
        if status_code == 200:
            x = posted_data["x"]
            y = posted_data["y"]
            return_value = x-y
        else:
            return_value = "At least one of operand inputs {x, y} is missing"

        return_map = {
            "Message":  return_value,
            "Status Code": status_code 
        }
        return jsonify(return_map)


class Multiply(Resource):
    def post(self):
        """
        Obtain posted data for multiplication, validate operands, calc product
        of inputs, return {product, status code}.
        """
        posted_data = request.get_json()

        status_code = input_validation(posted_data=posted_data, function_name="multiply")
        if status_code == 200:
            x = posted_data["x"]
            y = posted_data["y"]
            return_value = x*y
        else:
            return_value = "At least one of operand inputs {x, y} is missing"

        return_map = {
            "Message":  return_value,
            "Status Code": status_code 
        }
        return jsonify(return_map)


class Divide(Resource):
    def post(self):
        """
        Obtain posted data for division, validate operands, calc quotient of
        inputs, return {quotient, status code}.
        """
        posted_data = request.get_json()

        status_code = input_validation(posted_data=posted_data, function_name="divide")
        if status_code == 200:
            x = posted_data["x"]
            y = posted_data["y"]
            return_value = float(x)/float(y)
        elif status_code == 302:
            return_value = "Divide by zero error"
        else:  # this should be when status_code == 301
            return_value = "At least one of operand inputs {x, y} is missing"

        return_map = {
            "Message":  return_value,
            "Status Code": status_code 
        }
        return jsonify(return_map)


api.add_resource(Add, "/add")
api.add_resource(Subtract, "/subtract")
api.add_resource(Multiply, "/multiply")
api.add_resource(Divide, "/divide")
api.add_resource(Visit, "/visit")


@app.route("/")
def hello_world():
    return "Hello world!"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0") # Modify this for container address
"""