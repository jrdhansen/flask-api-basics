from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app=app)


def input_validation(posted_data, function_name):
    """
    Validate input data for a given calculator operation (function_name).
    Confirm that all fields populated and proper data types. Return status code.
    """
    if function_name == "add":
        if "x" not in posted_data or "y" not in posted_data:
            return 301  # status code we defined in Resource Method Chart for missing an operand
        else:
            return 200  # status code for all inputs being available and valid


class Add(Resource):
    def post(self): # If here, then the resource Add was requested using POST method
        """
        Obtain posted data for addition, validate operands, sum inputs,
        return {sum, status code}.
        """
        posted_data = request.get_json()

        status_code = input_validation(posted_data=posted_data, function_name="add")
        if status_code == 200:
            x = int(posted_data["x"])
            y = int(posted_data["y"])
            return_value = x+y
        else:
            return_value = "At least one of operand inputs {x, y} is missing"

        return_map = {
            "Message":  return_value,
            "Status Code": status_code 
        }
        return jsonify(return_map)


class Subtract(Resource):
    pass


class Multiply(Resource):
    pass


class Divide(Resource):
    pass


api.add_resource(Add, "/add")


@app.route("/")
def hello_world():
    return "Hello world!"


if __name__ == "__main__":
    app.run(debug=True)