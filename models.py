# models.py
from app import db


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    players_present = db.Column(db.Integer, nullable=False)
    level_present = db.Column(db.String(50), nullable=False)
    level_required = db.Column(db.String(50), nullable=False)
    pitch_address = db.Column(db.String(200), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    rental_price = db.Column(db.Float, nullable=False)
    is_full = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return f"<Match {self.id}: {self.pitch_address} on {self.date_time}>"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(50), nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey("match.id"), nullable=False)
    match = db.relationship("Match", backref=db.backref("players", lazy=True))

    def __repr__(self):
        return f"<Player {self.id}: {self.name} (Level: {self.level})>"
