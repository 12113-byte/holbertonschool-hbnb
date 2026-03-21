# Import the base Repository interface (
from app.persistence.repository import Repository

# Import SQLAlchemy instance here
from app import db


class SQLAlchemyRepository(Repository):
  
    #SQLAlchemy implementation of the Repository pattern.

    #This replaces the in-memory storage and uses a real database
    #via SQLAlchemy ORM.
    

    def __init__(self, model):
        
        #Initialize repository with a specific model.
        self.model = model  # Store model class (User, Place, etc.)

    def add(self, obj):
        
        #Add a new object to the database.
        db.session.add(obj)       # Stage object for insert
        db.session.commit()       # Save changes to database

    def get(self, obj_id):
       
        return self.model.query.get(obj_id)

    def get_all(self):
       
        return self.model.query.all()

    def update(self, obj_id, data):
       
        #Update an existing object. 
        obj = self.get(obj_id)

        if obj:
            # Loop through fields and update dynamically
            for key, value in data.items():
                setattr(obj, key, value)

            db.session.commit()  # Save updates

        return obj

    def delete(self, obj_id):
        
        #Delete an object from the database.
        obj = self.get(obj_id)

        if obj:
            db.session.delete(obj)
            db.session.commit()

        return obj

    def get_by_attribute(self, attr_name, attr_value):
       
        #Retrieve object by a specific attribute.
        return self.model.query.filter_by(**{attr_name: attr_value}).first()
