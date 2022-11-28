import numpy as np
from numpy import random
import random
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd


# This function will increment:
# First place votes, second place votes, ballot appearance tally, pairwise comparison array, and Borda tally
def Borda_Plr_PairComp(ballot, FirstPlaceVotes, SecondPlaceVotes, BordaTally, PairCompArr):
    NumCands = len(ballot)
    FirstPlaceVotes[ballot[0]] += 1
    if ballot[1] != -1:
        SecondPlaceVotes[ballot[1]] += 1
    for j in range(NumCands):
        if int(ballot[j]) != -1:
            BordaTally[int(ballot[j])] += (NumCands - j)
            for w in range(NumCands):
                if w not in ballot:
                    PairCompArr[ballot[j]][w] += 1
        else:
            continue
        for x in range(j + 1, NumCands):
            if ballot[x] != -1:
                PairCompArr[ballot[j]][ballot[x]] += 1


# Calculate Condorcet winner
def Condorcet(PairwiseComparisonArray):
    CondorcetWinner = None
    NumCands = len(PairwiseComparisonArray)
    for z in range(NumCands):
        if CondorcetWinner is not None:
            break
        for g in range(NumCands):
            if (PairwiseComparisonArray[g][z] >= PairwiseComparisonArray[z][g]) and (z != g):
                break
            elif g == NumCands - 1:
                CondorcetWinner = z + 1
                break
    return CondorcetWinner


# Calculate Instant Runoff winner
def InstantRunoff(VoterMatrix, FirstPlaceVotes):
    NumCands = len(FirstPlaceVotes)
    IRrankings = np.zeros(NumCands)
    IRVoterMatrix, IRtally = VoterMatrix.copy(), FirstPlaceVotes.copy()
    for i in range(NumCands):
        a = np.sort(IRtally)
        elimination = np.where(IRtally == a[i])[0][0]
        IRrankings[i] = int(elimination) + 1
        IRtally = np.zeros(NumCands)
        IRVoterMatrix[IRVoterMatrix == elimination] = -1
        for ballot in IRVoterMatrix.T:
            for candidate in ballot:
                if candidate != -1:
                    IRtally[int(candidate)] += 1
                    break
    InstantRunoffWinner = int(IRrankings[NumCands - 1])
    return InstantRunoffWinner, IRrankings


# Calculate Baldwin winner
def Baldwin(VoterMatrix, BordaTally):
    NumCands = len(BordaTally)
    BaldwinRankings = np.zeros(NumCands)
    baldwinVoterMatrix, baldwinTally = VoterMatrix.copy(), BordaTally.copy()
    for z in range(NumCands):
        b = np.sort(baldwinTally)
        elimination = np.where(baldwinTally == b[z])[0][0]
        BaldwinRankings[z] = int(elimination) + 1
        baldwinTally = np.zeros(NumCands)
        baldwinVoterMatrix[baldwinVoterMatrix == elimination] = -1
        for ballot in baldwinVoterMatrix.T:
            bordaPos = 0
            for idx, candidate in enumerate(ballot):
                if candidate == -1:
                    bordaPos += 1
                else:
                    baldwinTally[int(candidate)] += NumCands - idx + bordaPos
    BaldwinWinner = int(BaldwinRankings[NumCands - 1])
    return BaldwinWinner, BaldwinRankings


# Number of simulations
numSim = int(input("Enter the number of simulations: "))

# Record how frequently methods agree
C_exist, B_C, IR_C, BW_C, P_C, B_BW, B_P, B_IR, P_IR, P_BW, BW_IR = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

# Variables for Borda score differences boxplot
BordaCondDiffs = []
BordaDiffs = []

plt.figure(1)
plt.xlim(-1, 1)
plt.ylim(-1, 1)
plt.axhline(0, color='k')
plt.axvline(0, color='k')
plt.grid()

