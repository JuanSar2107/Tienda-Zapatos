from dataclasses import dataclass, field

from werkzeug.security import generate_password_hash, check_password_hash

from roles import ADMIN_ROLE, USER_ROLE, AVAILABLE_ROLES


@dataclass
class User:
    name: str
    email: str
    role: str = ADMIN_ROLE
    password_hash: str = field(default="", repr=False)

    def __post_init__(self):
        if self.role not in AVAILABLE_ROLES:
            raise ValueError(f"Rol no valido: {self.role}")

    @property
    def is_admin(self):
        return self.role == ADMIN_ROLE

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


_USERS_BY_EMAIL = {}


def get_user_by_email(email):
    return _USERS_BY_EMAIL.get(email.lower())


def create_user(name, email, password, role=USER_ROLE):
    email = email.lower()
    if email in _USERS_BY_EMAIL:
        raise ValueError("Ese correo ya esta registrado")

    user = User(name=name, email=email, role=role)
    user.set_password(password)
    _USERS_BY_EMAIL[email] = user
    return user


def get_cliente_actual():
    return User(name="Alex Rivera", email="cliente@pasofirme.com", role=USER_ROLE)
