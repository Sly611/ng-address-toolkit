import json
from pathlib import Path
from functools import lru_cache

DATA_DIR = Path(__file__).parent / "data"

@lru_cache(maxsize=1)
def _load(filname: str) -> dict:
    with open(DATA_DIR / filname, encoding="utf-8") as file:
        return json.load(file)
    
def get_states() -> list:
    """
    Return a list of all Nigerian states.
    :rtype: list
    """
    return _load("states.json")


def get_lgas() -> list:
    """
    Return a list of all Local Government Areas (LGAs).
    :rtype: list
    """
    return _load("lgas.json")


def get_wards() -> list:
    """
    Return a list of all wards.
    :rtype: list
    """
    return _load("wards.json")


def get_towns() -> list:
    """
    Return a list of all towns and settlements.
    :rtype: list
    """
    return _load("towns.json")


def get_lgas_by_state(state_code: str) -> list:
    """
    Return all LGAs belonging to a given state.

    :param state_code: Two-letter state code (e.g. "LA", "AB")
    :type state_code: str
    :rtype: list
    """
    state_code = state_code.upper()
    return [lga for lga in get_lgas() if lga["state_code"] == state_code]


def get_wards_by_lga(lga_key: str) -> list:
    """
    Return all wards belonging to a given LGA.

    :param lga_key: LGA key (e.g. "ikeja")
    :type lga_key: str
    :rtype: list
    """
    lga_key = lga_key.lower()
    return [ward for ward in get_wards() if ward["lga_key"] == lga_key]


def search(query: str, level: str = "all") -> list:
    """
    Search for locations by name using simple substring matching (case-insensitive).

    Note: This is not a fuzzy search. Spelling must be accurate.
    For example, "ikej" will not match "Ikeja".

    :query: Search term
    :type query: str
    :level: Level to search in. Options: "all", "state", "lga", "ward", "town"
    :type level: str
    :return: List of matching location dictionaries
    :rtype: list
    """
    if not query or not query.strip():
        raise ValueError("Search query cannot be empty")

    level = level.lower().strip()
    valid_levels = {"all", "state", "lga", "ward", "town"}

    if level not in valid_levels:
        raise ValueError(
            f"Invalid level '{level}'. Valid options are: {', '.join(sorted(valid_levels))}"
        )

    query = query.lower().strip()
    results = []

    if level in ("all", "state"):
        results.extend(
            [s for s in get_states() if query in s["name"].lower()]
        )

    if level in ("all", "lga"):
        results.extend(
            [l for l in get_lgas() if query in l["name"].lower()]
        )

    if level in ("all", "ward"):
        results.extend(
            [w for w in get_wards() if query in w["name"].lower()]
        )

    if level in ("all", "town"):
        results.extend(
            [t for t in get_towns() if query in t["name"].lower()]
        )

    return results