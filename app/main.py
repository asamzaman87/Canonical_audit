from flask import Flask, request, jsonify, make_response
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, and_
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)

# Configuration for database connection
# Postgres was used as the database because it supports JSON data types natively and can be scaled if needed
# TODO: In the future, consider externalizing configuration to environment variables or configuration files.
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:abc123@localhost/Canonical'
db = SQLAlchemy(app)


# Define the Event model
# This model reflects the structure of the events table in the database.
class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    user_identity = db.Column(db.String(50), nullable=False)
    event_data = db.Column(db.JSON)

    # Constructor to create new Event objects
    # event_data is used to store event-specific data
    def __init__(self, event_type, timestamp, user_identity, event_data):
        self.event_type = event_type
        self.timestamp = timestamp
        self.user_identity = user_identity
        self.event_data = event_data


# Create the database tables
# TODO: Handle database migrations separately.
with app.app_context():
    db.create_all()


# Function to check username and password for basic authentication.
# Hardcoded for simplicity.
# TODO: Replace with a more secure authentication mechanism like OAuth2 or token-based authentication.
def check_auth(username, password):
    return username == 'admin' and password == 'secret'


@app.route('/events', methods=['POST'])
def create_event():
    # Extract the authorization header
    auth = request.authorization

    # Check authorization
    # TODO: Consider returning a more generic error message to prevent attackers from knowing if the username exists.
    if not auth or not check_auth(auth.username, auth.password):
        return make_response('Access denied', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    # Extract data from request
    event_type = request.json.get('event_type')
    timestamp = datetime.now()
    user_identity = request.json.get('user_identity')
    event_data = request.json.get('event_data')

    # Input validation
    if not event_type or not user_identity or not event_data:
        return jsonify({'message': 'Invalid request. Required fields missing.'}), 400

    # Create event
    event = Event(event_type=event_type, timestamp=timestamp, user_identity=user_identity, event_data=event_data)

    # Store in database
    try:
        db.session.add(event)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to create the event. Database error occurred.'}), 500

    return 'Event created successfully'


@app.route('/events/query', methods=['GET'])
def query_events():
    # Extract the authorization header
    auth = request.authorization

    # Check authorization
    if not auth or not check_auth(auth.username, auth.password):
        return make_response('Access denied', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    common_filters = {}
    unique_filters = {}

    # Filter construction based on request parameters.
    for key, val in request.args.items():
        if key in ["event_type", "timestamp", "user_identity"]:
            common_filters[key] = val
        else:
            unique_filters[key] = val

    query = Event.query

    conditions = []

    # Apply common filters
    for key, value in common_filters.items():
        filter_condition = getattr(Event, key) == value
        conditions.append(filter_condition)

    # Apply unique filters
    # Extracting info from event_data accordingly
    # TODO: Consider having the request url state the types of the values
    for key, value in unique_filters.items():
        filter_condition = func.json_extract_path_text(Event.event_data, key) == value
        conditions.append(filter_condition)

    # Combine filter conditions using AND
    if conditions:
        filters_combined = and_(*conditions)
        query = query.filter(filters_combined)

    # Execute query
    events = query.all()

    # Build response
    result = []
    for event in events:
        event_dict = {
            "event_type": event.event_type,
            "timestamp": event.timestamp,
            "user_identity": event.user_identity,
            "event_data": event.event_data
        }
        result.append(event_dict)

    # Return 404 if no results
    if not result:
        return jsonify({'message': 'No results found for the specified query.'}), 404
    return jsonify(result)


if __name__ == '__main__':
    app.run()
