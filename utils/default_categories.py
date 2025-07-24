from sqlalchemy.orm import Session
from models.models import Category


def create_default_categories(db: Session):
    """Create default categories if they do not exist."""
    default_categories = [
        "Restaurante", "Museo", "Parque", "Hospital",
        "Escuela", "Centro Comercial", "Hotel", "Bar",
        "Gimnasio", "Supermercado"
    ]

    for cat_name in default_categories:
        existing = db.query(Category).filter(Category.name == cat_name).first()
        if not existing:
            db.add(Category(name=cat_name))
    db.commit()
