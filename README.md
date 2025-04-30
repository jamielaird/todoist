# Todoist CLI

A command-line interface for interacting with Todoist tasks using the Todoist REST API v2.

## Features

- Secure token management with 1Password CLI integration or environment variables
- View all of your Todoist tasks with advanced filtering options
- Create new tasks with optional subtasks, due dates, priorities, and more
- Manage your projects and labels
- Complete and delete tasks
- Rich, colorized output for better visualization
- Configuration file support for personalized defaults
- "Task Reset" workflow with predefined subtasks

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

3. Authentication options:

   a. **Using 1Password CLI** (recommended for security):
   - Follow the installation instructions at https://developer.1password.com/docs/cli/get-started/
   - Sign in to your 1Password account using `op signin`
   - Store your Todoist API token in 1Password at the path `op://Private/Todoist/token`
     - You can generate an API token at https://app.todoist.com/app/settings/integrations/developer

   b. **Using environment variables**:
   - Export your Todoist API token as an environment variable:
     ```
     export TODOIST_API_TOKEN="your-api-token-here"
     ```

## Usage

The new CLI provides a more intuitive command structure:

### Listing Tasks

```
# List all tasks
python main.py list

# Filter tasks by priority
python main.py list --priority 4

# Filter tasks by due date
python main.py list --due today
```

### Managing Tasks

```
# Create a new task
python main.py add "Task name"

# Create a task with priority and due date
python main.py add "Important task" --priority 4 --due tomorrow

# Create a task with subtasks
python main.py add "Project" --subtask "Step 1" --subtask "Step 2"

# Complete a task
python main.py complete task_id

# Delete a task
python main.py delete task_id
```

### Projects and Labels

```
# List all projects
python main.py projects

# List all labels
python main.py labels

# Create a task in a specific project
python main.py add "Task name" --project "Project Name"

# Create a task with labels
python main.py add "Task name" --label "work" --label "urgent"
```

### Special Workflows

```
# Create a "Task Reset" with predefined subtasks
python main.py reset
```

### Help and Options

```
# Show general help
python main.py --help

# Show command-specific help
python main.py add --help
```

## Configuration

You can create a configuration file at `~/.todoist-cli.json` with defaults:

```json
{
  "token_path": "op://Private/Todoist/token",
  "default_project": "Inbox",
  "default_priority": 1,
  "use_colors": true,
  "verbose": false
}
```

## Backwards Compatibility

The application maintains compatibility with the previous command structure:

```
python main.py                   # List all tasks
python main.py create_reset_task # Create Task Reset with predefined subtasks
python main.py create "Task name" ["Subtask 1" "Subtask 2" ...] # Create custom task
```

## Project Structure

The project now uses a modular structure:

```
todoist/
├── main.py                # Main CLI entry point
├── requirements.txt       # Dependencies
├── README.md             
└── todoist_cli/          # Package directory
    ├── __init__.py       # Package initialization
    ├── api.py            # API interaction
    ├── auth.py           # Authentication handling
    ├── commands.py       # Command implementation
    └── utils.py          # Utility functions
```

## Links and Resources

- [Todoist REST API v2 Documentation](https://developer.todoist.com/rest/v2/)
- [todoist-api-python Package](https://pypi.org/project/todoist-api-python/)
- [1Password CLI Documentation](https://developer.1password.com/docs/cli/)
- [Rich Text Library](https://rich.readthedocs.io/en/stable/introduction.html)
