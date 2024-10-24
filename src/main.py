#!/usr/bin/env python3
import os
import json
import time
import argparse

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
    snapshots_file_path = os.path.join(meta_path, "snapshots.json")

    #create a timestamp
    timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Read the files at the current snapshot and their content
    files = {}
    for file_name in os.listdir(repo_name):
        if file_name != ".meta":
            file_path = os.path.join(repo_name, file_name)
            try:
                with open(file_path, "r") as f:
                    files[file_name] = f.read()
            except IOError as e:
                print(f"Error reading file '{file_name}': {e}")
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

    print(f"Created Snapshot at '{timestamp}' with description: '{description}'")

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

#rollback function to rollback to a previous snapshot
def rollback(repo_name,snapshot_index):
    #path to the jsonfile
    snapshots_file_path = os.path.join(repo_name, ".meta", "snapshots.json")

    #read the list of current snapshots from snapshots.json file
    try:
        with open(snapshots_file_path, "r") as f:
            snapshots=json.load(f)
        
        #check if a snapshot index is invalid
        if snapshot_index < 1 or snapshot_index > len(snapshots):
            print("Invalid snapshot index.")
            return

        #retrieving the given snapshot
        target_snapshot=snapshots[snapshot_index - 1]
        print(f"rolling back to snapshot '{snapshot_index}' ({target_snapshot['timestamp']}) : '{target_snapshot['description']}'")

        #clear the current files in the repository except .meta
        for file_name in os.listdir(repo_name):
            if file_name != ".meta":
                file_path=os.path.join(repo_name, file_name)
                os.remove(file_path)
            
        #restore files and contents from snapshots
        for file_name, content in target_snapshot['files'].items():
            file_path=os.path.join(repo_name, file_name)
            with open(file_path, "w") as f:
                f.write(content)
            
        print("rollback successful.")

    #if any errors are found print them
    except FileNotFoundError:
        print("No snapshots found. Please create a snapshot first.")
    except json.JSONDecodeError:
        print("Error reading snapshots file.")
    except OSError as e:
        print(f"Error during rollback: {e}")


#restore function to restore contents of one particular file at a particular snapshot
def restore(repo_name, snapshot_index, file_name):
    snapshots_file_path=os.path.join(repo_name, ".meta", "snapshots.json")

    #read the list of current snapshots
    try:
        with open(snapshots_file_path, "r") as f:
            snapshots=json.load(f)
    
        if(snapshot_index < 1 or snapshot_index > len(snapshots)):
            print("Invalid snapshot index.")
            return
        
        target_snapshot = snapshots[snapshot_index - 1]
        
        #check if the specified file exists in the snapshot
        if file_name not in target_snapshot['files']:
            print(f"File '{file_name}'not found in the specified snapshot")
            return

        #store the contents in the specified file
        content = target_snapshot['files'][file_name]
        file_path = os.path.join(repo_name, file_name)
        with open(file_path, "w") as f:
            f.write(content)
        
        print(f"Restored '{file_name}' to the state from'{target_snapshot['timestamp']}'.")

    except FileNotFoundError:
        print("No snapshots found. Please create a snapshot first.")
    except json.JSONDecodeError:
        print("Error reading snapshots file.")
    except OSError as e:
        print(f"Error during restore: {e}")



import argparse
import os
import json
import time

# Define all your functions (initialize_repo, create_snapshot, view_history, rollback, restore)

# Entry point function
def main():
    parser = argparse.ArgumentParser(prog='simv', description='A simple version control tool')
    subparsers = parser.add_subparsers(dest='command', help='Sub-command help')

    # `init` command
    init_parser = subparsers.add_parser('init', help='Initialize a new repository')
    init_parser.add_argument('repo_name', help='Name of the repository')

    # `snapshot` command
    snapshot_parser = subparsers.add_parser('snapshot', help='Create a new snapshot')
    snapshot_parser.add_argument('repo_name', help='Name of the repository')
    snapshot_parser.add_argument('description', nargs='?', default='', help='Description for the snapshot')

    # `history` command
    history_parser = subparsers.add_parser('history', help='View snapshot history')
    history_parser.add_argument('repo_name', help='Name of the repository')

    # `rollback` command
    rollback_parser = subparsers.add_parser('rollback', help='Rollback to a specific snapshot')
    rollback_parser.add_argument('repo_name', help='Name of the repository')
    rollback_parser.add_argument('snapshot_index', type=int, help='Index of the snapshot to rollback to')

    # `restore` command
    restore_parser = subparsers.add_parser('restore', help='Restore a specific file from a snapshot')
    restore_parser.add_argument('repo_name', help='Name of the repository')
    restore_parser.add_argument('snapshot_index', type=int, help='Index of the snapshot to restore from')
    restore_parser.add_argument('file_name', help='Name of the file to restore')

    # Parse arguments
    args = parser.parse_args()

    # Map commands to functions
    if args.command == 'init':
        initialize_repo(args.repo_name)
    elif args.command == 'snapshot':
        create_snapshot(args.repo_name, args.description)
    elif args.command == 'history':
        view_history(args.repo_name)
    elif args.command == 'rollback':
        rollback(args.repo_name, args.snapshot_index)
    elif args.command == 'restore':
        restore(args.repo_name, args.snapshot_index, args.file_name)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

