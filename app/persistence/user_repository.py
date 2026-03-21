from app.models.user import User
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):

    def __init__(self):
        # Pass User model to parent class
        super().__init__(User)

    def get_user_by_email(self, email):
        
        # find user by email.
        return self.model.query.filter_by(email=email).first()
