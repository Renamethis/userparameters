from app import db

class User(db.Model):
    __tablename__ = 'users'
    query = db.session.query_property()
    username = db.Column(db.String(40), primary_key=True)
    def to_json(self):
        return {
            'Username': self.username,
        }

class Parameter(db.Model):
    __tablename__ = 'parameters'
    query = db.session.query_property()
    username = db.Column(db.String(40), db.ForeignKey(User.username), primary_key=True)
    parameterName = db.Column(db.String(40), nullable=False, primary_key=True)
    ptype = db.Column(db.String(10), nullable=False, unique=False, primary_key=True)
    value = db.Column(db.String(50), nullable=False, unique=False)
    def to_json(self):
        return {
            'Name': self.parameterName,
            'User': self.username,
            'Type': self.ptype,
            'Value': self.value
        }