import cmath
import math
import sys

import matplotlib.pyplot as plt
import numpy as np


COMMAND_INITIAL = '\0'

COMMAND_HELP = '?'

COMMAND_QUIT = 'q'
COMMAND_ABORT = '~'

COMMAND_ADD = 'a'
COMMAND_LOCAL_SUMMARY = 's'
COMMAND_GLOBAL_SUMMARY = 'S'

COMMAND_SHOW_GRAPH = '!'
COMMAND_DAMAGE = 'd'
COMMAND_HEAL = 'h'
COMMAND_PHASE_SHIFT = 'r'

COMMAND_OVERWRITE = 'o'

CONFIRM_YES = 'Y'
CONFIRM_NO = 'N'

OVERWRITE_MAX_HEALTH = 'H'
OVERWRITE_HEALTH = 'h'
OVERWRITE_PHASE = 'p'
OVERWRITE_INITIATIVE = 'i'

def main():
    welcome()

    character_list: list[character] = []

    command_help()

    command = COMMAND_INITIAL
    while (command != COMMAND_QUIT):
        try:
            main_command_loop(character_list)
        except (command_abort):
            print("COMMAND ABORTED")
            command_global_summary(character_list)
            print()

def welcome():
    print("Welcome to Character Tracker!")
    print("This program supports tracking multiple characters at once, but it is advised for screen sharers")
    print("to track their own characters on seperate screens")
    print()
    print("Enter anything to continue...")
    input()

def main_command_loop(character_list):
    print("Enter Command:")
    command = input()

    print()
    if (command == COMMAND_HELP):
        command_help()
    elif (command == COMMAND_ADD):
        command_add(character_list)
    elif (command == COMMAND_QUIT):
        command = command_quit()
    elif (command == COMMAND_LOCAL_SUMMARY):
        command_local_summary(character_list)
    elif (command == COMMAND_GLOBAL_SUMMARY):
        command_global_summary(character_list)
    elif (command == COMMAND_SHOW_GRAPH):
        command_show_graph(character_list)
    elif (command == COMMAND_DAMAGE):
        command_damage(character_list)
    elif (command == COMMAND_HEAL):
        command_heal(character_list)
    elif (command == COMMAND_PHASE_SHIFT):
        command_phase_shift(character_list)
    elif (command == COMMAND_OVERWRITE):
        command_overwrite(character_list)
    
    print()

def command_help():
    print("--HELP MENU--")
    print("Character tracker is used for health in the complex domain.")
    print("Enter arguments one line at a time.")
    print("This is because I'm both too lazy and too dumb to tokenize input.")
    print()
    print(f"'{COMMAND_HELP}' - Print this help menu.")
    print()
    print(f"'{COMMAND_ABORT}' - Input at any time to immediately abort process and return to main command loop.")
    print(f"'{COMMAND_QUIT}' - Quit the program.")
    print()
    print(f"'{COMMAND_ADD}' - Add a character")
    print(f"'{COMMAND_LOCAL_SUMMARY}' - Print all details for one character.")
    print(f"'{COMMAND_GLOBAL_SUMMARY}' - Print summaries for all characters.")
    print()
    print(f"'{COMMAND_SHOW_GRAPH}' - Display a visual representation of one character.")
    print(f"'{COMMAND_DAMAGE}' - Damage a character.")
    print(f"'{COMMAND_HEAL}' - Heal a character.")
    print(f"'{COMMAND_PHASE_SHIFT}' - Rotate a character's phase shift.")
    print()
    print(f"'{COMMAND_OVERWRITE}' - Overwrite a certain stat.")
    
# Override a certain stat
def command_overwrite(character_list):
    print("--OVERWRITE--")
    character = get_character(character_list)
    print("What would you like to overwrite?")
    print(f"'{OVERWRITE_MAX_HEALTH}' - Max health")
    print(f"'{OVERWRITE_HEALTH}' - Health")
    print(f"'{OVERWRITE_PHASE}' - Phase")
    print(f"'{OVERWRITE_INITIATIVE}' - Initiative")
    
    is_command_given = False
    while (not is_command_given):
        command = input()
        input_abort(command)
        
        is_command_given = True        
        if (command == OVERWRITE_MAX_HEALTH):
            overwrite_max_health(character)
        elif (command == OVERWRITE_HEALTH):
            overwrite_health(character)
        elif (command == OVERWRITE_PHASE):
            overwrite_phase(character)
        elif (command == OVERWRITE_INITIATIVE):
            overwrite_initiative(character)
        else:
            print("Enter one of the commands.")
            print(f"'{OVERWRITE_MAX_HEALTH}' - Max health")
            print(f"'{OVERWRITE_HEALTH}' - Health")
            print(f"'{OVERWRITE_PHASE}' - Phase")
            print(f"'{OVERWRITE_INITIATIVE}' - Initiative")
            is_command_given = False

