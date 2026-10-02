import logging

from sqlalchemy.orm import Session

from app.models.category import Category
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate

logger = logging.getLogger(__name__)


class CategoryService:

    @staticmethod
    def create_category(
        db: Session,
        category_data: CategoryCreate,
        user_id: int,
    ) -> Category:
        logger.info(
            "Creating category for user_id=%s, name=%s",
            user_id,
            category_data.name,
        )

        category = Category(
            name=category_data.name,
            description=category_data.description,
            user_id=user_id,
        )

        CategoryRepository.create(
            db,
            category,
        )

        db.commit()
        db.refresh(category)

        logger.info(
            "Category created successfully: category_id=%s, user_id=%s",
            category.id,
            user_id,
        )

        return category

    @staticmethod
    def get_category(
        db: Session,
        category_id: int,
        user_id: int,
    ) -> Category | None:
        return CategoryRepository.get_by_id(
            db,
            category_id,
            user_id,
        )

    @staticmethod
    def get_user_categories(
        db: Session,
        user_id: int,
    ) -> list[Category]:
        return CategoryRepository.get_all_by_user(
            db,
            user_id,
        )

    @staticmethod
    def delete_category(
        db: Session,
        category_id: int,
        user_id: int,
    ) -> bool:
        category = CategoryRepository.get_by_id(
            db=db,
            category_id=category_id,
            user_id=user_id,
        )

        if category is None:
            return False

        logger.info(
            "Deleting category: category_id=%s, user_id=%s",
            category_id,
            user_id,
        )

        CategoryRepository.delete(
            db=db,
            category=category,
        )

        db.commit()

        logger.info(
            "Category deleted successfully: category_id=%s, user_id=%s",
            category_id,
            user_id,
        )

        return True