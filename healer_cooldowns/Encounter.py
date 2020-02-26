from MyExceptions import Error, FormatError
from Classes import Person, Monk, Druid, Paladin, Priest, Shaman
import random

'''
This module holds all of the functions that are required by the encounter to run the simulation. The flow looks like this:

The driver module calls the addSpells() function to add spells from the classes into the encounters spellList array
The driver calls the aoeEvent() function for each event
aoeEvent() calls reduceCD() (reducing the status) and castRandAvailAoe() (to pick a random spell or two)
castRandAvailAoe() calls the castSpell() function (puts the spell on cooldown)

The rest are static functions used by the driver to set up which classes are participating in the encounter.
'''


class Encounter(object):

    def __init__(self):
        # tracking all spells the encounter class has access to cast
        self.spellList = []
        # tracking minor spells (I've defined minor spells as having an under two minute cooldown)
        self.minorSpells = []
        # tracking what was actually used during the encounter
        self.abilitiesUsed = []
        # tracking how many spells were used
        self.totalSpells = 0
        # tracking the sum of the cooldowns used (higher cooldown means more "worth" the ability is)
        self.spellSum = 0
        # tracking how many times no ability was able to be cast for an event
        self.totalNones = 0

    # This function aggregrates the spell list from a person into
    # the encounter object.
    def addSpells(self, spellList):
        for spell in spellList:
            if spell["hasSpell"]:
                self.spellList.append(spell)
                if spell["cooldown"] < 120:
                    self.minorSpells.append(spell)  

    # This function passes the time from the last event, and tries to cast one or two spells
    # randomly, if two spells are chosen, the second spell is always a minor ability, it then
    # returns an array of abilities that it used.
    def aoeEvent(self, time):
        # set up an array to track what was used on this event
        spellsUsed = []
        # randomly cast either one or two spells
        r = random.randint(0, 1)
        # pass the time from last event
        self.reduceCD(time, self.spellList)
        if r == 0:
            # cast a random spell
            spell = self.castRandAvailAoe(self.spellList)
            # if there was a spell off cooldown to use, add it to the list of used spells
            if spell:
                spellsUsed.append(spell)
        if r == 1:
            # cast one random spell and one minor spell
            spell1 = self.castRandAvailAoe(self.spellList)
            if spell1:
                spellsUsed.append(spell1)
            spell2 = self.castRandAvailAoe(self.minorSpells)
            if spell2:
                spellsUsed.append(spell2)
        # append whatever was used to spellsUsed
        self.abilitiesUsed.append(spellsUsed)   

    # This function reduces the "status" value based on however much 
    # time was passed to it. If the status is already 0 it skips it,
    # and if the status gets reduced below 0, it resets it to 0.
    def reduceCD(self, time, spellList):
        for spell in spellList:
            if spell["status"] == 0:
                continue
            else:
                spell["status"] -= time
                if spell["status"] < 0:
                    spell["status"] = 0

    # This function will cast a random ability and return the ability that was used
    # if no spell was off cooldown for casting, it will return nothing and add to
    # the none counter. 
    def castRandAvailAoe(self, spellList):
        # shuffle the spellList so that we pick a random one
        random.shuffle(spellList)

        # look for an aoe ability that is off cooldown
        for spell in spellList:
            if spell["status"] == 0 and spell["type"] == "aoe":
                # if we find one that's off cooldown, cast it
                self.castSpell(spell)
                # add it to the total spells tally
                self.totalSpells += 1
                # add it's cooldown to the sum
                self.spellSum += spell["cooldown"]
                return spell
            else:
                continue
        # if we make it here, all were on cooldown, add it to the none list
        self.totalNones += 1

    # This function will actually put the ability chosen on cooldown.
    def castSpell(self, spell):
        if spell["hasSpell"]:
            if spell["talentCooldown"]:
                spell["status"] = spell["shortCooldown"]
            else:
                spell["status"] = spell["cooldown"]
            return spell
        else:
            return ("Does not have {}".format(spell["name"])), self

    # This function asks the user for their set of event times, or offers them a default, returns an array of times
    @staticmethod
    def getEventTimes():
        userTimes = input('''Please enter the time (in seconds) between each event in the encounter.\
 Numbers should be sepearated by a comma and a space. (e.g: 15, 25, 27, 18) etc. 
The default encounter for this module is the Vectis fight, to use that, type "default"\n''')
        if userTimes.lower() == "default":
            return [20, 25, 25, 27, 53, 25, 26, 25, 54, 25, 25, 26, 54, 25, 25, 25]
        else:
            userTimes = userTimes.split(",")

        # if the length of the split is 1, either there is only one event (unlikely), or they formatted the times wrong
        if len(userTimes) == 1:
            raise FormatError("The formatting was input incorrectly, or there was only one time passed.")

        # build the array of event times
        eventTimes = []
        for time in userTimes:
            eventTimes.append(int(time))
        return(eventTimes)

    # static method used for determining which class is in the encounter to call a class specific function
    @staticmethod
    def getClassSpells():
        inputClassType = input("What class is this person? (Druid, Monk, Paladin, Priest, Shaman)\n")

        # using a dictionary as a switch statement
        # CREDIT: https://jaxenter.com/implement-switch-case-statement-python-138315.html
        switch = {
            "druid": Encounter.createDruid,
            "monk": Encounter.createMonk,
            "paladin": Encounter.createPaladin,
            "priest": Encounter.createPriest,
            "shaman": Encounter.createShaman
        }

        try:
            # call the function according to what the user typed in
            person = switch[inputClassType.lower()]()
        except:
            # if that didn't work, they typed something wrong, tell them then call the function again
            print("That was not the correct class name, please try again.")
            Encounter.getClassSpells()
        
        # return the array that was retrieved from the switch statement
        return person.spellList

    @staticmethod
    def createDruid():
        # get the information needed to create a druid object
        name = input("What is the name of the druid?\n")
        tree = input("Does {} have Tree form? (yes/no)\n".format(name))
        tranq = input("Does {} have the talent for short Tranquility? (yes/no)\n".format(name))
        flourish = input("Does {} have the flourish talent? (yes/no)\n".format(name))

        # set the druid object values based on the answers
        if tree.lower() == ("yes" or "y"):
            hasTree = True
        else:
            hasTree = False
        if tranq.lower() == ("yes" or "y"):
            hasShortTranq = True
        else:
            hasShortTranq = False
        if flourish.lower() == ("yes" or "y"):
            hasFlourish = True
        else:
            hasFlourish = False

        # actually create and return the druid object
        return Druid(hasTree, hasShortTranq, hasFlourish, name)

    @staticmethod
    def createMonk():
        name = input("What is the name of the monk?\n")
        crane = input("Does {} have the Way of the Crane talent? (yes/no)\n".format(name))

        if crane.lower() == ("yes" or "y"):
            hasCrane = True
        else:
            hasCrane = False

        return Monk(hasCrane, name)

    @staticmethod
    def createPaladin():
        name = input("What is the name of the paladin?\n")
        avenger = input("Does {} have the Holy Avenger talent? (yes/no)\n".format(name))

        if avenger.lower() == ("yes" or "y"):
            hasAvenger = True
        else:
            hasAvenger = False

        return Paladin(hasAvenger, name)

    @staticmethod
    def createPriest():
        name = input("What is the name of the priest?\n")
        spec = input("What spec is {}? (holy/disc)\n".format(name.title()))

        if spec == "holy":
            talent = input("Does {} have Holy Word: Savlation? (yes/no)\n".format(name))
        elif spec == "disc":
            talent = input("Does {} have the Evangelism talent? (yes/no)\n".format(name))
        else:
            print("That is not a valid spec name. Please try again.\n")
            Encounter.createPriest()

        if talent == ("yes" or "y"):
            hasTalent = True
        else:
            hasTalent = False

        return Priest(hasTalent, name, spec)

    @staticmethod
    def createShaman():
        name = input("What is the name of the Shaman?\n")
        totem = input("Does {} have the Earthen Wall Totem talent? (yes/no)\n".format(name))
        ascend = input("Does {} have the Ascendence talent? (yes/no)\n".format(name))

        if totem.lower() == ("yes" or "y"):
            hasTotem = True
        else:
            hasTotem = False
        if ascend.lower() == ("yes"):
            hasAscend = True
        else:
            hasAscend = False

        return Shaman(hasTotem, hasAscend, name)