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
import bcrypt

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
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        # STEP 4: store username and password into database
        Users.insert_one({
             'username': username,
             'password': hashed_pw,
             'sentence': '',
             'credits': 6
        })
        # STEP 5: notify user of successful registration
        return_json = {
             'status': 200,
             'message': 'You successfully registered for the DBaaS API'
        }
        return jsonify(return_json)


def verify_pw(user, pw):
    hashed_pw = Users.find({
        'username': user
    })[0]['password']
    if bcrypt.hashpw(pw.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False

def get_credits_balance(user):
    return Users.find({
        'username': user
    })[0]['credits']

class Store(Resource):
    def post(self):
        # STEP 1: get posted data
        posted_data = request.get_json()
        # STEP 2: read the data
        username = posted_data['username']
        password = posted_data['password']
        sentence = posted_data['sentence']
        # STEP 2.2: assume correct username & password and sufficient credits balance (bad assumption, but just getting up MPV API).
        status_code = 200
        status_message = 'Successful login, sentence in DBaaS updated, credits balance updated'
        # STEP 3: verify that the username's password is correct
        correct_pw = verify_pw(username, password)
        if not correct_pw:
            status_code = 302
            status_message = 'Incorrect username or password'
        # STEP 4: verify that the user has sufficient credits balance to store a sentence
        num_credits = get_credits_balance(username)
        if num_credits <= 0:
            status_code = 301
            status_message = 'Insufficient credits balance to complete operation'
        # STEP 5: store the sentence, decrement the user's credits balance, return 200 status code
        Users.update_one({
            'username':username
        },
        {
            '$set':{
                'sentence':sentence},
                'credits': num_credits-1
        })

        return_json = {
            'status': status_code,
            'status_message': status_message
        }
        return jsonify(return_json)



api.add_resource(Register, '/register')
api.add_resource(Store, '/store')

if __name__ == '__main__':
     app.run(host='0.0.0.0')
        

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