def overwrite_max_health(character):
    new = scan_positive_nonzero_integer("Enter new max hp:")
    character.max_health = new
    character.clamp_health()
    print("Max health overwritten.")
    
def overwrite_health(character):
    new = scan_positive_nonzero_integer("Enter new hp:")
    arg = cmath.phase(character.health)
    character.health = cmath.rect(new, arg)
    character.clamp_health()
    print("Health overwritten.")
    
def overwrite_phase(character):
    new = scan_argument("Enter new phase shift (degrees):")
    
    new = deg_to_rad(difference)
    difference = new - character.phase
    character.shift_phase(difference)
    print("Phase overwritten.")
    
def overwrite_initiative(character):
    new = scan_positive_nonzero_integer("Enter new initiative:")
    character.initiative = new
    print("Initiative overwritten.")
    
def command_phase_shift(character_list):
    character = get_character(character_list)
    arg = scan_argument("Enter phase shift argument (degrees)")

    character.shift_phase(deg_to_rad(arg))
    print(f"{character.name}'s phase shifted by {arg}")

def command_heal(character_list):
    character = get_character(character_list)
    heal_mod = scan_positive_nonzero_integer("Enter value of healing received")
    heal_arg = deg_to_rad(scan_argument("Enter argument of healing received (degrees)"))
    heal = cmath.rect(heal_mod, heal_arg)

    character.take_heal(heal)

def command_damage(character_list):
    character = get_character(character_list)
    damage_mod = scan_positive_nonzero_integer("Enter value of damage taken")
    damage_arg = deg_to_rad(scan_argument("Enter argument of damage taken (degrees)"))
    damage = cmath.rect(damage_mod, damage_arg)

    character.take_damage(damage)
    print(f"{character.name} damaged by {damage_mod}∠{rad_to_deg(damage_arg)}")

def scan_argument(print_prompt) -> int:
    while (1):
        print(print_prompt)
        number = input()
        input_abort(number)
        try:
            return int(number)
        except ValueError:
            print("Please enter an integer")
            continue

def scan_positive_nonzero_integer(print_prompt) -> int:
    while (1):
        print(print_prompt)
        number = input()
        input_abort(number)
        try:
            number = int(number)
        except ValueError:
            print("Please enter a positive, non-zero integer")
            continue
        
        if (number <= 0):
            print("Please enter a positive, non-zero integer")
        else:
            return number

def command_show_graph(character_list):
    character = get_character(character_list)
    print("Showing graph...")
    character.print_graph()
    print("Graph closed.")

def command_add(character_list):
    print("--ADD CHARACTER--")
    name = scan_name(character_list)
    max_hitpoints = scan_positive_nonzero_integer("Enter max hitpoints:")
    
    initiative = scan_positive_nonzero_integer("Enter initiative:")
        
    character_list.append(character(max_hitpoints, initiative, name))
    print(f"{name} added!")

def scan_name(character_list):
    while (1):
        print("Enter name:")
        name = input()
        input_abort(name)

        is_name_unique = True
        for character in character_list:
            if (character.name == name):
                print(F"{name} is already taken!")
                is_name_unique = False
                break
        
        if (is_name_unique):
            return name
        
    print("Something went wrong in scan_name!!!")
    return None

def command_global_summary(character_list):
    print("----GLOBAL SUMMARY----")
    sort_by_initiative(character_list)
    for character in character_list:

        lower, upper = character.get_danger_arg()
        lower = round(rad_to_deg(lower), 2)
        upper = round(rad_to_deg(upper), 2)

        print(f"Summary for {character.name}")
        print(f"Initiative: {character.initiative}")
        print(f"Phase shift: {rad_to_deg(character.phase)}")
        print(f"Danger argument = {lower} <= DEATH <= {upper}")
        print(f"Polar health: {round(abs(character.health), 2)}∠{round(positive_principle_arg(rad_to_deg(cmath.phase(character.health))), 2)}")
        print("----------------------")

def command_local_summary(character_list):
    print("--LOCAL SUMMARY--")
    character = get_character(character_list)

    lower, upper = character.get_danger_arg()
    lower = round(rad_to_deg(lower), 2)
    upper = round(rad_to_deg(upper), 2)
    print(f"Summary for {character.name}")
    print(f"Hitpoints: {round_complex(character.health)}")
    print(f"Initiative: {character.initiative}")
    print(f"Hitpoint value: {round(abs(character.health), 2)}/{character.max_health}")
    print(f"Phase shift: {round(rad_to_deg(character.phase), 2)}")
    print(f"Danger argument = {lower} <= DEATH <= {upper}")
    print(f"Polar health: {round(abs(character.health), 2)}∠{round(positive_principle_arg(rad_to_deg(cmath.phase(character.health))), 2)}")

