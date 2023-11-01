--- SKI SURVIVAL by Evan Nygard ---
--- 15-112 term project ---

--- INTRODUCTION TO GAMEPLAY ---
Ski Survival is a game based on SkiFree by Chris Pirih. The basic goal in Standard mode is to survive as long as possible without crashing into obstacles or being eaten by werewolves. Obstacles are randomly generated on the map such that no two obstacles collide on top of each other. Additionally, obstacles saturate the map to an increasing degree as gameplay continues over time.

The types of obstacles are:
- Trees
- Rocks, which can be jumped over
- Fallen logs, which can be jumped over
- Rivers, which span the entire width and can (and must) be jumped over
- Slalom poles, which cannot be jumped over. If the player passes very close to the pole on the proper side, extra points are earned.
- Snowdrifts, which do not cause death upon collision but do slow you down
- Werewolves, which are an NPC (non-player character) that attempts to chase the player down

In addition to standard mode, two other gameplay modes exist:
- Werewolf Chase - same goal as Standard mode (survive as long as possible) but generates huge packs of werewolves instead of most normal obstacles
- Slalom - a timed round where the only way to earn points is by skirting around slalom poles (which form the vast majority of obstacles on this map). Attempt to score as many points as possible before the 60-second time limit is up.

--- SETTING UP SOURCE FILES ---
Make sure all images are downloaded from the zip file. Additionally, three supporting source files -  highScoreStandard.txt, highScoreWerewolf.txt, and highScoreSlalom.txt - should be included, although they can be created manually if necessary. To do this, create the three text files in the same directory as the code files and type in the number '0' in each one. The program will do the rest.

--- HOW TO RUN ---
The program should be run from term_project.py. In VSCode, the program is run by hitting Cmd-B (on Mac) from the term_project.py file. Substitute instructions for running code for your particular OS and editor, as long as you're running the program from term_project.py.

--- EXTERNAL MODULES ---
Ski Survival requires CMU 112 Graphics in order to run properly, as well as tkinter and the built in modules math, copy, time, and random.

--- SHORTCUT COMMANDS ---
Shortcut commands are executed by typing in keys as the game is running.

Commands that work in any mode:
'p' = pause the game
'r' = restart the game
'h' = return to the home screen

Additionally, the following commands will generate particular obstacles in Standard mode only:
't' = Tree
'k' = Rock
'l' = Fallen log
'v' = River
's' = Slalom pole
'd' = Snowdrift
'w' = Werewolf

Note that these shortcuts will bypass the check-for-collision algorithm, so there is a chance that one of these objects could be generated on top of another.