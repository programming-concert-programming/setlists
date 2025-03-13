"""
Here, we store constants and other basic, shared elements: anything intended to be re-purposed.
Currently:
- Constants for user-specific details for which the below is a placeholder to be replaced with your details. Hints:
    - `SETLIST_FM_KEY`: Quickly and freely provided at [setlist.net](https://api.setlist.fm/docs/1.0/index.html).
    - `SPOTIFY_KEY`: As before. This is optional, relevant only to tasks specific to the spotify API.
    - `USER_AGENT`: user agent info. Find yours at a site like [useragentstring.com](https://useragentstring.com/)
- Basic lists:
    - `default_band_list`: a sample default list of bands for example searches
    - `spotify_features`: the names of 9 features to retrieve from the spotify API for cross-reference.
"""

__author__ = ["Mark Gotham"]

from pathlib import Path
THIS_DIR = Path.cwd()

USER_AGENT = "put your details here ;)"
HEADERS = {"User-Agent": USER_AGENT}
PARSER = "html.parser"  # or "lxml" (preferred) or "html5lib", if installed

SETLIST_FM_KEY = "put your key here ;)"

SPOTIFY_ID = "put your ID here ;)"
SPOTIFY_SECRET = "put your secrets here ... only the Spotify ones though ... ;)"


default_band_list = [
    "Bastille",
    "Coldplay",
    "FooFighters",
    "ImagineDragons",
    "Keane",
    "KingsOfLeon",
    "Maroon5",
    "Muse",
    "OneRepublic",
    "PanicAtTheDisco",
    "SnowPatrol",
    "TheFray",
    "TheScript",
    "ThirtySecondsToMars",
    "Train",
    "Travis",
    "TwentyOnePilots",
]

spotify_features = [
    "danceability",
    "energy",
    "loudness",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo"
]
