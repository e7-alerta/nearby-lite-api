from fastapi import requests

from requests import Response
import requests

from dash.types import place_loads, gplace_loads


def get_glaces(ids: list[str]):

    # url = "http://31.220.80.217:8055/items/gplaces"
    # url = "http://127.0.0.1:5070/items/glaces"
    url = "http://31.220.80.217:8055/items/glaces"
    payload = ""
    querystring = {
        "filter[id][_in]": ",".join(ids),
        "limit": "20"
    }
    response = requests.request("GET", url, data=payload, params=querystring)
    data = response.json()["data"]
    # map data to model
    places = []
    for item in data:
        place = gplace_loads(item)
        places.append(
            place
        )
    return places


def get_places(ids: list[str]):

    url = "http://31.220.80.217:8055/items/places"
    payload = ""
    querystring = {
        "filter[id][_in]": ",".join(ids),
        "limit": "20"
    }
    response = requests.request("GET", url, data=payload, params=querystring)
    data = response.json()["data"]
    # map data to model
    places = []
    for item in data:
        place = place_loads(item)
        places.append(
            place
        )
    return places
