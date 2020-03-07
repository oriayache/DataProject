from DataProject1 import app, db,login_manager
from flask_login import UserMixin

class user(db.Model,UserMixin ):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))

    def get_id(self):
        return self.id