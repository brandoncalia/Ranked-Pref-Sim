import numpy as np
from pathlib import Path
import os

parent_path = Path(__file__).parent
files_path = os.path.join(parent_path, 'Files')
result_files = os.path.join(parent_path, 'Results')

# Iterate through each dataset in 'Files' folder
for filename in os.listdir(files_path):

    election_file = os.path.join(files_path, filename)
    votes = open(election_file)
    info = votes.readlines()[1:11]
    numAlternatives = int(info[8].split(': ')[1])
    numVoters = int(info[9].split(': ')[1])
    resultName = info[0].split(': ')[1].replace(' ', '').strip()
    pairCompArr = np.zeros((numAlternatives, numAlternatives))
    bordaTally = np.zeros(numAlternatives)
    FirstPlaceVotes = np.zeros(numAlternatives)
    SecondPlaceVotes = np.zeros(numAlternatives)
    appearanceTally = np.zeros(numAlternatives)
    voterMatrix = np.empty((numAlternatives, 0))
    singleCandBallots, fullBallots, numSpotsFilled = 0, 0, 0
    votes = open(election_file)

    for line in votes.readlines()[numAlternatives + 12:]:

        # Create the ballot array
        rankings = line.strip().split(': ')
        numBallots = int(rankings[0])
        rankings = rankings[1].split(',')
        ballot = np.repeat(-1, numAlternatives)
        ballot[0:len(rankings)] = rankings

        # Check for duplicate candidates and reformat to Python indexing
        for j in range(numAlternatives):
            count = len(np.where(ballot == ballot[j])[0])
            if count > 1 and ballot[j] != -1:
                ballot = np.delete(ballot, np.where(ballot == ballot[j])[0][count - 1])
                ballot = np.resize(ballot, numAlternatives)
                ballot[numAlternatives - 1] = -1
        for w in range(numAlternatives):
            if ballot[w] != -1:
                ballot[w] -= 1

        # Check for blank ballot
        if np.array_equal(ballot, [-1] * numAlternatives):
            continue

        # Begin tallying / storing votes
        currentBallot = [int(val) for val in ballot]
        for cand in currentBallot:
            if cand != -1:
                numSpotsFilled += 1 * numBallots
        if currentBallot[1] == -1:
            singleCandBallots += 1 * numBallots
        elif -1 not in currentBallot:
            fullBallots += 1 * numBallots
        voterMatrix = np.append(voterMatrix, np.repeat(np.array([currentBallot]).T, numBallots, axis=1), axis=1)

    # Borda, Plurality, & Pairwise Comparisons
        FirstPlaceVotes[currentBallot[0]] += 1 * numBallots
        if currentBallot[1] != -1:
            SecondPlaceVotes[currentBallot[1]] += 1 * numBallots
        for j in range(numAlternatives):
            if int(currentBallot[j]) != -1:
                bordaTally[int(currentBallot[j])] += (numAlternatives - j) * numBallots
                appearanceTally[int(currentBallot[j])] += 1 * numBallots
                for w in range(numAlternatives):
                    if w not in currentBallot:
                        pairCompArr[currentBallot[j]][w] += 1 * numBallots
            else:
                continue
            for x in range(j + 1, numAlternatives):
                if currentBallot[x] != -1:
                    pairCompArr[currentBallot[j]][currentBallot[x]] += 1 * numBallots
    bordaWinner, pluralityWinner = np.argmax(bordaTally) + 1, np.argmax(FirstPlaceVotes) + 1
    singleCandBallots = singleCandBallots / numVoters
    numSpotsFilled = numSpotsFilled / (numVoters * numAlternatives)
    fullBallots = fullBallots / numVoters

    # Instant Runoff
    IRVoterMatrix, IRtally = voterMatrix.copy(), FirstPlaceVotes[:]
    for i in range(numAlternatives - 1):
        a = np.sort(IRtally)
        elimination = np.where(IRtally == a[i])[0][0]
        IRtally = np.zeros(numAlternatives)
        IRVoterMatrix[IRVoterMatrix == elimination] = -1
        for ballot in IRVoterMatrix.T:
            for candidate in ballot:
                if candidate != -1:
                    IRtally[int(candidate)] += 1
                    break
    IRwinner = np.argmax(IRtally) + 1

    # Condorcet
    condorcetWinner = None
    for z in range(numAlternatives):
        if condorcetWinner is not None:
            break
        for g in range(numAlternatives):
            if (pairCompArr[g][z] >= pairCompArr[z][g]) and (z != g):
                break
            elif g == numAlternatives - 1:
                condorcetWinner = z + 1
                break

    # Baldwin
    baldwinVoterMatrix, baldwinTally = voterMatrix.copy(), bordaTally[:]
    for z in range(numAlternatives - 1):
        b = np.sort(baldwinTally)
        elimination = np.where(baldwinTally == b[z])[0][0]
        baldwinTally = np.zeros(numAlternatives)
        baldwinVoterMatrix[baldwinVoterMatrix == elimination] = -1
        for ballot in baldwinVoterMatrix.T:
            for idx, candidate in enumerate(ballot):
                if candidate != -1:
                    baldwinTally[int(candidate)] += numAlternatives - idx
    baldwinWinner = np.argmax(baldwinTally) + 1

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
            results.write('A Condorcet winner does not exist.\n')
        results.write(f'Instant runoff selects:\n{IRwinner}\n\n')
        results.write(f'Baldwin selects:\n{baldwinWinner}\n\n')
        results.write(f'Borda tally:\n{bordaTally}\n\n')
        results.write(f'First place votes tally:\n{FirstPlaceVotes}\n\n')
        results.write(f'Second place votes tally:\n{SecondPlaceVotes}\n\n')
        results.write(f'Appearance tally:\n{appearanceTally}\n\n')
        results.write(f'Portion of voters ranking only a single candidate:\n{singleCandBallots:.4f}\n\n')
        results.write(f'Portion of voters ranking all candidates:\n{fullBallots:.4f}\n\n')
        results.write(f'Average portion of candidates that a voter ranked:\n{numSpotsFilled:.4f}')
