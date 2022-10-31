class Driver (db.model):
  __tablename__ = 'drivers'
  id = db.Column(db.Integer, primary_key=True)
  ...
  vehicles = db.relationship ('Vehicle', backref='drivers', lazy=True)


class Vehicle (db.model):
  __tablename__ = 'vehicles'
  id = db.Column(db.Integer, primary_key=True)
  make = db.Column(db.String(), nullable=False)
  ...
  driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=False)