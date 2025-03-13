# Never Mind the Playlist ... Here's the Setlist!

This repo provides tools for exploring the set lists on
[setlist.fm](https://www.setlist.fm/) and related data.
The functionality combines 
structured API calls to the setlist.fm API,
with complementary web scraping for data not available there, such as venue capacity.

This repository aims to support  ***non-***commercial computational methods for 
data science research, teaching, and general interest,
promoting engagement with and understanding of the composition of setlists.

For more on the motivation, terminology and more please refer to our paper
'Mark Gotham and Shujin Gan, "Set Ready, Go! On the Structure of Live Music Setlists", forthcoming, 2025.'
This is forthcoming; a pre-print is available on request.
To cite this work, please refer to the paper and
[this repo (you are here)](https://github.com/programming-concert-programming/setlists).


## Directories

- `datasets`: A place to store `.csv` files for setlists and related data in this project.
  - See note at [`datasets/README.md`](./datasets/README.md)
- `distinct_setlist_IDs`: A place to store `.csv` files for distinct setlists.
  - See note at [`distinct_setlist_IDs/README.md`](./distinct_setlist_IDs/README.md)
- `playlist_upv`: A place to store `.txt` files for playlist (sic, not setlist) from the UPV project.
  - See note at [`playlist_upv/README.md`](./playlist_upv/README.md)


## Licences and contributing

This repository is emphatically ***non-***commercial.
It is intended for research, teaching, and general interest in the data science of setlists. 
We have read the terms of all relevant services, such as
[setlist.fm's API service]https://www.setlist.fm/help/terms
and believe that this repo is consistent with both the letter and spirit of those rules.
Please make sure any downstream uses are similarly compliant. 
If you have any concerns, please reach out.

New code here is provided under the MIT licence.

New contributions to this repo, for bug fixes and additional functionality are welcome
as long as they are consistent with the above.
