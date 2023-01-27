from flask import Flask     # Import flask package and the Flask class
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
    c = (2*500)/0
    s = str(c)
    return 'bye_'+s

if __name__ == '__main__':
    app.run()  # leave this empty until specifying an IP and port. If debug=True in run() method you will get error 
               # messages in the client.