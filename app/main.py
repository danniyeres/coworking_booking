from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db import init_db
from app.routers.users.routes import router as users_router
from app.routers.locations.routes import router as locations_router
from app.routers.rooms.routes import router as rooms_router
from app.routers.bookings.routes import router as bookings_router
from app.routers.payments.routes import router as payments_router
from app.routers.reviews.routes import router as reviews_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Coworking API", lifespan=lifespan)

app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(locations_router, prefix="/locations", tags=["Locations"])
app.include_router(rooms_router, prefix="/rooms", tags=["Rooms"])
app.include_router(bookings_router, prefix="/bookings", tags=["Bookings"])
app.include_router(payments_router, prefix="/payments", tags=["Payments"])
app.include_router(reviews_router, prefix="/reviews", tags=["Reviews"])
