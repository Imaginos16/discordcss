from beautifuldiscord.app import discord_process
from shutil import copyfile
import subprocess
import os

# Defines
THEME_NAME = 0
THEME_PATH = 1

# Variables
class vars:
    chosen_theme = None  # chosen list of theme info from theme_list, None until chosen
    

# Themes
theme_list = [
    ["Default"],
    ["Information Superhighway", "themes/InformationSuperhighway/discord.css"],
    ["Syndicate", "themes/Syndicate/discord.css"],
    ["WIP theme", "themes/ToonTown/discord.css"],
]

#==================================================================#
# Builds the menu to choose themes from (or revert to normal.)
# Ways to improve this in the future:
# * Smarter reverting - only revert when it needs to! right now
#   it will always revert when it may not need to
#==================================================================#
def select_theme():
    print("Select a theme to enable!")
    print("    #   Number - Theme\n    =========================================")
    iteration = 1
    for theme in theme_list:
        print(">#" + str(iteration) + " - " + theme[THEME_NAME])
        iteration += 1
    print(" ");
    chosen_index = 0
    while vars.chosen_theme == None:
        chosen_index = input("Theme #> ")
        if(not chosen_index.isnumeric()):
            print("Please enter the number of the theme.")
            continue
        if(not chosen_index.isnumeric() or not int(chosen_index) > 0 or not int(chosen_index) <= len(theme_list)):
            print("Please enter a valid selection.")
            continue
        chosen_index = int(chosen_index)
        vars.chosen_theme = theme_list[chosen_index-1]

#==================================================================#
# The actual beautifuldiscord call and setup
#==================================================================#
def hook():
    #setup (check needs to happen before file is copied or it will always fail)
    needs_to_hook = not os.path.exists("discord.css")
    print("Selected " + vars.chosen_theme[THEME_NAME] + "! Loading...")
    copyfile(vars.chosen_theme[THEME_PATH], os.path.abspath("discord.css"))
    if(not needs_to_hook):
        return
    #call
    print("hooking into discord (please wait until relaunch)")
    subprocess.run(["beautifuldiscord", "--css", os.path.abspath("discord.css")])

#==================================================================#
# reverts hook, removes the discord.css file from main part of repo
#==================================================================#
def unhook_and_cleanup():
    try:
        subprocess.run(["beautifuldiscord", "--revert"])
    except Exception as error:
        print(error)
        print("As discord is still assumingly hooked to the css, we are not going to del the css file.")
        return
    os.remove("discord.css")

#==================================================================#
# Main code
#==================================================================#
def main():
    select_theme()
    if(vars.chosen_theme[THEME_NAME] == "Default"):
        unhook_and_cleanup()
        return
    hook()

main()
