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
## :diamond_shape_with_a_dot_inside: Early (fruitless) simulation methods
