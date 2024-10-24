#!/usr/bin/env python3
import os
import json
import time

# Initialize a repo
def initialize_repo(repo_name):
    # Check if repo already exists
    if not os.path.exists(repo_name):
        try:
            # Create the repository directory
            os.makedirs(repo_name)
            print(f"Initialized empty repository: '{repo_name}'")
            
            # Create the .meta directory inside the repository
            meta_path = os.path.join(repo_name, ".meta")
            os.makedirs(meta_path)

            # Create an empty snapshots.json file in .meta
            snapshots_file_path = os.path.join(meta_path, "snapshots.json")
            with open(snapshots_file_path, 'w') as f:
                f.write("[]")  # Initialize with an empty list of snapshots

            # Success message for .meta directory and snapshots.json
            print(f"Created .meta directory and snapshots.json inside '{repo_name}'")
            
        except OSError as e:
            print(f"Error creating repository: {e}")
    else:
        print(f"Repository '{repo_name}' already exists.")

#creating a snapshot
def create_snapshot(repo_name,description=""):
    #create path strings  to open the files
    meta_path=os.path.join(repo_name, ".meta")
    snapshots_file_path=os.path.join(meta_path, "snapshots.json")

    #create a timestamp
    timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
    
   # Read the files at the current snapshot and their content
    files = {}
    for file_name in os.listdir(repo_name):
        if file_name != ".meta":
            file_path = os.path.join(repo_name, file_name)
            with open(file_path, "r") as f:
                files[file_name] = f.read()
    #new snapshot list in python format
    snapshot={
            "timestamp"   : timestamp,
            "description" : description,
            "files"       : files

        }
    
    #read all the snapshots from snapshots.json into snapshotselse create an empty list
    try:
        with open(snapshots_file_path, "r") as f:
            snapshots=json.load(f)
        
    except(FileNotFoundError , json.JSONDecodeError):
        print(f"Could not read snapshots. Initializing empty snapshots list.")
        snapshots=[]
    snapshots.append(snapshot)

    #updating the snapshots.json filre with the new snapshot
    with open(snapshots_file_path, "w") as f:
        json.dump(snapshots, f, indent=4)

    print(f"Created Snapshot at '{timestamp}' with description : '{description}'")

#viewing the history
def view_history(repo_name):
    snapshots_file_path=os.path.join(repo_name, ".meta", "snapshots.json")

#open the snapshots file and display them with an id
    try:
        with open(snapshots_file_path, "r") as f:
            snapshots=json.load(f)
            if not snapshots:
                print("No snapshots found")
            else:
                print("History of Snapshots")
                for ind,snapshot in enumerate(snapshots):
                    print(f"{ind + 1}. [{snapshot['timestamp']}] {snapshot['description']}")
    except FileNotFoundError:
        print("No history available. Please create a snapshot first.")
    except json.JSONDecodeError:
        print("Error reading snapshots.")


if __name__ == "__main__":
    repo_name = input("Enter the name of the repository: ")
    initialize_repo(repo_name)

    description=input("Enter a description for the Snapshot :")
    create_snapshot(repo_name, description)

    view_history(repo_name)
