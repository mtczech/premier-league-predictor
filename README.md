What do I need to predict the winner of a soccer game (goal margin)?

For both defense and offense, I could compare expected goals for and against
when the player is on the pitch vs when they aren't, but some players play pretty much every game.


Defense:

Each GK's goals conceded vs expected goals conceded based on shots taken (XGoT).
(If XGoT is unavailable, use XG. With enough data, it should average out.)
If a goalie is a backup and hasn't played a significant number of games,
assume they are replacement level.
(In the MLB, the 386th best hitter is replacement level. This is out of 764 hitters.)
Each defense's XG conceded
Modifiers to XG conceded based on injuries to certain players (no, because I don't know what those are.)

Offense:

Each attacking player's goals scored based on shots taken (xGoT) 
Finishing multiplier = Goals Scored/xGoT

Multiply the above by the number of shots they will be expected to take
Add all of these multipliers up and divide by the number of shots the team is expected to take to get a team's finishing multiplier

Expected Offensive Value Added can be broken down into finishing, dribbling,
moving, and passing.
(xGoT) = chances finished

Take injuries into account (percentage of xOVA that is actually on the pitch)

The team's XG scored

Neutral:

Whether or not a team is playing at home (On average, teams win about 61 percent of their points at home, this is smaller for better teams.)

1-800-392-5749 Chase Investment Customer Service 

In the end, assume goals are scored as a Poisson distribution with frequency
(expected goals scored) by both teams.