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
- We have written to songexploder, raising this use case and offering to provide structured data of this kind to their site.
"""

__author__ = ["Mark Gotham", "Shujin Gan"]

from bs4 import BeautifulSoup
import io

from PyPDF2 import PdfReader
import re
from typing import Optional
from urllib.request import Request, urlopen

# Constants
from utils import USER_AGENT, THIS_DIR

TARGET_URL = "https://songexploder.net/episodes"
PARSER = "html.parser"  # or "lxml" (preferred) or "html5lib", if installed
HEADERS = {"User-Agent": USER_AGENT}


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
                    print(page, "... href found, adding.")
                    transcript_urls.append(href_value)
                else:
                    print(page, "... No href found.")
            else:
                print(page, "... None found on this page")
        except Exception as e:
            print(f"Error occurred: {e}")

    return list(dict.fromkeys(transcript_urls))


def extract_transcript_text(
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


def extract_sentences_with_keywords(text: str, pattern: str) -> list:
    """
    Extract sentences containing specific keywords from the text.

    Args:
    - text (str): The text to extract sentences from.
    - pattern (str): The pattern to match in the sentences.

    Returns:
    - list: A list of sentences containing the keywords.
    """
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=[.?])\s', text)
    return [sentence for sentence in sentences if re.search(pattern, sentence, re.IGNORECASE)]


def main(
        search_pattern: str = r"\b(?:set|setlist|set list)\b",
        use_local_url_list: bool = True,
        print_when_empty: bool = False
):
    if use_local_url_list:
        from song_exploder_transcript_urls import se_urls as transcript_urls
    else:

        podcast_pages = get_podcast_pages(TARGET_URL, HEADERS)
        transcript_urls = get_transcript_urls(podcast_pages, HEADERS)

    print("Processing these URLs... ")
    count = 0
    for transcript_url in transcript_urls:
        count += 1
        print("...", transcript_url)
        text = extract_transcript_text(transcript_url, HEADERS)
        pattern = search_pattern
        sentences = extract_sentences_with_keywords(text, pattern)

        output_file_path = THIS_DIR / "song_exploder" / f"results_{count}.txt"

        if sentences:  # i.e., any results found
            with open(output_file_path, "a", encoding="utf-8") as output_file:
                output_file.write(transcript_url + '\n')
                for sentence in sentences:
                    output_file.write(sentence + '\n')
                output_file.write('======== END ============' + '\n')
        else:
            print(f"No sentences found in {transcript_url}")
            if print_when_empty:
                with open(output_file_path, 'a', encoding='utf-8') as output_file:
                    output_file.write(transcript_url + '\n')
                    output_file.write("No sentences found." + '\n')
                    output_file.write('======== END ============' + '\n')


if __name__ == "__main__":
    main()
