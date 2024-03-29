"""
User requirements:
- Allow users to register, costs 0 credits
- Each user gets 6 credits (credit = unit of purchase) for free at registration
- Store a sentence on our database, one sentence costs one credit
- Retrieve a user's stored sentence from our db at a price of one credit
- Allow the user to check their credit balance
"""

import sys
from flask import Flask, jsonify, request
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)

client = MongoClient('mongodb://db:27017')
db = client.SentencesDB
Users = db['Users']  # rather than having Sentences as separate collection,
                     # store sentences as embedded doc w/in a single user's doc


#-------------------------------------------------------------------------------
# HELPER FUNCTIONS

def verify_pw(user, pw):
    hashed_pw = Users.find({
        'username': user
    })[0]['password']
    if bcrypt.hashpw(pw.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False

def get_credits_balance(user):
    return Users.find_one({
        'username': user
    })['credits']


def get_user_stored_sentence(user):
    return Users.find_one({
        'username': user
    })['sentence']
#-------------------------------------------------------------------------------


@app.route('/register', methods=['POST'])
def register():
    """
    Create a new user.

    Params from posted request object
    :param username str: supplied username for new user registration
    :param password str: supplied password for new user registration
    """
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


@app.route('/store', methods=['POST'])
def store():
    """
    Store a given user's desired sentence in the DBaaS db.

    Params from posted request object
    :param username str: supplied username for verifying existing user
    :param password str: supplied password for verifying existing user
    :param sentence str: supplied sentence to be stored for verified existing user
    """
    # STEP 1: get posted data
    posted_data = request.get_json()
    # STEP 2: read the data
    username = posted_data['username']
    password = posted_data['password']
    sentence = posted_data['sentence']
    # STEP 2.2: assume correct username & password and sufficient credits balance (bad assumption, but just getting up MVP API).
    status_code = 200
    status_message = 'Successful login, sentence in DBaaS updated, credits balance updated'
    # STEP 3: verify that the username's password is correct
    correct_pw = verify_pw(username, password)
    num_credits = get_credits_balance(username)
    if not correct_pw:
        status_code = 302
        status_message = 'Incorrect username or password'
    # STEP 4: verify that the user has sufficient credits balance to store a sentence
    elif num_credits <= 0:
        status_code = 301
        status_message = 'Insufficient credits balance to complete operation'
    # STEP 5: if they have the right [user,pw] and sufficient credits, store the
    # sentence, decrement the user's credits balance, return 200 status code
    else:
        #print('num_credits before decrement: {}'.format(num_credits), file=sys.stderr)
        #num_credits -= 1  # decrement credits since we're successfully storing a sentence in this block
        #print('num_credits after  decrement: {}'.format(num_credits), file=sys.stderr)
        filter = {'username': username}
        new_doc_values = {'$set': {'sentence': sentence, 'credits': (num_credits-1)}}
        Users.update_one(filter, new_doc_values)

    return_json = {
        'status': status_code,
        'status_message': status_message
    }
    return jsonify(return_json)


@app.route('/check_credits_balance', methods=['POST'])
def check_credits_balance():
    """
    Retrieve a given user's credit balance.

    Params from posted request object
    :param username str: supplied username for verifying existing user
    :param password str: supplied password for verifying existing user
    """
    posted_data = request.get_json()
    username = posted_data['username']
    password = posted_data['password']
    status_code = 200
    # STEP 3: verify that the username's password is correct
    correct_pw = verify_pw(username, password)
    num_credits = get_credits_balance(username)
    if not correct_pw:
        status_code = 302
        status_message = 'Incorrect username or password'
    status_message = 'Credits balance for username \'{}\' is: {}'.format(username, num_credits)
    return_json = {
        'status': status_code,
        'status_message': status_message
    }
    return jsonify(return_json)


@app.route('/retrieve', methods=['POST'])
def retrieve():
    """
    Retrieve a given user's stored sentence.

    Params from posted request object
    :param username str: supplied username for verifying existing user
    :param password str: supplied password for verifying existing user
    """
    posted_data = request.get_json()
    username = posted_data['username']
    password = posted_data['password']
    status_code = 200
    correct_pw = verify_pw(username, password)
    num_credits = get_credits_balance(username)
    if not correct_pw:
        status_code = 302
        status_message = 'Incorrect username or password'
    elif num_credits <= 0:
        status_code = 301
        status_message = 'Insufficient credits balance to complete operation'
    # If correct_pw and sufficient credits, retrieve sentence and decrement credits
    else:
        filter = {'username': username}
        new_doc_values = {'$set': {'credits': (num_credits-1)}}
        Users.update_one(filter, new_doc_values)
        sentence = get_user_stored_sentence(username)
        status_message = 'Your sentence is: \'{}\''.format(sentence)
    return_json = {
        'status': status_code,
        'status_message': status_message
    }
    return jsonify(return_json)


if __name__ == '__main__':
     app.run(host='0.0.0.0')