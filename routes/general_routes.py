from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, selectinload
from db.database import get_db
from fastapi import HTTPException, Request, APIRouter, Depends, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from utils.fresh_recommendations import get_fresh_recommendations
from models.models import Location, Category, LocationCategoryReviewed
from schemas.schemas import LocationSchema, CategoryCreate, LocationCreate, CategoryOut, RecommendationOut
from schemas.schemas import ReviewInput

router = APIRouter(tags=["Generals"])


templates = Jinja2Templates(directory="templates")


# main route (server map)
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


@router.post("/reviews/", response_model=dict)
def mark_location_as_reviewed(data: ReviewInput, db: Session = Depends(get_db)):
    """Mark a location-category combination as reviewed."""
    try:
        association = db.query(LocationCategoryReviewed).filter(
            LocationCategoryReviewed.location_id == data.location_id,
            LocationCategoryReviewed.category_id == data.category_id).first()

        if not association:
            raise HTTPException(status_code=400, detail="Location-Category association not found")

        association.last_reviewed = datetime.utcnow()
        db.commit()

        return {
            "status": "success",
            "message": "Marked as reviewed successfully"
        }

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error while marking as reviewed")


@router.get("/recommendations/", response_model=list[RecommendationOut])
def get_recommendations_needs_review(db: Session = Depends(get_db)):
    """Get 10 location-category combinations that need review."""
    try:
        return get_fresh_recommendations(db)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while retrieving recommendations")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
