import numpy as np
from pathlib import Path
import os
import pandas as pd
import statistics
import matplotlib.pyplot as plt

# Place all Preflib files in 'Files' folder located in the same directory as the code
# Results will be printed in the 'Results' folder

parent_path = Path(__file__).parent
files_path = os.path.join(parent_path, 'Files')
result_files = os.path.join(parent_path, 'Results')

# Method agreement counter
# Borda (B), Condorcet (C), Baldwin (BW), Instant runoff (IR), Plurality (P)
C_exist, B_C, IR_C, BW_C, P_C, B_BW, B_P, B_IR, P_IR, P_BW, BW_IR = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

numFiles = 0
avgVoters, avgCands = 0, 0
numCands_i = []  # Individual values of candidate number for each election

# q = average portion of voters ranking only a single candidate
# r = average portion of registered candidates ranked by a voter
# s = average potion of voters ranking all registered candidates
q, r, s = 0, 0, 0
q_i, r_i, s_i = [], [], []  # Individual values of q, r, s for each file

# Optional data variables used to create the boxplot seen on Github
# s_i_3cand, s_i_4cand, s_i_5cand, s_i_6cand, s_i_7cand = [], [], [], [], []


# Check if the file contains write in candidates, and if so, record them
def CheckWriteIns(ElectionFile, NumCands):
    WriteIn = False
    WriteInIndex = -1
    WriteInCands = []
    file = open(ElectionFile)
    for line in file.readlines()[12:11 + NumCands + 1]:
        WriteInIndex += 1
        if 'Write-In' in line or 'Write In' in line:
            WriteIn = True
            WriteInCands.append(WriteInIndex)
    return WriteIn, WriteInCands


# Function to record:
# If a ballot contains only one candidate
# If a ballot contains available candidates
# What portion of available candidates a voter ranked
def CollectBallotMetrics(ballot, WriteInCandidates, WriteInExistence, NumBallots):

    # Number of NON WRITE-IN spots on the ballot filled in
    NumSpotsFilled = 0
    for cand in ballot:
        if cand != -1 and cand not in WriteInCandidates:
            NumSpotsFilled += 1 * NumBallots

    # Ballots containing only a single candidate
    SingleCandBallots = 0
    if ballot[1] == -1:
        SingleCandBallots += 1 * NumBallots

    # Ballots containing ALL available candidates, not including write-ins
    FullBallots = 0
    # If there is a write-in, check if at least all REGISTERED candidates appear
    if WriteInExistence is True:
        WriteInAppearances = 0
        for cand in ballot:
            if cand in WriteInCandidates:
                WriteInAppearances += 1
        if np.count_nonzero(ballot != -1) == numAlternatives - len(WriteInCandidates) + WriteInAppearances:
            FullBallots += 1 * NumBallots

    # If election does not contain write-ins, simply check that there are no blank spots
    else:
        if -1 not in ballot:
            FullBallots += 1 * NumBallots

    return SingleCandBallots, FullBallots, NumSpotsFilled


# This function will increment:
# First place votes, second place votes, ballot appearance tally, pairwise comparison array, and Borda tally
# For the inputted ballot / number of ballots
def Borda_Plr_PairComp(ballot, NumBallots, FirstPlaceVotes, SecondPlaceVotes, AppearanceTally, BordaTally, PairCompArr):
    NumCands = len(ballot)
    FirstPlaceVotes[ballot[0]] += 1 * NumBallots
    if ballot[1] != -1:
        SecondPlaceVotes[ballot[1]] += 1 * NumBallots
    for j in range(NumCands):
        if int(ballot[j]) != -1:
            BordaTally[int(ballot[j])] += (NumCands - j) * NumBallots
            AppearanceTally[int(ballot[j])] += 1 * numBallots
            for w in range(NumCands):
                if w not in ballot:
                    PairCompArr[ballot[j]][w] += 1 * numBallots
        else:
            continue
        for x in range(j + 1, NumCands):
            if ballot[x] != -1:
                PairCompArr[ballot[j]][ballot[x]] += 1 * NumBallots


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
    IRVoterMatrix, IRtally = VoterMatrix.copy(), FirstPlaceVotes.copy()
    for i in range(NumCands - 1):
        a = np.sort(IRtally)
        elimination = np.where(IRtally == a[i])[0][0]
        IRtally = np.zeros(NumCands)
        IRVoterMatrix[IRVoterMatrix == elimination] = -1
        for ballot in IRVoterMatrix.T:
            for candidate in ballot:
                if candidate != -1:
                    IRtally[int(candidate)] += 1
                    break
    InstantRunoffWinner = np.argmax(IRtally) + 1
    return InstantRunoffWinner


