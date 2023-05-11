import unittest
from fastapi.testclient import TestClient
from main import app


class PaymentGatewayTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        # Set up any test-specific configurations or data

    def test_process_payment_success_creditcard(self):
        # Test the successful payment processing for a credit card
        payload = {
            "amount": 100.0,
            "currency": "USD",
            "type": "creditcard",
            "card": {
                "number": "4111111111111111",
                "expirationMonth": "12",
                "expirationYear": "2023",
                "cvv": "123",
            },
        }

        response = self.client.post("/process_payment", json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")
        self.assertIsNotNone(response.json()["authorization_code"])

    def test_process_payment_success_debitcard(self):
        # Test the successful payment processing for a debit card
        payload = {
            "amount": 100.0,
            "currency": "USD",
            "type": "debitcard",
            "card": {
                "number": "4000056655665556",
                "expirationMonth": "12",
                "expirationYear": "2023",
                "cvv": "123",
            },
        }

        response = self.client.post("/process_payment", json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")
        self.assertIsNotNone(response.json()["authorization_code"])

    def test_process_payment_invalid_card_number_creditcard(self):
        # Test processing payment with an invalid credit card number
        payload = {
            "amount": 100.0,
            "currency": "USD",
            "type": "creditcard",
            "card": {
                "number": "1234567890123456",
                "expirationMonth": "12",
                "expirationYear": "2023",
                "cvv": "123",
            },
        }

        response = self.client.post("/process_payment", json=payload)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Invalid card number")

    def test_process_payment_expired_card_debitcard(self):
        # Test processing payment with an expired debit card
        payload = {
            "amount": 100.0,
            "currency": "USD",
            "type": "debitcard",
            "card": {
                "number": "4000056655665556",
                "expirationMonth": "05",
                "expirationYear": "2022",
                "cvv": "123",
            },
        }

        response = self.client.post("/process_payment", json=payload)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Card has expired")
        # Add more assertions to validate the error response

    def test_process_payment_insufficient_balance_creditcard(self):
        # Test processing payment with insufficient balance in a credit card
        payload = {
            "amount": 10000.0,
            "currency": "USD",
            "type": "creditcard",
            "card": {
                "number": "4111111111111111",
                "expirationMonth": "12",
                "expirationYear": "2023",
                "cvv": "123",
            },
        }

        response = self.client.post("/process_payment", json=payload)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["detail"], "Insufficient funds")

    def test_process_payment_insufficient_balance_debitcard(self):
        # Test processing payment with insufficient balance in a debit card
        payload = {
            "amount": 10000.0,
            "currency": "USD",
            "type": "debitcard",
            "card": {
                "number": "4000056655665556",
                "expirationMonth": "12",
                "expirationYear": "2023",
                "cvv": "123",
            },
        }

        response = self.client.post("/process_payment", json=payload)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["detail"], "Insufficient funds")

    def test_process_payment_invalid_credit_card_cvv(self):
        # Test invalid credit card payment with invalid CVV
        payload = {
            "amount": 100.0,
            "currency": "USD",
            "type": "creditcard",
            "card": {
                "number": "4111111111111111",
                "expirationMonth": 12,
                "expirationYear": 2023,
                "cvv": "999",
            },
        }

        response = self.client.post("/process_payment", json=payload)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Invalid CVV")


if __name__ == "__main__":
    unittest.main()
