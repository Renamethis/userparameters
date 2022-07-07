from ..extensions import db

class User(db.Model):
    __tablename__ = 'users'
    query = db.session.query_property()
    username = db.Column(db.String(40), primary_key=True)
    def to_json(self):
        return {
            'username': self.username,
        }

class Parameter(db.Model):
    __tablename__ = 'parameters'
    query = db.session.query_property()
    parameterName = db.Column(db.String(40), nullable=False, primary_key=True)
    username = db.Column(db.String(40), db.ForeignKey(User.id), primary_key=True)
    ptype = db.Column(db.String(10), nullable=False, unique=False, primary_key=True)
    value = db.Column(db.String(50), nullable=False, unique=False)
    def to_json(self):
        return {
            'parameter_name': self.parameterName,
            'username': self.username,
            'ptype': self.type,
            'value': self.value
        }