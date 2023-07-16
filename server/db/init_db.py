from crud import crud_user


def init_db():
    # init admin user
    user = crud_user.get_user_by_name('admin')
    if user:
        if not user.check_password('admin'):
            crud_user.remove(user)
    else:
        crud_user.create_user('admin', 'admin')
