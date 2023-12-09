from pydantic import BaseModel


class Location(BaseModel):
    lat: float
    lng: float


# Model for representing a place
class Place(BaseModel):
    id: str
    name: str
    lat: float
    lng: float
    address: str


class GPlace(BaseModel):
    id: str
    name: str
    lat: float
    lng: float
    address: str
    pass
