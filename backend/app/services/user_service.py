from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.models.user import User


class UserService:

    @staticmethod
    def create_user(
        db: Session,
        user_data: UserCreate,
    ) -> User:

        existing_user = UserRepository.get_by_email(
            db,
            user_data.email,
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered.",
            )

        hashed_password = hash_password(user_data.password)

        return UserRepository.create(
            db=db,
            name=user_data.name,
            email=user_data.email,
            hashed_password=hashed_password,
        )