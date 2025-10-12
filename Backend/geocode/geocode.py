from __future__ import annotations

import os
import time
import uuid
from typing import Dict, Tuple, List

import httpx

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "AIzaSyDupqg3HPeQuhG5M8YaIFou9Vi0d27CKgQ")

GEOCODE_TTL = 24 * 60 * 60
PLACES_TTL  = 6  * 60 * 60

_geo_cache: Dict[Tuple[float, float], Tuple[float, dict]] = {}
_ac_cache:  Dict[Tuple[str, str, str], Tuple[float, List[dict]]] = {}
_pd_cache:  Dict[str, Tuple[float, dict]] = {}

def _alive(ts: float, ttl: float) -> bool:
    return (time.time() - ts) < ttl

def _k(lat: float, lng: float) -> Tuple[float, float]:
    return (round(lat, 3), round(lng, 3))

def _cache_get_geocode(lat: float, lng: float):
    v = _geo_cache.get(_k(lat, lng))
    if v and _alive(v[0], GEOCODE_TTL):
        return v[1]
    return None

def _cache_set_geocode(lat: float, lng: float, val: dict):
    _geo_cache[_k(lat, lng)] = (time.time(), val)

def _get_component(res: dict, *types: str) -> str:
    for comp in res.get("address_components", []):
        t = comp.get("types", [])
        if any(tt in t for tt in types):
            return comp.get("long_name") or comp.get("short_name") or ""
    return ""

def _extract_suburb(res: dict) -> str:
    return (
        _get_component(res, "locality")
        or _get_component(res, "sublocality", "sublocality_level_1")
        or _get_component(res, "administrative_area_level_2")
        or (res.get("formatted_address", "").split(",")[0] if res.get("formatted_address") else "")
    )


async def reverse_geocode_service(lat: float, lng: float, language: str = "en") -> dict:
    if not API_KEY:
        return {"suburbName": "", "state": "", "postcode": "", "confidence": 0.0, "source": "google", "error": "no_api_key"}

    cached = _cache_get_geocode(lat, lng)
    if cached:
        return cached

    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "latlng": f"{lat},{lng}",
        "key": API_KEY,
        "result_type": "locality|sublocality|administrative_area_level_2",
        "language": language or "en",
    }

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(url, params=params)
    except httpx.RequestError as e:
        return {"suburbName": "", "state": "", "postcode": "", "confidence": 0.0, "source": "google", "error": str(e)}

    if r.status_code != 200:
        return {"suburbName": "", "state": "", "postcode": "", "confidence": 0.0, "source": "google", "error": f"http {r.status_code}"}

    data = r.json()
    if data.get("status") != "OK" or not data.get("results"):
        resp = {"suburbName": "", "state": "", "postcode": "", "confidence": 0.0, "source": "google"}
        _cache_set_geocode(lat, lng, resp)
        return resp

    res = data["results"][0]
    suburb   = _extract_suburb(res)
    state    = _get_component(res, "administrative_area_level_1")
    postcode = _get_component(res, "postal_code")
    conf = 0.95 if (suburb and _get_component(res, "locality")) else (0.8 if suburb else 0.6)

    resp = {"suburbName": suburb, "state": state, "postcode": postcode, "confidence": conf, "source": "google"}
    _cache_set_geocode(lat, lng, resp)
    return resp

async def places_autocomplete_service(q: str, country: str = "AU", limit: int = 8, language: str = "en") -> dict:
    if not API_KEY or not q or len(q.strip()) < 2:
        return {"suggestions": []}

    key = (q.strip().lower(), country.upper(), language or "en")
    v = _ac_cache.get(key)
    if v and _alive(v[0], PLACES_TTL):
        return {"suggestions": v[1][:limit]}

    url = "https://maps.googleapis.com/maps/api/place/autocomplete/json"
    params = {
        "input": q,
        "key": API_KEY,
        "language": language or "en",
        "components": f"country:{country}",
        "types": "geocode",
        "sessiontoken": str(uuid.uuid4()),
    }

    suggestions: List[dict] = []
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(url, params=params)
        if r.status_code == 200:
            data = r.json()
            for p in data.get("predictions", []):
                pid = p.get("place_id")
                desc = p.get("description") or ""
                if pid:
                    suggestions.append({"label": desc, "place_id": pid})
    except httpx.RequestError:
        suggestions = []

    _ac_cache[key] = (time.time(), suggestions)
    return {"suggestions": suggestions[:limit]}

async def place_details_service(place_id: str, language: str = "en") -> dict:
    if not API_KEY or not place_id:
        return {"name": "", "lat": None, "lng": None}

    v = _pd_cache.get(place_id)
    if v and _alive(v[0], PLACES_TTL):
        return v[1]

    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "key": API_KEY,
        "language": language or "en",
        "fields": "geometry/location,name,formatted_address"
    }

    out = {"name": "", "lat": None, "lng": None}
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(url, params=params)
        if r.status_code == 200:
            data = r.json()
            if data.get("status") == "OK":
                result = data.get("result") or {}
                loc = (result.get("geometry") or {}).get("location") or {}
                out = {
                    "name": result.get("name") or result.get("formatted_address") or "",
                    "lat": loc.get("lat"),
                    "lng": loc.get("lng"),
                }
    except httpx.RequestError:
        out = {"name": "", "lat": None, "lng": None}

    _pd_cache[place_id] = (time.time(), out)
    return out

async def places_find_service(q: str, country: str = "AU", language: str = "en") -> dict:
    ac = await places_autocomplete_service(q=q, country=country, limit=1, language=language)
    if not ac.get("suggestions"):
        return {"name": "", "lat": None, "lng": None}
    pid = ac["suggestions"][0]["place_id"]
    return await place_details_service(place_id=pid, language=language)
