from decouple import config

ENV = config('ENV', default='development')

if ENV == 'production':
    from .production import *
else:
    from .development import *