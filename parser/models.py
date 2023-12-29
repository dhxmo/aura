from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


# TODO: port to a local sqlite instance

class Assistant(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    assistant_id = db.Column(db.String(50))
    thread_id = db.Column(db.String(50))

    user_id = db.Column(db.String(50), nullable=False)
