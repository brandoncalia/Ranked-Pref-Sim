# Ranked-Pref-Sim 
Simulate & collect data on mathematically realistic ranked preference elections based on ballot repositories from real elections
## :bulb: Background
In a ranked preference election, voters are given a set of candidates over which they may rank in preferential order. <br /> <br /> 
There are multiple different counting methods that can be used to determine the winner. Despite all methods appearing perfectly fair, they may disagree and pick different winners. <br /> <br /> 
This makes the system difficult to implement - if two seemingly fair methods pick two different winners for the same election, how do we know who the most reasonable candidate to elect is? <br /> <br /> 
Our question becomes: <br /> 
*Can we estimate a reasonable probability that any two methods will disagree on a given ranked preference election?*  <br /> <br /> 
In order to answer this, we must first solve a smaller problem: <br /> 
*How can we accurately simulate a ranked preference election?* <br /> <br /> 
The script aims to accomplish just that, based on both mathematical/political literature & data collected from real elections. 
## :diamond_shape_with_a_dot_inside: Counting methods
The following ranked choice counting methods were implemented and tested in the code: 
* [Plurality](https://en.wikipedia.org/wiki/Plurality_voting#:~:text=In%20single%2Dwinner%20plurality%20voting,the%20largest%20number%20of%20votes.)
* [Borda](https://en.wikipedia.org/wiki/Borda_count#:~:text=The%20Borda%20count%20is%20a%20ranked%20voting%20system%3A%20the%20voter,most%20preferred%2C%20and%20so%20on.)
* [Condorcet](https://en.wikipedia.org/wiki/Condorcet_method#:~:text=A%20Condorcet%20method%20(English%3A%20%2F,there%20is%20such%20a%20candidate.))
* [Instant runoff](https://en.wikipedia.org/wiki/Instant-runoff_voting)
* [Baldwin](https://en.wikipedia.org/wiki/Nanson%27s_method#Baldwin_method)