def command_quit():
    command = COMMAND_INITIAL
    while command != CONFIRM_YES and command != CONFIRM_NO:
        print(f"Are you sure? {CONFIRM_YES}/{CONFIRM_NO}")
        command = input()
        input_abort(command)

    if command == CONFIRM_YES:
        command = COMMAND_INITIAL
        while command != CONFIRM_YES and command != CONFIRM_NO:
            print(f"Are you REALLY sure? {CONFIRM_YES}/{CONFIRM_NO}")
            command = input()
            input_abort(command)

        if command == CONFIRM_YES:
            print("Ok bye 🖕")
            sys.exit()

    return COMMAND_INITIAL

def input_abort(command):
    if (command == COMMAND_ABORT):
        raise command_abort()
    
class character:
    def __init__(self, health, initiative, name):
        self.health = complex(health, 0)
        self.name = name
        self.phase = float(0)
        self.max_health = health
        self.initiative = initiative

    def clamp_health(self):
        arg = cmath.phase(self.health)
        value = abs(self.health)

        if (value > self.max_health):
            value = self.max_health
        
        self.health = cmath.rect(value, arg)
    
    def clamp_argument(self):
        if (self.phase < 0):
            self.phase = 0
        elif (self.phase > 2 * math.pi):
            self.phase = 2 * math.pi
    
    def take_damage(self, damage):
        self.health -= damage
        self.clamp_health()

    def take_heal(self, heal):
        self.health += heal
        if (abs(self.health) > self.max_health):
            overheal = abs(self.health) - self.max_health
            print(f"{self.name} overhealed by {overheal}.")
        else:
            print(f"Healed {self.name} by {heal}")
        self.clamp_health()
    
    def shift_phase(self, shift_argument):
        cartesian_shift = cmath.rect(1, shift_argument)
        self.health *= cartesian_shift
        self.phase += shift_argument
        self.clamp_argument()

    def get_danger_arg(self):
        arg1 = self.phase + math.pi * 3 / 4
        arg2 = self.phase - math.pi * 3 / 4

        if (arg1 > 2 * math.pi):
            arg1 -= 2 * math.pi
        
        if (arg2 < 0):
            arg2 += 2 * math.pi
        
        if (arg1 > arg2):
            return arg2, arg1
        else:
            return arg1, arg2
    
    def print_graph(self):
        plt.axhline(0, color = 'black', linewidth = 1)
        plt.axvline(0, color = 'black', linewidth = 1)
        plt.axis('off')

        theta = np.linspace(0, 2*np.pi, 400)
        x_circle = self.max_health * np.cos(theta)
        y_circle = self.max_health * np.sin(theta)
        plt.plot(x_circle, y_circle, color = 'black', linestyle = '--', label = 'Circle')

        x_line = [0, self.max_health * np.cos(self.phase)]
        y_line = [0, self.max_health * np.sin(self.phase)]
        plt.plot(x_line, y_line, color = 'gray', label = 'Phase')

        fill_around_argument = self.phase + math.pi
        theta_sector = np.linspace(fill_around_argument - (1/4 * math.pi), fill_around_argument + (1/4 * math.pi), 100)
        x_sector = self.max_health * np.cos(theta_sector)
        y_sector = self.max_health * np.sin(theta_sector)
        x_fill = np.concatenate([[0], x_sector])
        y_fill = np.concatenate([[0], y_sector])
        plt.fill(x_fill, y_fill, color = 'red', alpha = 0.3, label = 'Sector')

        x_point = self.health.real
        y_point = self.health.imag

        plt.plot(x_point, y_point, marker = 'o', color = 'green', markersize = 9)

        plt.axis('equal')

        print("Close graph to continue.")
        plt.show()

def get_character(character_list) -> character:
    if (len(character_list) == 1):
        return character_list[0]
    found = False
    while (not found):
        print("Enter character name:")
        name = input()
        input_abort(name)

        for character in character_list:
            if character.name == name:
                found = True
                return character
        print(f"Character named '{name}' not found")
        
def sort_by_initiative(character_list):
    sorted = False
    while (not sorted):
        sorted = True
        for i in range(0, len(character_list)):
            for j in range(i, len(character_list)):
                if (character_list[i].initiative < character_list[j].initiative):
                    swap_characters(character_list, i, j)
                    sorted = False
                

def swap_characters(character_list, index1, index2):
    temp = character_list[index1]
    character_list[index1] = character_list[index2]
    character_list[index2] = temp
    

def deg_to_rad(arg):
    new = arg * math.pi / 180
    return new

def rad_to_deg(arg):
    new = arg / math.pi * 180
    return new

def positive_principle_arg(arg):
    new = arg
    if (new > 2 * math.pi):
        new -= 2 * math.pi

    if (new < 0):
        new += 2 * math.pi
    return new

def round_complex(z):
    new = complex(round(z.real, 2), round(z.imag, 2))
    return new

class command_abort(Exception):
    pass

if (__name__ == "__main__"):
    main()
        