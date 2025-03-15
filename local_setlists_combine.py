"""
Routines for working with full setlist data and comparing these setlists across a tour.
"""

__author__ = "Mark Gotham"

import json
import matplotlib.pyplot as plt
from numpy import arange, linspace
import pandas as pd
from pathlib import Path

THIS_DIR = Path.cwd()


def setlist_2_song_list(
        setlist_data: dict
) -> list:
    """
    Given full setlist information,
    prune the trimmings, to return only a list of song names.

    Args:
        setlist_data (dict): The json dict for a setlist exactly as retrieved from setlist.fm.
    """
    songs = []
    for top_level_item in setlist_data:
        if "song" in top_level_item.keys():
            for song in top_level_item["song"]:
                songs.append(song["name"])
    return songs


def event_id_2_song_list(event_id: str = "1b94b560") -> list:
    """
    Retrieve full setlist data from a file at "setlists/{event_id}.json".
    Extract the list of songs in order, and return that alone.

    Args:
        event_id: a Valid setlist.fm event ID which corresponds to a file at "setlists/{event_id}.json".

    Returns:
        list
    """
    file_path = THIS_DIR / "setlists" / f"{event_id}.json"

    with open(file_path, "r") as file:
        data = json.load(file)
        return setlist_2_song_list(data)


def all_events_on_tour(
        artist_name: str,
        tour_name: str,
) -> list:
    """
    Get event IDs for every event in a tour, in order.
    """
    path_to_file = THIS_DIR / "data" / f"{artist_name}_event_date_tour_venue.csv"
    df = pd.read_csv(path_to_file, sep=",", engine="python")
    df.sort_values(by="date")
    return df.event_id[df.tour_name == tour_name]


def all_songlists_on_tour(
        artist_name: str,
        tour_name: str,
) -> list:
    """
    Retrieve the list of songs for every set on a named tour.
    """
    all_songlists = []
    event_ids = all_events_on_tour(artist_name, tour_name)
    for event_id in event_ids:
        songlist = event_id_2_song_list(event_id)
        all_songlists.append(songlist)
    return all_songlists


def plot_cross_tour_correspondence(
        artist_name: str,
        tour_name: str,
        proportional_position=True
) -> None:
    """
    Plot lists with correspondence.

    Args:
        artist_name (str): Valid artist name
        tour_name (str): Valid tour name. See `all_songlists_on_tour`
        proportional_position (bool, optional): Whether to use proportional position or the index. Defaults to True.
    """

    lists = all_songlists_on_tour(artist_name, tour_name)
    # Define the x-coordinates of the lists
    x_coords = arange(len(lists))

    # Create a dictionary to store the y-coordinates of each item
    y_coords = {}
    for i, lst in enumerate(lists):
        for j, item in enumerate(lst):
            if item not in y_coords:
                y_coords[item] = []
            if proportional_position:
                proportional_position_val = (j + 1) / (len(lst) + 1)
                y_coords[item].append((i, proportional_position_val))
            else:
                y_coords[item].append((i, j))

    plt.figure(figsize=(30, 10))

    for item, coords in y_coords.items():
        x = [x for x, _ in coords]
        y = [y for _, y in coords]
        plt.scatter(x, y, label=item)
        for i in range(len(coords) - 1):
            plt.plot(
                [coords[i][0], coords[i + 1][0]],
                [coords[i][1], coords[i + 1][1]],
                label=None,
                color="gray",
                alpha=0.5
            )

    plt.xticks(x_coords, [str(i + 1) for i in range(len(lists))])  # 1-index

    if proportional_position:
        plt.ylim(0, 1)
        plt.yticks(
            linspace(0, 1, 11),
            [f"{int(p * 100)}%" for p in linspace(0, 1, 11)]
        )
    else:
        plt.ylim(-1, max(len(lst) for lst in lists))
        plt.yticks(arange(max(len(lst) for lst in lists)),
                   [f"Item {i + 1}" for i in range(max(len(lst) for lst in lists))])

    # plt.legend()
    plt.tight_layout()

    plt.savefig(THIS_DIR / "plots" / f"{artist_name}_{tour_name}_cross_tour.pdf")


if __name__ == "__main__":
    plot_cross_tour_correspondence(
        "Coldplay",
        "Music of the Spheres",
        proportional_position=True
    )
