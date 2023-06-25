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
- To run the unittests simply do python run.py after ensuring the Flask App is running
