import os
from typing import List, Type

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

import dash.api
from dash.types import Place, GooglePlace
from error import Duplicate, Missing
from model import Location

from service import PlacesService as service

router = APIRouter(prefix="/near")


@router.get("/gplaces")
def get_gplaces(
        lat: float,
        lng: float
) -> list[GooglePlace]:
    raw_gplaces = service.get_nearby_gplaces(Location(lat=lat, lng=lng)).places
    ids = [gplace.id for gplace in raw_gplaces]
    # split ids in chunks of 5
    chunks = [ids[x:x + 20] for x in range(0, len(ids), 20)]
    # get places from dash
    gplaces = []
    for chunk in chunks:
        gplaces += dash.api.get_glaces(chunk)
    return gplaces


@router.get("/places")
def get_places(
        lat: float,
        lng: float
) -> list[Place]:
    raw_places = service.get_nearby_places(Location(lat=lat, lng=lng)).places
    ids = [place.id for place in raw_places]
    # split ids in chunks of 5
    chunks = [ids[x:x + 20] for x in range(0, len(ids), 20)]
    # get places from dash
    places = []
    for chunk in chunks:
        places += dash.api.get_places(chunk)
    return places
