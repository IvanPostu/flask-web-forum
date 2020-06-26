
from flask_login import LoginManager
from flask_security import current_user, LoginForm
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, AdminIndexView
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, url_for, request
from dotenv import load_dotenv


import os
from config import Configuration

APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)


app = Flask(__name__)
app.config.from_object(Configuration)

db: SQLAlchemy = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from models import Post, Tag, User, Role  # noqa: E402 F401


class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        return super(BaseModelView, self).on_model_change(form, model, is_created)


class AdminView(AdminMixin, ModelView):
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    pass


class PostAdminView(AdminMixin, BaseModelView):
    form_columns = ['title', 'body', 'tags']


class TagAdminView(AdminMixin, BaseModelView):
    form_columns = ['name', 'posts']


class CustomLoginForm(LoginForm):

    def validate(self):
        # Put code here if you want to do stuff before login attempt
        response = super(CustomLoginForm, self).validate()

        # Put code here if you want to do stuff after login attempt

        return response


admin = Admin(app, 'FlaskApp', url='/', index_view=HomeAdminView(name='Home'))
admin.add_view(PostAdminView(Post, db.session))
admin.add_view(TagAdminView(Tag, db.session))


login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# user_datastore: SQLAlchemyUserDatastore = SQLAlchemyUserDatastore(
#     db, User, Role)
# security = Security(app, user_datastore, login_form=CustomLoginForm)


# role = Role.query.first()
# user = User.query.first()

# role_is_added: bool = user_datastore.add_role_to_user(user, role)

# print(role_is_added)
