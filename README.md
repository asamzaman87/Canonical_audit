# EventLogger: Real-Time Audit Log Microservice

EventLogger is a Python-based microservice built with Flask and SQLAlchemy for real-time recording and querying of diverse event data from various systems. It leverages PostgreSQL's native JSON support for efficient data handling of both invariant and event-specific content. The service is also secured with basic HTTP authentication.

## Features

- **Event Recording**: The service can accept and record a wide range of event data from various sources, making it highly versatile and adaptable. It uses a flexible data model that accommodates a common set of fields, as well as fields that are specific to each event type.

- **Event Querying**: Provides an HTTP endpoint for querying recorded event data by field values. The service can handle complex queries and return relevant data swiftly and accurately.

- **Security**: Employs basic HTTP authentication to ensure the integrity and confidentiality of the event data, thereby securing event submission and query endpoints.

## Technologies Used
- Flask
- SQLAlchemy
- PostgreSQL
- Python

## Future Improvements
While the service is fully functional and robust, future revisions can improve its usability and versatility, including:
- Enhancing security by replacing basic HTTP authentication with OAuth2 or token-based authentication.
- Handling database migrations separately.
- Externalizing configuration to environment variables or configuration files.



# Canonical_audit

To deploy the code using a single command:
- chmod +x deploy.sh
- ./deploy.sh

Instructions for testing the solution using CURL:

- Assuming your Flask application is running on localhost:5000
  
curl -X POST -u admin:secret -H "Content-Type: application/json" -d '{
    "event_type": "old_account",
    "user_identity": "Asad_Zaman",
    "event_data": {
        "account_id": 1346,
        "email": "john.doe@example.com"
    }
}' http://localhost:5000/events

- You should get notified of the event being created, now to access the event via a query

curl -X GET -u admin:secret "http://localhost:5000/events/query?user_identity=Asad_Zaman"

- You should get the stored event as the output
- Note: I used a local Postgres database to store the events
- To run the unittests simply do python test.py after ensuring the Flask App is running
- For requirements.txt: pip install -r requirements.txt
- main.py, which is in the app directory, has the main code