# Calculate Baldwin winner
def Baldwin(VoterMatrix, BordaTally):
    NumCands = len(BordaTally)
    baldwinVoterMatrix, baldwinTally = VoterMatrix.copy(), BordaTally.copy()
    for z in range(NumCands - 1):
        b = np.sort(baldwinTally)
        elimination = np.where(baldwinTally == b[z])[0][0]
        baldwinTally = np.zeros(NumCands)
        baldwinVoterMatrix[baldwinVoterMatrix == elimination] = -1
        for ballot in baldwinVoterMatrix.T:
            bordaPos = 0
            for idx, candidate in enumerate(ballot):
                if candidate == -1:
                    bordaPos += 1
                else:
                    baldwinTally[int(candidate)] += NumCands - idx + bordaPos
    BaldwinWinner = np.argmax(baldwinTally) + 1
    return BaldwinWinner


# Iterate through each dataset in 'Files' folder
for filename in os.listdir(files_path):

    if str(filename).endswith('.ini'):
        continue

    election_file = os.path.join(files_path, filename)
    votes = open(election_file)
    info = votes.readlines()[1:11]
    numAlternatives = int(info[8].split(': ')[1])
    numVoters = int(info[9].split(': ')[1])
    resultName = info[0].split(': ')[1].replace(' ', '').strip()

    # Optional filtering
    #if numVoters < 2500:
        #continue

    # Check for write-ins
    writeIn, writeInCands = CheckWriteIns(election_file, numAlternatives)

    # Averages
    avgCands += numAlternatives - len(writeInCands)
    numCands_i.append(numAlternatives)
    numFiles += 1
    avgVoters += numVoters

    # Counting method variables
    pairCompArr = np.zeros((numAlternatives, numAlternatives))
    bordaTally = np.zeros(numAlternatives)
    FirstPlaceVotes = np.zeros(numAlternatives)
    SecondPlaceVotes = np.zeros(numAlternatives)
    appearanceTally = np.zeros(numAlternatives)
    voterMatrix = np.full((numAlternatives, numVoters), -1)
    singleCandBallots, fullBallots, numSpotsFilled, counter = 0, 0, 0, 0

    # Start tallying votes
    votes = open(election_file)
    for line in votes.readlines()[numAlternatives + 12:]:

        # Create the ballot array
        rankings = line.strip().split(': ')
        numBallots = int(rankings[0])
        rankings = rankings[1].split(',')
        rankings = list(dict.fromkeys(rankings))  # Remove any duplicates
        rankings = [int(val) - 1 for val in rankings]  # Reformat to python indexing
        ballot = np.repeat(-1, numAlternatives)
        ballot[0:len(rankings)] = rankings

        # Data on ballot structure
        a, b, c = CollectBallotMetrics(ballot, writeInCands, writeIn, numBallots)
        singleCandBallots += a
        fullBallots += b
        numSpotsFilled += c

        # Store ballots in matrix
        voterMatrix[:, counter:numBallots + counter] = np.repeat(np.array([ballot]).T, numBallots, axis=1)
        counter += numBallots

        # Borda, Plurality, appearance, & pairwise comparisons
        Borda_Plr_PairComp(ballot, numBallots, FirstPlaceVotes,
                           SecondPlaceVotes, appearanceTally, bordaTally, pairCompArr)

    # Determine Borda & Plurality winners
    bordaWinner, pluralityWinner = np.argmax(bordaTally) + 1, np.argmax(FirstPlaceVotes) + 1

    # Averages for ballot structures
    singleCandBallots = singleCandBallots / numVoters  # Variable 'q'
    q += singleCandBallots
    q_i.append(singleCandBallots)

    numSpotsFilled = numSpotsFilled / (numVoters * (numAlternatives - len(writeInCands)))  # Variable 'r'
    r += numSpotsFilled
    r_i.append(numSpotsFilled)

    fullBallots = fullBallots / numVoters  # Variable 's'
    s += fullBallots
    s_i.append(fullBallots)

    # Data for boxplot
    # if numAlternatives == 3:
        # s_i_3cand.append(fullBallots)
    # elif numAlternatives == 4:
        # s_i_4cand.append(fullBallots)
    # elif numAlternatives == 5:
        # s_i_5cand.append(fullBallots)
    # elif numAlternatives == 6:
        # s_i_6cand.append(fullBallots)
    # elif numAlternatives == 7:
        # s_i_7cand.append(fullBallots)

    # Condorcet, Instant Runoff, & Baldwin
    condorcetWinner = Condorcet(pairCompArr)
    IRwinner = InstantRunoff(voterMatrix, FirstPlaceVotes)
    baldwinWinner = Baldwin(voterMatrix, bordaTally)

    # Mark files containing method disagreements with !
    if condorcetWinner == baldwinWinner == pluralityWinner == bordaWinner == IRwinner:
        resultFilename = os.path.join(result_files, f'{resultName}RESULTS.txt')
    else:
        resultFilename = os.path.join(result_files, f'!{resultName}RESULTS.txt')

    # Write results to text file
    with open(resultFilename, 'w') as results:
        results.write(f'Plurality selects:\n{pluralityWinner}\n\n')
        results.write(f'Borda selects:\n{bordaWinner}\n\n')
        if condorcetWinner is not None:
            results.write(f'Condorcet selects:\n{condorcetWinner}\n\n')
        else:
            results.write('A Condorcet winner does not exist.\n\n')
        results.write(f'Instant runoff selects:\n{IRwinner}\n\n')
        results.write(f'Baldwin selects:\n{baldwinWinner}\n\n')
        results.write(f'Borda tally:\n{bordaTally}\n\n')
        results.write(f'First place votes tally:\n{FirstPlaceVotes}\n\n')
        results.write(f'Second place votes tally:\n{SecondPlaceVotes}\n\n')
        results.write(f'Appearance tally:\n{appearanceTally}\n\n')
        results.write(f'Portion of voters ranking only a single candidate:\n')
        results.write(f'{singleCandBallots:.3f}\n\n')
        results.write(f'Portion of voters ranking all registered candidates:\n')
        results.write(f'{fullBallots:.3f}\n\n')
        results.write(f'Average portion of registered candidates that a voter ranked:\n')
        results.write(f'{numSpotsFilled:.3f}\n\n')

    # Record the methods that agree
    if condorcetWinner is not None:
        C_exist += 1
        if condorcetWinner == bordaWinner:
            B_C += 1
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

