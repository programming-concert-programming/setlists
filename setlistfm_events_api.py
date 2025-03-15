"""
Given a valid API key (see `utils.py`), retrieve setlist.fm data.
"""

__author__ = ["Mark Gotham", "Shujin Gan"]

from pathlib import Path
from typing import Union, Optional

THIS_DIR = Path.cwd()

from utils import SETLIST_FM_KEY

import json
import pandas as pd
import requests
import time
import numpy as np


def get_event_data(
        event_id: str,
        api_key: Optional[str] = None
) -> Optional[dict]:
    """
    Given a valid setlist.fm event_id, return the event data.
    Call the Setlist.fm API, get the.json formatted data.
    """
    if api_key is None:
        api_key = SETLIST_FM_KEY
    url = f"https://api.setlist.fm/rest/1.0/setlist/{event_id}"
    headers = {"Accept": "application/json", "x-api-key": api_key}
    r = requests.get(url, headers=headers)
    return r.json()


def extract_event_date(event_data: dict) -> list:
    """
    Extract the event date and year from the event data.
    """
    date = event_data.get("eventDate", "")
    if date:
        year = date[6:]  # dd-MM-YYYY format
    else:
        year = ""
    return [date, year]


def extract_tour_name(event_data: dict) -> Union[str, float]:
    """
    Extract the tour name from the event data.
    """
    tour = event_data.get("tour")
    if tour:
        return tour["name"]
    else:
        return np.nan


def extract_venue_data(event_data: dict) -> list:
    """
    Extract the venue id and name from the event data.
    """
    venue = event_data["venue"]
    return [venue["id"], venue["name"]]


def process_event_ids(
        event_ids: list,
        write_full_sets: bool = True
) -> dict:
    """
    Process a list of event ids and return a dictionary with the results.
    In the case of failure with one event ID, print a note (rather than raising an error)
    and continue to later items on the list.

    Args:
        event_ids (list): A list of valid setlist.fm event IDs.
        write_full_sets (bool): If true, as well as
            writing event-level data to a csv in the "data" directory, also
            dump full set information to separate .json files in the "setlists" directory.

    """
    results = {
        "event_id": [],
        "date": [],
        "year": [],
        "tour_name": [],
        "venue_id": [],
        "venue_name": []
    }

    for event_id in event_ids:

        print(f"Processing event id: {event_id}")
        time.sleep(3)

        try:
            event_data = get_event_data(event_id)
        except:
            print(f"Failed to retrieve data for event {event_id}")
            continue

        if write_full_sets:
            try:
                with open(THIS_DIR / "setlists" / f"{event_id}.json", "w") as f:
                    json.dump(event_data['sets']['set'], f, indent=4)
            except:
                print(f"Failed to retrieve full setlist data for event {event_id}")
                continue

        date, year = extract_event_date(event_data)
        tour_name = extract_tour_name(event_data)
        venue_id, venue_name = extract_venue_data(event_data)
        results["event_id"].append(event_id)
        results["date"].append(date)
        results["year"].append(year)
        results["tour_name"].append(tour_name)
        results["venue_id"].append(venue_id)
        results["venue_name"].append(venue_name)
    return results


def export_to_csv(
        results: dict,
        filename: str
) -> None:
    """
    Export the results to a csv file.

    Args:
        results (dict): Dictionary containing the results to export.
        filename (str): The name of the output file.
            Please note that the path (where to write the csv to) is hard-coded to the "data" directory.
            Only the name is variable.
    """
    df = pd.DataFrame(results)
    out_path = THIS_DIR / "data" / filename
    df.to_csv(out_path, index=False)


def load_event_ids_from_csv(
        filename: Union[Path, str] = THIS_DIR / "distinct_setlist_IDs" / "Test.csv"
) -> list:
    """
    Load event ids from a csv file.

    Args:
        filename (str): Name of the csv file to load from (default: "event_dates.csv").

    Returns:
        list: List of event ids loaded from the csv file.
    """
    df = pd.read_csv(filename, sep=",", engine="python")
    return df["eventID"].unique()


def main(band_name: str = "Test") -> None:
    """
    Main function to process event ids and export results to csv files.

    This function loads event ids from a csv file
    located at `distinct_setlist_IDs/{band_name}.csv`
    retrieves data for those events using the Setlist.fm API,
    and exports the results to csv files.
    """
    event_ids = load_event_ids_from_csv(THIS_DIR / "distinct_setlist_IDs" / f"{band_name}.csv")
    results = process_event_ids(event_ids)
    export_to_csv(results, f"{band_name}_event_date_tour_venue.csv")


if __name__ == "__main__":
    main(band_name = "Test")
