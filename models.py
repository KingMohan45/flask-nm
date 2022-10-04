from flask_sqlalchemy import SQLAlchemy

from core import app

db=SQLAlchemy(app)

#creating of the model
class Todo(db.Model):
    __tablename__ = 'todo_list'

    id= db.Column(db.Integer(), primary_key=True)
    task = db.Column(db.String(100))
    is_complete =db.Column(db.Boolean())
    create_at = db.Column(db.DateTime(), default=db.func.now())
    update_at = db.Column(db.DateTime(), default=db.func.now(), onupdate=db.func.now())

    def serialize(self):
        """
        Returns the object data in easily serializeable format
        """
        
        return {
            'id': self.id,
            'task': self.task,
            'is_complete': self.is_complete,
            'create_at': self.create_at,
            'update_at': self.update_at
        }