from Encounter import Encounter
from Classes import Person, Monk, Druid, Paladin, Priest, Shaman
from time import time as myTime
import multiprocessing

'''
This module is the module that will actually be executed in order to perform the simulations.
All of the data required by the script will be retrieved by asking the user during
run time. If the script encounters an error, sometimes it will tell the user and 
let them try and fix it, but others will stop the script all together (may need refining)
'''

# This function handles running a number of simulations for multiprocessing purposes (comment and credit below)
def runEncounterSims(process_id, numSimulations, allSpells, eventTimes, allowedNones, return_dict):
    highestSum = 0
    spellOrder = None
    for x in range(int(numSimulations)):
        encounter = Encounter()

        for spellList in allSpells:
            encounter.addSpells(spellList)
        
        for time in eventTimes:
            encounter.aoeEvent(time)

        # if the sum is higher than the highest, and it meets our 'none' requirements:
        if encounter.spellSum > highestSum and encounter.totalNones <= allowedNones:
            # record the order of the spells used
            spellOrder = encounter.abilitiesUsed
            # record the number of spells used
            highestCount = encounter.totalSpells
            # record the sum of the cooldowns
            highestSum = encounter.spellSum

    if spellOrder:
        return_dict[process_id] = {"spellOrder":spellOrder, "spellCount":highestCount, "spellSum":highestSum}
    else:
        return_dict[process_id] = None

