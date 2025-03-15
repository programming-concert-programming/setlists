"""
Routines for retrieving track and album information from the Spotify API
from an existing data frame that includes song names.

Note:
We had prepared functionality for additionally getting audio features from the Spotify API.
It is no longer possible to access these features from the Spotify API;
the functionality has recently been deprecated (between our starting to prepare this topic and now writing these words).
Such is the fragility of some APIs.
The code is available on request (but is ... frankly ... worthless).
"""

__author__ = ["Mark Gotham", "Shujin Gan"]


import numpy as np
import pandas as pd
import spotipy
import time

from utils import default_band_list, SPOTIFY_ID, SPOTIFY_SECRET, THIS_DIR


def authenticate_spotify() -> spotipy.Spotify:
    """
    Authenticate with Spotify using client credentials.
    See imports above and notes in utils; add client details there.

    Returns:
        spotipy.Spotify: An authenticated Spotify client.
    """
    return spotipy.Spotify(
        auth_manager=spotipy.oauth2.SpotifyClientCredentials(
            client_id=SPOTIFY_ID,
            client_secret=SPOTIFY_SECRET
        )
    )


def load_data(artist: str) -> pd.DataFrame:
    """
    Load setlist data for a given artist from a CSV file

    Constraints:
    The module expects the csv to contain a "song" column.

    This function hard codes a search by first
    trying to access a file at "data" / f"{artist}_setlist.csv"
    and (failing that) one at "data" / f"{artist}_average_setlist.csv"
    only.

    Args:
        artist (str): The name of the artist.

    Returns:
        pd.DataFrame: A DataFrame containing the setlist data.
    """
    option_1 = THIS_DIR / "data" / f"{artist}_setlist.csv"
    option_2 = THIS_DIR / "data" / f"{artist}_average_setlist.csv"

    if option_1.exists():
        return pd.read_csv(option_1, sep=",", engine="python")
    elif option_2.exists():
        return pd.read_csv(option_2, sep=",", engine="python")
    else:
        raise ValueError(f"The file {option_1} does not exist")


def get_unique_tracks(df: pd.DataFrame) -> list:
    """
    Get a list of unique tracks from a DataFrame containing a "song" column.

    Args:
        df (pd.DataFrame): A DataFrame containing setlist data.

    Returns:
        list: A list of unique tracks.
    """
    return df["song"].unique().tolist()


def search_track(sp: spotipy.Spotify, track: str, artist: str) -> tuple:
    """
    Search for a track on Spotify.

    Args:
        sp (spotipy.Spotify): An authenticated Spotify client.
        track (str): The name of the track to search for.
        artist (str): The name of the artist to search for.

    Returns:
        tuple: A tuple containing the track name and ID.
    """
    search_result = sp.search(q=f"{track} {artist}", type="track", limit=1)
    if len(search_result["tracks"]["items"]) == 0:
        return np.nan, np.nan
    else:
        return search_result["tracks"]["items"][0]["name"], search_result["tracks"]["items"][0]["id"]


def get_track_data(
        artist: str,
        tracks: list,
        sp: spotipy.Spotify = authenticate_spotify(),
        write: bool = True
) -> pd.DataFrame:
    """
    Save track data to a CSV file.

    Args:
        artist (str): The name of the artist.
        tracks (list): A list of unique tracks.
        sp (spotipy.Spotify): An authenticated Spotify client.
        write: Write the data to a local csv.

    Returns:
        pd.DataFrame: A DataFrame containing track data.
    """

    track_data = {
        "track": [],
        "found": [],
        "id": []
    }
    for track in tracks:
        track_name, track_id = search_track(sp, track, artist)
        track_data["track"].append(track)
        track_data["found"].append(track_name)
        track_data["id"].append(track_id)
    df = pd.DataFrame(track_data)

    track_df = THIS_DIR / "data" / f"{artist}_tracks.csv"

    if write:
        df.to_csv(track_df, index=False)

    return df


def get_album_data(
        artist: str,
        df: pd.DataFrame,
        sp: spotipy.Spotify = authenticate_spotify(),
        write: bool = True
) -> pd.DataFrame:
    """
    Get album data for a given DataFrame.

    Args:
        artist (str): The name of the artist.
        df (pd.DataFrame): A DataFrame containing track data.
        sp (spotipy.Spotify): An authenticated Spotify client.
        write: Write the data to a local csv.

    Returns:
        pd.DataFrame: A DataFrame containing album data.
    """
    artist_list = []
    album_list = []
    type_list = []
    release_date_list = []
    date_precision_list = []
    album_id_list = []

    for _, row in df.iterrows():
        time.sleep(1)
        if pd.isna(row["id"]):
            artist_list.append(np.nan)
            album_list.append(np.nan)
            album_id_list.append(np.nan)
            type_list.append(np.nan)
            release_date_list.append(np.nan)
            date_precision_list.append(np.nan)
        else:

            try:
                result = sp.track(row["id"])
            except spotipy.exceptions.SpotifyException as e:
                print(f"Error: {e}")
                continue


            is_by_artist = False
            for artist_name in result["artists"]:
                if artist_name["name"] == artist:
                    is_by_artist = True
            if is_by_artist:
                artist_list.append(artist)
            else:
                artist_list.append(result["artists"][0]["name"])
            type_list.append(result["album"]["album_type"])
            album_list.append(result["album"]["name"])
            release_date_list.append(result["album"]["release_date"])
            date_precision_list.append(result["album"]["release_date_precision"])
            album_id_list.append(result["album"]["id"])

    df["artist"] = artist_list
    df["album_id"] = album_id_list
    df["album"] = album_list
    df["type"] = type_list
    df["release_date"] = release_date_list
    df["release_date_precision"] = date_precision_list

    if write:
        album_df = THIS_DIR / "data" / f"{artist}_albums.csv"
        df.to_csv(album_df, index=False)

    return df


def process_artist(
        artist: str = "Coldplay",
        sp: spotipy.Spotify = authenticate_spotify()
) -> None:
    """
    Process the data for one artist.

    Args:
        artist (str): The name of the artist.
        sp (spotipy.Spotify): An authenticated Spotify client.
    """
    print("Loading:", artist)
    setlist_df = load_data(artist)
    tracks = get_unique_tracks(setlist_df)
    track_df = get_track_data(artist, tracks, sp, write=True)
    album_df = get_album_data(artist, track_df, sp, write=True)
    print("... done")


def run_all(artist_list: list = default_band_list) -> None:
    """
    Run the processing for all bands.

    Args:
        artist_list (list, optional): A list of band names. Defaults to default_band_list.
    """
    sp = authenticate_spotify()
    for artist in artist_list:
        process_artist(artist, sp)


if __name__ == "__main__":
    run_all()
