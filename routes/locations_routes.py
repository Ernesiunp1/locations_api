from db.database import get_db
from fastapi import APIRouter
from models.models import Location, Category, LocationCategoryReviewed
from schemas.schemas import LocationSchema, LocationCreate, LocationOut
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session, selectinload
from fastapi import Depends


router = APIRouter(tags=["Locations"])


@router.post("/locations/", response_model=LocationSchema)
def create_new_location(location: LocationCreate, db: Session = Depends(get_db)):
    """Create a new location."""
    try:
        new_location = Location(
            latitude=location.latitude,
            longitude=location.longitude,
            name=location.name,
            rate=location.rate,
            description=location.description
        )
        db.add(new_location)
        db.commit()
        db.refresh(new_location)
        print("voy por aqui")
        # Asociar categorías existentes
        for category_id in location.category_ids:
            association = LocationCategoryReviewed(
                location_id=new_location.id,
                category_id=category_id
            )
            db.add(association)

        # Crear nuevas categorías si vienen en la solicitud
        for category_name in location.new_categories:
            existing = db.query(Category).filter(Category.name == category_name).first()
            if not existing:
                new_category = Category(name=category_name)
                db.add(new_category)
                db.commit()
                db.refresh(new_category)

                association = LocationCategoryReviewed(
                    location_id=new_location.id,
                    category_id=new_category.category_id
                )
                db.add(association)

        db.commit()
        return new_location

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Duplicate entry or constraint violation")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error while creating location")


@router.get("/list/locations", response_model=list[LocationOut])
def list_all_locations(db: Session = Depends(get_db)):
    """List all locations with their associated categories."""
    try:
        locations = db.query(Location).options(selectinload(Location.categories)).all()
        return locations
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while retrieving locations")


@router.get("/locations/{location_id}", response_model=LocationOut)
def get_location_by_id(location_id: int, db: Session = Depends(get_db)):
    """Get a specific location by ID."""
    try:
        location = db.query(Location).filter(Location.id == location_id).options(selectinload(Location.categories)).first()
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")
        return location
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while retrieving location")


@router.put("/locations/{location_id}", response_model=LocationSchema)
def update_location_by_id(location_id: int, location: LocationCreate, db: Session = Depends(get_db)):
    """Update a specific location by ID."""
    try:
        existing_location = db.query(Location).filter(Location.id == location_id).first()
        if not existing_location:
            raise HTTPException(status_code=404, detail="Location not found")

        existing_location.latitude = location.latitude
        existing_location.longitude = location.longitude
        existing_location.name = location.name
        existing_location.rate = location.rate
        existing_location.description = location.description

        # Limpiar relaciones previas
        db.query(LocationCategoryReviewed).filter(LocationCategoryReviewed.location_id == id).delete()

        # Asociar categorías nuevas
        for category_id in location.category_ids:
            association = LocationCategoryReviewed(
                location_id=existing_location.id,
                category_id=category_id
            )
            db.add(association)

        for category_name in location.new_categories:
            existing = db.query(Category).filter(Category.name == category_name).first()
            if not existing:
                new_category = Category(name=category_name)
                db.add(new_category)
                db.commit()
                db.refresh(new_category)

                association = LocationCategoryReviewed(
                    location_id=existing_location.id,
                    category_id=new_category.id
                )
                db.add(association)

        db.commit()
        db.refresh(existing_location)
        return existing_location

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid or duplicate data")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error while updating location")


@router.delete("/locations/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(location_id: int, db: Session = Depends(get_db)):
    """Delete a specific location by ID."""
    try:
        location = db.query(Location).filter(Location.id == location_id).first()
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")

        db.delete(location)
        db.commit()
        return  # No content (204)

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error while deleting location")
