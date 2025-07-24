from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, selectinload
from db.database import get_db
from fastapi import HTTPException, Request, APIRouter, Depends, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from utils.fresh_recommendations import get_fresh_recommendations
from models.models import Location, Category, LocationCategoryReviewed
from schemas.schemas import LocationSchema, CategoryCreate, LocationCreate, CategoryOut, RecommendationOut, \
    AsociationOut
from schemas.schemas import ReviewInput


router = APIRouter(tags=["Generals"])

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def serve_map(request: Request, db: Session = Depends(get_db)):
    """Serve the main map page with categories(Render the sandbox)"""
    try:
        categories = db.query(Category).all()
        return templates.TemplateResponse("map.html", {
            "request": request,
            "categories": categories
        })

    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while loading map page")


@router.post("/mark/reviews/")
def mark_location_as_reviewed(data: ReviewInput, db: Session = Depends(get_db)):
    """Mark a specific location-category combination as reviewed."""
    try:
        association = db.query(LocationCategoryReviewed).filter(
            LocationCategoryReviewed.location_id == data.location_id,
            LocationCategoryReviewed.category_id == data.category_id).first()

        if not association:
            raise HTTPException(status_code=400, detail="Location-Category association not found")

        association.last_reviewed = datetime.utcnow()
        association.was_reviewed = True
        db.commit()

        return {"message": "Location-category combination marked as reviewed successfully",
                "location_id": data.location_id,
                "category_id": data.category_id}

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error while marking as reviewed")


@router.get("/reviews/pending", response_model=list[AsociationOut])
def get_pending_reviews(db: Session = Depends(get_db)):
    """Get up to 10 location-category combinations pending review.
    (less strictly, and client info friendly that /recommendations/reviews")"""
    threshold = datetime.utcnow() - timedelta(days=30)

    subquery = db.query(LocationCategoryReviewed).filter(
        (LocationCategoryReviewed.was_reviewed == False) |
        (LocationCategoryReviewed.last_reviewed < threshold)
    ).order_by(
        LocationCategoryReviewed.was_reviewed.asc(),  # priority never reviewed
        LocationCategoryReviewed.last_reviewed.asc()  # then by last reviewed date
    ).limit(10).all()

    return subquery


@router.get("/recommendations/reviews", response_model=list[RecommendationOut])
def get_recommendations_needs_review(db: Session = Depends(get_db)):
    """Get 10 location-category combinations that need review.
    (more strictly, and client info friendly that /reviews/pending)"""
    try:
        return get_fresh_recommendations(db)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while retrieving recommendations")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
