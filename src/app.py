"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Queue
#from models import Person
from sendsms import send_sms

app = Flask(__name__)
app.url_map.strict_slashes = False

queue = Queue()

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

@app.route('/new', methods=['POST'])
def add_to_queue():
    contact = request.get_json()
    queue.enqueue(contact)
    send_sms("You have been added to the queue", contact['phone'])
    return jsonify(f"{contact['name']} added to queue")

@app.route('/skip', methods=['POST'])
def hosts_friend():
    contact = request.get_json()
    queue.skip_the_line(contact)
    send_sms("The hostess likes you, you're up next", contact['phone'])
    return jsonify(f"{contact['name']} added to queue")

@app.route('/next', methods=['GET'])
def process_next():
    contact = queue.dequeue()
    send_sms("It is your turn", contact['phone'])
    return jsonify(f"{contact['name']} removed from queue")

@app.route('/remove/<phone>', methods=['DELETE'])
def remove(phone):
    queue.leave_queue(phone)
    send_sms("You have left the queue", phone)
    return jsonify(f"{phone} has left the queue")

@app.route('/all', methods=['GET'])
def show_queue():
    queue1 = queue.get_queue()
    return jsonify(queue1)