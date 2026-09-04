from dataclasses import dataclass

from roles import ADMIN_ROLE, AVAILABLE_ROLES


@dataclass
class User:
    name: str
    email: str
    role: str = ADMIN_ROLE

    def __post_init__(self):
        if self.role not in AVAILABLE_ROLES:
            raise ValueError(f"Rol no valido: {self.role}")

    @property
    def is_admin(self):
        return self.role == ADMIN_ROLE
