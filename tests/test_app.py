import unittest
from app import create_app, db
from app.models import FitnessClass
from app.utils import ist_to_utc

class BookingAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()
            # Seed test data
            cls = FitnessClass(
                name="Test Yoga",
                datetime_utc=ist_to_utc("2025-07-01 10:00"),
                instructor="Test Alice",
                available_slots=2
            )
            db.session.add(cls)
            db.session.commit()
            self.class_id = cls.id

    def test_get_classes(self):
        response = self.client.get('/classes')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(isinstance(data, list))

    def test_book_success(self):
        payload = {
            "class_id": self.class_id,
            "client_name": "Tester",
            "client_email": "tester@example.com"
        }
        response = self.client.post('/book', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn("booking_id", response.get_json())

    def test_get_bookings(self):
        # Book first
        self.client.post('/book', json={
            "class_id": self.class_id,
            "client_name": "Tester",
            "client_email": "tester@example.com"
        })
        # Then get bookings
        response = self.client.get('/bookings?email=tester@example.com')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.get_json()) > 0)

if __name__ == '__main__':
    unittest.main()
