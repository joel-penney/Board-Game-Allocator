# Voting for Board Games

The purpose of this program is to decide how to allocate people to board games based on their preferences.

## Considerations

This script was created and distributed by the benevolence and enjoyment of the author, and as such should not be taken as necessarily representative of the author's perception of quality coding. Error handling is minimal and a correctly formatted pref.txt file is assumed for command line use. Use at your own risk.

A particular weakness is in the high runtime complexity of the central algorithm, which leads to unreasonable processing time on large inputs. Further investigation into a more effecient algorithm would be useful. Use the file tests/test5.txt to test for this.

## Use

### Web Frontend

Run main.py and access at port 5000 in a web browser. Nominate games and vote there; solutions are generated automatically as votes are added.

### Command Line

Run the file vote.py directly, with an accompanying pref.txt file that gives players' preferences for games in the following format:

\[game name 1\]:\[minimum player requirement\]:\[maximum player requirement\]

\[game name 2\]:\[minimum player requirement\]:\[maximum player requirement\]

...

\* <- divider symbol needed between list of games and list of player preferences.

\[player 1\]| \[game name 1\]:\[rating\], \[game name 2\]:\[rating\], ...

\[player 2\]| \[game name 1\]:\[rating\], \[game name 2\]:\[rating\], ...

...

Whitespace is ignored and higher numbers mean a greater player preference, usually on a scale of 4 to 1. A smaller range may be more appropriate when fewer choices are offered.
This format can also be seen in the existing examples of pref.txt and the tests/ files.

## Areas of Further Research

Tie breaking between game solutions of equal happiness rating is currently done by picking the solution that gives the most even number of players between all games. There is likely a better criteria.

It is likely better to weight solutions with fewer games higher that solutions with more games and fewer players per game, even if the happiness rating is slightly lower. Needs consideration on how to rate this. A simpler but less convenient solution is to print the best 2-game result, best 3-game result, etc., and make a manual choice of which set to use.

Manipulating the system: it may be possible for players to unfairly influence the script outcomes by intentionally giving a wide gap in ratings between their games, which can outweigh players who give a smaller difference in ratings between games. A mitigation is to keep the range of possible ratings small, especially when few games are given as options.

Finally, if you think this simple system desperately needs to consider more factors in determining its solutions, a pull request may be a viable solution to this problem.
