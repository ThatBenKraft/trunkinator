"""
# Trunkinator
Used to generate Trunk schedules.
Dependencies: pandas, openpyxl
"""

import pandas as pd

__author__ = "Ben Kraft"
__copyright__ = "None"
__credits__ = "Ben Kraft"
__license__ = "Apache"
__version__ = "1.0"
__maintainer__ = "Ben Kraft"
__email__ = "benjamin.kraft@tufts.edu"
__status__ = "Prototype"

# Defines constants
NUM_ROLES = 5
NUM_DAYS = 3
SPACING = 10
DATA_PATH = "trunker_data.xlsx"


class Show:
    # print(list(data_frame.iloc[:, 0]))
    def __init__(self, data_frame: pd.DataFrame) -> None:
        """
        Creates Show object.
        """
        self._data = data_frame

    def get_roles(self) -> list[str]:
        """
        Returns role names.
        """
        return list(self._data.columns)[1 : NUM_ROLES + 1]

    def get_days(self) -> list[str]:
        """
        Returns day names.
        """
        start_index = NUM_ROLES + 1
        return list(self._data.columns)[start_index : start_index + NUM_DAYS]

    def get_availabile_trunkers(self, role: str, day: str) -> list[str]:
        """
        Returns list of trunkers available for role on day.
        """
        # Gets combination of role and day availabilities
        availabilities = self._data[role] & self._data[day]
        # Returns with which trunkers have these availabilities
        return list(filter(None, availabilities * self._data["Trunker"]))

    def compile_availabilities(self, day: str) -> list[list[str]]:
        """
        Calculates and returns a list of trunkers available in roles on a specific
        day.
        """
        # Get list of available Trunkers for each role
        return [self.get_availabile_trunkers(role, day) for role in self.get_roles()]


def schedule_shows() -> None:
    """
    Runs main actions to schedule Trunkers into shows based on role and day
    availabilities.
    """
    # sheet_name = input("Please enter show name (Data sheet name): ")
    sheet_name = "Trash Mountain"
    # Reads excel data into dictionary
    show = Show(pd.read_excel(DATA_PATH, sheet_name, skiprows=1))
    # For each day:
    for day in show.get_days():
        role_availabilities = show.compile_availabilities(day)
        role_names = show.get_roles()
        # Prints title bar, trunker availabilities, and footer
        print("\n" + f" {day.upper()} ".center(NUM_ROLES * SPACING, "="))
        for role_name, available_trunkers in zip(role_names, role_availabilities):
            print(role_name.upper().ljust(10), ", ".join(available_trunkers))
        print("=" * NUM_ROLES * SPACING + "\n")
        # Prints role titles
        for role_name in role_names:
            print(role_name.upper().center(SPACING), end="")
        print("\n")
        # Prints all possible rosters from availabilities
        generate_rosters(role_availabilities)


def compile_availabilities(
    show: Show,
    day: str,
) -> list[list[str]]:
    """
    Calculates and returns a list of trunkers available in roles on a specific
    day.
    """
    role_availabilities: list[list[str]] = []
    # For each role
    for role in show.get_roles():
        # Builds list of available trunkers
        available_trunkers = show.get_availabile_trunkers(role, day)
        # Print out availabilities for role
        print(role.upper().ljust(10), ", ".join(available_trunkers))
        # Add to availabilities
        role_availabilities.append(available_trunkers)

    return role_availabilities


def generate_rosters(
    role_availabilities: list[list[str]],
    index: int = 0,
    roster: list[str] = [],
) -> None:
    """
    Iterates through availabilities to find all possible rosters.
    """
    # If index has reached the end of the roles list:
    if index == NUM_ROLES:
        # Print out combination
        for trunker in roster:
            print(trunker.center(SPACING), end="")
        print("")
        return
    # Iterates through roles:
    for role_index, role in enumerate(role_availabilities):
        # For each trunker in a role:
        for trunker in role:
            # Skips any trunker already in roster
            if trunker in roster:
                continue
            # Adds trunker to current roster
            roster.append(trunker)
            # Iterates to next role
            generate_rosters(role_availabilities[role_index + 1 :], index + 1, roster)
            roster.pop()


if __name__ == "__main__":
    schedule_shows()
