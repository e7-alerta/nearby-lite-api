import json

from pydantic import BaseModel
from typing import List, Optional


class GeoPoint(BaseModel):
    type: str
    coordinates: List[float]


class Place(BaseModel):
    id: str
    status: str
    date_created: str
    date_updated: str
    geopoint: GeoPoint
    address: Optional[str]
    city: Optional[str]
    district: Optional[str]
    region: Optional[str]
    subregion: Optional[str]
    postal_code: Optional[str]
    street: Optional[str]
    street_number: Optional[int]
    country: Optional[str]
    name: Optional[str]
    country_code: Optional[str]
    district: Optional[str]
    city: Optional[str]
    region: Optional[str]
    subregion: Optional[str]
    country: Optional[str]
    alerted: Optional[bool]
    photo: Optional[str]


def place_loads(data_dict: str) -> Place:
    data_dict["district"] = data_dict["raw_district"]
    data_dict["city"] = data_dict["raw_city"]
    data_dict["region"] = data_dict["raw_region"]
    data_dict["subregion"] = data_dict["raw_subregion"]
    data_dict["country"] = ""  # data_dict["raw_country"]
    # geo_point_obj = GeoPoint(**data_dict["geopoint"])
    place_obj = Place(**data_dict)
    return place_obj


def place_dumps(place: Place) -> str:
    return json.dumps(place.dict(), indent=4)


class GooglePlace(BaseModel):
    status: str
    name: Optional[str]
    placeId: Optional[str]
    reference: Optional[str]
    geopoint: GeoPoint
    address: Optional[str]
    street: Optional[str]
    streetNumber: Optional[int]
    district: Optional[str]
    region: Optional[str]
    subregion: Optional[str]
    country: Optional[str]
    photoRef: Optional[str]
    photo: Optional[str]


#    labels: Optional[List[str]]


def gplace_loads(data_dict: str) -> GooglePlace:
    data_dict["placeId"] = data_dict["place_id"]
    data_dict["photo"] = data_dict["photo"]
    data_dict["streetNumber"] = data_dict["street_number"]
    data_dict["reference"] = ""
    data_dict["district"] = ""
    data_dict["photoRef"] = ""
    data_dict["country"] = ""

    place_obj = GooglePlace(**data_dict)
    return place_obj
