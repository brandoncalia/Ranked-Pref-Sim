# Ranked-Pref-Sim 
A project in simulating & collecting data on mathematically realistic ranked preference elections based on ballot repositories from real elections <br /><br />
Read below for details on the project, theory, and methodology<br /><br />
For information exclusively on running the scripts, see [here](#Background)
## :bulb: Background
In a ranked preference election, voters are given a set of candidates over which they may rank in preferential order. <br /> <br /> 
There are multiple different counting methods that can be used to determine the winner. Despite all methods appearing perfectly fair, they may disagree and pick different winners. <br /> <br /> 
This makes the system difficult to implement - if two seemingly fair methods pick two different winners for the same election, how do we know who the most reasonable candidate to elect is? <br /> <br /> 
Our question becomes: <br /> 
*Can we estimate a reasonable probability that any two methods will disagree on a given ranked preference election?*  <br /> <br /> 
In order to answer this, we must first solve a smaller problem: <br /> 
*How can we accurately simulate a ranked preference election?* <br /> <br /> 
The script aims to accomplish just that, based on both mathematical/political literature & data collected from real elections. 
## :diamond_shape_with_a_dot_inside: Counting Methods
The following ranked choice counting methods were implemented and tested in the code: 
* [Plurality](https://en.wikipedia.org/wiki/Plurality_voting)
* [Borda](https://en.wikipedia.org/wiki/Borda_count)
* [Condorcet](https://en.wikipedia.org/wiki/Condorcet_method)
* [Instant runoff](https://en.wikipedia.org/wiki/Instant-runoff_voting)
* [Baldwin](https://en.wikipedia.org/wiki/Nanson%27s_method#Baldwin_method)
## :black_nib: Data Collection & Analysis of Real Elections
In order to simulate a realistic election, we must first understand what a real election looks like. [Preflib](https://www.preflib.org/) hosts full sets of ballots from historical ranked preference elections, which the program will take in and collect data on. Raw files look like: <br /> <br />
####  Running `historical-elections.py`:
To check the results of these elections using alternate counting methods, simply place all the Preflib files to check into the "Files" folder and run historical-elections.py. Results & election metrics will be individually printed in the "Results" folder as seen below. Files containing elections with method discrepencies are marked with a '!'. Note that the code can handle blank ballots and duplicate candidates, but does not take in file formats that include curly braces {}. <br /> <br />

## :crystal_ball: Simulation Parameters
We observe that a real election has the following characteristics that must be seen in our simulation method: 
* Incomplete ballots 
* Single-candidate ballots 
* Similar patterns of candidate ordering
    * Voters preferring a candidate *A* as their first choice are likely to rank similar candidate *B* next
* A relatively close race between 2-3 favorites
* High frequency of Condorcet existence

## :dart: The Spatial Model of Elections

The literature in the field of elections and voter theory is widely in agreement that a spatial model is the most accurate way to model a voter's preferences for any number of candidates. In the spatial model candidates are placed in multi-dimensional space, where each dimension is an issue, policy, or potential attribute of a candidate. Each voter has a point in this multi-dimensional space that best represents their opinions across multiple issues. A utility function can be used to model a voter's favor towards each candidate. A natural utility function is the Euclidean distance. However, this fails to account for a common theory that a voter might prefer the most extreme candidate on their side of an issue (scalar product), but only up to an extent. A mixed model, included both Euclidean distance, the scalar product, and an additional random variable is believed to be a sophisticated and accurate way to model a voter's utility for a candidate in space. The accuracy of such mixed models has been [experimentally verified]



## :chart_with_upwards_trend: Data & Results
#### Running `ranked-pref-sim.py`:


## :8ball: Conclusions


