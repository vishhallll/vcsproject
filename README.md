# Vishal's Version Control System (VCS)

## Overview
A simple version control system designed specifically for solo developers, with a focus on ease of use. Unlike more complex systems, this VCS automatically tracks all changes and allows users to create snapshots of their work without needing to manage a staging area.

## Features
- **Initialize a Repository (`init`)**: Set up a new repository for tracking your project.
- **Create Snapshots (`snapshot`)**: Save the current state of all tracked files with an optional description.
- **View History (`history`)**: List all snapshots along with their descriptions and timestamps.
- **Rollback (`rollback`)**: Revert your project to a previous snapshot easily.
- **Restore (`restore`)**: Temporarily view a past version without changing the current state.

## Installation
1. Clone this repository.
   `git clone <repository-url>`
2. Navigate to the project directory.
   `cd vcs`
3. Set up a virtual environment(optional):
   `python -m venv venv`
4. Activate the virtual environment:
   - For macOS/Linux: `source venv/bin/activate`
   - For Windows: `.\venv\Scripts\activate`

## Usage
Run the command line interface with the following commands:
- `init`: Initialize a new repository.
- `snapshot`: Create a new snapshot of the current state.
- `history`: List all snapshots.
- `rollback`: Revert to a specific snapshot.
- `restore`: View a snapshot without altering the current state.

### Example
`python src/main.py init my_repo`  
`python src/main.py snapshot "Initial version"`  
`python src/main.py history`  
`python src/main.py rollback 1`

## Contributing
Contributions are welcome! Please feel free to submit a pull request or suggest features.

## License
This project is open-source and available under the MIT License.
