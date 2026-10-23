import unittest
from app import app

class TestApp(unittest.TestCase):
    def test_health(self):
        r = app.test_client().get("/api/health")
        self.assertEqual(r.status_code, 200)

if __name__ == "__main__":
    unittest.main()

