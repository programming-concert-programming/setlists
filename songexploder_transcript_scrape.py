"""
This is another "run once" script.
Given the lack of research on set lists,
see if there is complementary data to be had.
In this case,
1. scrape `songexploder.net/` (with `BeautifulSoup`) to ...
2. get `.PDF` transcripts of artist interviews, and then ...
3. parse those PDFs (with `PyPDF2`) in order to ...
4 identify relevant cases (matching a search term) and return those values.

The module also supports storing the relevant URLs locally,
so the process can pick up directly from there.

Note:
- replace the `USER_AGENT` value with your equivalent. See `utils.py`.
- We have written to the Song Exploder team, raising this use case and offering to provide structured data of this kind to their site.
"""

__author__ = ["Mark Gotham", "Shujin Gan"]

from bs4 import BeautifulSoup
import io

from PyPDF2 import PdfReader
import re
import spacy  # NB: also install `spacy.cli.download("en_core_web_sm")`
from typing import Optional
from urllib.request import Request, urlopen

# Constants
from utils import HEADERS, PARSER, THIS_DIR

TARGET_URL = "https://songexploder.net/episodes"


def get_podcast_pages(
        target_url: str = TARGET_URL,
        headers: Optional[dict] = None
) -> list:
    """
    Extract podcast pages from the target URL.

    Args:
    - target_url (str): The target URL to extract pages from.
    - headers (dict): The headers to include in the HTTP request.

    Returns:
    - list: A list of page URLs.
    """
    if headers is None:
        headers = HEADERS

    req = Request(url=target_url, headers=headers)
    resp = urlopen(req)
    soup = BeautifulSoup(resp, PARSER, from_encoding=resp.info().get_param("charset"))

    podcast_pages = [link["href"] for link in soup.find_all("a", href=True) if link["href"][:25] == target_url[:25]]
    return podcast_pages


def get_transcript_urls(
        podcast_pages: list,
        headers: Optional[dict] = None
) -> list:
    """
    Extract transcript URLs from the podcast pages.

    Args:
    - podcast_pages (list): A list of podcast page URLs.
    - headers (dict): The headers to include in the HTTP request.

    Returns:
    - list: A list of transcript URLs.
    """
    if headers is None:
        headers = HEADERS

    transcript_urls = []
    for page in podcast_pages:
        try:
            req = Request(url=page, headers=headers)
            resp = urlopen(req)
            html = resp.read().decode("utf-8")
            pattern = r'<a\s+href="([^"]+)"[^>]*>click here\.?</a>'
            match_results = re.search(pattern, html, re.IGNORECASE)

            if match_results:
                title = match_results.group()
                pattern = r'<a\s+href="([^"]+)"'
                match = re.search(pattern, title)
                if match:
                    href_value = match.group(1)
                    transcript_urls.append(href_value)
                else:
                    print(page, "... No href found.")
            else:
                print(page, "... None found on this page")
        except Exception as e:
            print(f"Error occurred: {e}")

    return list(dict.fromkeys(transcript_urls))


def extract_transcript_text_from_url(
        transcript_url: str,
        headers: Optional[dict] = None
) -> str:
    """
    Extract text from a transcript URL.

    Args:
    - transcript_url (str): The URL of the transcript to extract text from.
    - headers (dict): The headers to include in the HTTP request.

    Returns:
    - str: The extracted text.
    """
    if headers is None:
        headers = HEADERS
    try:
        req = Request(url=transcript_url, headers=headers)
        remote_file = urlopen(req).read()
        memory_file = io.BytesIO(remote_file)
        pdf_file = PdfReader(memory_file)

        text = ""
        for page in pdf_file.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error occurred: {e}")
        return ""


def extract_sentences_with_keywords(
        text: str,
        keyword: str = "set"
) -> list:
    """
    Given a text, extract sentences that contain the specific keyword (default, "set") in any context
    and return that sentence lightly adapted to replace all white space with single regular space.

    Args:
    - text (str): The overall text to process.
    - keyword (str): The character string to match.

    Returns:
    - list: list of matching, and lightly pre-processed sentences.
    """
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=[.?])\s', text)
    return [
        re.sub(r'\s+', ' ', s)
        for s in sentences if keyword in s
    ]


