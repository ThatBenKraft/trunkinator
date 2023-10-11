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

FLAG_ROSTER_CREATION = False

NUM_ROLES = 5

DATA_PATH = "trunker_data.xlsx"


def schedule_shows() -> None:
    # sheet_name = input("Please enter show name (Data sheet name): ")
    sheet_name = "Trash Mountain"
    # Reads excel data into dictionary
    data_frame = pd.read_excel(DATA_PATH, sheet_name, skiprows=1)
    trunkers: list[str] = data_frame["Trunker"].to_list()
    availability_info: dict[str, list[bool]] = data_frame.drop("Trunker", axis=1).to_dict(orient="list")  # type: ignore

    # Acquires headers from keys
    headers = list(availability_info.keys())
    day_names, role_names = headers[NUM_ROLES:], headers[:NUM_ROLES]

    for day in day_names:
        print(day)
        day_availabilities = structure_availabilities(
            availability_info,
            trunkers,
            role_names,
            day,
        )

        generate_rosters(day_availabilities, NUM_ROLES)


def structure_availabilities(
    availability_info: dict[str, list[bool]],
    trunkers: list[str],
    role_names: list[str],
    day: str,
) -> list[list[str]]:
    role_availabilities: list[list[str]] = []

    # For each role
    for role in role_names:
        # Acquires boolean availabilities
        role_statuses = availability_info[role]
        day_statuses = availability_info[day]
        if any(not isinstance(i, bool) for i in role_statuses):
            raise ValueError("Role availability must be of type Boolean!")
        if any(not isinstance(i, bool) for i in day_statuses):
            raise ValueError("Day availability must be of type Boolean!")
        # Builds list of available trunkers
        available_trunkers: list[str] = [
            trunker
            for trunker, role_status, day_status in zip(
                trunkers, role_statuses, day_statuses
            )
            if role_status and day_status
        ]

        print(f"Role: {role},   Trunkers: {available_trunkers}")
        role_availabilities.append(available_trunkers)

    return role_availabilities


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
