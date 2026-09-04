from dataclasses import dataclass


@dataclass
class User:
    name: str
    email: str
    role: str = "admin"

    @property
    def is_admin(self):
        return self.role == "admin"
