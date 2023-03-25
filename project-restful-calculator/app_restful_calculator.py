from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app=app)


def input_validation(posted_data, function_name):
    """
    Validate input data for a given calculator operation (function_name).
    Confirm that all fields populated and proper data types. Return status code.

    :param posted_data json: should be of form {"x": x_value, "y": y_value}
    :param function_name str: should be in ['add', 'subtract', 'multiply', 'divide'] 
    :return status_code int: status code corresponding to input quality
    """
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


@app.route("/")
def hello_world():
    return "Hello world!"


if __name__ == "__main__":
    app.run(debug=True)
