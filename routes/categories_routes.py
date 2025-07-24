from db.database import get_db
from models.models import Category
from sqlalchemy.orm import Session
from schemas.schemas import CategoryCreate, CategoryOut
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import APIRouter, Depends, status, HTTPException


router = APIRouter(tags=["Categories"])


@router.post("/categories/", response_model=CategoryCreate)
def create_new_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """Add a new category."""
    new_category = Category(name=category.name)

    try:
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Category with this name already exists")

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while creating the category")


@router.get("/list/categories/", response_model=list[CategoryOut])
def list_all_categories(db: Session = Depends(get_db)):
    """List all categories."""
    try:
        categories = db.query(Category).all()
        if not categories:
            raise HTTPException(status_code=404, detail="No categories found")
        return categories
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error occurred while retrieving categories")


@router.get("/categories/{category_id}", response_model=CategoryOut)
def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    """Get a specific category by ID."""
    try:
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while retrieving category")


@router.put("/categories/{category_id}", response_model=CategoryOut)
def update_category_by_id(category_id: int, updated: CategoryCreate, db: Session = Depends(get_db)):
    """Update a specific category by ID."""
    try:
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        category.name = updated.name
        db.commit()
        db.refresh(category)
        return category

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Category with this name already exists")

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error while updating category")


@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Delete a specific category by ID."""
    try:
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        db.delete(category)
        db.commit()
        return  # 204 No Content → no body

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error while deleting category")
