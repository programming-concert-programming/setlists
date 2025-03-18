# Never Mind the Playlist ... Here's the Setlist!

A tutorial-demonstration on APIs and concert setlists
by [Mark Gotham](https://markgotham.github.io/)

## Overview

Main Topics:
- Technical methods: structured API calls, complementary web scraping, and related matters.
- Subject content: the order of musical events into a concert "setlist".

Learning outcomes:
- Gain direct experience with APIs.
- Explore what is possible, and some of the limitations.
- Triangulate data from multiple APIs and related data gathering techniques.
- Learn about regularities in concert setlists.

You will need:
- Python and Jupyter notebooks running locally
  - ... including various external libraries (see `environment.yml` or better, get conda to do that for you)
  - ... or the equivalent set up on a site like Google's colab.
- Clone or download the zip of [this code repo](https://github.com/programming-concert-programming/setlists).
  - I recommend cloning, so that you can keep up with any changes. 

Reference solutions are provided for everything discussed here.
The main python files are named in the form
`{where}_{what}_{how}.py`.
E.g., 
`setlistfm_events_api.py` goes to 
_setlist.fm_, and retrieves _events_ using the _api_.
Each task can be undertaken from scratch,
either ignoring the reference solution entirely, or using only as a prompt when stuck.
Alternatively, for a minimal version of the task,
simply identify the relevant parts of the code base, and
run them with your query.


## Context: a spectrum of data openness

Imagine a "spectrum of data openness".
- We have completely transparent, publicly shared, open-source data released under FAIR principles at one end. 
- At the other end, we have completely closed, proprietary software that is unavailable to external users.

Application Programming Interfaces (APIs) are designed to sit in the middle between.
Basically, someone owns and controls an environment (database, software, ...),
and instead of releasing _none_ or _all_ of it,
they chose to make _some_ parts of the data or system available to external parties.


## Task 1: setlist.fm API

Enough talk! Over to you now.

Let's start exploring the API kindly provided by [setlist.fm](https://www.setlist.fm/).
This is a crowdsourced collection of "setlists" at millions of concerts.

Before Getting Started
- Go to [setlist.fm's API description](https://api.setlist.fm/docs/1.0/index.html).
- Note that you can choose which data format you prefer: json vs xml.
- Note also the `Data Types`: we'll need these to retrieve the corresponding data.
- Note the terms of service and rate limits etc.

Getting Started:
- To get started, you need to get a "key".
  - Like most APIs, you need to apply for a "key" to use it.
  - Fortunately, this is easy with [setlist.fm (link as above)](https://api.setlist.fm/docs/1.0/index.html).
  - You register by choosing a username, email address and password, and briefly explaining your use case.
    - E.g., you could say "Basic exploration for research and teaching. Non-commercial."
    - The key is usually granted immediately.
- Note: not all APIs are so straightforward.

Task:
- Standard version:
  - Have a look at [the code repo](https://github.com/programming-concert-programming/setlists).
  - Figure out where to put your "key".
  - Pick any event on setlist.fm and note the event ID.
  - Get the code running to retrieve full data for that event.
- Hint:
  - For a simple starting point, you can see the ID of an event ID in the main, public-facing URLs. 
    - These URLs take various forms, ending with the event ID, such as:
      - `https://www.setlist.fm/setlists/{artist_and_other_text}_{event_ID}.html`
      - Or `https://www.setlist.fm/setlist/{artist}/{year/{venue-with-dashes}-{location}-{event_ID}.html`
  - From this, you can construct the version of the URL for the API which is in the form:
    - `https://api.setlist.fm/rest/1.0/setlist/{event_id}`
  - This doesn't work (manually) the other way round:
    - Knowing the event ID is not enough to reconstruct the public-facing URL. 
  - It _is enough_ via the API. The json data for an event includes a key:value pair for the URL.
- Bonus: Try writing all the scripts from nothing, without the reference solutions.


## Task 2: Spotify API (optional)

Setlist.fm provides some great data, but often you'll find that your research needs
(in this and any case)
are not entirely met and need extending to other API and/or web scraping.
To explore that, we begin with a complementary API from Spotify.
This requires a login, the creation of an "app" (you might call yours "Test"). More hoops.
Again, start by getting an API key, this time for Spotify.
Note the differences in the experience.

Task:
- Standard version:
  - Have a look at [the code repo](https://github.com/programming-concert-programming/setlists).
  - Figure out where to put your Spotify "ID" and "secret" (their term, quite common).
  - Using only that spotify authentication (hint `sp: spotipy.Spotify`)
    - Take the name of one or more tracks (`track: str`) and the corresponding artist (`artist: str`).
    - Try to retrieve structured data for that track from Spotify using the code provided.
      - Note: the album data is especially useful: this is not provided by the setlist.fm API.
- Bonus: Try writing all the scripts from nothing, without the reference solutions.

Question:
- How were those two API key-getting experiences similar/different? What usage restrictions did they impose?
- how effective was your string-based track search? Did it work for well-known cases? What about niche ones?

Context revisited:
- As a case in point for the context discussion above:
- Between starting to prepare this topic and now writing these words, 
    the Spotify API deprecated the audio features of its API.
    We have additional functionality for getting and working with those features, 
    but it is no longer possible to access these features from the API, so we won't demo them here.
- This is all too common and a reminder to think about research projects systematically.
  - Make arrangements for any data you will need and do not rely on the future provision of these APIs.


## Task 3: Complementary web scraping of setlist.fm

There's some data that `setlist.fm` provides right there in the API (as above).
Then there's some data retrievable from other APIs (also, demo'd above).
There's also some data in `setlist.fm`, ... not a structured part of the API.
'Average sets' are a case in point and very interesting here.
To get at this data programmatically, we need a webscrape of `setlist.fm` 
to complement the more structured API call.

Task:
- Pick an artist (`artist_id`) and tour (`tour_id`) of interest.
  - Head to the corresponding `target_url`at `https://www.setlist.fm/stats/average-setlist/{artist_id}.html?tour={tour_id}`
  - Use `BeautifulSoup` (or equivalent) to get parsed HTML of that tour stats page.
  - Extract songs from the tour stats page using a regex pattern.


## Task 4: Complementary web scraping of Wikipedia

There is, of course, also some data that `setlist.fm` doesn't provide.
Even here, we may get at that data via meaningful connections.
In the case of venues, `setlist.fm` has names and IDs, but not the capacity information.
Setlist.fm provides links to the corresponding `wikipedia` page for most venues,
and `wikipedia` provides capacity information.
So we can use `setlist.fm` pages, to get the `wikipedia` links, and then 
scrape those wikipedia pages for the capacity.
What could go wrong ;) ?

Task:
- Identify a venue page in the form `https://api.setlist.fm/rest/1.0/venue/{venue_id}`
- Write a script to find all the `<div>` entries with class `info` on that page.
- See if one has a link to wikipedia.
- Then head to that Wikipedia page and seek the HTML tables (`<th>` for table header cell). 
- Once you find a table, use `.find_next_sibling` to find the `<td>` elements with `class_="infobox-data"`


## Research Questions

At the end of this whole process, let's consider some high level questions:
- What data has / has not been made available?
- What is the quality of that data?
- What / how permissive are the API terms of use?
- What happens if (when) companies start limiting or stopping their APIs.

## Appendix: Definitions

- Application Programming Interface (API):
  - Primary: The main meaning of API is a formal mechanism for getting data from a source (open or closed). 
    - That's the meaning we'll use here.
    - We'll see how some organisations structure this, what they offer, and the steps needed to gain access.
  - Secondary: "API" is sometimes used to refer to interfaces more generally.
    - E.g., for the public-facing names and arguments of a code base (even if the code is all open source). 
    - So, a developer might say "let's get the API right first, we can work on inner logic later".
    - I raise this simply to disambiguate.
- Setlists: A list of tracks that an artist has played at a concert, listed in the order of their performance.
  - Tour: A series of concerts by an artist and usually associated with a particular (recently release) album.
  - Promotional show: A shorter performance typically performed for television channels, talk shows, or similar.
- Album: An ordered sequence of tracks released as a unit to be mechanically reproduced at any time.
  - The relationship between an album and the corresponding tour is interesting. 
- Playlist: A broader terms for organised sequence of tracks.
  - The main association is with this functionality on steaming services, to be mechanically reproduced at any time.
  - The term is also sometimes used as a large category that includes sub-categories of: 
    - Setlists (performed live, as above). We see setlists as categorically different, and have some evidence for this ;)
    - Radio broadcast (mechanically reproduced, but to be played through once more like a setlist)
