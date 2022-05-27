
from . import db


class Event(db.Model):
    """
    Represents an event, which is a line in the `que-faire-a-paris-` dataset.
    Each field must have the same name as in the table.
    """

    id = db.Column(db.Integer, primary_key=True)

    title_event = db.Column(db.String(100))
    tags = db.Column(db.String(100))

    date_start = db.Column(db.Date())

    latitude = db.Column(db.Float(32))
    longitude = db.Column(db.Float(32))
