"""
Script to request information from the MusicBrainz API
with a valid pair of endpoint and query.
"""

__author__ = "Mark Gotham"

import requests
import json
from utils import MUSICBRAINZ_BASE_URL
from utils import MUSICBRAINZ_HEADER  # NB: enter yours there

ENDPOINT = f"{MUSICBRAINZ_BASE_URL}/recording"

headers = {
    "User-Agent": MUSICBRAINZ_HEADER
}


def song_metadata_from_recording(
        song_title: str = None,
        artist: str = None,
        album_title: str = None,
) -> dict:
    """
    Fetches structured metadata from MusicBrainz API using the "recording" endpoint.
    Specify song title, album title, artist,
    or any combination.

    Args:
        song_title (str): Song title. Optional
        artist (str): Artist name. Optional
        album_title (str): Album title. Optional
    Returns:
        dict
    """

    query = []
    if song_title: query.append(f"title:{song_title}")
    if artist: query.append(f"artist:{artist}")
    if album_title: query.append(f"title:{album_title}")

    if len(query) == 0:
        raise ValueError("No query argument specified. Must have at least one.")
    elif len(query) == 1:
        pass
    else: # => 2
        query = " AND ".join(query)

    params = {
        "query": query,
        "fmt": "json",
        "limit": 1,
        "offset": 0
    }

    try:
        response = requests.get(ENDPOINT, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Extract first match (if exists)
        if "recordings" in data and data["recordings"]:
            return {
                "recording": data["recordings"][0],
                "search_query": params["query"]
            }
        return {"error": "No matching recording found."}

    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}


if __name__ == "__main__":
    # Demo:
    result = song_metadata_from_recording(
        song_title="Yellow",
        artist="Coldplay",
        album_title="Parachutes"
    )
    print(json.dumps(result, indent=2))