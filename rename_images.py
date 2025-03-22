#!/usr/bin/env python3
import os
import string

def rename_images():
    """
    Renames all JPG images in the current directory to alphabetical names (A.jpg, B.jpg, etc.)
    """
    # Get the directory of the script
    directory = os.path.dirname(os.path.abspath(__file__))
    
    # Get all jpg files in the directory
    jpg_files = [f for f in os.listdir(directory) if f.lower().endswith('.jpg')]
    
    # Sort the files to ensure consistent renaming
    jpg_files.sort()
    
    # Check if we have the right number of files
    if len(jpg_files) > 26:
        print(f"Warning: Found {len(jpg_files)} JPG files, but only 26 letters available.")
        print("Only the first 26 files will be renamed.")
        jpg_files = jpg_files[:26]
    elif len(jpg_files) < 26:
        print(f"Warning: Found only {len(jpg_files)} JPG files, but 26 letters available.")
        print("Will use only the first {len(jpg_files)} letters.")
    
    # Get uppercase letters
    letters = list(string.ascii_uppercase)
    
    # Rename files
    for i, file in enumerate(jpg_files):
        if i >= 26:
            break
            
        old_path = os.path.join(directory, file)
        new_name = f"{letters[i]}.jpg"
        new_path = os.path.join(directory, new_name)
        
        # Check if destination file already exists
        if os.path.exists(new_path) and old_path != new_path:
            print(f"Skipping {file}: {new_name} already exists")
            continue
            
        try:
            os.rename(old_path, new_path)
            print(f"Renamed {file} to {new_name}")
        except Exception as e:
            print(f"Error renaming {file}: {e}")

if __name__ == "__main__":
    rename_images()
