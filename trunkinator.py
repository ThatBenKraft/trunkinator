"""
# Trunkinator
Used to generate Trunk schedules.
Dependencies: pandas, openpyxl
"""

import pandas as pd

__author__ = "Ben Kraft"
__copyright__ = "None"
__credits__ = "Ben Kraft"
__license__ = "Apache 2.0"
__version__ = "1.0"
__maintainer__ = "Ben Kraft"
__email__ = "benjamin.kraft@tufts.edu"
__status__ = "Prototype"

# Defines constants
NUM_ROLES = 5
NUM_DAYS = 3
SPACING = 12
DATA_PATH = "trunker_data.xlsx"


class Show:
    """
    Used for show information calculation and storage.
    """

    def __init__(self, data_frame: pd.DataFrame) -> None:
        """
        Creates Show object. Takes Pandas dataframe as input
        """
        self._data = data_frame
        # Create role and roster storages
        self._role_availabilities: dict[str, list[list[str]]] = {}
        self._trunker_availabilities: dict[str, list[str]] = {}
        self._rosters: dict[str, list[list[str]]] = {}
        # For each day
        for day in self.get_day_names():
            # Calculate availabilities
            role_availabilities = [
                self._calculate_availabilities(role, day)
                for role in self.get_role_names()
            ]
            # Store availabilities
            self._role_availabilities[day] = role_availabilities
            # Initialize roster
            self._rosters[day] = []
            # Calculate rosters from availabilities
            self._calculate_rosters(role_availabilities, day)

    def get_role_names(self) -> list[str]:
        """
        Returns role names.
        """
        return list(self._data.columns)[1 : NUM_ROLES + 1]

    def get_day_names(self) -> list[str]:
        """
        Returns day names.
        """
        start_index = NUM_ROLES + 1
        return list(self._data.columns)[start_index : start_index + NUM_DAYS]

    def get_trunker_availabilities(self, day: str) -> list[str]:
        """
        Returns day trunker availabilities.
        """
        return self._trunker_availabilities[day]

    def get_role_availabilities(self, day: str) -> list[list[str]]:
        """
        Returns day role availabilities.
        """
        return self._role_availabilities[day]

    def get_rosters(self, day: str) -> list[list[str]]:
        """
        Returns day rosters.
        """
        return self._rosters[day]

    def _calculate_availabilities(self, role: str, day: str) -> list[str]:
        """
        Returns list of trunkers available for role on day.
        """
        # Gets list of available trunkers on a day
        availabilities = self._data["Trunker"] * self._data[day]
        # Assigns to member dictionary
        self._trunker_availabilities[day] = list(filter(None, availabilities))
        # Returns list of available trunkers on a day in a role
        return list(filter(None, availabilities * self._data[role]))

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
        if index == NUM_ROLES:
            # Add copy of roster to list
            self._rosters[day].append(roster.copy())
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
    sheet_name = input("Please enter show name (data sheet name): ")
    # sheet_name = "Trash Mountain"
    # Reads excel data into dictionary
    show = Show(pd.read_excel(DATA_PATH, sheet_name, skiprows=1))
    # For each day:
    for day in show.get_day_names():
        # Prints title bar
        print("\n" + f" {day.upper()} ".center(NUM_ROLES * SPACING, "="))
        # Acquires and capitalizes role names
        role_names = [name.upper() for name in show.get_role_names()]

        # Prints availabilities
        def between_lines(contents: str) -> str:
            return "| " + contents.ljust(SPACING * NUM_ROLES - 4) + " |"

        for role_name, role_availabilities in zip(
            role_names, show.get_role_availabilities(day)
        ):
            role_contents = role_name.ljust(SPACING)
            if role_availabilities:
                role_contents += ", ".join(role_availabilities)
            else:
                role_contents += "No Trunkers available!"
            print(between_lines(role_contents))

        print(between_lines(""))
        # Gets total number of trunkers available for day
        num_trunker_availabilities = len(show.get_trunker_availabilities(day))
        report = f"There are {num_trunker_availabilities} trunkers available for shows on {day}."
        # Prints report
        print(between_lines(report))
        # Prints bottom bar
        print("=" * NUM_ROLES * SPACING + "\n")

        # Prints role titles
        [print(role_name.center(SPACING), end="") for role_name in role_names]
        print("\n")
        # Prints rosters
        rosters = show.get_rosters(day)
        for roster in rosters:
            [print(trunker.center(SPACING), end="") for trunker in roster]
            print("")
        # Prints report
        print(f"\nThere are {len(rosters)} rosters available for shows on {day}.")

    print("")


if __name__ == "__main__":
    print_shows()
