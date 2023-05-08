import os

from domain import commands

from datetime import date, timedelta


class Option:
    def __init__(self, name, command, prep_call=None):
        self.name = name
        self.command = command
        self.prep_call = prep_call

    def choose(self):
        data = self.prep_call() if self.prep_call else None
        message = self.command.execute(data) if data else self.command.execute()
        print(message)

    def __str__(self):
        return self.name


def clear_screen():
    clear = "cls" if os.name == "nt" else "clear"
    os.system(clear)


def print_options(options):
    """
    1. Print the keyboard key for the user to enter to choose the option.
    2. Print the option text.
    3. Check if the user’s input matches an option and, if so, choose it.
    """
    for shortcut, option in options.items():
        print(f"({shortcut}) {option}")
    print()


def option_choice_is_valid(choice, options):
    return choice in options or choice.upper() in options


def get_option_choice(options):
    """
    1. Prompt the user to enter a choice, using Python’s built-in input function.
    2. If the user’s choice matches one of those listed, call that option’s choose method.
    3. Otherwise, repeat.
    """
    choice = input("Choose an option: ")
    while not option_choice_is_valid(choice, options):
        print("Invalid choice")
        choice = input("Choose an option: ")
    return options[choice.upper()]


def get_user_input(label, required=True):
    value = input(f"{label}: ") or None
    while required and not value:
        value = input(f"{label}: ") or None
    return value


def get_new_pallet_data():
    return {
        "storage_spot": get_user_input("Storage Spot"),
        "category": get_user_input("Product Category"),
        "notes": get_user_input("Notes", required=False),
    }


def get_storage_spot_for_removal():
    return get_user_input("Enter a storage spot to remove pallet")


def get_new_pallet_info():
    storage_spot = get_user_input("Enter a stow location to edit")
    field = get_user_input("Choose a value to edit (category or notes)")
    new_value = get_user_input(f"Enter the new value for {field}")
    return {
        "storage_spot": storage_spot,
        "field": field,
        "new_value": new_value,
    }


def loop():

    clear_screen()
    # All steps for showing and selecting options
    # https://www.w3schools.com/python/python_dictionaries.asp
    options = {
        "A": Option(
            "Add a Pallet",
            commands.AddPalletCommand(),
            prep_call=get_new_pallet_data,
        ),
        "X": Option("List expired pallets", commands.ListExpiredPalletsCommand(criteria={'date_added': f'<={date.today()-timedelta(days=30)}'})),
    
        "L": Option(
            "List pallets numerically", commands.ListPalletsCommand(order_by="storage_spot")
        ),
        "E": Option(
            "Edit a pallet",
            commands.EditLocationCommand(),
            prep_call=get_new_pallet_info,
        ),
        "R": Option(
            "Remove a pallet",
            commands.RemovePalletCommand(),
            prep_call=get_storage_spot_for_removal,
        ),
        "Q": Option("Quit", commands.QuitCommand()),
    }
    print_options(options)

    chosen_option = get_option_choice(options)
    clear_screen()
    chosen_option.choose()
    _ = input("Press ENTER to return to menu")


# this ensures that this module runs first
if __name__ == "__main__":
    commands.CreateStorageSpotsTableCommand().execute()

    # endless program loop
    while True:
        loop()