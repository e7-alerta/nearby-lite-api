import time

from sqlalchemy import create_engine, Table, Column, String, MetaData, func
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import WKTElement, Geometry
from pydantic import BaseModel
from typing import List
import psycopg2

from model import Location, GPlace, Place

MAX_DISTANCE_DEGREES = 3 / 111.0

metadata = MetaData()

places_table = Table(
    'places',
    metadata,
    Column('id', String, primary_key=True, index=True),
    Column('name', String),
    Column('geopoint', Geometry(geometry_type='POINT', srid=4326)),
    Column('address', String(255)),
)

glaces_table = Table(
    'glaces',
    metadata,
    Column('id', String, primary_key=True, index=True),
    Column('name', String),
    Column('geopoint', Geometry(geometry_type='POINT', srid=4326)),
    Column('address', String(255)),
)

# Configure the database
SQLALCHEMY_DATABASE_URL = "postgresql://ave1:sdnadmin4@31.220.80.217:5432/ave1"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()  # Use SessionLocal directly here
# session database created
print("session database created")


# Model for representing nearby places
class NearbyGPlaces(BaseModel):
    places: List[GPlace]


# Model for representing nearby places
class NearbyPlaces(BaseModel):
    places: List[Place]


# Service layer for places
class PlacesService:
    @staticmethod
    def get_nearby_places(location):
        user_location = WKTElement(f'POINT({location.lng} {location.lat})', srid=4326)

        # traking query time
        started_at = time.time()
        nearby_places = (
            db.query(
                places_table.c.id,
                places_table.c.name,
                places_table.c.geopoint.ST_Y().label('latitude'),
                places_table.c.geopoint.ST_X().label('longitude'),
                places_table.c.address
            )
            .filter(func.ST_Distance(places_table.c.geopoint, user_location) < MAX_DISTANCE_DEGREES)
            .order_by(func.ST_Distance(places_table.c.geopoint, user_location))
            .limit(40)
            .all()
        )

        elapsed_time = time.time() - started_at
        print(f" {len(nearby_places)} store places.  query time: {elapsed_time} seconds")

        places_list = []
        for row in nearby_places:
            places_list.append(Place(
                id=f"{row.id}",
                name=row.name,
                lat=row.latitude,
                lng=row.longitude,
                address=row.address
            ))
        return NearbyPlaces(places=places_list)

    @staticmethod
    def get_nearby_gplaces(location):
        user_location = WKTElement(f'POINT({location.lng} {location.lat})', srid=4326)

        # traking query time
        started_at = time.time()
        nearby_places = (
            db.query(
                glaces_table.c.id,
                glaces_table.c.name,
                glaces_table.c.geopoint.ST_Y().label('latitude'),
                glaces_table.c.geopoint.ST_X().label('longitude'),
                glaces_table.c.address
            )
            .filter(func.ST_Distance(glaces_table.c.geopoint, user_location) < MAX_DISTANCE_DEGREES)
            .order_by(func.ST_Distance(glaces_table.c.geopoint, user_location))
            .limit(40)
            .all()
        )

        elapsed_time = time.time() - started_at
        print(f" {len(nearby_places)} google places.  query time: {elapsed_time} seconds")

        places_list = []
        for row in nearby_places:
            places_list.append(GPlace(
                id=f"{row.id}",
                name=row.name,
                lat=row.latitude,
                lng=row.longitude,
                address=row.address
            ))
        return NearbyGPlaces(places=places_list)


# Dependency to obtain a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Test the get_nearby_places method
def test_get_nearby_places():
    # Use a database session
    db = SessionLocal()  # Use SessionLocal directly here
    try:
        # Sample user location coordinates
        user_location = Location(
            lat=-34.4080186107827,
            lng=-58.7187521159649
        )
        nearby_places = PlacesService.get_nearby_places(db, user_location)

    finally:
        db.close()  # Make sure to close the session


# Run the test
if __name__ == "__main__":
    for i in range(1, 10):
        test_get_nearby_places()
