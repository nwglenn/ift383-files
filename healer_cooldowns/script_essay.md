This is a script that will tell you an optimal order of using healer cooldowns during a raid boss fight in World of Warcraft. The way that it accomplishes this is by running simulations where random abilities are used throughout the boss fight and the script will keep track of which simulation had the best results. I have defined the best results as the sum of the spell cooldowns (as abilities with higher cooldowns carry more "weight", so I would prefer if the script prioritized getting the most value out of the spells) as well as the result with the least "nones". I have defined "nones" as events where a boss did something, and there was no healer cooldowns to be cast for that event. If I didn't try and filter out the nones, the script would front load all of the abilities just to get them on cooldown therefore being able to cast more which could potentially lead to lots of holes in the encounter where nothing could be cast. This particular script will gather all of the information during runtime regarding which healers their particular raid group has and the timers between each boss event (I have provided a "default" option which is a set of timers that pertain to the "Vectis" boss fight for easier testing). 

I had the idea for this script around a year ago, but never sat down and tried to implement it until this extra credit opportunity appeared. I used Python as that is the language that I have the most familiarity with and made the most sense for me to use for what the script needed to do. The code went through lots of phases as I learned more about how the script needed to work and how I could get it to work. At first, I had defined a bunch of classes that mapped up to the WoW classes and each had a specific function that would call their ability. It quickly became apparent that this would be too much to try and code, and didn't capture as much information that the script needed to make decisions. I then had the idea just to hold all of the spell information in dictionaries for each class so that I could keep track of things like cooldowns, spell names, whether they had a spell or not, and who owned the spell, etc. After I took down all of the spell information, I then created an Encounter class that would hold all of the functions required to actually carry out the encounter (pick spells, cast them, keep track of them, etc). I then tried to make the WoW classes as children to the Encounter class, but I quickly realized that I would need to make some of the Encounter variables class variables which didn't work with the logic I had been working with because I needed to create a fresh encounter for each simulation and class variables would carry over to the next simulation. I then created some static functions within the Ecnounter class just to be able to gather and create the objects needed by the user. Finally, I created a separate Driver file that would hold the main() method for execution of the script which gathers all of the user information as well as runs the encounter.

Code for the script started off pretty simple, I started with things like "can I build a class and have it cast a spell?" and then once I figured that out, I was able to make it simulate as if time was passing so that the spell could be cast again at a later time. Once I got that working, I was able to create the rest of the classes and then slowly start testing various Encounter functions until it all came together. The hardest part of the testing was first figuring out how I was going to store the information from what the script did (stuff like which spell was cast when, and how I was going to track cooldowns, how each simulation did, etc.) One of the hardest parts was figuring out how to hold the spell information, which I finally ended up with dictionaries, and another was trying to define what was the "best" result for a simulation. At first, it would front load all of the abilities and leave a lot of "none" events so I had to find a way to limit that by just not allowing ANY "none" events at first, then let it have one, then two, then three, etc until it found the simulation that lead to the least amount of nones possible. Another interesting problem that I had was how long the script took to execute. To get decently accurate results it would take upwards of 2+ minutes. I knew that multithreaded processing was a possibility so I looked into that and found the multiprocess python package that allowed me to split up the simulation groups and have 4 simulation threads running at the same time which drastically sped up results. Something that took 10 minutes before was taking ~25 seconds.

The word of advice I would give myself would be "use dictionaries right from the get go" so that I didn't have to spend so much of my time trying to figure out how to generalize my functions and track spell information. That was the slowly portion of the script which everything picked up after I got past that.


### EXAMPLE ON HOW TO RUN THE SCRIPT ###

Here is an example of what to input to the script in case it's needed for testing:

Inputs in order: default, 4, druid, druid1, yes, yes, no, priest, priest1, disc, yes, shaman, shaman1, yes, no, paladin, paladin1, no, 1000000

That would look like this:

$ python3 Driver.py

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