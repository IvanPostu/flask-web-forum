from app import manager, db
from models import Role
from main import *  # noqa: F401, F403


@manager.command
def insert():
    db.session.add_all(Role.app_roles())
    db.session.commit()


if __name__ == '__main__':
    manager.run()
