from sqlalchemy import Column, String, Boolean
from werkzeug.security import check_password_hash

from db.base_class import Base


class User(Base):
    user_name = Column(String(64), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    is_delete = Column(Boolean(), default=False, nullable=False)

    def check_password(self, password):
        return check_password_hash(self.password, password)
