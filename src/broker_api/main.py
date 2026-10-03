from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from broker_api.routes import geolocation, devices, health

app = FastAPI(title='Geo Api')
app.include_router(geolocation.router)
app.include_router(devices.router)
app.include_router(health.router)
app.mount("/map", StaticFiles(directory="src/broker_api/static", html=True), name="map")