if __name__ == "__main__":
    # tracking which simulation had the highest count of abilities used
    highestCount = 0
    # tracking which simulation had the highest sum of cooldowns used
    highestSum = 0
    # tracking the order the abilities were used in the "best" simulation
    spellOrder = []
    # assigning a floor to the amount of nones I want to allow, or else the simulation will just front load abilities and pay no attention to events where nothing can be cast.
    # I would rather there be no events without a cd being used than get the highest possible, so this value gets slowly incremented with each iteration if it's not possible
    # to cover every event with an ability
    allowedNones = 0
    # tracking whether or not we've found results that meet the criteria
    results = False
    # number of parallel processes to run (allow user to configure this?)
    processesNum = 4

    # getting the event times from the user
    eventTimes = Encounter.getEventTimes()

    # aggregating all of the spells that the encounter will have access to. This will be a matrix.
    allSpells = []
    numHealers = int(input("How many healers does your raid have? (2-5)\n"))
    for i in range(numHealers):
        print("--- Next Person ---")
        # add all of the people and their class/specs to the encounter. getClassSpells() returns an array of spells for each class.
        allSpells.append(Encounter.getClassSpells())
        print("Person Successfully Added\n")

    # getting the number of simulations the user would like to run

    # (note) since this script is mostly just trying random permutations and seeing which ends with the best results,
    # the higher the number of simulations, the more accurate it will be. I have noticed that ~1,000,000 simulations 
    # seems to be enough to get an accurate result almost every time. 1,000,000 simulations takes approximately 
    # 45 seconds. 100,000 simulations takes about 4 seconds, but is quite a bit less accurate. These numbers can 
    # vary a lot depending on CPU speeds and whether it has at least 4 cores to use.
    numSimulations = int(input("Please input the number of simulations that you'd like the script to run.\
 The higher the number of simulations, the more accurate the results. In general, 100,000 simulations\
 is decently accurate and takes ~4 seconds to run. 1,000,000 simulations is about as accurate as it gets,\
 but takes ~45 seconds to run. (This can vary heavily based on CPU speeds/number of cores)\n"))

    if numSimulations < 4:
        print("That is not enough simulations, this script requires at least 4. Please try again:")
        numSimulations = int(input("Please enter the number of simulations:\n"))

    # timing how long the script takes to complete
    startTime = myTime()

    # loop until we've found results we are satisfied with
    while results == False:
        # Using the multiprocessing library to increase the calculation speed drastically since this script is CPU gated.
        # The syntax for doing this is a modified version from the official python documentation as well as the following
        # stack overflow post:
        # https://docs.python.org/3/library/multiprocessing.html
        # https://stackoverflow.com/questions/10415028/how-can-i-recover-the-return-value-of-a-function-passed-to-multiprocessing-proce
        
        # create a multiprocess manager to pass information back to the main script from each process in the form of a dictionary
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        jobs = []
        # divide the total number of simulations up for each process to distribute the load evenly 
        numSimulationsPerProcess = numSimulations / processesNum

        for i in range(processesNum):
            # have each process run their number of encounter simluations i will be their process ID
            p = multiprocessing.Process(target=runEncounterSims, args=(i, numSimulationsPerProcess, allSpells, eventTimes, allowedNones, return_dict))
            jobs.append(p)
            p.start()

        for proc in jobs:
            proc.join()

        # the data in return_dict is stored in a nested dictionary, "key" refers to the process ID
        for key in return_dict:
            # if the simulation found results
            if return_dict[key]:
                if return_dict[key]["spellSum"] > highestSum:
                    highestSum = return_dict[key]["spellSum"]
                    highestCount = return_dict[key]["spellCount"]
                    spellOrder = return_dict[key]["spellOrder"]
                    results = True
        allowedNones += 1
    endTime = myTime()

    print("\n---------------RESULTS--------------\n")
    # formatting the results to be readable
    for x in range(len(spellOrder)):
        # if only one ability was cast for a specific event
        if len(spellOrder[x]) == 1:
            # if the spell has a shorter cooldown due to talents, make sure to display that cooldown instead of the base one
            if spellOrder[x][0]["talentCooldown"]:
                # Show the output like: [Cooldown] <tab> [Player] used [Ability]
                # the output of this ends up looking like: 180      Ruru used [Tree]
                print("{} \t {} used [{}]".format(spellOrder[x][0]["shortCooldown"], str(spellOrder[x][0]["owner"]).title(), spellOrder[x][0]["name"].title()))
            else:
                print("{} \t {} used [{}]".format(spellOrder[x][0]["cooldown"], str(spellOrder[x][0]["owner"]).title(), spellOrder[x][0]["name"].title()))
        # if two abilities were used for the event, show both cooldowns and abilities on one line.
        elif len(spellOrder[x]) == 2:
                if spellOrder[x][0]["talentCooldown"]:
                    # the output of this ends up looking like: 180 60   Nick used [Aura Mastery], Thunder used [Earthen Wall Totem]
                    print("{} {} \t {} used [{}], {} used [{}]".format(spellOrder[x][0]["shortCooldown"], spellOrder[x][1]["cooldown"], str(spellOrder[x][0]["owner"]).title(), spellOrder[x][0]["name"].title(), str(spellOrder[x][1]["owner"]).title(), spellOrder[x][1]["name"].title()))
                elif spellOrder[x][1]["talentCooldown"]:
                    print("{} {} \t {} used [{}], {} used [{}]".format(spellOrder[x][0]["cooldown"], spellOrder[x][1]["shortCooldown"], str(spellOrder[x][0]["owner"]).title(), spellOrder[x][0]["name"].title(), str(spellOrder[x][1]["owner"]).title(), spellOrder[x][1]["name"].title()))
                else:
                    print("{} {} \t {} used [{}], {} used [{}]".format(spellOrder[x][0]["cooldown"], spellOrder[x][1]["cooldown"], str(spellOrder[x][0]["owner"]).title(), spellOrder[x][0]["name"].title(), str(spellOrder[x][1]["owner"]).title(), spellOrder[x][1]["name"].title()))
        else:
            print("No spells were used on this event.")

    print("\nNumber of cooldowns used: " + str(highestCount))
    print("Sum of their cooldowns: " + str(highestSum))
    print("Total simulation run time: " + str(int(endTime - startTime)) + " seconds.")