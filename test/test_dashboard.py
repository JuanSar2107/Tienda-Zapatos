import os
import tempfile
import unittest

from app import create_app
from auth import db
from auth.models import User
from config import Config
from roles import ADMIN_ROLE, USER_ROLE


class DashboardTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")

        class TestConfig(Config):
            TESTING = True
            SQLALCHEMY_DATABASE_URI = "sqlite:///" + self.db_path

        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            admin = User(nombre="Alex Rivera", email="admin@pasofirme.com", role=ADMIN_ROLE)
            admin.set_password("clave123")
            cliente = User(nombre="Cliente Prueba", email="cliente@pasofirme.com", role=USER_ROLE)
            cliente.set_password("clave123")
            db.session.add_all([admin, cliente])
            db.session.commit()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def login(self, email, password):
        return self.client.post(
            "/login",
            data={"email": email, "password": password},
            follow_redirects=True,
        )

    def test_dashboard_requires_login(self):
        response = self.client.get("/", follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Iniciar sesión".encode(), response.data)

    def test_admin_login_loads_admin_dashboard(self):
        self.login("admin@pasofirme.com", "clave123")
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Los mas vendidos del mes", response.data)
        self.assertIn(b"Zapatito Estiloso", response.data)

    def test_client_login_redirects_to_tienda(self):
        response = self.login("cliente@pasofirme.com", "clave123")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Productos", response.data)
        self.assertNotIn(b"Los mas vendidos del mes", response.data)

    def test_client_cannot_access_admin_dashboard(self):
        self.login("cliente@pasofirme.com", "clave123")
        response = self.client.get("/", follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"Los mas vendidos del mes", response.data)


if __name__ == "__main__":
    unittest.main()