# Calculate averages
C_exist /= numFiles
B_C /= numFiles
IR_C /= numFiles
BW_C /= numFiles
P_C /= numFiles
B_BW /= numFiles
B_P /= numFiles
B_IR /= numFiles
P_IR /= numFiles
P_BW /= numFiles
BW_IR /= numFiles
q /= numFiles
r /= numFiles
s /= numFiles
avgCands /= numFiles
avgVoters /= numFiles

# Calculate standard deviations
if numFiles > 1:
    q_stdev = '{:.3f}'.format(statistics.stdev(q_i, q))
    r_stdev = '{:.3f}'.format(statistics.stdev(r_i, r))
    s_stdev = '{:.3f}'.format(statistics.stdev(s_i, s))
    cands_stdev = '{:.3f}'.format(statistics.stdev(numCands_i, avgCands))
else:
    q_stdev, r_stdev, s_stdev, cands_stdev = 'N/A', 'N/A', 'N/A', 'N/A'

# Table storing data on frequencies of method agreement
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

# Write average data for all elections tested
with open(os.path.join(parent_path, 'DATA.txt'), 'w', encoding='utf-8') as results:
    results.write(f'**************************************************'
                  f'**************************************************\n')
    results.write(f'Below is the data collected from all the inputted elections at large.\n')
    results.write(f'{numFiles} election(s) were tested, with an average of '
                  f'{avgVoters:.0f} voters and {avgCands:.1f} (σ = {cands_stdev}) candidates.\n')
    results.write(f'**************************************************'
                  f'**************************************************\n\n')
    results.write(f'Average portion of voters ranking only a single candidate:\n')
    results.write(f'μ = {q:.3f}, σ = {q_stdev}\n\n')
    results.write(f'Average portion of voters ranking all candidates:\n')
    results.write(f'μ = {s:.3f}, σ = {s_stdev}\n\n')
    results.write(f'Average portion of candidates that a voter ranked:\n')
    results.write(f'μ = {r:.3f}, σ = {r_stdev}\n\n')
    results.write(f'-----------------------------------------------\n'
                  f'Frequencies of agreement:\n'
                  f'-----------------------------------------------\n{data}')

# Used to create boxplot
# plt.figure(1)
# plt.boxplot([s_i_3cand, s_i_4cand, s_i_5cand, s_i_6cand, s_i_7cand], labels=['3', '4', '5', '6', '7'])
# plt.suptitle('Portion of Voters Ranking All Candidates as a Function of Candidate Number')
# plt.xlabel('Number of Available Alternatives')
# plt.ylabel('Portion Of Voters Ranking All Candidates')
# plt.show()
