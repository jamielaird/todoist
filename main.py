from todoist_api_python.api import TodoistAPI

api = TodoistAPI("op://Private/Todoist/token")

try:
    tasks = api.get_tasks()
    print(tasks)
except Exception as error:
    print(error)