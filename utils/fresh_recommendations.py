from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.models import LocationCategoryReviewed, Location, Category
from schemas.schemas import RecommendationOut
from sqlalchemy.orm import aliased
from sqlalchemy import or_


def get_fresh_recommendations(db: Session):
    threshold = datetime.utcnow() - timedelta(days=30)

    # Subconsulta: combinaciones revisadas en los últimos 30 días
    recent_reviews = db.query(
        LocationCategoryReviewed.location_id,
        LocationCategoryReviewed.category_id
    ).filter(
        LocationCategoryReviewed.last_reviewed >= threshold
    ).subquery()

    # Aliases para evitar conflicto al usar LocationCategoryReviewed varias veces
    LCR = aliased(LocationCategoryReviewed)
    Loc = aliased(Location)
    Cat = aliased(Category)

    # Consulta principal: combinaciones no revisadas recientemente
    results = db.query(
        LCR.location_id,
        LCR.category_id,
        Loc.name.label('location_name'),
        Cat.name.label('category_name'),
        LCR.last_reviewed
    ).join(Loc, LCR.location_id == Loc.id) \
     .join(Cat, LCR.category_id == Cat.id) \
     .outerjoin(recent_reviews, (LCR.location_id == recent_reviews.c.location_id) &
                               (LCR.category_id == recent_reviews.c.category_id)) \
     .filter(recent_reviews.c.location_id.is_(None)) \
     .order_by(LCR.last_reviewed.asc().nulls_first()) \
     .limit(10).all()

    return [
        RecommendationOut(
            location_id=r.location_id,
            category_id=r.category_id,
            location_name=r.location_name,
            category_name=r.category_name,
            last_reviewed=r.last_reviewed
        ) for r in results
    ]
