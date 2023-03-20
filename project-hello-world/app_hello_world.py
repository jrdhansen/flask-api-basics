from flask import Flask, jsonify, request  # Import flask package and the Flask class
app = Flask(__name__)       # Create a Flask class instance. The first arg is the name of the app's module or package.
                            # __name__ is just a convention

@app.route('/')             # Tell the app which URL triggers the hello_world() function. App is waiting for someone to
                            #   write the / at the end of IP 127.0.0.1:5000/, which triggers returning the string.
def hello_world():
    return 'Hello world!'

@app.route('/hithere')
def hi_there_everyone():
    return 'We just enetered URL ending with /hithere'

@app.route('/bye')
def bye():
    # Prepare a response for the request that came to /bye
    #c = (2*500)/0
    #s = str(c)
    my_age = 29_000
    ret_json = {
        'name': 'jhansen',
        'age': my_age,
        'phones': [
            {
                'phone_name': 'Pixel_6A',
                'phone_number': '435-812-9485'
            },
            {
                'phone_name': 'iPhone_14',
                'phone_number': '801-274-0031'
            }
        ]
    }
    return jsonify(ret_json)

@app.route('/add_two_nums', methods=['POST'])
def add_two_nums():
    # Get x,y from the posted data, sum as z, return z as JSON.
    data_dict = request.get_json()

    if 'x' not in data_dict or 'y' not in data_dict:
        return 'ERROR', 305

    x = data_dict['x']
    y = data_dict['y']
    z = x+y
    return_json = {
        'z':z
    }
    return jsonify(return_json), 200  # 200 denotes a successful request

if __name__ == '__main__':
    app.run()  # leave this empty until specifying an IP and port. If debug=True in run() method you will get error 
               # messages in the client.