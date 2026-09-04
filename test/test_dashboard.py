import unittest

from app import create_app


class DashboardTestCase(unittest.TestCase):
    def test_dashboard_loads(self):
        app = create_app()
        response = app.test_client().get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Los mas vendidos del mes", response.data)
        self.assertIn(b"Zapatito Estiloso", response.data)


if __name__ == "__main__":
    unittest.main()
