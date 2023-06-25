import unittest
from datetime import datetime
from main import app, db, Event


class EventAPITestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:abc123@localhost/Canonical'
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.auth_headers = {
            'Authorization': 'Basic YWRtaW46c2VjcmV0'  # Base64 encoding of 'admin:secret'
        }
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_event(self):
        event_type = 'test_event'
        user_identity = 'test_user'
        event_data = {'field1': 'value1', 'field2': 'value2'}

        response = self.app.post('/events', json={
            'event_type': event_type,
            'user_identity': user_identity,
            'event_data': event_data
        }, headers=self.auth_headers)

        self.assertEqual(response.status_code, 200)

        with app.app_context():
            event = Event.query.filter_by(event_type=event_type, user_identity=user_identity).first()
            self.assertIsNotNone(event)
            self.assertEqual(event.event_type, event_type)
            self.assertEqual(event.user_identity, user_identity)
            self.assertEqual(event.event_data, event_data)

    def test_create_event_missing_fields(self):
        response = self.app.post('/events', json={}, headers=self.auth_headers)
        self.assertEqual(response.status_code, 400)

    def test_query_events(self):
        event_type = 'test_event'
        user_identity = 'test_user'
        event_data = {'field1': 'value1', 'field2': 'value2'}
        event = Event(event_type=event_type, timestamp=datetime.now(), user_identity=user_identity,
                      event_data=event_data)
        with app.app_context():
            db.session.add(event)
            db.session.commit()

        response = self.app.get('/events/query?user_identity=test_user', headers=self.auth_headers)

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['event_type'], event_type)
        self.assertEqual(data[0]['user_identity'], user_identity)
        self.assertEqual(data[0]['event_data'], event_data)

    def test_query_events_no_results(self):
        response = self.app.get('/events/query?user_identity=test_user', headers=self.auth_headers)
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
