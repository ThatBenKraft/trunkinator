"""
# Trunkinator Terminal
Used to generate Trunk schedules. Displays show combinations in popup window.
Dependencies: pandas
"""

import os
import random
import time
import tkinter as tk
from pathlib import Path
from tkinter import scrolledtext

import pandas as pd

__author__ = "Ben Kraft"
__copyright__ = "None"
__credits__ = "Ben Kraft"
__license__ = "Apache 2.0"
__version__ = "1.0"
__maintainer__ = "Ben Kraft"
__email__ = "benjamin.kraft@tufts.edu"
__status__ = "Prototype"

# Defines number of roles in show and number of performance days in week
NUM_ROLES = 5
NUM_DAYS = 3
# Amount of blank space used in display padding
DISPLAY_PADDING = 3
# Sets terminal mode
TERMINAL_MODE = False

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Change the current working directory to the directory of the script
os.chdir(script_dir)
# Define a path for trunker show data
DATA_PATH = Path("trunker_data.xlsx")


def output(line: str, newline: bool = True):
    if newline:
        line = f"{line}\n"
    output_text.insert(tk.END, line)


class Show:
    """
    Used for show information calculation and storage. Includes get methods for
    names, availabilities, and rosters.
    """

    def __init__(
        self,
        data_frame: pd.DataFrame,
        num_roles: int = 5,
        num_days: int = 3,
    ) -> None:
        """
        Creates Show object and calculates all availabilities.
        """
        self.data = data_frame
        self.trunker_availabilities: dict[str, list[str]] = {}
        """
        ### Trunker Availabilities
        Dictionary of days tied to lists of trunkers available on that day.
        """
        self.role_availabilities: dict[str, list[list[str]]] = {}
        """
        ### Role Availabilities
        Dictionary of days tied to "role" lists. These lists tabulate all 
        trunkers available for each role, in order of role appearance in sheet.
        Ex. {"Mon": [["Sophie", "Ava"], ["Ben]], "Wed": [["Sophie"], ["Sid"]]}
        Note: Could be structured more clearly; made for easy (un)packing.
        """
        self.rosters: dict[str, list[list[str]]] = {}
        """
        ### Rosters
        Dictionary of days tied to all possible combinations of trunkers 
        available on that day, in order of role appearance in sheet.
        Ex. {"Mon": [["Ben", "Sophie", "Ava"], ["Sid", "Ava", "Sophie"]]}
        Note: Could be structured more clearly; made for easy (un)packing.
        """
        # Number of roles in a show
        self.num_roles = num_roles
        # Number of show days in a week
        self.num_days = num_days
        # For each show day:
        for day in self.get_day_names():
            # Calculate role availabilities
            role_availabilities = [
                self._calculate_availabilities(role, day)
                for role in self.get_role_names()
            ]
            # Store availabilities
            self.role_availabilities[day] = role_availabilities
            # Initialize roster
            self.rosters[day] = []
            # Calculate rosters from availabilities
            self._calculate_rosters(role_availabilities, day)

    def get_role_names(self) -> list[str]:
        """
        Returns list of role names.
        """
        return list(self.data.columns)[1 : self.num_roles + 1]

    def get_day_names(self) -> list[str]:
        """
        Returns list of day names.
        """
        # Accesses the day columns past the role columns
        return list(self.data.columns)[
            self.num_roles + 1 : self.num_roles + self.num_days + 1
        ]

    def get_rosters(self, day: str) -> list[list[str]]:
        """
        Returns list of day rosters.
        """
        return self.rosters[day]

    def _calculate_availabilities(self, role: str, day: str) -> list[str]:
        """
        Returns list of trunkers available for role on day.
        """
        # Gets list of available trunkers on a day
        availabilities = self.data["Trunker"] * self.data[day]
        # Assigns to member dictionary
        self.trunker_availabilities[day] = list(filter(None, availabilities))
        # Returns list of available trunkers on a day in a role
        return list(filter(None, availabilities * self.data[role]))

    def _calculate_rosters(
        self,
        availabilities: list[list[str]],
        day: str,
        index: int = 0,
        roster: list[str] = [],
    ) -> None:
        """
        Iterates through availabilities to find all possible rosters.
        """
        # If index has reached the end of the roles list:
        if index == self.num_roles:
            # Add copy of roster to list
            self.rosters[day].append(roster.copy())
            return
        # Iterates through roles:
        for role_index, role in enumerate(availabilities):
            # For each trunker in a role:
            for trunker in role:
                # Skips any trunker already in roster
                if trunker in roster:
                    continue
                # Adds trunker to current roster
                roster.append(trunker)
                # Iterates to next role
                self._calculate_rosters(
                    availabilities[role_index + 1 :], day, index + 1, roster
                )
                # Removes from roster to try a different Trunker in same spot.
                roster.pop()


