
from flask_login import LoginManager
from flask_security import current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, AdminIndexView
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, url_for, request, flash

from config import Configuration


app = Flask(__name__)
app.config.from_object(Configuration)

db: SQLAlchemy = SQLAlchemy(app)

migrate: Migrate = Migrate(app, db)
manager: Manager = Manager(app)
manager.add_command('db', MigrateCommand)


from models import Post, Tag, User, Role  # noqa: E402 F401


class AdminMixin:
    def is_accessible(self):
        return current_user.has_role(Role.admin().name)

    def inaccessible_callback(self, name, **kwargs):
        flash('This function is available only to the site administrator.')
        return redirect(url_for('auth.sign_in', next=request.url))


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


admin = Admin(app, 'FlaskApp', url='/', index_view=HomeAdminView(name='Home'))
admin.add_view(PostAdminView(Post, db.session))
admin.add_view(TagAdminView(Tag, db.session))


login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
