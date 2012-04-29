This is a youtube client for the command line that supports searching downloading and streaming youtube video's from the command line.


Requirements:
--------------
VLC media player
Python 2.6+


Commands:
---------
command: search / download / stream
query: 'multiple keywords' / singlekeyword
order: relevance, viewcount or rating
number of results: 1 - 50
shuffle: s


Controls:
---------
[ or { = prev
] or } = next
p or P = pause
r or R = reset
q or Q = stop


Example usage:
---------------
./youtube.py search 'ukf drum and bass' rating 20 s
Returns 20 videos with query sorted by rating

./youtube.py download 'ukf drum and bass' viewcount 10 s
Downloads 10 videos with query sorted by viewcount

./youtube.py stream 'ukf drum and bass' relevance 2 s
Stream 2 videos with query sorted by relevance


Enjoy!

0xPr0xy