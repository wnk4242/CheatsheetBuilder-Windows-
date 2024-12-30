
# Not going to use the following functions

def move_folders(folders, notes, parent_section=None):
    """Move one or more folders into another folder or up to the parent folder."""
    if not folders:
        print("No folders available to move.")
        input("Press Enter to continue...")
        return

    # List available folders
    folder_keys = list(folders.keys())
    print("Available Folders:")
    for i, folder in enumerate(folder_keys, 1):
        print(f"{i}. {folder.replace('_', ' ').title()}")

    # Prompt user for folders to move
    selected = input("Enter folder numbers to move (comma-separated, 'all' to select all, or press Enter to cancel): ").strip()
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

        # Get the folders to move
        selected_folders = {folder_keys[idx]: folders[folder_keys[idx]] for idx in selected_indices}

        # Display target folder options
        print("Available Target Folders:")
        available_target = False
        for i, folder in enumerate(folder_keys, 1):
            if i - 1 not in selected_indices:
                print(f"{i}. {folder.replace('_', ' ').title()}")
                available_target = True

        if parent_section:
            print("0. Move to Parent Folder")
            available_target = True

        if not available_target:
            print("No valid target folders available. Returning to menu.")
            input("Press Enter to continue...")
            return

        # Prompt user for the target folder
        target_choice = input("Enter target folder number (or press Enter to cancel): ").strip()
        if target_choice == "0" and parent_section:
            # Move to parent folder
            for folder_key in selected_folders:
                parent_section.setdefault("submenus", {})[folder_key] = folders.pop(folder_key)
            save_notes(notes)
            print("Selected folders moved to the parent folder successfully.")
        elif target_choice.isdigit():
            target_index = int(target_choice) - 1
            if target_index in selected_indices or target_index < 0 or target_index >= len(folder_keys):
                print("Invalid target folder. Returning to menu.")
            else:
                # Move to another folder
                target_folder_key = folder_keys[target_index]
                target_folder = folders[target_folder_key]
                for folder_key in selected_folders:
                    target_folder.setdefault("submenus", {})[folder_key] = folders.pop(folder_key)
                save_notes(notes)
                print(f"Selected folders moved successfully to '{target_folder_key.replace('_', ' ').title()}'.")
        else:
            print("No valid target folder selected. Returning to menu.")
    except ValueError:
        print("Invalid input. No folders moved.")
    input("Press Enter to continue...")




def move_notes_to_parent(section, parent_section, notes):
    """Move notes from the current folder to its parent folder."""
    notes_list = section.get("notes", [])
    if not notes_list:
        print("No notes available to move to the parent folder.")
        input("Press Enter to continue...")
        return

    # Display available notes
    print("Available Notes:")
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

def move_folders_to_parent(current_folders, parent_folders, notes):
    """
    Move one or more folders from the current folder to its parent folder.
    """
    if not current_folders:
        print("No folders available to move.")
        input("Press Enter to continue...")
        return

    # List available folders
    folder_keys = list(current_folders.keys())
    print("Available Folders:")
    for i, folder in enumerate(folder_keys, 1):
        print(f"{i}. {folder.replace('_', ' ').title()}")

    # Prompt user for folder numbers to move
    selected = input("Enter the folder numbers to move to the parent folder (comma-separated, or press Enter to cancel): ").strip()

    if not selected:
        print("No folders selected. Returning to menu.")
        input("Press Enter to continue...")
        return

    try:
        selected_indices = [int(x.strip()) - 1 for x in selected.split(",") if x.strip().isdigit()]

        # Validate selected indices
        if not all(0 <= idx < len(folder_keys) for idx in selected_indices):
            print("Invalid folder number(s). Returning to menu.")
            input("Press Enter to continue...")
            return

        # Ask for confirmation
        confirm = input("Are you sure you want to move the selected folders to the parent folder? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Move operation canceled.")
            input("Press Enter to continue...")
            return

        # Perform the move operation
        for idx in sorted(set(selected_indices), reverse=True):
            folder_key = folder_keys[idx]
            parent_folders.setdefault("submenus", {})[folder_key] = current_folders.pop(folder_key)

        save_notes(notes)
        print("Selected folders moved to the parent folder successfully.")
    except ValueError:
        print("Invalid input. No folders moved.")
    input("Press Enter to continue...")





