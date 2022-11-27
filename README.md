# Ranked-Pref-Sim :bar_chart:
A project in simulating & collecting data on mathematically realistic ranked preference elections based on ballot repositories from real elections 

![preflib](https://user-images.githubusercontent.com/41372799/200403009-c54868f9-6d27-497c-aed9-b9b35e3f06c6.JPG) <img width="420" alt="spatial21 (1)" src="https://user-images.githubusercontent.com/41372799/200413514-f5016c47-505a-4970-b04c-529898ccb2cc.PNG"> 


Read below for details on the project, theory, and methodology. For information exclusively on running the scripts, download the project as zip and see `historical-elections.py` and `ranked-pref-sim.py` in sections below
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
In order to simulate a realistic election, we must first understand what a real election looks like. [Preflib](https://www.preflib.org/) hosts full sets of ballots from historical ranked preference elections, which the program will take in and collect data on. Raw files look like (sample): <br /> <br />
![preflib](https://user-images.githubusercontent.com/41372799/200403009-c54868f9-6d27-497c-aed9-b9b35e3f06c6.JPG)



####  Running `historical-elections.py`:
*To check the results of these elections using alternate counting methods, simply place all the Preflib files to check into the "Files" folder and run historical-elections.py. Results & election metrics will be individually printed in the "Results" folder as seen below. Files containing elections with method discrepencies are marked with a '!'. At large results are housed in the created 'DATA.TXT' file.*

We ran 127 real elections and collected the following data: 

However, filtering by only larger political elections (> 2500 voters) yields the following:

**Note**: on Preflib, some ballot files contain ties marked with curly braces. For example, {3,5} would denote a tie between candidates 3 and 5. This is an issue, since the counting methods require a strict ordering. We choose to discard tied candidates, considering them "illegible" ballots. Some ballots contain large sets of entries for {1,2}, which is clearly *not* a candidate tie since it appears everywhere on multiple ballots in multiple elections. These entries were simply discarded. 

## :crystal_ball: Simulation Parameters
With an understanding of what a real election looks like and data on their metrics, we can begin creating our own simulation method. As opposed to randomly (uniformly) generated ballots, a real election has the following characteristics that must be seen in our simulation method: 
* Incomplete ballots 
* Single-candidate ballots 
* Similar patterns of candidate ordering
    * Voters preferring a candidate *A* as their first choice are likely to rank similar candidate *B* next
* A relatively close race between 2-3 favorites with other candidates lagging behind more
* Potentially high frequency of Condorcet existence
   * Every election we ran had a Condorcet winner
   * We can't directly program this, but the parameters we use should in turn create results like this

We observe a range of about 15-30% of all ballots containing only a single candidate, and a range of anywhere from 0-60% containing all candidates. On average, voters tend to rank about 60% of the total available alternatives. Most political elections tend to include 3-7 candidates. 

We also hypothesize that a voter is less likely to rank all the available candidates as the number of available alternatives increase. Below is the data collected to test this theory: 


Our probability that a voter ranks all the available candidates will therefore become a decreasing linear function of candidate number plus a random normal variable. 

## :dart: The Spatial Model of Elections

The literature in the field of elections and voter theory is widely in agreement that a spatial model is the most accurate way to model a voter's preferences for any number of candidates. In the spatial model, candidates are placed in multi-dimensional space, where each dimension is an issue, policy, or potential attribute of a candidate. Each voter has a point in this multi-dimensional space that best represents their opinions across multiple issues. A utility function can be used to model a voter's favor towards each candidate. A natural utility function is the Euclidean distance. However, a common theory is that a voter might prefer the most extreme candidate on their side of an issue (but only up to an extent). Euclidean distance does not account for this preference, but a scalar product of voter and candidate position would. A mixed utility model, including both Euclidean distance and the scalar product is believed to be ideal. We also include a random variable in our function to account for small, miscalleanous favors and voter beliefs. 

Therefore, our utility function becomes: 

$U(V,C)=\alpha |V-C| + \beta V\cdot C + R(V,C)$

$(0 < \alpha < 1)$

$(0 < \beta < 1)$


With $\alpha$ and $\beta$ being scaling variables to account for the weight given to Euclidean distance / scalar product calculations, and $R(V,C)$ denoting a random variable drawn from a normal distribution, $\mu=0, \sigma=.025$.


In two dimensional space, we choose to distribute both voters and candidates the same - each x and y coordinate is drawn from a normal distribution, $\mu = 0, \sigma = .34$. Additional politcal science knowledge on the distribution of voter beliefs would be useful to improve this choice. 



## :chart_with_upwards_trend: Data & Results
The simulation script utilizes the spatial model of elections and parameters that reflect the data gathered on real elections. We test 5,000 simulated elections, each with a random number of candidates between 4 and 9 and a random number of voters between 2500 and 50,000. 

#### Running `ranked-pref-sim.py`:
*The script runs itself. Just run it in any python editor to simulate and see results for yourself. Note that simulations can be timely, particularly with large voter numbers. More efficient ways of packing ballots are in the works.*

Here is a sample scatterplot & results of one simulated election:

<img width="479" alt="spatial21 (1)" src="https://user-images.githubusercontent.com/41372799/200413514-f5016c47-505a-4970-b04c-529898ccb2cc.PNG">


Below is the recorded data on the frequences of agreement of our tested counting methods: 

Spatial positioning of Plurality vs. Condorcet winners, Baldwin vs. Instant Runoff winners when the methods disagree:

We also hypothesize that the closer a race is, the more likely methods are to disagree. To confirm: 





## :8ball: Conclusions
Our best conclusions from the data we collected:
* Close races are a strong predictor of method disagreements
* Condorcet winners occur very, very frequently, in both real election and simulation
* Our distribution of voters and candidates is very strongly deterministic of frequencies of method disagreemeents\
* Plurality has extremely poor agreement with any other method - even Instant Runoff appears to pick the Condorcet winner ~90% of the time. Plurality picks differently from any other method nearly half the time, indicating our need to move away from simple plurality systems

We are most interested in the high frequency of Condorcet existence. This number being so high, both in practice and simulation, suggests that it could be a viable method. The main roadblock to Condorcet's method has always been it's potential lack of existence, but our data suggests it can be used in some way. Duncan Black's method, for example, could capitalize on this. We also have convincing evidence against using the traditional plurality count, seeing how frequently it disagrees with more advanced methods. We remain interested in attempting to "classify" the types (extreme, moderate, very similar to another candidate, etc.) of candidates who might win each respective method, therefore determining specific metrics which might help choose a better winner when methods do disagree. Our plot of Plurality vs. Condorcet winners was a rudimentary first attempt at this. That being said, our main goal is finding the necessary body of political science research that can lead us in the right direction to implementing an accurate political distribution of voters and candidates in an election. 
