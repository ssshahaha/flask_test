from crud.base import CRUDBase
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash


class CRUDUser(CRUDBase[User]):
    def get_user_by_name(self, user_name):
        with self.DB() as db:
            return db.query(User).filter(User.user_name == user_name).first()

    def check_password(self, user_password, password):
        return check_password_hash(user_password, password)

    def create_user(self, user_name, password):
        user_data = {'user_name': user_name, 'password': generate_password_hash(password)}
        self.create(user_data)


crud_user = CRUDUser(User)
