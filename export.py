def export_notes(notes):
    """Export all notes to a text file."""
    with open("notes.txt", "w") as file:
        def export_section(file, section, prefix=""):
            for note in section.get("notes", []):
                file.write(f"{prefix}- {note}\n")
            for folder, content in section.get("submenus", {}).items():
                file.write(f"{prefix}{folder.replace('_', ' ').title()}:\n")
                export_section(file, content, prefix + "  ")
        export_section(file, notes["r_cheatsheet"])
    print("Notes exported successfully to notes.txt.")
    input("Press Enter to continue...")
