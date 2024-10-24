# simV - A Simple Version Control Tool
`simV` is a lightweight version control tool designed to be simpler than Git. It allows solo developers to manage snapshots of their projects easily. With `simV`, you can initialize repositories, create snapshots, view history, rollback to previous versions, and restore files.

## Installation
1. Clone the `simV` project to your local machine: `git clone <repository-url>`
2. Add `simV` to your terminal path for easy access: `alias simv='python3 /path/to/your/vcs/src/main.py'` Replace `/path/to/your` with the actual path where the `simV` project is located.
3. Reload your terminal configuration: `source ~/.zshrc`

## Usage
Once set up, you can use `simV` commands similar to Git:

### Initialize a Repository
- **Command**: `simv init <repo_name>`
- **Example**: `simv init my_project`
- **Description**: This command initializes a new repository with the specified name. It creates a `.meta` folder inside the repository to store snapshots.

### Create a Snapshot
- **Command**: `simv snapshot <repo_name> [description]`
- **Example**: `simv snapshot my_project "Initial commit with basic setup"`
- **Description**: Captures the current state of the files in the repository, storing them as a snapshot. Optionally, you can include a description to keep track of changes in each snapshot.

### View Snapshot History
- **Command**: `simv history <repo_name>`
- **Example**: `simv history my_project`
- **Description**: Displays a list of all snapshots that have been taken in the specified repository. Each entry shows the timestamp and description of the snapshot, allowing you to track the project's progress over time.

### Rollback to a Snapshot
- **Command**: `simv rollback <repo_name> <snapshot_index>`
- **Example**: `simv rollback my_project 2`
- **Description**: Reverts the entire repository back to the state it was in at the specified snapshot index. This is useful if you want to undo changes and return to a previous working state.

### Restore a Specific File
- **Command**: `simv restore <repo_name> <snapshot_index> <file_name>`
- **Example**: `simv restore my_project 2 main.py`
- **Description**: Restores a single file from a specific snapshot to its state at that time. This is useful if you only want to recover one file instead of rolling back the entire repository.

## Notes
- Replace `<repo_name>` with the name of the repository you wish to work with.
- `snapshot_index` corresponds to the index of the snapshot as shown in the history.
- For restoring, provide the name of the file you want to revert.

## Example Workflow
```bash
# Initialize a new repository
simv init demo_repo

# Create a snapshot with a description
simv snapshot demo_repo "Added initial project files"

# Create another snapshot
simv snapshot demo_repo "Implemented core logic"

# View history of snapshots
simv history demo_repo

# Rollback to the first snapshot
simv rollback demo_repo 1

# Restore a specific file from the second snapshot
simv restore demo_repo 2 app.py
