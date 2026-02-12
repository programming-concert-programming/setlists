"""
Here, we store constants and other basic, shared elements: anything intended to be re-purposed.
Currently:
- Constants for user-specific details for which the below is a placeholder to be replaced with your details. Hints:
    - `SETLIST_FM_KEY`: Quickly and freely provided at [setlist.fm](https://api.setlist.fm/docs/1.0/index.html).
    - `SPOTIFY_KEY`: As before. This is optional, relevant only to tasks specific to the spotify API.
    - `USER_AGENT`: user agent info. Find yours at a site like [useragentstring.com](https://useragentstring.com/)
- Basic lists:
    - `default_band_list`: a sample default list of bands for example searches
    - `spotify_features`: the names of 9 features to retrieve from the spotify API for cross-reference.
"""

__author__ = "Mark Gotham"

from pathlib import Path
THIS_DIR = Path.cwd()

USER_AGENT = "put your details here ;)"
HEADERS = {"User-Agent": USER_AGENT}
PARSER = "html.parser"  # or "lxml" (preferred) or "html5lib", if installed

SETLIST_FM_KEY = "put your key here ;)"

SPOTIFY_ID = "put your ID here ;)"
SPOTIFY_SECRET = "put your secrets here ... only the Spotify ones though ... ;)"


default_band_id_dict = {
    "Bastille": "bastille-23def877",
    "Coldplay": "coldplay-3d6bde3",
    "FooFighters": "foo-fighters-bd6893a",
    "ImagineDragons": "imagine-dragons-5bd1b7fc",
    "Keane": "keane-bd6bdfa",
    "KingsOfLeon": "kings-of-leon-23d6985b",
    "Maroon5": "maroon-5-4bd6bfea",
    "Muse": "muse-53d6ebd5",
    "OneRepublic": "onerepublic-33d6bc51",
    "PanicAtTheDisco": "panic-at-the-disco-23d6bccb",
    "SnowPatrol": "snow-patrol-13d6bd05",
    "TheFray": "the-fray-53d6bfe9",
    "TheScript": "the-script-53d657dd",
    "ThirtySecondsToMars": "thirty-seconds-to-mars-5bd6e3e8",
    "Train": "train-7bd6b650",
    "Travis": "travis-1bd6bd10",
    "TwentyOnePilots": "twenty-one-pilots-7bd3caf0"
}


default_band_list = list(default_band_id_dict.keys())


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
