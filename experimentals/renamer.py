import os

def rename_xml(directory):
    """
    Renames XML files in the given directory to have a shorter name.
    """
    for filename in os.listdir(directory):
        if filename.endswith(".xml"):
            # Extract the number from the filename
            num = filename[8:12]
            # Construct the new filename
            new_filename = f"P{num}.xml"
            # Construct the full paths for the old and new filenames
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)
            # Rename the file
            os.rename(old_path, new_path)

# Example usage
directory = os.getcwd()
rename_xml(directory)
