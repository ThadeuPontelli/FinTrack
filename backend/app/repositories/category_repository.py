from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import Category


class CategoryRepository:

    @staticmethod
    def create(
        db: Session,
        category: Category,
    ) -> Category:
        db.add(category)
        db.flush()
        db.refresh(category)

        return category

    @staticmethod
    def get_by_id(
        db: Session,
        category_id: int,
        user_id: int,
    ) -> Category | None:
        return db.scalar(
            select(Category).where(
                Category.id == category_id,
                Category.user_id == user_id,
            )
        )

    @staticmethod
    def get_all_by_user(
        db: Session,
        user_id: int,
    ) -> list[Category]:
        return list(
            db.scalars(
                select(Category)
                .where(Category.user_id == user_id)
                .order_by(Category.name)
            ).all()
        )

    @staticmethod
    def delete(
        db: Session,
        category: Category,
    ) -> None:
        db.delete(category)

    @staticmethod
    def exists_for_user(
        db: Session,
        category_id: int,
        user_id: int,
    ) -> bool:
        return (
            db.scalar(
                select(Category.id).where(
                    Category.id == category_id,
                    Category.user_id == user_id,
                )
            )
            is not None
        )
