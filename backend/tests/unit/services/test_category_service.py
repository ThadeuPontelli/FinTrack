from unittest.mock import MagicMock, patch

from app.models.category import Category
from app.schemas.category import CategoryCreate
from app.services.category_service import CategoryService


def test_create_category():
    db = MagicMock()

    category_data = CategoryCreate(
        name="Alimentação",
        description="Gastos com alimentação",
    )

    with patch(
        "app.services.category_service.CategoryRepository.create"
    ) as repository_create:
        category = CategoryService.create_category(
            db=db,
            category_data=category_data,
            user_id=1,
        )

    assert category.name == "Alimentação"
    assert category.description == "Gastos com alimentação"
    assert category.user_id == 1

    repository_create.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(category)


def test_get_category():
    db = MagicMock()
    category = Category(
        id=1,
        name="Alimentação",
        description="Gastos com alimentação",
        user_id=1,
    )

    with patch(
        "app.services.category_service.CategoryRepository.get_by_id",
        return_value=category,
    ) as repository_get:
        result = CategoryService.get_category(
            db=db,
            category_id=1,
            user_id=1,
        )

    assert result == category

    repository_get.assert_called_once_with(
        db,
        1,
        1,
    )


def test_get_user_categories():
    db = MagicMock()

    categories = [
        Category(
            id=1,
            name="Alimentação",
            user_id=1,
        ),
        Category(
            id=2,
            name="Transporte",
            user_id=1,
        ),
    ]

    with patch(
        "app.services.category_service.CategoryRepository.get_all_by_user",
        return_value=categories,
    ) as repository_get:
        result = CategoryService.get_user_categories(
            db=db,
            user_id=1,
        )

    assert result == categories

    repository_get.assert_called_once_with(
        db,
        1,
    )


def test_delete_category():
    db = MagicMock()

    category = Category(
        id=1,
        name="Alimentação",
        user_id=1,
    )

    with patch(
        "app.services.category_service.CategoryRepository.get_by_id",
        return_value=category,
    ), patch(
        "app.services.category_service.CategoryRepository.delete"
    ) as repository_delete:
        result = CategoryService.delete_category(
            db=db,
            category_id=1,
            user_id=1,
        )

    assert result is True

    repository_delete.assert_called_once_with(
        db=db,
        category=category,
    )

    db.commit.assert_called_once()


def test_delete_category_returns_false_when_not_found():
    db = MagicMock()

    with patch(
        "app.services.category_service.CategoryRepository.get_by_id",
        return_value=None,
    ):
        result = CategoryService.delete_category(
            db=db,
            category_id=999,
            user_id=1,
        )

    assert result is False
    db.commit.assert_not_called()