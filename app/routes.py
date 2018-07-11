"""
MAIN SERVER MODULE TO QUERY ALL THE EPD OPERATIONS
"""

import json
import jwt
import pyotp
from flask import jsonify, make_response, request, render_template
from json_response import JsonResponse
from app import app

@app.errorhandler(404)
def not_found():
    """
    Error handler for 404 - Not found
    """
    return make_response(jsonify({"error": "Not found"}), 404)

@app.errorhandler(400)
def bad_request():
    """
    Error handler for 404 - Bad request
    """
    return make_response(jsonify({"error": "Bad request"}), 400)

@app.route("/epd/api/v1.0/index")
def index():
    """
    Flask function to entertain the query for the login page
    """
    return render_template("login.html")

@app.route("/epd/api/v1.0/login-verification", methods=['POST', 'GET'])
def login_verification():
    """
    Flask function to verify the login credentials through ajax call from html page
    """

    _secret = "secret"

    try:
        username = request.json[0].get("value", "")
        user_otp = request.json[1].get("value", "")

        time_based_otp = pyotp.TOTP("LOGINATEPDASSIST")

        if int(user_otp) != int(time_based_otp.now()):
            return jsonify({"result": "Enter a correct verification code"})

        payload = {"username": username}
        token = jwt.encode(payload, _secret)

        print "\n\nbreak\n\n"

        return jsonify({"token": token})

    except IndexError as error:
        print "Problem occured: {}".format(error)
        return jsonify({"result": "Please correctly fill the fields"})
	
@app.route("/epd/api/v1.0/main")
def main_page():
	return render_template("main.html")