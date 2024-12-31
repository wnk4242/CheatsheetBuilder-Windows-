def export_notes(notes, cheatsheet_file):
    """Export all notes to a text file."""
    # Derive the export file name from the cheatsheet file name
    export_file = cheatsheet_file.replace(".json", ".txt")

    with open(export_file, "w") as file:
        def export_section(file, section, prefix=""):
            for note in section.get("notes", []):
                file.write(f"{prefix}- {note}\n")
            for folder, content in section.get("submenus", {}).items():
                file.write(f"{prefix}{folder.replace('_', ' ').title()}:\n")
                export_section(file, content, prefix + "  ")
        export_section(file, notes["r_cheatsheet"])
    print(f"Cheatsheet exported successfully to {export_file}.")
    input("Press Enter to continue...")
