from todoist.api import TodoistAPI
import config

api = TodoistAPI(config.access_token)

# get all projects
api.sync()
print(api.state['projects'])
