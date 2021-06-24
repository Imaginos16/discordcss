from shutil import copyfile
import subprocess
import os
import filecmp

# Defines
THEME_NAME = 0
THEME_PATH = 1

# Variables
class vars:
    chosen_theme = None  # chosen list of theme info from theme_list, None until chosen

# Colors
class color:
    black = "\u001b[30m"
    red = "\u001b[31m"
    green = "\u001b[32m"
    yellow = "\u001b[33m"
    blue = "\u001b[34m"
    magenta = "\u001b[35m"
    cyan = "\u001b[36m"
    white = "\u001b[37m"
    end = "\u001b[0m"

# Themes
theme_list = [
    ["Default"],
    ["Exit"],
    ["Information Superhighway", "themes/InformationSuperhighway/discord.css"],
    ["Syndicate", "themes/Syndicate/discord.css"],
    ["ToonTown", "themes/ToonTown/discord.css"],
]

#==================================================================#
# Builds the menu to choose themes from (or revert to normal.)
# Ways to improve this in the future:
# * Smarter reverting - only revert when it needs to! right now
#   it will always revert when it may not need to
#==================================================================#
def select_theme():
    print(f"{color.green}Select a theme to enable!{color.end}")
    print("    #   Number - Theme\n    =========================================")
    iteration = 1
    for theme in theme_list:
        print(f">#{str(iteration)} - {theme[THEME_NAME]}")
        iteration += 1
    print(" ");
    chosen_index = 0
    while vars.chosen_theme == None:
        chosen_index = input("Theme #> ")
        if(not chosen_index.isnumeric()):
            print(f"{color.red}Please enter the number of the theme.{color.end}")
            continue
        if(not chosen_index.isnumeric() or not int(chosen_index) > 0 or not int(chosen_index) <= len(theme_list)):
            print(f"{color.red}Please enter a valid selection.{color.end}")
            continue
        chosen_index = int(chosen_index)
        vars.chosen_theme = theme_list[chosen_index-1]

#==================================================================#
# The actual beautifuldiscord call and setup
# if the hot reloader is already set up, the selected option may be the same
#==================================================================#
def hook():
    #setup (check needs to happen before file is copied or it will always fail)
    skip_hook = os.path.exists("discord.css")
    if(skip_hook and filecmp.cmp(vars.chosen_theme[THEME_PATH], "discord.css")):
        return
    print(f"{color.green}Selected {vars.chosen_theme[THEME_NAME]}!{color.end}{color.yellow}Loading...{color.end}")
    copyfile(vars.chosen_theme[THEME_PATH], os.path.abspath("discord.css"))
    if(skip_hook):
        return
    #call
    print(f"{color.yellow}hooking into discord (please wait until relaunch){color.end}")
    try:
        subprocess.run(["beautifuldiscord", "--css", os.path.abspath("discord.css")], stdout = subprocess.DEVNULL)
    except Exception as error:
        print(error)

#==================================================================#
# reverts hook, removes the discord.css file from main part of repo
#==================================================================#
def unhook_and_cleanup():
    already_default = not os.path.exists("discord.css")
    if(already_default):
        return
    try:
        subprocess.run(["beautifuldiscord", "--revert"], stdout = subprocess.DEVNULL)
    except Exception as error:
        print(f"{color.red}{error}{color.red}")
        print(f"{color.yellow}As discord is still assumingly hooked to the css, we are not going to del the css file.{color.end}")
        return
    os.remove("discord.css")

#==================================================================#
# Main code
#==================================================================#
def main():
    select_theme()
    if(vars.chosen_theme[THEME_NAME] == "Exit"):
        return
    if(vars.chosen_theme[THEME_NAME] == "Default"):
        unhook_and_cleanup()
        return
    hook()

main()
