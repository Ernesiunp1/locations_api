from pydantic import BaseModel, Field
from datetime import datetime


class CategoryOut(BaseModel):
    """Represents the output format for a category."""
    id: int
    name: str

    class Config:
        from_attributes = True


class LocationSchema(BaseModel):
    id: int
    latitude: float
    longitude: float
    name: str
    categories: list[CategoryOut]

    class Config:
        from_attributes = True


class LocationOut(BaseModel):
    """Represents the output format for a location."""
    id: int
    name: str | None = None
    latitude: float
    longitude: float
    rate: float = 0.0
    description: str | None = None
    created_at: datetime
    updated_at: datetime | None = None
    categories: list[CategoryOut] = []

    class Config:
        from_attributes = True


class LocationCreate(BaseModel):
    """Represents the data required to create a new location with categories."""
    name: str
    latitude: float
    longitude: float
    category_ids: list[int]  # IDs
    new_categories: list[str] = []  # name of new categories to create
    rate: float
    description: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = None


class LocationCreateResponse(BaseModel):
    """Response when creating a location."""
    location: LocationSchema
    categories: list[CategoryOut]
    created_categories: list[str]


class CategoryCreate(BaseModel):
    """ Represents the data required to create a new category."""
    name: str


class ReviewOut(BaseModel):
    """ Represents the output format for a review recommendation."""
    location_id: int
    category_id: int
    last_reviewed: datetime | None


class LocationCategoryCreate(BaseModel):
    """Represents the data required to associate a location with a category."""
    location_id: int
    category_id: int


class LocationCategoryOut(BaseModel):
    """Represents the output format for location-category association."""
    id: int
    location_id: int
    category_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class RecommendationOut(BaseModel):
    """Represents a recommendation with location and category details."""
    location_id: int
    category_id: int
    location_name: str | None
    category_name: str
    last_reviewed: datetime | None


class ReviewInput(BaseModel):
    location_id: int
    category_id: int