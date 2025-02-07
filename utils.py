import os
import json

NOTES_FILE = "notes.json"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def list_json_files():
    """List all available JSON files in the current directory."""
    files = [f for f in os.listdir() if f.endswith('.json')]
    return files


def choose_notes_file():
    """Allow the user to choose a JSON file for the notes."""
    files = list_json_files()
    if not files:
        print("No JSON files found in the current directory.")
        input("Press Enter to continue...")
        return None
    print("\nAvailable JSON files:")
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")
    choice = input("\nEnter the number of the file you want to load (or press Enter to cancel): ").strip()
    # Handle the case where the user presses Enter to cancel
    if not choice:
        return None
    # Handle invalid input
    if not (choice.isdigit() and 1 <= int(choice) <= len(files)):
        print("Invalid choice. Please enter a valid number to select a cheatsheet.")
        return None
    # Valid choice
    return files[int(choice) - 1]



def load_notes(file_name=None):
    """Load notes from the specified JSON file."""
    if file_name is None:  # Use default file if no file_name is provided
        file_name = NOTES_FILE
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            return json.load(file)
    else:
        return {"r_cheatsheet": {}}


def save_notes(notes, file_name=None):
    """Save notes to the specified JSON file."""
    if file_name is None:  # Use default file if no file_name is provided
        file_name = NOTES_FILE
    with open(file_name, "w") as file:
        json.dump(notes, file, indent=4)

