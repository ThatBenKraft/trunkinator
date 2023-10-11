aders = list(availability_info.keys())
    # # Separates headers into roles and days
    # role_names, day_names = headers[:NUM_ROLES], headers[NUM_ROLES:]

    # # For each day:
    # for day in day_names:
    #     # Prints title bar
    #     print("")
    #     print(f" {day.upper()} ".center(NUM_ROLES * SPACING, "="))
    #     # Prints day availabilities
    #     day_availabilities = compile_availabilities(
    #         availability_info,
    #         trunkers,
    #         role_names,
    #         day,
    #     )
    #     # Prints closer and role titles
    #     print("=" * NUM_ROLES * SPACING, "\n")
    #     for role_name in role_names:
    #         print(role_name.upper().center(SPACING), end="")
    #     print("\n")
    #     # Prints all possible rosters from availabilities
    #     generate_r