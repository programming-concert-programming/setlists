"""
Web scraping routines for setlist.fm's the pre-computed "average" setlist information.
This complements the more structured API calls elsewhere.
"""

__author__ = ["Mark Gotham", "Shujin Gan"]

from bs4 import BeautifulSoup
import pandas as pd
import re
from typing import Optional
from urllib.request import Request, urlopen
from urllib.error import HTTPError

# Constants
from utils import HEADERS, THIS_DIR, default_band_id_dict

BASE_URL = "https://www.setlist.fm"


def get_tour_ids(
        artist_id: str,
        headers: Optional[dict] = None
) -> list:
    """
    Extract tour IDs from the stats page of an artist
    (`https://www.setlist.fm/stats/{band_ID}.html`).

    Args:
    - artist_id (str): The ID of the artist.
    - headers (dict): The headers to include in the HTTP request.

    Returns:
    - list: A list of tour IDs.
    """
    if headers is None:
        headers = HEADERS

    target_url = f"{BASE_URL}/stats/{artist_id}.html"
    req = Request(url=target_url, headers=headers)

    try:
        resp = urlopen(req)
    except HTTPError as e:
        print(f"Error occurred: {e}")
        return []

    soup = BeautifulSoup(resp, "html.parser", from_encoding=resp.info().get_param("charset"))

    tour_ids = []
    for link in soup.find_all("a", href=True):
        pattern = r"\.\./stats/.*?tour=([^&]+)"
        match_results = re.search(pattern, link["href"], re.IGNORECASE)
        if match_results:
            tour_id = match_results.group(1)
            tour_ids.append(tour_id)
    return tour_ids


def get_tour_name(soup: BeautifulSoup) -> str:
    """
    Extract the tour name from the tour stats page.

    Args:
    - soup (BeautifulSoup): The parsed HTML of the tour stats page.

    Returns:
    - str: The tour name.
    """
    h1_tag = soup.find("h1")
    if h1_tag:
        tour_name = h1_tag.get_text(strip=True)
        tour_name = tour_name[26:]
        return tour_name
    else:
        return "No <h1> tag found."


def get_songs(soup: BeautifulSoup) -> list:
    """
    Extract the songs from the tour stats page.

    Args:
    - soup (BeautifulSoup): The parsed HTML of the tour stats page.

    Returns:
    - list: A list of songs.
    """
    pattern = r'<a\s+class="songLabel"\s+href="[^"]*"\s+title="[^"]*">([^<]+)</a>'
    matches = re.findall(pattern, str(soup))
    return matches


def run_one(
        artist_id: str = "coldplay-3d6bde3",
        artist_name: str = "Coldplay",
        headers: Optional[dict] = None
):
    if headers is None:
        headers = HEADERS

    tour_ids = get_tour_ids(artist_id, headers)

    tour_id_df = []
    songs = []
    tours = []

    for tour_id in tour_ids:
        target_url = f"{BASE_URL}/stats/average-setlist/{artist_id}.html?tour={tour_id}"
        req = Request(url=target_url, headers=headers)

        try:
            resp = urlopen(req)
        except HTTPError as e:
            print(f"Error occurred: {e}")
            continue

        soup = BeautifulSoup(resp, "html.parser", from_encoding=resp.info().get_param("charset"))

        tour_name = get_tour_name(soup)
        print("Tour Name:", tour_name)

        matches = get_songs(soup)
        for song_label in matches:
            tour_id_df.append(tour_id)
            songs.append(song_label)
            tours.append(tour_name)

    df = pd.DataFrame({
        "eventID": tour_id_df,
        "tour": tours,
        "song": songs
    })

    df.to_csv(THIS_DIR / "data" / f"{artist_name}_average_setlist.csv", index=False)


def run_all(band_dict: dict = default_band_id_dict) -> None:
    for k in band_dict:
        print(f"Now processing {k} ... ")
        run_one(band_dict[k], k)


if __name__ == "__main__":
    run_one()
