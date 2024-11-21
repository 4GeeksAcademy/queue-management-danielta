from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    phone = db.Column(db.Integer, unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "phone": self.phone
            # do not serialize the password, its a security breach
        }
    
class Queue:

    def __init__(self):
        self._queue = []
        # depending on the _mode, the queue has to behave like a FIFO or LIFO
        self._mode = 'FIFO'

    def enqueue(self, contact):
        self._queue.append(contact)
        return None
    
    def skip_the_line(self, contact):
        self._queue.insert(0, contact)
        return contact
    
    def dequeue(self):
        contact = self._queue.pop(0)
        return contact
            
    def get_queue(self):
        return self._queue
    
    def leave_queue(self, phone):
        for i in range(0,len(self._queue)):
            if self._queue[i]['phone'] == phone:
                contact = self._queue.pop(i)
                return contact
    
    def size(self):
        return len(self._queue) 