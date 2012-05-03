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
timespan (optional): today, week, month, all
shuffle (optional): shuffle


Controls:
---------
[ or { = prev
] or } = next
p or P = pause
r or R = reset
q or Q = quit


Example usage:
---------------
./youtube.py search 'ukf drum and bass' rating 20 shuffle
Returns 20 videos with query sorted by rating and shuffled

./youtube.py download 'ukf drum and bass' viewcount 10 shuffle
Downloads 10 videos with query sorted by viewcount and shuffled

./youtube.py stream 'ukf drum and bass' relevance 2 month
Stream 2 videos with query sorted by relevance and uploaded between now and a month ago


Enjoy!

0xPr0xy