# HealerCDs - Non-Github README formatted
Program for determining optimal healer raid-wide area-of-effect (aoe) spells for a boss encounter in World of Warcraft

Run the Driver.py to start the application. It will ask for the fight and healer details during execution.

If you are unfamiliar with World of Warcraft, here is an example of the script being run along with some example inputs:

### EXAMPLE ###

Please enter the time (in seconds) between each event in the encounter. Numbers should be sepearated by a comma and a space. (e.g: 15, 25, 27, 18) etc.
The default encounter for this module is the Vectis fight, to use that, type "default"
default
How many healers does your raid have? (2-5)
4
--- Next Person ---
What class is this person? (Druid, Monk, Paladin, Priest, Shaman)
druid
What is the name of the druid?
Druid1
Does Druid1 have Tree form? (yes/no)
yes
Does Druid1 have the talent for short Tranquility? (yes/no)
yes
Does Druid1 have the flourish talent? (yes/no)
no
Person Successfully Added

--- Next Person ---
What class is this person? (Druid, Monk, Paladin, Priest, Shaman)
priest
What is the name of the priest?
Priest1
what spec is priest1? (holy/disc)
disc
Does Priest1 have the Evangelism talent? (yes/no)
yes
Person Successfully Added

--- Next Person ---
What class is this person? (Druid, Monk, Paladin, Priest, Shaman)
Shaman
What is the name of the Shaman?
Shaman1
Does Shaman1 have the Earthen Wall Totem talent? (yes/no)
yes
Does Shaman1 have the Ascendence talent? (yes/no)
no
Person Successfully Added

--- Next Person ---
What class is this person? (Druid, Monk, Paladin, Priest, Shaman)
Paladin
What is the name of the paladin?
Paladin1
Does Paladin1 have the Holy Avenger talent? (yes/no)
no
Person Successfully Added

Please input the number of simulations that you'd like the script to run. The higher the number of simulations, the more accurate the results. In general, 100,000 simulations is decently accurate and takes ~4 seconds to run. 1,000,000 simulations is about as accurate as it gets, but takes ~45 seconds to run. (This can vary heavily based on CPU speeds/number of cores)
1000000

---------------RESULTS--------------

180      Priest1 used [Power Word: Barrier]
180 90   Shaman1 used [Healing Tide Totem], Priest1 used [Evangelism]
120 60   Druid1 used [Tranquility], Shaman1 used [Earthen Wall Totem]
180      Paladin1 used [Aura Mastery]
180 90   Shaman1 used [Spirit Link Totem], Priest1 used [Evangelism]
180      Druid1 used [Tree]
180      Priest1 used [Power Word: Barrier]
180 60   Shaman1 used [Healing Tide Totem], Shaman1 used [Earthen Wall Totem]
120 90   Druid1 used [Tranquility], Priest1 used [Evangelism]
180      Paladin1 used [Aura Mastery]
180 60   Shaman1 used [Spirit Link Totem], Shaman1 used [Earthen Wall Totem]
180      Druid1 used [Tree]
180 60   Priest1 used [Power Word: Barrier], Shaman1 used [Earthen Wall Totem]
120      Druid1 used [Tranquility]
180 90   Shaman1 used [Healing Tide Totem], Priest1 used [Evangelism]
180 60   Paladin1 used [Aura Mastery], Shaman1 used [Earthen Wall Totem]

Number of cooldowns used: 25
Sum of their cooldowns: 3540
Total simulation run time: 48 seconds.