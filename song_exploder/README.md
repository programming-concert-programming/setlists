# Song Exploder Transcript Notes

This directory can be used to host a local copy of `.txt` files
for sentences identified in song exploder transcript extract.

In this repo, we ... :
- provide a [`raw`](./raw) directory in case that is useful to users
(there is support for it in the code),
but do not publicly store any data there.
- provide and use a [`filtered`](./filtered) directory for short quotes indicating true positive match.

See the code for the logic of in/exclusion.
Most transcripts have clearly no match.
A little over 10% (c.40 per c.300 cases in early 2026) return a _possible_ match.
The following 8 are true positives: manually filtered cases from among those 40
which clearly refer to and comment on a setlist:
- [`100-gecs-transcript`](./filtered/100-gecs-transcript.txt)
- [`Green-Day`](./filtered/Green-Day.txt)
  - "we had our set list, and we were just gonna stick to it."
  - This is notable as the already known, motivating case with insight into setlist formation.
- [`hozier-transcript`](./filtered/hozier-transcript.txt)
- [`Local-Natives`](./filtered/Local-Natives.txt)
  - "sweet moment in the set"
  - Interesting comment on the flow of a set.
- [`Madonna`](./filtered/Madonna.txt)
  - "clock tick ... DJ ... easy to mix in a set." 
- [`open-mike-eagle-transcript`](./filtered/open-mike-eagle-transcript.txt)
  - "in my live-set lately"
- [`semisonic-transcript`](./filtered/semisonic-transcript.txt)
- [`Tears-For-Fears`](./filtered/Tears-For-Fears.txt)
The [filtered directory](./filtered) includes these short quotes (separate files for each.

Some other cases match in the sense of clear reference to
"sets, setlist" etc. but no real comment on it
(e.g., "the lumineers": "we had played a set and ...").

The rest are false positivesL
- Common cases include: 'drum set', 'set [it] up', 'on a|the set' (meaning film/TV), 'set in|of|at|a', 'box set' ...
- We filter many of these automatically, but the script still returns some.
- again, it's better to err on the side of having some false positives.

There may be unknown false negatives, but it seems unlikely given the inclusive criteria.
