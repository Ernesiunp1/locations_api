from db.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint, Boolean


class Location(Base):
    """Represents a geographical location with associated categories and review information."""
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    rate = Column(Float, default=0.0)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    location_categories = relationship("LocationCategoryReviewed", back_populates="location")
    categories = relationship("Category", secondary="location_category_reviewed", back_populates="locations",
                              overlaps="location_categories,category_locations")


class Category(Base):
    """Represents a category that can be associated with locations."""
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    category_locations = relationship("LocationCategoryReviewed", back_populates="category")
    locations = relationship("Location", secondary="location_category_reviewed", back_populates="categories",
                             overlaps="location_categories,category_locations")


class LocationCategoryReviewed(Base):
    """Represents the relationship between locations and categories, with review information."""
    __tablename__ = "location_category_reviewed"
    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    was_reviewed = Column(Boolean, default=False)
    last_reviewed = Column(DateTime, nullable=True)

    location = relationship("Location", back_populates="location_categories", overlaps="categories,locations")
    category = relationship("Category", back_populates="category_locations", overlaps="locations,categories")

    __table_args__ = (
        UniqueConstraint("location_id", "category_id", name="unique_location_category_pair"),
    )
