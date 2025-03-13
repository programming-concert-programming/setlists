# Placeholder directory for song exploder transcript scrape output

This directory could be used to host a local copy of `.txt` files
for sentences identified in song exploder transcripts that match the search term.

- The files are named in the form `results_<number>.txt`.
- `number` is that of the ordering in the URL list, not the episode number. This may change.
- In the case of searching for references to setlists using the search term `` results in
  - 1 single true positives
    - The already known and motivating case of the Green Day episode (`results_21.txt`)
      - "we had our set list, and we were just gonna stick to it." (`2024/02/Song-Exploder-Green-Day-Transcript.pdf`)
  - Some borderline cases:
    - "sweet moment in the set" (`2023/08/Song-Exploder-Local-Natives-Transcript.pdf`, `results_31.txt`)
    - 'clock tick ... DJ ... easy to mix in a set.' (`2022/08/Song-Exploder-Madonna-Transcript.pdf`, `results_49.txt`)
    - "played a set" (`http://songexploder.net/transcripts/the-lumineers-transcript.pdf`, `results_216.txt`)
    - "in my live-set lately" (`http://songexploder.net/transcripts/open-mike-eagle-transcript.pdf`, `results_271.txt`)
  - 88 many false positives
    - Common cases include: 'drum set', 'set [it] up', 'on a|the set' (meaning film/TV), 'set in|of|at|a', 'box set' ...
    - We may return and adapt the script to exclude such cases.
  - Unknown false negatives
  - c.200 cases of no match.