def print_shows() -> None:
    """
    Loads data sheet and prints out Trunker availability and possible rosters.
    """
    sheet_name = entry.get()
    try:
        data_frame = pd.read_excel(DATA_PATH, sheet_name)
    except FileNotFoundError:
        output(
            f"\n{DATA_PATH} not found! Make sure the excel file exists in "
            "the same directory as script!\n"
        )
        return
    except ValueError:
        output(f"\n'{sheet_name}' not found as sheet within {DATA_PATH}.\n")
        return
    # Reads excel data into dictionary
    show = Show(data_frame, NUM_ROLES, NUM_DAYS)
    # Fabricates waittime (Makes it feel like it's doin' somethin')
    output("\nCalculating show details. ", newline=False)
    for _ in range(10):
        time.sleep(0.55 + random.uniform(-0.5, 0.25))
        output(". ", newline=False)
    output("")

    # Gets names of all roles
    role_names = show.get_role_names()
    # Makes combined list of trunker names and roles
    full_strings = list(show.data["Trunker"]) + role_names
    # Finds the maximum length of string within trunker names and roles
    spacing = max(len(item) for item in full_strings) + DISPLAY_PADDING
    # Defines the full display width
    display_width = spacing * NUM_ROLES
    output_text.configure(width=display_width)
    # For each day:
    for day in show.get_day_names():
        # Prints title bar
        output("\n" + f" {day.upper()} ".center(display_width, "="))

        # Helper function for creating strings with vertical bars
        def between_lines(content: str) -> str:
            return "| " + content.ljust(display_width - 4) + " |"

        # Prints availabilities
        for role_name, role_availabilities in zip(
            role_names, show.role_availabilities[day]
        ):
            role_contents = role_name.upper().ljust(spacing)
            if role_availabilities:
                role_contents += ", ".join(role_availabilities)
            else:
                role_contents += "No Trunkers available!"
            output(between_lines(role_contents))

        output(between_lines(""))
        # Gets total number of trunkers available for day
        num_trunker_availabilities = len(show.trunker_availabilities[day])
        report = f"There are {num_trunker_availabilities} trunkers available for shows on {day}."
        # Prints report
        output(between_lines(report))
        # Prints bottom bar
        output("=" * display_width + "\n")

        # Prints role titles
        [output(role_name.center(spacing), newline=False) for role_name in role_names]
        output("\n")
        # Prints rosters
        rosters = show.get_rosters(day)
        for roster in rosters:
            [output(trunker.center(spacing), newline=False) for trunker in roster]
            output("")
        # Prints report
        output(f"\nThere are {len(rosters)} rosters available for shows on {day}.")

    output("")


if __name__ == "__main__":
    # Creates main application window
    root = tk.Tk()
    root.title("Trunkinator")

    # Defines a custom font with larger size
    nice_font = ("Consolas", 14)  # Change the font family and size as needed
    big_font = ("Consolas", 16)  # Change the font family and size as needed

    # Creates title label for the text entry
    entry_label = tk.Label(root, text="Show Name (Excel Sheet Name):", font=nice_font)
    entry_label.pack(padx=10, pady=(10, 0))

    # Creates entry widget for input
    entry = tk.Entry(root, font=nice_font)
    entry.pack(padx=10, pady=10)

    # Creates submit button
    submit_button = tk.Button(
        root, text="Generate Show", font=nice_font, command=print_shows
    )
    submit_button.pack(pady=5)

    # Creates text widget for output
    output_text = scrolledtext.ScrolledText(root, width=30, height=17, font=big_font)
    output_text.pack(padx=10, pady=10)

    # Runs the application
    root.mainloop()