for s in range(numSim):

    numAlternatives = random.randint(3, 7)
    numVoters = random.randint(2500, 50000)
    voterMatrix = np.empty((numAlternatives, numVoters))
    bordaTally = np.zeros(numAlternatives)
    FirstPlaceVotes = np.zeros(numAlternatives)
    SecondPlaceVotes = np.zeros(numAlternatives)
    pairCompArr = np.zeros((numAlternatives, numAlternatives))
    single_cand_ballot_prob = random.uniform(.15, .3)
    full_ballot_function = -.1375 * numAlternatives + 1.16
    full_ballot_prob = full_ballot_function + np.random.normal(0, .1)

    # Assign cartesian coordinates to each candidate
    candidateCoordinates = np.random.normal(0, .4, size=(numAlternatives, 2))
    while np.amax(candidateCoordinates) > 1 or np.amin(candidateCoordinates) < -1:
        candidateCoordinates = np.random.normal(0, .4, size=(numAlternatives, 2))

    for q in range(numVoters):

        ballot = np.full(numAlternatives, -1)

        # Determine coordinates of voter
        voterCoordinates = np.random.normal(0, .33, size=2)
        while np.amax(voterCoordinates) > 1 or np.amin(voterCoordinates) < -1:
            voterCoordinates = np.random.normal(0, .33, size=2)

        # For 1st simulation, plot each voter
        if s == 0:
            plt.plot(voterCoordinates[0], voterCoordinates[1], '*', color='k', markersize=2)

        # Determine utility function
        utility = np.zeros(numAlternatives)
        for i in range(numAlternatives):
            utility[i] += -1 * abs(np.linalg.norm(voterCoordinates - candidateCoordinates[i, :]))
            utility[i] += np.dot(voterCoordinates, candidateCoordinates[i, :])
            utility[i] += np.random.normal(0, .05)

        # Determine voter's ranking of the candidates
        sortedUtility = np.sort(utility)[::-1]
        candidatePreferences = np.zeros(numAlternatives)
        for z in range(numAlternatives):
            candidatePreferences[z] = np.where(utility == sortedUtility[z])[0]

        # Roll for how many candidates the voter will rank
        ballotRoll = random.uniform(0, 1)
        if ballotRoll <= single_cand_ballot_prob:
            ballot[0] = candidatePreferences[0]
        elif single_cand_ballot_prob < ballotRoll <= single_cand_ballot_prob + full_ballot_prob:
            ballot[:] = candidatePreferences
        else:
            ballot[0] = candidatePreferences[0]
            ballot[1] = candidatePreferences[1]
            for w in range(2, numAlternatives):
                if sortedUtility[w] > (sortedUtility[1] - .05):
                    ballot[w] = candidatePreferences[w]

        # Create ballot and store in voterMatrix
        ballot = np.asarray([int(element) for element in ballot])
        voterMatrix[:, q] = ballot

        # Borda, plurality, and pairwise comparison array tallies
        Borda_Plr_PairComp(ballot, FirstPlaceVotes, SecondPlaceVotes, bordaTally, pairCompArr)

    # For 1st simulation, plot each candidate (figure 1)
    if s == 0:
        for n in range(numAlternatives):
            plt.plot(candidateCoordinates[n][0], candidateCoordinates[n][1], 'o', color='r', markersize=15)
            plt.annotate(str(n + 1), xy=(candidateCoordinates[n][0], candidateCoordinates[n][1]),
                         ha='center', va='center')

    # Determine winners
    bordaWinner, pluralityWinner = np.argmax(bordaTally) + 1, np.argmax(FirstPlaceVotes) + 1
    IRwinner, IRrankings = InstantRunoff(voterMatrix, FirstPlaceVotes)
    condorcetWinner = Condorcet(pairCompArr)
    baldwinWinner, baldwinRankings = Baldwin(voterMatrix, bordaTally)

    # Label method winners on figure 1
    if s == 0:
        plt.text(-1, 1.05, f'Borda: {bordaWinner}', ha='left', size=9)
        if condorcetWinner is not None:
            plt.text(-.65, 1.05, f'Condorcet: {condorcetWinner}', ha='left', size=9)
        else:
            plt.text(-.65, 1.05, 'Condorcet: --', ha='left', size=9)
        plt.text(-.20, 1.05, f'Instant runoff: {IRwinner}', ha='left', size=9)
        plt.text(.35, 1.05, f'Plurality: {pluralityWinner}', ha='left', size=9)
        plt.text(.75, 1.05, f'Baldwin: {baldwinWinner}', ha='left', size=9)
        plt.text(0, 1.15, f'Borda tally: {bordaTally}', ha='center', size=9)
        plt.text(0, 1.24, f'First place votes tally: {FirstPlaceVotes}', ha='center', size=9)
        plt.text(-1.1, -1.2, f'BW order of elimination: {baldwinRankings}', ha='left', size=9)
        plt.text(1.1, -1.2, f'IR order of elimination: {IRrankings}', ha='right', size=9)

    # Plot differences of winners of different methods on separate figures
    # Condorcet & Plurality
    plt.figure(2)
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.axhline(0, color='k')
    plt.axvline(0, color='k')
    if s == 0:
        plt.grid()
    plt.suptitle('Plurality vs. Condorcet Winners When The Methods Disagree')
    if pluralityWinner != condorcetWinner and condorcetWinner is not None:
        plt.figure(2)
        plt.plot(candidateCoordinates[pluralityWinner - 1][0],
                 candidateCoordinates[pluralityWinner - 1][1], 'o', color='b', markersize=4)
        plt.plot(candidateCoordinates[condorcetWinner - 1][0],
                 candidateCoordinates[condorcetWinner - 1][1], 'o', color='r', markersize=4)

    # Baldwin & Instant Runoff
    plt.figure(3)
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.axhline(0, color='k')
    plt.axvline(0, color='k')
    if s == 0:
        plt.grid()
    plt.suptitle('Baldwin vs. Instant Runoff Winners When The Methods Disagree')
    if baldwinWinner != IRwinner:
        plt.figure(3)
        plt.plot(candidateCoordinates[int(baldwinWinner) - 1][0],
                 candidateCoordinates[int(baldwinWinner) - 1][1], 'o', color='b', markersize=4)
        plt.plot(candidateCoordinates[int(IRwinner) - 1][0],
                 candidateCoordinates[int(IRwinner) - 1][1], 'o', color='r', markersize=4)

    # Check for agreement between methods
    if condorcetWinner is not None:
        C_exist += 1
        if condorcetWinner == bordaWinner:
            B_C += 1
            sorted = np.sort(bordaTally)[::-1]
            DIFF = (sorted[0] - sorted[1]) / sorted[0]
            plt.figure(4)
            BordaDiffs.append(DIFF)
        else:
            sorted = np.sort(bordaTally)[::-1]
            DIFF = (sorted[0] - sorted[1]) / sorted[0]
            BordaCondDiffs.append(DIFF)
        if condorcetWinner == baldwinWinner:
            BW_C += 1
        if condorcetWinner == IRwinner:
            IR_C += 1
        if condorcetWinner == pluralityWinner:
            P_C += 1
    if bordaWinner == baldwinWinner:
        B_BW += 1
    if bordaWinner == IRwinner:
        B_IR += 1
    if bordaWinner == pluralityWinner:
        B_P += 1
    if pluralityWinner == baldwinWinner:
        P_BW += 1
    if pluralityWinner == IRwinner:
        P_IR += 1
    if baldwinWinner == IRwinner:
        BW_IR += 1

