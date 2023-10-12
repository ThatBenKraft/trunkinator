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
        self._availabilities: dict[str, list[list[str]]] = {}
        self._rosters: dict[str, list[list[str]]] = {}
        # For each day
        for day in self.get_day_names():
            # Calculate availabilities
            availabilities = [
                self._calculate_availability(role, day)
                for role in self.get_role_names()
            ]
            # Store availabilities
            self._availabilities[day] = availabilities
            # Initialize roster
            self._rosters[day] = []
            # Calculate rosters from availabilities
            self._calculate_rosters(availabilities, day)

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

    def get_availabilities(self, day: str) -> list[list[str]]:
        """
        Returns day availabilities.
        """
        return self._availabilities[day]

    def get_rosters(self, day: str) -> list[list[str]]:
        """
        Returns day rosters.
        """
        return self._rosters[day]

    def _calculate_availability(self, role: str, day: str) -> list[str]:
        """
        Returns list of trunkers available for role on day.
        """
        # Gets combination of role and day availabilities
        availabilities = self._data[role] & self._data[day]
        # Returns with which trunkers have these availabilities
        return list(filter(None, availabilities * self._data["Trunker"]))

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
        for role_name, available_trunkers in zip(
            role_names, show.get_availabilities(day)
        ):
            print(role_name.ljust(10) + ", ".join(available_trunkers))
        # Prints bottom bar
        print("=" * NUM_ROLES * SPACING + "\n")

        # Prints role titles
        [print(role_name.center(SPACING), end="") for role_name in role_names]
        print("\n")

        # Prints rosters
        for roster in show.get_rosters(day):
            [print(trunker.center(SPACING), end="") for trunker in roster]
            print("")

    print("")


if __name__ == "__main__":
    print_shows()
