"""
Setlist.fm provides some venue data, but not the capacity.
We find this with a complementary webscrape of Wikipedia,
finding the relevant Wikipedia page on Setlist.fm.
"""

__author__ = ["Mark Gotham", "Shujin Gan"]

from bs4 import BeautifulSoup
import pandas as pd
import re
import requests
import time
from typing import Optional
from urllib.request import urlopen, Request


from utils import HEADERS, PARSER, SETLIST_FM_KEY, THIS_DIR


def send_request(
        url: str,
        headers: Optional[dict] = None,
        parser: Optional[str] = None
) -> BeautifulSoup:
    """
    Send an HTTP request and parse the HTML response.

    Args:
        url (str): The URL to send the request to.
        headers (Optional[dict]): The headers to include in the request. Defaults to None.
        parser (Optional[str]): The parser to use for the HTML. Defaults to None.

    Returns:
        BeautifulSoup: The parsed HTML response.
    """
    if headers is None:
        headers = HEADERS
    if parser is None:
        parser = PARSER

    request = Request(url=url, headers=headers)
    response = urlopen(request)
    return BeautifulSoup(response, parser, from_encoding=response.info().get_param("charset"))


def get_venue_url(
        venue_id: str,
        api_key: Optional[str] = None
) -> str:
    """
    Get the URL of a venue from Setlist.fm.

    Args:
        venue_id (str): A valid Setlist.fm venue ID.
        api_key (Optional[str]): A valid Setlist.fm API key. Defaults to None.

    Returns:
        str: The Setlist.fm URL of the venue.
    """
    if api_key is None:
        api_key = SETLIST_FM_KEY

    url = f"https://api.setlist.fm/rest/1.0/venue/{venue_id}"
    headers = {"Accept": "application/json", "x-api-key": api_key}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data["url"]


def get_wikipedia_page(url: str) -> Optional[str]:
    """
    Get the Wikipedia page URL from a Setlist.fm venue page.

    Args:
        url (str): The URL of the Setlist.fm venue page.

    Returns:
        Optional[str]: The URL of the Wikipedia page, or None if not found.
    """
    soup = send_request(url)
    div_info = soup.find("div", class_="info")
    if div_info is None:
        return None

    links = div_info.find_all("a")
    urls = [link["href"] for link in links if link.has_attr("href")]

    for link_url in urls:
        if "wikipedia.org" in link_url:
            print(f"{link_url} ... found and added.")
            return link_url
        else:
            print(f"{link_url} ... non-wiki site, ignoring...")
    return None


def get_capacity_from_wikipedia(url: Optional[str]) -> Optional[int]:
    """
    Get the capacity data from a Wikipedia page.
    This is slightly hacky but seems to work in practice.

    For example, on https://en.wikipedia.org/wiki/Millennium_Stadium,
    the numbers in the table, include capacity values of
    "73,931 for rugby union and football" and "78,000 for boxing".

    Taking the larger of these seems reasonable as
    most concerts will be set up more like boxing,
    in the sense that concerts need a stage more similar in size to a boxing ring
    than to a large playing field.

    That these numbers also include footnote number is a weakness,
    though that should only be a problem in cases where there are thousands of footnotes
    ... which seems unlikely ;)

    Args:
        url (Optional[str]): The URL of the Wikipedia page.

    Returns:
        Optional[int]: The capacity of the venue, or None if not found.
    """
    if url is None:
        return None

    soup = send_request(url)
    th_capacity = soup.find("th", string="Capacity")
    if th_capacity is None:
        return None

    td_capacity = th_capacity.find_next_sibling("td", class_="infobox-data")
    if td_capacity is None:
        return None

    td_capacity_text = td_capacity.get_text(strip=True)
    numbers_only = re.findall(r"\d{1,3}(?:,\d{3})*", td_capacity_text)

    if not numbers_only:
        return None

    numbers_only = [int(number.replace(",", "")) for number in numbers_only]

    return max(numbers_only)


def main(artist_name: str = "Test"):
    """
    Get the capacity data for venues and save it to a CSV file.

    Args:
        artist_name (str, optional): The name of the artist. Defaults to "Test".
    """
    base_path = THIS_DIR / "data"
    in_csv = base_path / f"{artist_name}_event_date_tour_venue.csv"
    df = pd.read_csv(in_csv, sep=",", engine="python")

    venue_df = pd.DataFrame()

    capacity_list = []
    venue_ids = []
    venue_urls = []
    venue_names = []

    sleep_time = 2.5  # seconds

    for _, row in df.iterrows():
        print(f'Processing venue ID: {row["venue_id"]}')
        time.sleep(sleep_time)

        venue_ids.append(row["venue_id"])
        venue_names.append(row["venue_name"])

        url = get_venue_url(row["venue_id"])
        venue_urls.append(url)
        print(url)

        try:
            wikipedia_url = get_wikipedia_page(url)
            result = get_capacity_from_wikipedia(wikipedia_url)
            capacity_list.append(result)
        except requests.exceptions.RequestException as e:
            print(f"RequestException error: {e}")
            capacity_list.append(None)
        except Exception as e:
            print(f"Unexpected error: {e}")
            capacity_list.append(None)

    venue_df["capacity"] = capacity_list
    venue_df["venue_id"] = venue_ids
    venue_df["url"] = venue_urls
    venue_df["venue_name"] = venue_names

    print(venue_df)

    out_csv = base_path / f"{artist_name}_venue_capacity.csv"
    venue_df.to_csv(out_csv, index=False)


if __name__ == "__main__":
    main()
