from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.exc import SAWarning

from db.database import engine, Base, get_db
from routes.general_routes import router as crud_router
from routes.locations_routes import router as locations_router
from routes.categories_routes import router as categories_router
from utils.default_categories import create_default_categories
from fastapi.middleware.cors import CORSMiddleware
from db.database import create_tables
import warnings

warnings.filterwarnings("ignore", category=SAWarning)

app = FastAPI(title="Map My World Rest API",
              description="A simple FastAPI Rest API with CRUD operations and default categories. includes"
                          " graphical map interface for testing.",
              version="1.0.0",
              contact={
                  "name": "Ernesto Vivas",
                  "url": "https://www.linkedin.com/in/ernesto-vivas-cede%C3%B1o-a5707834/",
                  "email": "vivas.ernesto@gmail.com",
              },
              license_info={
                  "name": "MIT",
                  "url": "https://opensource.org/licenses/MIT",
              },
              docs_url="/docs",  # URL para Swagger UI
              redoc_url="/redoc",  # URL para ReDoc (alternativa a Swagger)
              openapi_url="/openapi.json",  # URL del esquema OpenAPI

              )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)

# adding routers
app.include_router(crud_router)
app.include_router(locations_router)
app.include_router(categories_router)


@app.on_event("startup")
def startup_event():
    """Create default categories on startup."""
    db = next(get_db())
    create_default_categories(db)
    create_tables()
