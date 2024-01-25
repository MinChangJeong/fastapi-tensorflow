from fastapi import FastAPI
from sound.sound_routes import sound_router
from stats.stats_routes import stats_router


app = FastAPI()

# Include routers from different modules
app.include_router(sound_router, prefix="/sound", tags=["sound"])
app.include_router(stats_router, prefix="/stats", tags=["stats"])