def filter_true_positives(sentence: str) -> bool:
    """
    Given a sentence with the keyword (here "set") in it, take a closer look for true positives.

    Include:
    - any instance of "setlist"
    - any instance of "set list" (next word = "list").
    - cases where "set" is the last word in the sentence.

    Exclude:
    - cases where "set" is present but the following work makes it clearly irrelevant:
    e.g., "set up", "set out".

    This function will print cases that have been considered
    and found to match ("Match: {x}.")
    as well as those excluded (`Excluding: {x}`).
    This enables for simple verification of most cases at a glance.

    Include "set list" (obviously!) as well as ambiguous cases like "set for", "set at" (which might be relevant).

    Args:
    - sentence (str): The overall sentence to process (everything else is hard-coded).

    Returns:
    - list: bool, True is the sentences matches the given criteria.
    """
    if "setlist" in sentence:
        print("Match: `setlist`.")
        return True
    else:
        exclude_previous = ["box", "drum", "skill", "sun"] # "skill set" ...
        exclude_next = ["against", "her", "him", "in", "it", "of", "off", "out", "up", "the"]

        nlp = spacy.load("en_core_web_sm")
        this_case = nlp(sentence)

        for token in this_case:

            if "set" in token.text: # Token at least _includes_ "set" (maybe be longer)

                if token.text not in ("set", "sets"):
                    print(f"Excluding: {token.text}")  # E.g. "set" within a longer word list "cassette".
                    return False

                if token.i == len(this_case):  # The token is exactly "set" or  "sets"
                    print(f"Match: last word is `{token.text}`.")
                    return True

                next_token = this_case[token.i + 1]

                if next_token == "list":
                    print("Match: `set list`")
                    return True
                if next_token.text in exclude_next:
                    print(f"Excluding: `set {next_token}`.")
                    return False
                if token.i > 0:
                    prev_token = this_case[token.i - 1]
                    if prev_token.text in exclude_previous:
                        print(f"Excluding: `{prev_token} set`.")
                        return False

                print(f"Match: {token.text} {next_token.text}")
                return True

        return False


def check_local_list() -> list:
    """
    Retrieve the latest list of podcast pages and check this against the local collection.
    Return a list of new pages not currently included in the local list.
    """
    from song_exploder import se_urls as stored_transcript_urls
    podcast_pages = get_podcast_pages(TARGET_URL, HEADERS)
    found_transcript_urls = get_transcript_urls(podcast_pages, HEADERS)
    return [x for x in found_transcript_urls if x not in stored_transcript_urls]


def url_to_file_name(url: str) -> str:
    """
    Simple string adjustment for mapping from URL to more useful and succinct file name.
    """
    usual_start = "Song-Exploder-"
    usual_end = "-Transcript"

    file_name = url.split("/")[-1][:-4]

    if file_name.lower().endswith(usual_end):
        file_name = file_name[:-len(usual_end)]

    if file_name.startswith(usual_start):
        file_name = file_name[len(usual_start):]

    return file_name + ".txt"


def process_text(text: str) -> list:
    """
    First, organise into sentence and filter for any with the character string "set"
    (`extract_sentences_with_keywords()`).
    Then, only in those (rare) cases of a sentence with "set" further, undertake a closer look for true positives
    (`filter_true_positives()`).
    """
    matches = []
    sentences = extract_sentences_with_keywords(text)
    for s in sentences:
        if filter_true_positives(s):
            print("match:", s)
            matches.append(s)

    return matches


def main(
        use_local_raw_text: bool = True,
        use_local_url_list: bool = True,
        write_local: bool = False
):
    """
    Main function for searching instances of "set" in the transcripts.

    Args:
        use_local_raw_text: Search on already downloaded raw text files ... if False then ...
        use_local_url_list: Search online, but using the already retrieved list of URLs
        ... if false then everything is from scratch.
        write_local: Write the raw text to local files when retrieved.
    """
    if use_local_raw_text:
        raw_dir = THIS_DIR / "song_exploder" / "raw"
        files = [f for f in raw_dir.glob('*.txt') if f.is_file()]
        print(len(files))

        for f in files:
            with open(f, "r", encoding="utf-8") as input_file:
                text_content = input_file.read()
                matches = process_text(text_content)
                if not matches:
                    continue
                output_file_name = THIS_DIR / "song_exploder" / "filtered" /  f.name
                with open(output_file_name, "w", encoding="utf-8") as output_file:
                    output_file.write(f.name + '\n')
                    for m in matches:
                        output_file.write(m + '\n')

    else:
        if use_local_url_list:
            from song_exploder import se_urls as transcript_urls
        else:
            podcast_pages = get_podcast_pages(TARGET_URL, HEADERS)
            transcript_urls = get_transcript_urls(podcast_pages, HEADERS)

        for transcript_url in transcript_urls:
            print(transcript_url)
            text = extract_transcript_text_from_url(transcript_url, HEADERS)

            if write_local:
                output_file_path = THIS_DIR / "song_exploder" / "raw" / url_to_file_name(transcript_url)

                with open(output_file_path, "a", encoding="utf-8") as output_file:
                    output_file.write(text)

            matches = process_text(text)
            if matches:
                file_name = url_to_file_name(transcript_url)
                output_file_path = THIS_DIR / "song_exploder" / "filtered" /  file_name
                with open(output_file_path, "r", encoding="utf-8") as output_file:
                    for m in matches:
                        output_file.write(m + '\n')


if __name__ == "__main__":
    main()
