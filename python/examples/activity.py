import os
from velora_api import Client

api=Client(os.environ['VELORA_TOKEN'])
api.set_activity('Python example',key='python-example',state='Testing activity',ttl=60)
try:
    input('Press Enter to clear this example activity...')
finally:
    api.clear_activity('python-example')
