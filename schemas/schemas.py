from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class LocationCreate(BaseModel):
    """Represents the data required to create a new location with categories."""
    name:           str = Field(..., description="Name of the location")
    latitude:       float = Field(..., description="Latitude coordinate of the location")
    longitude:      float = Field(..., description="Longitude coordinate of the location")
    category_ids:   list[int] = Field(..., description="List of existing category IDs to associate with this location")
    new_categories: list[str] = Field(default_factory=list, description="List of new category names to create and associate")
    rate:           float = Field(..., description="Rating of the location from 0.0 to 5.0")
    description:    str | None = Field(None, description="Optional description of the location")
    created_at:     datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the location was created")
    updated_at:     datetime | None = Field(None, description="Timestamp of the last update to the location (optional)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Universidad de Antioquia",
                "latitude": 6.25184,
                "longitude": -75.56359,
                "category_ids": [1],
                "new_categories": [],
                "rate": 4.5,
                "description": "Principal universidad pública de Antioquia",
                "created_at": "2025-07-24T03:37:16.406Z",
                "updated_at": "2025-07-24T03:37:16.406Z"
            }
        }
    }


class CategoryOut(BaseModel):
    """Represents the output format for a category."""
    id:   int = Field(..., description="Unique identifier of the category", example=1)
    name: str = Field(..., description="Name of the category", example="Museo")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Museo"
            }
        }
    }


class LocationSchema(BaseModel):
    """Basic location schema with associated categories."""
    id:         int = Field(..., description="Unique ID of the location")
    latitude:   float = Field(..., description="Latitude coordinate")
    longitude:  float = Field(..., description="Longitude coordinate")
    name:       str = Field(..., description="Name of the location")
    categories: list[CategoryOut] = Field(..., description="List of categories associated with the location")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "latitude": 6.25184,
                "longitude": -75.56359,
                "name": "Parque de los Deseos",
                "categories": [
                    {"id": 1, "name": "Parque"},
                    {"id": 2, "name": "Cultural"}
                ]
            }
        }


class LocationOut(BaseModel):
    """Represents the output format for a location with all fields."""
    id:          int = Field(..., description="Unique ID of the location")
    name:        str | None = Field(None, description="Name of the location")
    latitude:    float = Field(..., description="Latitude of the location")
    longitude:   float = Field(..., description="Longitude of the location")
    rate:        float = Field(0.0, description="Average rating for the location")
    description: str | None = Field(None, description="Optional description of the location")
    created_at:  datetime = Field(..., description="Timestamp when the location was created")
    updated_at:  datetime | None = Field(None, description="Timestamp when the location was last updated")
    categories:  list[CategoryOut] = Field(default_factory=list, description="List of associated categories")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Museo de Arte Moderno",
                "latitude": 6.235,
                "longitude": -75.575,
                "rate": 4.8,
                "description": "Museo dedicado al arte contemporáneo en Medellín",
                "created_at": "2025-07-24T03:37:16.406Z",
                "updated_at": "2025-07-24T03:37:16.406Z",
                "categories": [
                    {"id": 3, "name": "Museo"},
                    {"id": 4, "name": "Arte"}
                ]
            }
        }


class LocationCreateResponse(BaseModel):
    """Response returned after successfully creating a location."""
    location:    LocationSchema = Field(..., description="Created location details")
    categories:  list[CategoryOut] = Field(..., description="Categories already existing and linked")
    created_categories: list[str] = Field(..., description="Names of newly created categories")

    model_config = {
        "json_schema_extra": {
            "example": {
                "location": {
                    "id": 10,
                    "latitude": 6.2442,
                    "longitude": -75.5812,
                    "name": "Cerro Nutibara",
                    "categories": [{"id": 5, "name": "Turismo"}]
                },
                "categories": [{"id": 5, "name": "Turismo"}],
                "created_categories": ["Mirador"]
            }
        }
    }


class LocationUpdate(BaseModel):
    """Represents the data required to update an existing location."""
    name:        Optional[str] = Field(None, description="Name of the location")
    latitude:    Optional[float] = Field(None, description="Latitude")
    longitude:   Optional[float] = Field(None, description="Longitude")
    rate:        Optional[float] = Field(None, description="Rating of the location")
    description: Optional[str] = Field(None, description="Description")
    created_at:  Optional[datetime] = Field(None, description="When it was created")
    updated_at:  Optional[datetime] = Field(default_factory=datetime.utcnow, description="Last update")

    category_ids:   Optional[list[int]] = Field(default_factory=list, description="IDs of categories to associate")
    new_categories: Optional[list[str]] = Field(default_factory=list, description="New category names to create")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Universidad de Antioquia actualizado",
                "latitude": 6.25184,
                "longitude": -75.56359,
                "rate": 4.5,
                "description": "Principal universidad pública de Antioquia",
                "created_at": "2025-07-24T03:42:36.415783",
                "updated_at": "2025-07-24T03:42:36.415787",
                "category_ids": [1],
                "new_categories": []
            }
        }
    }


class CategoryCreate(BaseModel):
    """ Represents the data required to create a new category."""
    name: str = Field(..., description="name for the category")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Restaurante actualizado"
            }
        }
    }


class CategoryUpdate(BaseModel):
    """Data required to update a category."""
    name: str = Field(..., description="New name for the category")


class ReviewOut(BaseModel):
    """Represents the output format for a review recommendation."""
    location_id: int
    category_id: int
    last_reviewed: datetime | None
    was_reviewed: bool = Field(..., description="Indicates if the item was already reviewed")
    review_notes: str | None = Field(None, description="Optional notes from the last review")


class LocationCategoryCreate(BaseModel):
    """Represents the data required to associate a location with a category."""
    location_id: int
    category_id: int
    source: str | None = Field(None, description="Optional metadata on how the association was created")


class LocationCategoryOut(BaseModel):
    """Represents the output format for location-category association."""
    id: int
    location_id: int
    category_id: int
    created_at: datetime
    location_name: str | None = None
    category_name: str | None = None

    class Config:
        from_attributes = True


class RecommendationOut(BaseModel):
    """Represents a recommendation with location and category details."""
    id: int
    location_id: int
    category_id: int
    location_name: str | None
    category_name: str
    last_reviewed: datetime | None


class ReviewInput(BaseModel):
    """Input schema to submit a review of a location-category pair."""
    location_id: int
    category_id: int


class AsociationOut(BaseModel):
    """Represents the output format for an association between a location and a category."""
    id: int = Field(..., description="Unique identifier for the association")
    location_id: int = Field(..., description="ID of the associated location")
    category_id: int = Field(..., description="ID of the associated category")
    was_reviewed: bool | None = Field(default=False, description="Indicates if the association has been reviewed")
    last_reviewed: datetime | None = Field(None, description="Timestamp of the last review")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "location_id": 10,
                "category_id": 5,
                "was_reviewed": True,
                "last_reviewed": "2025-07-24T03:42:36.415787"
            }
        }
