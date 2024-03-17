from split_settings.tools import include
from decouple import config

include('base.py')

if 'Development' in config('ENV_NAME'):
    include('development.py')
elif 'Production' in config('ENV_NAME'):
    include('production.py')