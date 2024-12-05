from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


def setup_admin(app, db):
    from model import (
        Users,
        Request
    )

    admin = Admin(app, url="/database")

    admin.add_view(ModelView(Users, db.session))
    admin.add_view(ModelView(Request, db.session))