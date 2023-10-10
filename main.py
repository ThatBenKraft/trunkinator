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

ROLES = [["Ben", "Charlie"], ["Charlie"]]

FLAG_ROSTER_CREATION = False

DATA_PATH = "trunker_data.xlsx"


def schedule_shows() -> None:
    # sheet_name = input("Please enter show name (Data sheet name): ")
    sheet_name = "Trash Mountain"

    data_frame = pd.read_excel(DATA_PATH, sheet_name)
    print(data_frame)

    generate_rosters(ROLES, len(ROLES))


def generate_rosters(
    roles: list[list[str]], full_length: int, index=0, roster: list[str] = []
) -> None:
    if FLAG_ROSTER_CREATION:
        print(f"Current roster: {roster}")
    # If index has reached the end of the roles list:
    if index == full_length:
        # Print out combination
        print(", ".join(roster))
        return
    # Iterates through roles:
    for role_index, role in enumerate(roles):
        # For each trunker in a role:
        for trunker in role:
            # Skips any trunker already in roster
            if trunker in roster:
                continue
            # Adds trunker to current roster
            roster.append(trunker)
            # Iterates to next role
            generate_rosters(roles[role_index + 1 :], full_length, index + 1, roster)
            roster.pop()


if __name__ == "__main__":
    schedule_shows()
