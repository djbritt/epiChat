import flask_sqlalchemy, app
import os

app.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://djbritt:db123!@localhost/postgres'
# postgresql://djbritt:db123!@localhost/postgres

db = flask_sqlalchemy.SQLAlchemy(app.app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True) # key
    message = db.Column(db.String(200))
    name = db.Column(db.String(200))
    pic = db.Column(db.String(1000))
    
    def __init__(self, m, n, p):
        self.message = m
        self.name = n
        self.pic = p
    
    def __repr__(self): # what's __repr__?
        return '%s %s %s' % (self.message, self.pic, self.name)
        
if __name__ == "__main__":
    messageQuery = Message.query.all()
    print messageQuery
            