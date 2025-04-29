# Todoist CLI

A command-line interface for interacting with Todoist tasks using the Todoist REST API v2.

## Features

- Secure token management with 1Password CLI integration
- View all of your Todoist tasks
- Create new tasks with optional subtasks
- Quickly create a "Task Reset" workflow with predefined subtasks

## Installation

1. Clone this repository:
```
git clone https://github.com/jamielaird/todoist.git
cd todoist
```

2. Install the required packages:
```
pip install -r requirements.txt
```

3. Ensure you have 1Password CLI installed and configured:
   - Follow the installation instructions at https://developer.1password.com/docs/cli/get-started/
   - Sign in to your 1Password account using `op signin`
   - Store your Todoist API token in 1Password at the path `op://Private/Todoist/token`
     - You can generate an API token at https://app.todoist.com/app/settings/integrations/developer

## Usage

The script provides several commands:

### View all tasks
```
python main.py
```

### Create a "Task Reset" with predefined subtasks
```
python main.py create_reset_task
```

### Create a custom task with optional subtasks
```
python main.py create "Task name" ["Subtask 1" "Subtask 2" ...]
```

### Display help information
```
python main.py help
```

## Configuration

The application retrieves your Todoist API token from 1Password using the CLI. Ensure you have:

1. 1Password CLI installed
2. An active 1Password session (`op signin`)
3. Your Todoist API token stored at `op://Private/Todoist/token`

## Links and Resources

- [Todoist REST API v2 Documentation](https://developer.todoist.com/rest/v2/)
- [todoist-api-python Package](https://pypi.org/project/todoist-api-python/)
- [1Password CLI Documentation](https://developer.1password.com/docs/cli/)
