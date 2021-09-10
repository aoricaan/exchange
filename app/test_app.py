from unittest import TestCase
from fastapi.testclient import TestClient
from app import app


class Test(TestCase):
    def test_exchange(self):
        client = TestClient(app.app)
        response = client.get("/exchange", headers={'Authorization': 'Bearer token'})
        self.assertEqual(response.status_code, 200)
        response = response.json()
        self.assertIn('rates', response)
        self.assertIsInstance(response['rates'], dict)
        self.assertIn('diario_oficial_de_la_federacion', response['rates'])
        self.assertIn('fixer', response['rates'])
        self.assertIn('banxico', response['rates'])