# Record frequencies of agreement
C_exist /= numSim
B_C /= numSim
IR_C /= numSim
BW_C /= numSim
P_C /= numSim
B_BW /= numSim
B_P /= numSim
B_IR /= numSim
P_IR /= numSim
P_BW /= numSim
BW_IR /= numSim

agreements = [
                ['Condorcet existence', f'{C_exist:.3f}'],
                ['Condorcet-Borda', f'{B_C:.3f}'],
                ['Condorcet-IRV', f'{IR_C:.3f}'],
                ['Condorcet-Baldwin', f'{BW_C:.3f}'],
                ['Condorcet-Plurality', f'{P_C:.3f}'],
                ['Borda-IRV', f'{B_IR:.3f}'],
                ['Borda-Baldwin', f'{B_BW:.3f}'],
                ['Borda-Plurality', f'{B_P:.3f}'],
                ['Plurality-IRV', f'{P_IR:.3f}'],
                ['Plurality-Baldwin', f'{P_BW:.3f}'],
                ['Baldwin-IR', f'{BW_IR:.3f}']
            ]
data = pd.DataFrame(agreements, columns=['Method(s)', 'Frequency of Agreement'])

# Print results
print(data)

# Create legends for figures 2-3 & display all plots
plt.figure(2)
legend_elements = [Line2D([0], [0], marker='o', color='w', label='Plurality', markerfacecolor='b', markersize=12),
                   Line2D([0], [0], marker='o', color='w', label='Condorcet', markerfacecolor='r', markersize=12)]
plt.legend(handles=legend_elements)
plt.figure(3)
legend_elements = [Line2D([0], [0], marker='o', color='w', label='Baldwin', markerfacecolor='b', markersize=12),
                   Line2D([0], [0], marker='o', color='w', label='Instant Runoff', markerfacecolor='r', markersize=12)]
plt.legend(handles=legend_elements)

# Borda score differences boxplot
plt.figure(4)
plt.suptitle('Comparing Differences In Top 2 Borda Scores')
plt.ylabel('% Diff Between 1st & 2nd Place Borda Scores')
plt.xlim(0, 3)
plt.boxplot([BordaDiffs, BordaCondDiffs], labels=['B-C Agree', 'B-C Disagree'])

plt.show()
