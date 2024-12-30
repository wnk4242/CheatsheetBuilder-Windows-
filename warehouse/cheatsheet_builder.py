# This is not modularized script. The functions are not up to date.
import os
import json


NOTES_FILE = "notes.json"

# Load notes from the file
def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as file:
            return json.load(file)
    else:
        return {"r_cheatsheet": {}}

# Save notes to the file
def save_notes(notes):
    with open(NOTES_FILE, "w") as file:
        json.dump(notes, file, indent=4)

# Initialize notes
notes = load_notes()

def main_menu():
    """Display the main menu and handle user input."""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n--- Cheatsheet Building System ---")

        print("1. Cheatsheet Builder")
        print("2. Search Notes")
        print("3. Export Notes")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            cheatsheet_menu("Cheatsheet Builder", notes["r_cheatsheet"])
        elif choice == "2":
            search_notes()
        elif choice == "3":
            export_notes()
        elif choice == "4":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

def cheatsheet_menu(title, section, parent_section=None):
    """Display a menu for a specific section with pagination and toggleable options."""
    page = 0  # Start on the first page
    notes_per_page = 10  # Set the number of notes per page
    alphabetical_order = False  # Default to original order
    truncated_display = True  # Default to truncated note display

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n--- {title.replace('_', ' ').title()} ---")

        # Fallback for terminal width
        try:
            window_width = os.get_terminal_size().columns
        except OSError:
            window_width = 80  # Default width if terminal size cannot be fetched

        # Column width
        left_column_width = 35
        right_column_width = max(10, window_width - left_column_width - 40)

        # Prepare notes for display with pagination
        notes_list = section.get("notes", [])
        if alphabetical_order:
            notes_list = sorted(notes_list)

        total_pages = max(1, (len(notes_list) + notes_per_page - 1) // notes_per_page)
        start_idx = page * notes_per_page
        end_idx = start_idx + notes_per_page
        current_notes = notes_list[start_idx:end_idx]

        # Handle truncated note display
        if truncated_display:
            current_notes = [
                (note[:right_column_width - 3] + "...") if len(note) > right_column_width - 3 else note
                for note in current_notes
            ]

        # Prepare folders for display
        folders = section.get("submenus", {})
        folder_keys = list(folders.keys())

        # Display folders and notes separately
        notes_display = ["Notes (Page {}/{}):".format(page + 1, total_pages)] if current_notes else []
        notes_display += [f"- {note}" for note in current_notes]

        folders_display = ["Folders:"] if folders else []
        folders_display += [
            f"{i + 1}. {folder.replace('_', ' ').title()}" for i, folder in enumerate(folder_keys)
        ]

        # Combine notes and folders for the right column
        right_side_display = notes_display + folders_display

        # Prepare options for display in the left column
        options = [
            "Options:",
            "a. Add Note",
            "s. Edit Note",
            "d. Delete Notes",
            "f. Add Folder",
            "g. Edit Folder",
            "h. Delete Folders",
            "j. Move Notes to Folder",
            "k. Move Folders to Another Folder",
            "l. Move Notes to Parent Folder",
            "v. Arrange Folder Order",
            "n. Toggle Note Order ({})".format("Alphabetical" if alphabetical_order else "Original"),
            "w. Toggle Note Display ({})".format("Truncated" if truncated_display else "Full"),
            "e. Go Back",
        ]

        # Add pagination options
        if page > 0:
            options.append("; Previous Page")
        if page < total_pages - 1:
            options.append("' Next Page")

        # Adjust spacing between columns
        max_lines = max(len(options), len(right_side_display))
        for i in range(max_lines):
            left = options[i] if i < len(options) else ""
            right = right_side_display[i] if i < len(right_side_display) else ""
            print(f"{left:<{left_column_width}} | {right:<{right_column_width}}")

        choice = input("\nEnter your choice: ").strip()

        if choice.lower() == 'a':
            add_note(section)
            total_pages = max(1, (len(notes_list) + notes_per_page - 1) // notes_per_page)
            page = total_pages - 1
        elif choice.lower() == 's':
            edit_note(section)
        elif choice.lower() == 'd':
            delete_notes(section)
        elif choice.lower() == 'f':
            add_folder(section.setdefault("submenus", {}))
        elif choice.lower() == 'g':
            edit_folder(section.get("submenus", {}))
        elif choice.lower() == 'h':
            delete_folders(section.get("submenus", {}))
        elif choice.lower() == 'j':
            move_notes_to_folder(section, section.get("submenus", {}))
        elif choice.lower() == 'k':
            move_folders_to_folder(section.get("submenus", {}))
        elif choice.lower() == 'l':
            if parent_section:
                move_notes_to_parent(section, parent_section)
            else:
                print("No parent folder available.")
                input("Press Enter to continue...")
        elif choice.lower() == 'v':
            arrange_folders_order(section.get("submenus", {}))
        elif choice.lower() == 'n':
            alphabetical_order = not alphabetical_order
            print(f"Order toggled to {'Alphabetical' if alphabetical_order else 'Original'}.")
            input("Press Enter to continue...")
        elif choice.lower() == 'w':
            truncated_display = not truncated_display
            print(f"Note display toggled to {'Truncated' if truncated_display else 'Full'}.")
            input("Press Enter to continue...")
        elif choice.lower() == 'e':
            return  # Exit the menu immediately
        elif choice == ";" and page > 0:
            page -= 1  # Go to the previous page
        elif choice == "'" and page < total_pages - 1:
            page += 1  # Go to the next page
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(folder_keys):  # Only folders are navigable
                folder_key = folder_keys[idx]
                cheatsheet_menu(folder_key.replace('_', ' ').title(), folders[folder_key], parent_section=section)
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")





def arrange_folders_order(folders):
    """Arrange the order of folders."""
    if not folders:
        print("No folders available to arrange.")
        input("Press Enter to continue...")
        return

    # List current folder order
    folder_keys = list(folders.keys())
    print("\nCurrent Folder Order:")
    for i, folder in enumerate(folder_keys, 1):
        print(f"{i}. {folder.replace('_', ' ').title()}")

    # Prompt user for new order
    print("\nEnter the new order of folder numbers, separated by commas (e.g., '3,1,2'), or press Enter to cancel:")
    new_order_input = input("New Order: ").strip()

    if not new_order_input:
        print("No changes made. Returning to menu.")
        input("Press Enter to continue...")
        return

    try:
        # Parse the new order
        new_order_indices = [int(x.strip()) - 1 for x in new_order_input.split(",") if x.strip().isdigit()]

        # Validate the new order
        if sorted(new_order_indices) != list(range(len(folder_keys))):
            raise ValueError("Invalid order. Please ensure all folder numbers are included exactly once.")

        # Reorder folders
        reordered_folders = {folder_keys[idx]: folders[folder_keys[idx]] for idx in new_order_indices}

        # Update the folder structure
        folders.clear()
        folders.update(reordered_folders)

        save_notes(notes)
        print("Folders reordered successfully.")
    except ValueError as e:
        print(f"Error: {e}. No changes made.")
    input("Press Enter to continue...")


def move_folders_to_folder(folders):
    """Move one or more folders into another folder."""
    if not folders:
        print("No folders available to move.")
        input("Press Enter to continue...")
        return

    # List available folders
    folder_keys = list(folders.keys())
    print("\nAvailable Folders:")
    for i, folder in enumerate(folder_keys, 1):
        print(f"{i}. {folder.replace('_', ' ').title()}")

    # Prompt user for folder numbers to move
    selected = input("Enter the folder numbers to move (comma-separated, or type 'all' to select all, or press Enter to cancel): ").strip()
    if not selected:
        print("No folders selected. Returning to menu.")
        input("Press Enter to continue...")
        return

    try:
        if selected.lower() == "all":
            selected_indices = list(range(len(folder_keys)))
        else:
            selected_indices = [int(x.strip()) - 1 for x in selected.split(",") if x.strip().isdigit()]

        # Validate selected indices
        selected_indices = sorted(set(selected_indices))
        if not all(0 <= idx < len(folder_keys) for idx in selected_indices):
            print("Invalid folder number(s). Returning to menu.")
            input("Press Enter to continue...")
            return

        # Display target folders
        print("\nAvailable Target Folders:")
        for i, folder in enumerate(folder_keys, 1):
            if i - 1 not in selected_indices:  # Exclude already selected folders
                print(f"{i}. {folder.replace('_', ' ').title()}")

        # Prompt user for target folder
        target_choice = input("Enter the target folder number to move the selected folders into (or press Enter to cancel): ").strip()
        if not target_choice.isdigit():
            print("No target folder selected. Returning to menu.")
            input("Press Enter to continue...")
            return

        target_index = int(target_choice) - 1
        if target_index not in range(len(folder_keys)) or target_index in selected_indices:
            print("Invalid target folder number. Returning to menu.")
            input("Press Enter to continue...")
            return

        # Perform the move operation
        target_folder_key = folder_keys[target_index]
        target_folder = folders[target_folder_key]

        for idx in selected_indices:
            folder_key = folder_keys[idx]
            target_folder.setdefault("submenus", {})[folder_key] = folders.pop(folder_key)

        save_notes(notes)
        print("Selected folders moved successfully.")
    except ValueError:
        print("Invalid input. No folders moved.")
    input("Press Enter to continue...")


def rearrange_folders(folders):
    """Allow the user to rearrange the order of folders."""
    folder_keys = list(folders.keys())
    print("\nAvailable Folders:")
    for i, folder in enumerate(folder_keys, 1):
        print(f"{i}. {folder.replace('_', ' ').title()}")

    new_order = input(
        "\nEnter the new order of folder numbers (comma-separated, e.g., 3,1,2): ").strip()
    try:
        indices = [int(x.strip()) - 1 for x in new_order.split(",") if x.strip().isdigit()]
        if len(indices) != len(folder_keys) or sorted(indices) != list(range(len(folder_keys))):
            raise ValueError("Invalid input. The numbers must match the current folder indices.")
        folder_keys = [folder_keys[i] for i in indices]
        reordered_folders = {key: folders[key] for key in folder_keys}
        folders.clear()
        folders.update(reordered_folders)
        save_notes(notes)
        print("Folders rearranged successfully.")
    except ValueError as e:
        print(f"Error: {e}")
    input("Press Enter to continue...")



def move_notes_to_parent(section, parent_section):
    """Move notes from the current folder to its parent folder."""
    notes_list = section.get("notes", [])
    if not notes_list:
        print("No notes available to move to the parent folder.")
        input("Press Enter to continue...")
        return

    # Display available notes
    print("\nAvailable Notes:")
    for i, note in enumerate(notes_list, 1):
        print(f"{i}. {note}")

    # Prompt user for note numbers to move
    selected = input("Enter the note numbers to move (comma-separated, or 'all' to move all notes, or press Enter to cancel): ").strip()
    if not selected:
        print("No notes selected. Returning to menu.")
        input("Press Enter to continue...")
        return

    if selected.lower() == 'all':
        parent_section.setdefault("notes", []).extend(notes_list)
        section["notes"] = []
        print("All notes moved to the parent folder successfully.")
    else:
        try:
            indices = [int(x.strip()) - 1 for x in selected.split(",") if x.strip().isdigit()]
            indices = sorted(set(indices), reverse=True)  # Remove duplicates and sort descending
            selected_notes = [notes_list[idx] for idx in indices if 0 <= idx < len(notes_list)]

            if not selected_notes:
                print("No valid notes selected. Returning to menu.")
                input("Press Enter to continue...")
                return

            parent_section.setdefault("notes", []).extend(selected_notes)
            for idx in indices:
                if 0 <= idx < len(notes_list):
                    notes_list.pop(idx)

            print("Selected notes moved to the parent folder successfully.")
        except ValueError:
            print("Invalid input. No notes moved.")
    save_notes(notes)
    input("Press Enter to continue...")





def add_note(section):
    """Add a new note to the section."""
    note = input("Enter the new note (or press Enter to cancel): ").strip()
    if not note:
        print("No note added. Returning to the menu.")
        input("Press Enter to continue...")
        return
    section.setdefault("notes", []).append(note)
    save_notes(notes)
    print("Note added successfully.")
    input("Press Enter to continue...")



def edit_note(section):
    """Edit an existing note in the section."""
    notes_list = section.get("notes", [])
    if not notes_list:
        print("No notes to edit.")
        input("Press Enter to return to the menu...")
        return

    print("\nAvailable Notes:")
    for i, note in enumerate(notes_list, 1):
        print(f"{i}. {note}")

    choice = input("Enter the note number to edit (or press Enter to cancel): ").strip()

    if not choice:  # If the user presses Enter without input
        print("No edits made. Returning to the menu.")
        input("Press Enter to continue...")
        return

    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(notes_list):
            print(f"Current note: {notes_list[idx]}")
            new_note = input("Enter the new note (or press Enter to cancel): ").strip()
            if not new_note:
                print("No changes made. Returning to the menu.")
                input("Press Enter to continue...")
                return
            notes_list[idx] = new_note
            save_notes(notes)
            print("Note updated successfully!")
        else:
            print("Invalid note number. Returning to the menu.")
    else:
        print("Invalid input. Returning to the menu.")

    input("Press Enter to continue...")


def delete_notes(section):
    """Delete multiple notes from the section."""
    notes_list = section.get("notes", [])
    if not notes_list:
        print("No notes to delete.")
        input("Press Enter to continue...")
        return

    # Display available notes
    print("\nAvailable Notes:")
    for i, note in enumerate(notes_list, 1):
        print(f"{i}. {note}")

    # Prompt user for note numbers to delete
    selected = input("Enter the note numbers to delete (comma-separated, or press Enter to cancel): ").strip()
    if not selected:
        print("No notes selected. Returning to menu.")
        input("Press Enter to continue...")
        return

    try:
        indices = [int(x.strip()) - 1 for x in selected.split(",") if x.strip().isdigit()]
        indices = sorted(set(indices), reverse=True)  # Remove duplicates and sort descending
        for idx in indices:
            if 0 <= idx < len(notes_list):
                notes_list.pop(idx)
        save_notes(notes)
        print("Selected notes deleted successfully.")
    except ValueError:
        print("Invalid input. No notes deleted.")
    input("Press Enter to continue...")

def add_folder(folders):
    """Add a new folder."""
    folder_name = input("Enter the name of the new folder (or press Enter to cancel): ").strip().replace(' ', '_').lower()
    if not folder_name:
        print("No folder added. Returning to the menu.")
        input("Press Enter to continue...")
        return
    if folder_name in folders:
        print("Folder already exists. Returning to the menu.")
    else:
        folders[folder_name] = {"notes": [], "submenus": {}}
        save_notes(notes)
        print(f"Folder '{folder_name.replace('_', ' ').title()}' added successfully!")
    input("Press Enter to continue...")

def edit_folder(folders):
    """Edit the name of an existing folder."""
    if not folders:
        print("No folders to edit. Returning to the menu.")
        input("Press Enter to continue...")
        return

    # Display the list of folders
    folder_keys = list(folders.keys())
    print("\nAvailable Folders:")
    for i, folder in enumerate(folder_keys, 1):
        print(f"{i}. {folder.replace('_', ' ').title()}")

    # Prompt user to select a folder to edit
    choice = input("Enter the folder number to edit (or press Enter to cancel): ").strip()

    if not choice:
        print("No folder selected. Returning to the menu.")
        input("Press Enter to continue...")
        return

    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(folder_keys):
            current_name = folder_keys[idx]
            print(f"Current folder name: {current_name.replace('_', ' ').title()}")
            new_name = input("Enter the new name (or press Enter to cancel): ").strip().replace(' ', '_').lower()
            if not new_name:
                print("No changes made. Returning to the menu.")
            elif new_name in folders and new_name != current_name:
                print("A folder with this name already exists. No changes made.")
            else:
                folders[new_name] = folders.pop(current_name)
                save_notes(notes)
                print("Folder name updated successfully!")
        else:
            print("Invalid folder number. Returning to the menu.")
    else:
        print("Invalid input. Returning to the menu.")
    input("Press Enter to continue...")


def delete_folders(folders):
    """Delete multiple folders from the current section."""
    if not folders:
        print("No folders to delete. Returning to the menu.")
        input("Press Enter to continue...")
        return

    # List available folders
    folder_keys = list(folders.keys())
    print("\nAvailable Folders:")
    for i, folder in enumerate(folder_keys, 1):
        print(f"{i}. {folder.replace('_', ' ').title()}")

    # Prompt user for folder numbers to delete
    selected = input("Enter the folder numbers to delete (comma-separated, or press Enter to cancel): ").strip()

    if not selected:
        print("No folders selected. Returning to the menu.")
        input("Press Enter to continue...")
        return

    try:
        indices = [int(x.strip()) - 1 for x in selected.split(",") if x.strip().isdigit()]
        indices = sorted(set(indices), reverse=True)  # Remove duplicates and sort descending

        for idx in indices:
            if 0 <= idx < len(folder_keys):
                folder_key = folder_keys[idx]
                confirm = input(f"Are you sure you want to delete '{folder_key.replace('_', ' ').title()}'? (y/n): ").lower()
                if confirm == 'y':
                    del folders[folder_key]
                    print(f"Folder '{folder_key.replace('_', ' ').title()}' deleted.")
                else:
                    print(f"Deletion of folder '{folder_key.replace('_', ' ').title()}' canceled.")
            else:
                print(f"Invalid folder number: {idx + 1}. Skipping.")

        save_notes(notes)
        print("Folder deletion process completed.")
    except ValueError:
        print("Invalid input. No folders deleted.")
    input("Press Enter to continue...")




def move_notes_to_folder(section, folders):
    """Move multiple notes from the current section into a specified folder."""
    notes_list = section.get("notes", [])
    if not notes_list:
        print("No notes available to move.")
        input("Press Enter to continue...")
        return

    # Display available notes
    print("\nAvailable Notes:")
    for i, note in enumerate(notes_list, 1):
        print(f"{i}. {note}")

    # Prompt user for note numbers to move
    selected = input(
        "Enter the note numbers to move (comma-separated, or type 'all' to move all notes, or press Enter to cancel): "
    ).strip()

    if not selected:
        print("No notes selected. Returning to menu.")
        input("Press Enter to continue...")
        return

    if selected.lower() == "all":
        indices = list(range(len(notes_list)))  # Select all notes
    else:
        try:
            indices = [int(x.strip()) - 1 for x in selected.split(",") if x.strip().isdigit()]
            indices = sorted(set(indices), reverse=True)  # Remove duplicates and sort descending
        except ValueError:
            print("Invalid input. No notes moved.")
            input("Press Enter to continue...")
            return

    selected_notes = [notes_list[idx] for idx in indices if 0 <= idx < len(notes_list)]

    # Display available folders
    if not folders:
        print("No folders available to move the notes into.")
        input("Press Enter to continue...")
        return

    print("\nAvailable Folders:")
    folder_keys = list(folders.keys())
    for i, folder in enumerate(folder_keys, 1):
        print(f"{i}. {folder.replace('_', ' ').title()}")

    # Prompt user for target folder
    folder_choice = input("Enter the folder number to move the notes into (or press Enter to cancel): ").strip()
    if not folder_choice.isdigit():
        print("No folder selected. Returning to menu.")
        input("Press Enter to continue...")
        return

    folder_index = int(folder_choice) - 1
    if not (0 <= folder_index < len(folder_keys)):
        print("Invalid folder number. Returning to menu.")
        input("Press Enter to continue...")
        return

    # Move notes to the selected folder
    target_folder_key = folder_keys[folder_index]
    target_folder = folders[target_folder_key]
    target_folder.setdefault("notes", []).extend(selected_notes)
    for idx in sorted(indices, reverse=True):
        if 0 <= idx < len(notes_list):
            notes_list.pop(idx)

    save_notes(notes)
    print(f"Selected notes moved successfully to '{target_folder_key.replace('_', ' ').title()}'.")
    input("Press Enter to continue...")


def search_notes():
    """Search for a keyword in all notes."""
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
    keyword = input("Enter a keyword to search: ").lower()

    def search_section(section, path=""):
        """Recursively search notes and folders for the keyword."""
        found = False
        for note in section.get("notes", []):
            if keyword in note.lower():
                print(f"Note: {note} (Path: {path})")
                found = True
        for folder, content in section.get("submenus", {}).items():
            if search_section(content, path + folder.replace('_', ' ').title() + " > "):
                found = True
        return found

    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen again for better presentation
    print(f"Search Results for '{keyword}':")

    if not search_section(notes["r_cheatsheet"]):
        print("No matches found.")

    input("\nPress Enter to return to the menu...")


def export_notes():
    """Export all notes to a text file."""
    with open("r_notes.txt", "w") as file:
        def export_section(file, section, prefix=""):
            for note in section.get("notes", []):
                file.write(f"{prefix}- {note}\n")
            for folder, content in section.get("submenus", {}).items():
                file.write(f"{prefix}{folder.replace('_', ' ').title()}:\n")
                export_section(file, content, prefix + "  ")
        export_section(file, notes["r_cheatsheet"])
    print("Notes exported successfully to r_notes.txt.")

def export_structure():
    """Export the structure of folders to a text file."""
    def traverse_structure(section, depth=0):
        """Recursive helper function to traverse the folder structure."""
        lines = []
        submenus = section.get("submenus", {})
        for folder_name, folder_content in submenus.items():
            lines.append(f"{'  ' * depth}- {folder_name.replace('_', ' ').title()}")
            lines.extend(traverse_structure(folder_content, depth + 1))
        return lines

    # Start traversing from the top-level R Cheatsheet
    structure_lines = traverse_structure(notes["r_cheatsheet"])
    with open("folder_structure.txt", "w") as file:
        file.write("\n".join(structure_lines))
    print("Folder structure exported to 'folder_structure.txt'.")

if __name__ == "__main__":
    main_menu()
